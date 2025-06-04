from flask import Blueprint, g, request

from utils.http import make_response

bp = Blueprint('role', __name__, url_prefix='/role')


@bp.get('')
def index_get():
    role = request.args.get('role')

    assert g.role.role == 'admin'

    items = g.role.agency.roles

    if role:
        items = [i for i in items if i.role == role]

    return make_response([i.to_dict_item() for i in items])
