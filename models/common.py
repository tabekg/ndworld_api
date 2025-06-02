from sqlalchemy import Table, Column, Integer, ForeignKey

from utils.database import Base

agency_companies = Table(
    'agency_companies', Base.metadata,
    Column('agency_id', Integer, ForeignKey('agencies.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True),
)

resume_categories = Table(
    'resume_categories', Base.metadata,
    Column('resume_id', Integer, ForeignKey('resumes.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
)
