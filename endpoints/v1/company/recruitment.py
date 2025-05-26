from flask import Blueprint, request, g

from models.resume import Resume
from utils.http import make_response

bp = Blueprint('recruitment', __name__, url_prefix='/recruitment')


@bp.get('/resume/check')
def resume_check_get():
    first_name = request.args['first_name']
    last_name = request.args['last_name']

    items = g.db.query(Resume).filter(
        Resume.company_id == g.company.id,
        Resume.first_name.ilike(first_name),
        Resume.last_name.ilike(last_name),
    ).all()

    return make_response([item.to_dict_item() for item in items])
