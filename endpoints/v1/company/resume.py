import json

from flask import Blueprint, g, request

from models.category import Category
from models.common import resume_categories, agency_companies
from models.resume import Resume
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
            .all(), ['name'], {
                'agency': lambda b: orm_to_dict(b.agency, ['title']),
            }),
    }, ['title']))
