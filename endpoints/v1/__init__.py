from flask import Blueprint
from endpoints.v1 import auth, user, resume, company
from utils.http import make_response

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth.bp)
bp.register_blueprint(user.bp)
bp.register_blueprint(resume.bp)
bp.register_blueprint(company.bp)


@bp.get('')
def index_get():
    return make_response()
