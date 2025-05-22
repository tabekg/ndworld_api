from sqlalchemy import String, Column, Boolean, Integer, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    # role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", back_populates="user", uselist=False, passive_deletes=True)
    roles = relationship("Role", back_populates="user", passive_deletes=True)
    auth_providers = relationship("AuthProvider", back_populates="user", passive_deletes=True)
    auth_sessions = relationship("AuthSession", back_populates="user", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'first_name', 'last_name',
            'payload', 'is_disabled',
            'created_at',
        ], additional_fields={
            'resume': lambda a: a.resume.to_dict_item() if a.resume else None,
        })


class Role(Base):
    __tablename__ = 'roles'

    permissions = Column(ARRAY(VARCHAR(255)), nullable=False, default=list, server_default='{}')

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=True)
    branch_id = Column(Integer, ForeignKey('branches.id', ondelete='CASCADE'), nullable=True)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="roles", passive_deletes=True)
    company = relationship("Company", back_populates="roles", passive_deletes=True)
    branch = relationship("Branch", back_populates="roles", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, [
            'created_at',
        ])
