from flask import Blueprint
from endpoints.v1 import auth

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth.bp)
