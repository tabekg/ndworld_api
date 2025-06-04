from flask import Blueprint, g

from controllers.auth import auth_required
from models.category import Category
from utils.http import make_response

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.before_request
@auth_required()
def before_request():
    pass


@bp.get('')
def index_get():
    items = g.db.query(Category).all()
    return make_response([i.to_dict_item() for i in items])
