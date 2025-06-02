from sqlalchemy import Table, Column, Integer, ForeignKey

from utils.database import Base

job_offer_resumes = Table(
    'job_offer_resumes', Base.metadata,
    Column('job_offer_id', Integer, ForeignKey('job_offers.id', ondelete='CASCADE'), primary_key=True),
    Column('resume_id', Integer, ForeignKey('resumes.id', ondelete='CASCADE'), primary_key=True),
)

agency_companies = Table(
    'agency_companies', Base.metadata,
    Column('agency_id', Integer, ForeignKey('agencies.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True),
)
