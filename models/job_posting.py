import enum

from sqlalchemy import String, Column, Text, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from models.common import job_offer_resumes
from utils.database import Base


class JobPostingStatusEnum(enum.Enum):
    draft = 'DRAFT'
    published = 'PUBLISHED'
    closed = 'CLOSED'
    archived = 'ARCHIVED'


class JobOfferStatusEnum(enum.Enum):
    pending = 'PENDING'
    viewed = 'VIEWED'
    closed = 'CLOSED'
    withdrawn = 'WITHDRAWN'
    expired = 'EXPIRED'


class JobPosting(Base):
    __tablename__ = 'job_postings'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(Enum(JobPostingStatusEnum), nullable=False, default=JobPostingStatusEnum.draft)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    company = relationship("Company", back_populates="job_postings", passive_deletes=True)
    job_offers = relationship("JobOffer", back_populates="job_posting", passive_deletes=True)
    workers = relationship("Worker", back_populates="job_posting", passive_deletes=True)


class JobOffer(Base):
    __tablename__ = 'job_offers'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id', ondelete='CASCADE'), nullable=False)

    status = Column(Enum(JobOfferStatusEnum), nullable=False, server_default='pending')
    sent_at = Column(DateTime, server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    message = Column(Text, nullable=True)

    resumes = relationship("Resume", secondary=job_offer_resumes, back_populates="job_offers")
    company = relationship("Company", back_populates="offers", passive_deletes=True)
    job_posting = relationship("JobPosting", back_populates="offers", passive_deletes=True)
    workers = relationship("Worker", back_populates="job_offer", passive_deletes=True)
