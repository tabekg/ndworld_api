from flask import Blueprint, request, g

from models.category import Category
from models.resume import Resume, ResumeStatusEnum
from utils.http import make_response, orm_to_dict
from utils.image import set_image, set_images

bp = Blueprint('resume', __name__, url_prefix='/resume')


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
    item.patronymic = data.get('patronymic') or None

    item.summary = data.get('summary') or None
    item.marital_status = data.get('marital_status') or None
    item.birth_date = data.get('birth_date') or None
    item.about = data.get('about') or None
    item.residential_address = data.get('residential_address') or None
    item.registered_address = data.get('registered_address') or None

    item.instagram = data.get('instagram') or None
    item.telegram = data.get('telegram') or None
    item.email = data.get('email') or None
    item.linkedin = data.get('linkedin') or None
    item.phone_number = data['phone_number']
    if data.get('phone_numbers'):
        item.phone_numbers = [i.trim() for i in data['phone_numbers'] if i and i.trim()]
    else:
        item.phone_numbers = []

    item.categories = g.db.query(Category).filter(
        Category.parent_id.isnot(None),
        Category.id.in_([i['id'] for i in data['categories'] if i.get('id') is not None])
    ).all()

    if not id_:
        g.db.flush()

    if data.get('photos'):
        pass

    item.photo = set_image(f'resume_photo_{item.id}', data.get('photo'), item.photo, required=True)
    item.passport_front = set_image(
        f'resume_passport_front_{item.id}',
        data.get('passport_front'), item.passport_front, required=False,
    )
    item.passport_back = set_image(
        f'resume_passport_back_{item.id}',
        data.get('passport_back'), item.passport_back, required=False,
    )
    item.birth_certificate = set_image(
        f'resume_birth_certificate_{item.id}',
        data.get('birth_certificate'), item.birth_certificate, required=False,
    )
    item.photos = set_images(f'resume_photos_{item.id}', data.get('photos'), item.photos, min_count=0, max_count=10)

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
    status = request.args.get('status')

    if id_:
        item = g.db.query(Resume).filter(
            Resume.agency_id == g.agency.id,
            Resume.id == id_,
        )

        if g.role.role == 'agent':
            item = item.filter(Resume.role_id == g.role.id)

        return make_response(item.one().to_dict_item())

    if status:
        items = g.db.query(Resume).filter(
            Resume.agency_id == g.agency.id,
            Resume.status == ResumeStatusEnum[status],
        )

        if g.role.role == 'agent':
            items = items.filter(Resume.role_id == g.role.id)

        return make_response(
            orm_to_dict(items.all(), [
                'name',
                'surname',
                'patronymic',
                'status',
                'created_at',
            ], {
                'role': lambda a: orm_to_dict(a.role, [], {
                    'user': lambda b: orm_to_dict(b.user, ['name', 'surname']),
                })
            })
        )

    return make_response()
