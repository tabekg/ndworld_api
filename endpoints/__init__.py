from flask import Blueprint
from endpoints import v1
from utils.http import make_response

bp = Blueprint('', __name__, url_prefix='')

bp.register_blueprint(v1.bp)


@bp.get('/')
def index_get():
    return make_response({'message': 'API is running...'})
