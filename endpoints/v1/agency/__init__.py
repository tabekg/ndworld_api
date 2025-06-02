from flask import Blueprint

from controllers.auth import agency_auth_required
from utils.http import make_response
from . import resume

bp = Blueprint('agency', __name__, url_prefix='/agency')

bp.register_blueprint(resume.bp)


@bp.before_request
@agency_auth_required()
def before_request():
    pass


@bp.get('')
def index_get():
    return make_response()
