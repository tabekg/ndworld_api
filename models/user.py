from sqlalchemy import String, Column, Boolean, Integer, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict



class Role(Base):
    __tablename__ = 'roles'

    permissions = Column(ARRAY(VARCHAR(255)), nullable=False, default=list, server_default='{}')

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=True)
    agency_id = Column(Integer, ForeignKey('agencies.id', ondelete='CASCADE'), nullable=True)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="roles", passive_deletes=True)
    company = relationship("Company", back_populates="roles", passive_deletes=True)
    agency = relationship("Agency", back_populates="roles", passive_deletes=True)
    auth_sessions = relationship("AuthSession", back_populates="role", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'created_at',
        ])


class User(Base):
    __tablename__ = 'users'

    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    roles = relationship("Role", back_populates="user", passive_deletes=True, order_by=Role.id.asc())
    auth_providers = relationship("AuthProvider", back_populates="user", passive_deletes=True)
    auth_sessions = relationship("AuthSession", back_populates="user", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'name', 'surname',
            'payload', 'is_disabled',
            'created_at',
        ], {
            'roles': lambda a: orm_to_dict(a.roles, [], {
                'company': lambda b: orm_to_dict(b.company, ['title']) if b.company else None,
                'agency': lambda b: orm_to_dict(b.agency, ['title']) if b.agency else None,
            }),
        })
