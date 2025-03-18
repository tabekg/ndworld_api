from flask import Blueprint, g, request

from controllers.auth import auth_required
from models.user import UserSkill, UserEducation, UserExperience
from utils.http import make_response, orm_to_dict

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('')
@auth_required()
def index_get():
    return make_response(g.user.to_dict_item())


@bp.post('')
@auth_required()
def index_post():
    data = request.json

    g.user.first_name = data.get('first_name', g.user.first_name) or None
    g.user.last_name = data.get('last_name', g.user.last_name) or None

    g.user.contact_email = data.get('contact_email', g.user.contact_email) or None
    g.user.contact_phone_number = data.get('contact_phone_number', g.user.contact_phone_number) or None
    g.user.birth_date = data.get('birth_date', g.user.birth_date) or None
    g.user.about = data.get('about', g.user.about) or None

    g.db.commit()

    return make_response(g.user.to_dict_item())


@bp.get('/skill')
@auth_required()
def skill_get():
    return make_response(orm_to_dict(g.user.skills))


@bp.post('/skill')
@auth_required()
def skill_post():
    data = request.json
    id_ = data.get('id') or None

    if id_ is not None and id_:
        item = g.db.query(UserSkill).filter(UserSkill.user_id == g.user.id, UserSkill.id == id_).one()
    else:
        item = UserSkill(user_id=g.user.id)
        assert data['skill_name']
        assert g.db.query(UserSkill).filter(
            UserSkill.user_id == g.user.id,
            UserSkill.skill_name == data['skill_name'],
        ).first() is None
        g.db.add(item)

    item.skill_name = data.get('skill_name', item.skill_name) or item.skill_name
    item.proficiency = data.get('proficiency', item.proficiency) or None

    g.db.commit()

    return make_response(item.to_dict_item())


@bp.get('/education')
@auth_required()
def education_get():
    return make_response(orm_to_dict(g.user.educations))


@bp.post('/education')
@auth_required()
def education_post():
    data = request.json
    id_ = data.get('id') or None

    if id_ is not None and id_:
        item = g.db.query(UserEducation).filter(UserEducation.user_id == g.user.id, UserEducation.id == id_).one()
    else:
        item = UserEducation(user_id=g.user.id)
        assert data['institution'] and data['degree'] and data['start_date']
        assert g.db.query(UserEducation).filter(
            UserEducation.user_id == g.user.id,
            UserEducation.institution == data['institution'],
            UserEducation.degree == data['degree'],
        ).first() is None

        g.db.add(item)

    item.institution = data.get('institution', item.institution) or item.institution
    item.degree = data.get('degree', item.degree) or item.degree
    item.start_date = data.get('start_date', item.start_date) or item.start_date
    item.end_date = data.get('end_date', item.end_date) or None
    item.description = data.get('description', item.description) or None

    g.db.commit()

    return make_response(item.to_dict_item())


@bp.get('/experience')
@auth_required()
def experience_get():
    return make_response(orm_to_dict(g.user.experiences))


@bp.post('/experience')
@auth_required()
def experience_post():
    data = request.json
    id_ = data.get('id') or None

    if id_ is not None and id_:
        item = g.db.query(UserExperience).filter(UserExperience.user_id == g.user.id, UserExperience.id == id_).one()
    else:
        item = UserExperience(user_id=g.user.id)
        assert data['company'] and data['position'] and data['start_date']
        assert g.db.query(UserExperience).filter(
            UserExperience.user_id == g.user.id,
            UserExperience.company == data['company'],
            UserExperience.position == data['position'],
        ).first() is None

        g.db.add(item)

    item.company = data.get('company', item.company) or item.company
    item.position = data.get('position', item.position) or item.position
    item.start_date = data.get('start_date', item.start_date) or item.start_date
    item.end_date = data.get('end_date', item.end_date) or None
    item.description = data.get('description', item.description) or None

    g.db.commit()

    return make_response(item.to_dict_item())
