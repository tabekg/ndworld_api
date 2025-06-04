from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from models.common import agency_companies
from utils.database import Base
from utils.http import orm_to_dict


class Company(Base):
    __tablename__ = 'companies'

    title = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    workers = relationship("Worker", back_populates="company", passive_deletes=True, foreign_keys='Worker.company_id')
    roles = relationship("Role", back_populates="company", passive_deletes=True)

    agencies = relationship("Agency", secondary=agency_companies, back_populates="companies")

    def to_dict_item(self):
        return orm_to_dict(self, [
            'title', 'address',
            'payload', 'is_disabled',
        ])
