import requests

from utils.config import config


def link_image(image_id, name):
    response = requests.post(config.get('besoft_cloud', 'api_url') + '/tp/v1/image/link', params={
        '_project_key': config.get('besoft_cloud', 'public_key'),
    }, json={
        'id': image_id,
        'name': name,
    }, headers={
        'Authorization': 'Bearer ' + config.get('besoft_cloud', 'private_key'),
    })

    json = response.json()

    assert json['status'] == 'success'

    return json['payload']


def unlink_image(image_id, name):
    response = requests.post(config.get('besoft_cloud', 'api_url') + '/tp/v1/image/unlink', params={
        '_project_key': config.get('besoft_cloud', 'public_key'),
    }, json={
        'id': image_id,
        'name': name,
    }, headers={
        'Authorization': 'Bearer ' + config.get('besoft_cloud', 'private_key'),
    })

    json = response.json()

    assert json['status'] == 'success'

    return json['payload']
