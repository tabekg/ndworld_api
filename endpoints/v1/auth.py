import requests
from flask import Blueprint, request, g

from controllers.auth import create_access_token, create_auth_session, create_auth_provider
from controllers.user import create_user
from models.auth import AuthProvider
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
            AuthProvider.identity == payload['phone_number'],
        ).first()

        if auth_provider is None:
            user = create_user(g.db, 'candidate', payload['phone_number'])

            auth_provider = create_auth_provider(user.id, 'whatsapp', payload['phone_number'])
            g.db.add(auth_provider)
            g.db.flush()
        else:
            user = auth_provider.user

        auth_session = create_auth_session(user.id)
        g.db.add(auth_session)
        g.db.flush()

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
