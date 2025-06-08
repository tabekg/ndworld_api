from flask import Blueprint, request, g

from models.category import Category
from models.resume import Resume, ResumeStatusEnum
from models.worker import Worker
from utils.http import make_response, orm_to_dict
from utils.image import unlink_image, link_image

bp = Blueprint('worker', __name__, url_prefix='/worker')


@bp.post('')
def index_post():
    data = request.json
    id_ = data.get('id')
    status = ResumeStatusEnum(data['status'].upper())
    item = None

    assert status in [ResumeStatusEnum.available, ResumeStatusEnum.draft]

    if id_:
        item = g.db.query(Resume).filter(Resume.id == id_, Resume.agency_id == g.agency.id).one()

    if not item:
        item = Resume(
            agency_id=g.agency.id, status=status, role_id=g.role.id,
        )
        g.db.add(item)

    item.name = data['name']
    item.surname = data['surname']
    item.patronymic = data.get('patronymic')

    item.summary = data.get('summary')
    item.marital_status = data.get('marital_status')
    item.birth_date = data.get('birth_date') if data.get('birth_date') else None
    item.about = data.get('about')
    item.residential_address = data.get('residential_address')
    item.registered_address = data.get('registered_address')

    item.instagram = data.get('instagram')
    item.telegram = data.get('telegram')
    item.email = data.get('email')
    item.linkedin = data.get('linkedin')
    item.phone_number = data['phone_number']

    item.categories = g.db.query(Category).filter(
        Category.parent_id.isnot(None),
        Category.id.in_([i['id'] for i in data['categories'] if i.get('id') is not None])
    ).all()

    if not id_:
        g.db.flush()

    if data['photo'] and (item.photo is None or item.photo['id'] != data['photo']['id']):
        if item.photo is not None:
            unlink_image(f'resume_photo_{item.id}')
        link_image(f'resume_photo_{item.id}', data['photo']['id'])
        item.photo = data['photo']

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
