import json

from flask import Blueprint, g, request

from models.category import Category
from models.common import resume_categories, agency_companies
from models.resume import Resume, ResumeStatusEnum
from models.worker import Worker, WORKER_LEVEL_PENDING
from utils.http import make_response, orm_to_dict

bp = Blueprint('resume', __name__, url_prefix='/resume')


@bp.get('/explore')
def explore_get():
    category_ids = json.loads(request.args['category_ids'])

    categories = g.db.query(Category).filter(
        Category.id.in_(category_ids),
        Category.is_disabled.is_(False),
    ).all()

    return make_response(orm_to_dict(categories, ['title'], {
        'parent': lambda a: orm_to_dict(a.parent, ['title'], {}, ['title']),
        'resumes': lambda a: orm_to_dict(
            g.db.query(Resume).join(resume_categories, resume_categories.c.resume_id == Resume.id)
            .join(agency_companies, agency_companies.c.agency_id == Resume.agency_id)
            .filter(resume_categories.c.category_id == a.id)
            .filter(agency_companies.c.company_id == g.company.id)
            .filter(Resume.status == ResumeStatusEnum.available)
            .all(), ['name'], {
                'agency': lambda b: orm_to_dict(b.agency, ['title']),
            }),
    }, ['title']))


@bp.post('/request')
def request_post():
    list_ = request.json['list']
    items = []

    for item in list_:
        category_id = item['category_id']
        resume_ids = item['resume_ids']

        category = g.db.query(Category).filter(
            Category.id == category_id,
            Category.is_disabled.is_(False),
        ).first()

        if not category:
            continue

        assert g.db.query(Category).filter(Category.parent_id == category.id).first() is None

        resumes = g.db.query(Resume).join(resume_categories, resume_categories.c.resume_id == Resume.id) \
            .join(agency_companies, agency_companies.c.agency_id == Resume.agency_id) \
            .filter(resume_categories.c.category_id == category.id) \
            .filter(agency_companies.c.company_id == g.company.id) \
            .filter(Resume.status == ResumeStatusEnum.available) \
            .filter(Resume.id.in_(resume_ids)) \
            .all()

        for resume in resumes:
            worker = Worker(
                agency_id=resume.agency_id,
                company_id=g.company.id,
                resume_id=resume.id,
                category_id=category.id,
                level=WORKER_LEVEL_PENDING,
            )
            g.db.add(worker)

            resume.status = ResumeStatusEnum.unavailable

            g.db.flush()
            items.append(worker)

    g.db.commit()

    return make_response(orm_to_dict(items))
