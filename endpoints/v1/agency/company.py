from flask import Blueprint, g

from utils.http import make_response

bp = Blueprint('company', __name__, url_prefix='/company')


@bp.get('')
def index_get():
    assert g.role.role == 'admin'

    items = g.role.agency.companies

    return make_response([i.to_dict_item() for i in items])
