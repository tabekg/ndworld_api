from flask import Blueprint, request, g

from models.resume import Resume, ResumeStatusEnum
from utils.http import make_response

bp = Blueprint('resume', __name__, url_prefix='/resume')


@bp.post('')
def index_post():
    data = request.json
    id_ = data.get('id')
    status = ResumeStatusEnum(data['status'].upper())
    item = None

    assert status in [ResumeStatusEnum.available, ResumeStatusEnum.draft]

    if id_:
        item = g.db.query(Resume).filter(Resume.id == id_, Resume.agency_id == g.agency.id).first()

    if not item:
        item = Resume(agency_id=g.agency.id, status=status)
        g.db.add(item)

    item.name = data['name']
    item.surname = data['surname']
    item.patronymic = data.get('patronymic')

    g.db.commit()

    return make_response(item.to_dict_item())


@bp.get('/check')
def check_get():
    name = request.args['name']
    surname = request.args['surname']

    items = g.db.query(Resume).filter(
        Resume.agency_id == g.agency.id,
        Resume.name.ilike(name),
        Resume.surname.ilike(surname),
    ).all()

    return make_response([item.to_dict_item() for item in items])


@bp.get('')
def index_get():
    id_ = request.args['id']

    item = g.db.query(Resume).filter(
        Resume.agency_id == g.agency.id,
        Resume.id == id_,
    ).one()

    return make_response(item.to_dict_item())
