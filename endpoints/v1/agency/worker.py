from flask import Blueprint, request, g

from models.resume import Resume
from models.worker import Worker
from utils.http import make_response, orm_to_dict

bp = Blueprint('worker', __name__, url_prefix='/worker')


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
    id_ = request.args.get('id')
    level = request.args.get('level')

    if id_:
        item = g.db.query(Resume).filter(
            Resume.agency_id == g.agency.id,
            Resume.id == id_,
        )

        if g.role.role == 'agent':
            item = item.filter(Resume.role_id == g.role.id)

        return make_response(item.one().to_dict_item())

    if level:
        items = g.db.query(Worker).join(Resume).filter(
            Worker.agency_id == g.agency.id,
            Worker.level == level,
        )

        if g.role.role == 'agent':
            items = items.filter(Resume.role_id == g.role.id)

        return make_response(
            orm_to_dict(items.all(), [
                'level', 'payload'
            ], {
                'company': lambda a: orm_to_dict(a.company, ['title', 'address']),
                'resume': lambda a: orm_to_dict(
                    a.resume, [
                        'name',
                        'surname',
                        'patronymic',
                        'phone_number',
                        'phone_numbers',
                        'telegram',
                        'instagram',
                    ], {
                        'role': lambda b: orm_to_dict(b.role, [], {
                            'user': lambda c: orm_to_dict(c.user, ['name', 'surname']),
                        })
                    })
            })
        )

    return make_response()
