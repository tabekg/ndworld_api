from flask import Blueprint, g

from controllers.auth import auth_required
from utils.http import make_response

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('')
@auth_required()
def index_get():
    return make_response(g.user.to_dict_item())


@bp.post('')
@auth_required()
def index_post():
    return make_response(g.user.to_dict_item())
