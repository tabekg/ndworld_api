import enum

from sqlalchemy import String, Column, Boolean, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


class CompanyTypeEnum(str, enum.Enum):
    employer = 'EMPLOYER'
    recruitment = 'RECRUITMENT'


AVAILABLE_COMPANY_TYPES = [CompanyTypeEnum.employer, CompanyTypeEnum.recruitment]


class Company(Base):
    __tablename__ = 'companies'

    title = Column(String(255), nullable=False)

    type = Column(Enum(CompanyTypeEnum), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    branches = relationship("Branch", back_populates="company", passive_deletes=True)
    roles = relationship("Role", back_populates="company", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'title', 'type',
            'payload', 'is_disabled',
            'created_at',
        ])


class Branch(Base):
    __tablename__ = 'branches'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)

    address = Column(String(255), nullable=False)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    company = relationship("Company", back_populates="branches", passive_deletes=True)
    roles = relationship("Role", back_populates="branch", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'address',
            'payload', 'is_disabled',
            'created_at',
        ])
