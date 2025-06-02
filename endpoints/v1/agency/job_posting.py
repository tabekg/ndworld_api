from flask import Blueprint, g, request

from models.job_posting import JobPosting
from utils.http import make_response, orm_to_dict

bp = Blueprint('job-posting', __name__, url_prefix='/job-posting')


@bp.get('/latest')
def latest_get():
    items = g.db.query(JobPosting).order_by(JobPosting.id.desc()).limit(10).all()
    return make_response(
        [orm_to_dict(i, [
            'title',
            'description',
            'location',
            'status',
        ], {
                         'company': lambda a: orm_to_dict(a.company, ['title'])
                     }) for i in items],
    )


@bp.get('')
def index_get():
    id_ = request.args.get('id')

    if id_:
        item = g.db.query(JobPosting).filter(JobPosting.id == id_).one()
        return make_response(
            orm_to_dict(item, [
                'title',
                'description',
                'location',
                'status',
            ], {
                            'company': lambda a: orm_to_dict(a.company, [
                                'title',
                                'address'
                            ])
                        }),
        )

    return make_response()
