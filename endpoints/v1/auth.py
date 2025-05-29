import requests
from flask import Blueprint, request, g

from controllers.auth import create_access_token, create_auth_session, create_auth_provider, auth_required
from controllers.user import create_user, create_role
from models.auth import AuthProvider
from models.user import Role
from utils.config import config
from utils.exception import ResponseException
from utils.http import make_response

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.post('/send-otp')
def send_otp_post():
    phone_number = request.json['phone_number']

    assert phone_number and phone_number[0] != '+'

    response = requests.post(config.get('besoft_cloud', 'api_url') + '/tp/v1/authentication/send-otp', params={
        '_project_key': config.get('besoft_cloud', 'public_key'),
    }, json={
        'phone_number': phone_number,
        'channels': ['whatsapp'],
    }, headers={
        'Authorization': 'Bearer ' + config.get('besoft_cloud', 'private_key'),
    })

    json = response.json()
    status = json.get('status') or 'unknown_error'

    if status == 'unknown_error':
        raise ResponseException(status='besoft_cloud_service_error', status_code=500)

    return make_response(
        payload=json.get('payload'),
        status=status,
        status_code=response.status_code,
    )


@bp.post('/verify-otp')
def verify_otp_post():
    token = request.json['token']
    otp = request.json['otp']

    response = requests.post(config.get('besoft_cloud', 'api_url') + '/tp/v1/authentication/verify-otp', params={
        '_project_key': config.get('besoft_cloud', 'public_key'),
    }, json={
        'otp': otp,
        'token': token,
    }, headers={
        'Authorization': 'Bearer ' + config.get('besoft_cloud', 'private_key'),
    })

    json = response.json()
    status = json.get('status') or 'unknown_error'
    payload = json.get('payload') or {}

    if status == 'unknown_error':
        raise ResponseException(status='besoft_cloud_service_error', status_code=500)

    if status == 'success':
        auth_provider = g.db.query(AuthProvider).filter(
            AuthProvider.name == 'whatsapp',
            AuthProvider.identifier == payload['phone_number'],
        ).first()

        if auth_provider is None:
            user = create_user(g.db)
            create_role(g.db, user_id=user.id)
            auth_provider = create_auth_provider(g.db, user.id, 'whatsapp', payload['phone_number'])
        else:
            user = auth_provider.user

        role_id = None

        if len(user.roles) > 0:
            role_id = user.roles[0].id

        auth_session = create_auth_session(g.db, user_id=user.id, role_id=role_id)

        g.db.commit()

        return make_response(
            payload={
                'access_token': create_access_token({'sessionHash': auth_session.hash}),
                'user': user.to_dict_item(),
                'auth_session': auth_session.to_dict_item(),
                'auth_provider': auth_provider.to_dict_item(),
            },
            status=status,
            status_code=response.status_code,
        )

    return make_response(
        payload=payload,
        status=status,
        status_code=response.status_code,
    )


@bp.post('/role')
@auth_required()
def role_post():
    role_id = request.json['role_id']

    role = g.db.query(Role).filter(Role.id == role_id, Role.user_id == g.user.id).one()

    g.auth_session.role_id = role.id
    g.db.commit()

    return make_response()
