from flask import Blueprint, g, request

from controllers.auth import candidate_required
from models.candidate import CandidateSkill
from utils.http import make_response, orm_to_dict
from utils.image import link_image, unlink_image

bp = Blueprint('candidate', __name__, url_prefix='/candidate')


@bp.before_request
@candidate_required()
def before_request():
    pass


@bp.get('')
def index_get():
    return make_response(g.candidate.to_dict_item())


@bp.post('')
def index_post():
    data = request.json
    photo_id = data.get('photo_id', g.candidate.photo_id)

    if photo_id != g.candidate.photo_id:
        if g.candidate.photo_id is not None:
            unlink_image(g.candidate.photo_id, f'candidate_photo_{g.candidate.id}')
        if photo_id is not None:
            res = link_image(photo_id, f'candidate_photo_{g.candidate.id}')
            g.candidate.photo_id = photo_id
            g.candidate.photo_path = res['path']
        else:
            g.candidate.photo_id = None
            g.candidate.photo_path = None

    g.candidate.contact_email = data.get('contact_email', g.candidate.contact_email) or None
    g.candidate.contact_phone_number = data.get('contact_phone_number', g.candidate.contact_phone_number) or None
    g.candidate.birth_date = data.get('birth_date', g.candidate.birth_date) or None
    g.candidate.about = data.get('about', g.candidate.about) or None
    g.candidate.summary = data.get('summary', g.candidate.summary) or None

    g.db.commit()

    return make_response(g.candidate.to_dict_item())


@bp.get('/passport')
def passport_get():
    return make_response({
        'front_passport_path': g.candidate.front_passport_path,
        'back_passport_path': g.candidate.back_passport_path,
    })


@bp.post('/passport')
def passport_post():
    data = request.json
    front_passport_id = data.get('front_passport_id', g.candidate.front_passport_id)
    back_passport_id = data.get('back_passport_id', g.candidate.back_passport_id)

    if front_passport_id != g.candidate.front_passport_id:
        if g.candidate.front_passport_id is not None:
            unlink_image(g.candidate.front_passport_id, f'candidate_front_passport_{g.candidate.id}')
        if front_passport_id is not None:
            res = link_image(front_passport_id, f'candidate_front_passport_{g.candidate.id}')
            g.candidate.front_passport_id = front_passport_id
            g.candidate.front_passport_path = res['path']
        else:
            g.candidate.front_passport_id = None
            g.candidate.front_passport_path = None

    if back_passport_id != g.candidate.back_passport_id:
        if g.candidate.back_passport_id is not None:
            unlink_image(g.candidate.back_passport_id, f'candidate_back_passport_{g.candidate.id}')
        if back_passport_id is not None:
            res = link_image(back_passport_id, f'candidate_back_passport_{g.candidate.id}')
            g.candidate.back_passport_id = back_passport_id
            g.candidate.back_passport_path = res['path']
        else:
            g.candidate.back_passport_id = None
            g.candidate.back_passport_path = None

    g.db.commit()

    return make_response({
        'front_passport_path': g.candidate.front_passport_path,
        'back_passport_path': g.candidate.back_passport_path,
    })


@bp.get('/skill')
def skill_get():
    return make_response(orm_to_dict(g.candidate.skills))


@bp.post('/skill')
def skill_post():
    data = request.json
    id_ = data.get('id') or None

    if id_ is not None and id_:
        item = g.db.query(CandidateSkill).filter(CandidateSkill.candidate_id == g.candidate.id, CandidateSkill.id == id_).one()
    else:
        item = CandidateSkill(candidate_id=g.candidate.id)
        assert data['skill_name']
        assert g.db.query(CandidateSkill).filter(
            CandidateSkill.candidate_id == g.candidate.id,
            CandidateSkill.skill_name == data['skill_name'],
        ).first() is None
        g.db.add(item)

    item.skill_name = data.get('skill_name', item.skill_name) or item.skill_name
    item.proficiency = data.get('proficiency', item.proficiency) or None

    g.db.commit()

    return make_response(item.to_dict_item())


@bp.get('/education')
def education_get():
    return make_response(orm_to_dict(g.candidate.educations))


# @bp.post('/education')
# def education_post():
#     data = request.json
#     id_ = data.get('id') or None
#
#     if id_ is not None and id_:
#         item = g.db.query(UserEducation).filter(UserEducation.user_id == g.user.id, UserEducation.id == id_).one()
#     else:
#         item = UserEducation(user_id=g.user.id)
#         assert data['institution'] and data['degree'] and data['start_date']
#         assert g.db.query(UserEducation).filter(
#             UserEducation.user_id == g.user.id,
#             UserEducation.institution == data['institution'],
#             UserEducation.degree == data['degree'],
#         ).first() is None
#
#         g.db.add(item)
#
#     item.institution = data.get('institution', item.institution) or item.institution
#     item.degree = data.get('degree', item.degree) or item.degree
#     item.start_date = data.get('start_date', item.start_date) or item.start_date
#     item.end_date = data.get('end_date', item.end_date) or None
#     item.description = data.get('description', item.description) or None
#
#     g.db.commit()
#
#     return make_response(item.to_dict_item())


@bp.get('/experience')
def experience_get():
    return make_response(orm_to_dict(g.candidate.experiences))


# @bp.post('/experience')
# def experience_post():
#     data = request.json
#     id_ = data.get('id') or None
#
#     if id_ is not None and id_:
#         item = g.db.query(UserExperience).filter(UserExperience.user_id == g.user.id, UserExperience.id == id_).one()
#     else:
#         item = UserExperience(user_id=g.user.id)
#         assert data['company'] and data['position'] and data['start_date']
#         assert g.db.query(UserExperience).filter(
#             UserExperience.user_id == g.user.id,
#             UserExperience.company == data['company'],
#             UserExperience.position == data['position'],
#         ).first() is None
#
#         g.db.add(item)
#
#     item.company = data.get('company', item.company) or item.company
#     item.position = data.get('position', item.position) or item.position
#     item.start_date = data.get('start_date', item.start_date) or item.start_date
#     item.end_date = data.get('end_date', item.end_date) or None
#     item.description = data.get('description', item.description) or None
#
#     g.db.commit()
#
#     return make_response(item.to_dict_item())
