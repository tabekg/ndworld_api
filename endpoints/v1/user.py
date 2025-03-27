from flask import Blueprint, g, request

from controllers.auth import auth_required
from utils.http import make_response
from utils.image import link_image, unlink_image

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('')
@auth_required()
def index_get():
    return make_response(g.user.to_dict_item())


@bp.post('')
@auth_required()
def index_post():
    data = request.json
    photo_id = data.get('photo_id', g.user.photo_id)

    if photo_id != g.user.photo_id:
        if g.user.photo_id is not None:
            unlink_image(g.user.photo_id, f'user_photo_{g.user.id}')
        if photo_id is not None:
            res = link_image(photo_id, f'user_photo_{g.user.id}')
            g.user.photo_id = photo_id
            g.user.photo_path = res['path']
        else:
            g.user.photo_id = None
            g.user.photo_path = None

    g.user.first_name = data.get('first_name', g.user.first_name) or None
    g.user.last_name = data.get('last_name', g.user.last_name) or None

    g.user.contact_email = data.get('contact_email', g.user.contact_email) or None
    g.user.contact_phone_number = data.get('contact_phone_number', g.user.contact_phone_number) or None
    g.user.birth_date = data.get('birth_date', g.user.birth_date) or None
    g.user.about = data.get('about', g.user.about) or None
    g.user.summary = data.get('summary', g.user.summary) or None

    g.db.commit()

    return make_response(g.user.to_dict_item())
