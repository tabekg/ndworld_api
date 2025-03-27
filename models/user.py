from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


# class UserRoleEnum(str, enum.Enum):
#     super_admin = 'SUPER_ADMIN'
#     admin = 'ADMIN'
#     manager = 'MANAGER'
#
#
# AVAILABLE_USER_ROLES = [UserRoleEnum.super_admin, UserRoleEnum.admin, UserRoleEnum.manager]


class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    # role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    candidate = relationship("Candidate", back_populates="user", uselist=False)

    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")
    auth_sessions = relationship("AuthSession", back_populates="user", cascade="all, delete-orphan")

    def to_dict_item(self):
        return orm_to_dict(self, [
            'first_name', 'last_name',
            'payload', 'is_disabled',
            'created_at',
        ], additional_fields={
            'candidate': lambda a: a.candidate.to_dict_item() if a.candidate else None,
        })
