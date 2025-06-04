from flask import Blueprint

from controllers.auth import company_auth_required
from utils.http import make_response
from . import recruitment, agency

bp = Blueprint('company', __name__, url_prefix='/company')

bp.register_blueprint(recruitment.bp)
bp.register_blueprint(agency.bp)


@bp.before_request
@company_auth_required()
def before_request():
    pass


@bp.get('')
def index_get():
    return make_response()
