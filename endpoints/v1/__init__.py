from flask import Blueprint
from endpoints.v1 import auth
from utils.http import make_response

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth.bp)


@bp.get('/')
def index_get():
    return make_response()
