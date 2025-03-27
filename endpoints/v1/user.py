from flask import Blueprint, g, request

from controllers.auth import auth_required
from utils.http import make_response

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.before_request
@auth_required()
def before_request():
    pass


@bp.get('')
def index_get():
    return make_response(g.user.to_dict_item())


@bp.post('')
def index_post():
    data = request.json

    g.user.first_name = data.get('first_name', g.user.first_name) or None
    g.user.last_name = data.get('last_name', g.user.last_name) or None

    g.db.commit()

    return make_response(g.user.to_dict_item())
