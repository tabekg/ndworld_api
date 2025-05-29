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

    g.user.name = data.get('name', g.user.name) or None
    g.user.surname = data.get('surname', g.user.surname) or None

    g.db.commit()

    return make_response(g.user.to_dict_item())
