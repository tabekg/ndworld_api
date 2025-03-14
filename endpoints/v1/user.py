from flask import Blueprint, g

from controllers.auth import auth_required
from utils.http import make_response, orm_to_dict

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('/')
@auth_required()
def index_get():
    return make_response(orm_to_dict(g.user, [
        'first_name', 'last_name',
        'contact_email', 'contact_phone_number',
        'birth_date', 'about', 'payload', 'is_disabled',
        'created_at',
    ], additional_fields={
        'experiences': lambda a: orm_to_dict(a.experiences, []),
        'educations': lambda a: orm_to_dict(a.educations, []),
        'skills': lambda a: orm_to_dict(a.skills, []),
    }))
