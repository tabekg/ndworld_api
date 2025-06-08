from typing import Optional

import requests

from utils.config import config


def link_image(name: str, image_id: int):
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


def unlink_image(name: str, image_id: Optional[int] = None):
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


def set_image(name, new_image, old_image, required=False):
    if not new_image:
        if required:
            if old_image:
                return old_image
            raise ValueError(f"Image is required for '{name}', but both new and old images are missing.")
        return None

    if old_image and new_image['id'] == old_image['id']:
        return old_image

    link_image(name, new_image['id'])

    if old_image:
        unlink_image(name, old_image['id'])

    return new_image


def set_images(name, new_images, old_images, min_count=1, max_count=10):
    new_ids = {img['id'] for img in new_images or []}
    old_ids = {img['id'] for img in old_images or []}

    to_link = new_ids - old_ids
    to_unlink = old_ids - new_ids

    final_ids = old_ids.union(new_ids)
    final_count = len(final_ids)

    if final_count < min_count:
        raise ValueError(f"Минимум {min_count} фото требуется для '{name}', но передано только {final_count}.")
    if final_count > max_count:
        raise ValueError(f"Максимум {max_count} фото допускается для '{name}', но передано {final_count}.")

    for img_id in to_link:
        link_image(name, img_id)
    for img_id in to_unlink:
        unlink_image(name, img_id)

    kept_ids = old_ids & new_ids
    result = [img for img in new_images or [] if img['id'] in new_ids] + \
             [img for img in old_images or [] if img['id'] in kept_ids and img['id'] not in new_ids]

    return result
