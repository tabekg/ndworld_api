from flask import Blueprint, request, g

from models.resume import Resume
from utils.http import make_response

bp = Blueprint('recruitment', __name__, url_prefix='/recruitment')


@bp.get('/resume/check')
def resume_check_get():
    name = request.args['name']
    surname = request.args['surname']

    items = g.db.query(Resume).filter(
        Resume.agency_id == g.agency.id,
        Resume.name.ilike(name),
        Resume.surname.ilike(surname),
    ).all()

    return make_response([item.to_dict_item() for item in items])
