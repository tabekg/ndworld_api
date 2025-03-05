import requests
from flask import Blueprint, request
from utils.config import config
from utils.exception import ResponseException
from utils.http import make_response

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.post('/send-otp')
def send_otp_post():
    phone_number = request.json['phone_number']

    assert phone_number and phone_number[0] == '+'

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
    result = json.get('result')

    if status == 'unknown_error':
        raise ResponseException(status='besoft_cloud_service_error')

    return make_response(
        payload=json.get('payload'),
        status=status,
        result=result,
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
    payload = json.get('payload') or {}
    status = json.get('status') or 'unknown_error'
    result = json.get('result')

    if status == 'unknown_error':
        raise ResponseException(status='besoft_cloud_service_error')

    success_data = {}

    # if status == 'success':
    #     user = g.db.query(User).filter(
    #         User.phone_number == payload['phone_number'],
    #         User.provider_name == 'whatsapp',
    #     ).first()
    #     if user is None:
    #         user = User(
    #             provider_name='whatsapp',
    #             provider_id=payload['phone_number'],
    #             phone_number=payload['phone_number'],
    #         )
    #         g.db.add(user)
    #         g.db.commit()
    #     success_data = {
    #         'access_token': create_access_token({'id': user.id}),
    #     }

    return make_response(
        payload={
            **payload,
            **success_data,
        },
        status=status,
        result=result,
        status_code=response.status_code,
    )
