from flask import Blueprint, g

from utils.http import make_response

bp = Blueprint('agency', __name__, url_prefix='/agency')


@bp.get('')
def index_get():
    assert g.role.role == 'admin'

    items = g.role.company.agencies

    return make_response([i.to_dict_item() for i in items])
