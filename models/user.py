from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


USER_ROLE_LEVELS = {
    0: 'REGULAR',
    10: 'REPORTER',
    30: 'MANAGER',
    50: 'ADMIN',
    100: 'SUPER_ADMIN',
}


class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    # role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", back_populates="user", uselist=False)

    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")
    auth_sessions = relationship("AuthSession", back_populates="user", cascade="all, delete-orphan")

    def to_dict_item(self):
        return orm_to_dict(self, [
            'first_name', 'last_name',
            'payload', 'is_disabled',
            'created_at',
        ], additional_fields={
            'resume': lambda a: a.resume.to_dict_item() if a.resume else None,
        })


class UserRole(Base):
    __tablename__ = 'user_roles'

    level = Column(Integer, nullable=False, default=1, server_default='1')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    branch_id = Column(Integer, ForeignKey('companies.id'), nullable=True)

    user = relationship("User", back_populates="roles")
    company = relationship("Company", back_populates="roles")
    branch = relationship("Branch", back_populates="roles")

    def to_dict_item(self):
        return orm_to_dict(self, [
            'created_at',
        ])
