from flask import Blueprint, request, g

from models.job_posting import JobPostingStatusEnum, JobPosting
from models.resume import Resume, ResumeStatusEnum
from utils.http import make_response

bp = Blueprint('job-posting', __name__, url_prefix='/job-posting')


@bp.post('')
def index_post():
    data = request.json
    id_ = data.get('id')
    status = JobPostingStatusEnum(data['status'].upper())
    item = None

    assert status in [JobPostingStatusEnum.draft, JobPostingStatusEnum.published]

    if id_:
        item = g.db.query(JobPosting).filter(JobPosting.id == id_, JobPosting.company_id == g.company.id).first()

    if not item:
        item = JobPosting(company_id=g.company.id, status=status)
        g.db.add(item)

    item.title = data['title']
    item.description = data['description']
    item.location = data.get('location')

    g.db.commit()

    return make_response(item.to_dict_item())


@bp.get('')
def index_get():
    id_ = request.args['id']

    item = g.db.query(Resume).filter(
        Resume.agency_id == g.agency.id,
        Resume.id == id_,
    ).one()

    return make_response(item.to_dict_item())
