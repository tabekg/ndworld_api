from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


WORKER_LEVEL_PENDING = 0
WORKER_LEVEL_APPROVED = 100
WORKER_LEVEL_REJECTED = -100
WORKER_LEVEL_HIRED = 200
WORKER_LEVEL_ACTIVE = 500
WORKER_LEVEL_RESIGNED = 600
WORKER_LEVEL_TERMINATED = 700
WORKER_LEVEL_COMPLETED = 1000


class WorkerStep(Base):
    __tablename__ = 'worker_steps'

    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

    level = Column(Integer, nullable=False, default=WORKER_LEVEL_PENDING, server_default=f'{WORKER_LEVEL_PENDING}')
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    comment = Column(Text, nullable=True)

    worker = relationship("Worker", back_populates="steps")
    role = relationship("Role", foreign_keys="WorkerStep.role_id")


class Worker(Base):
    __tablename__ = 'workers'

    agency_id = Column(Integer, ForeignKey('agencies.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    level = Column(Integer, nullable=False, default=WORKER_LEVEL_PENDING, server_default=f'{WORKER_LEVEL_PENDING}')
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    agency = relationship("Agency", back_populates="workers", foreign_keys="Worker.agency_id")
    company = relationship("Company", back_populates="workers", foreign_keys="Worker.company_id")
    resume = relationship("Resume", back_populates="workers", passive_deletes=True)
    category = relationship("Category", back_populates="workers", passive_deletes=True)

    steps = relationship("WorkerStep", back_populates="worker", foreign_keys="WorkerStep.worker_id")
