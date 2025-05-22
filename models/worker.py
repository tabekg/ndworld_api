import enum

from sqlalchemy import Column, Text, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from utils.database import Base


class WorkerStatusEnum(str, enum.Enum):
    pending = 'PENDING'
    hired = 'HIRED'
    rejected = 'REJECTED'
    #   TODO: more statuses...
    active = 'ACTIVE'
    resigned = 'RESIGNED'
    terminated = "TERMINATED"
    completed = "COMPLETED"


class Worker(Base):
    __tablename__ = 'workers'

    agent_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id', ondelete='CASCADE'), nullable=False)
    job_offer_id = Column(Integer, ForeignKey('job_offers.id', ondelete='CASCADE'), nullable=False)

    status = Column(Enum(WorkerStatusEnum), nullable=False)
    hired_at = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)

    agent = relationship("Company", back_populates="workers", foreign_keys="Worker.agent_id")
    company = relationship("Company", back_populates="workers", foreign_keys="Worker.company_id")
    resume = relationship("Resume", back_populates="workers", passive_deletes=True)
    job_posting = relationship("JobPosting", back_populates="workers", passive_deletes=True)
    job_offer = relationship("JobOffer", back_populates="workers", passive_deletes=True)
