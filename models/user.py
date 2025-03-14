from sqlalchemy import String, Column, Boolean, Text, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


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

    contact_email = Column(String(255), nullable=True)
    contact_phone_number = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    about = Column(Text, nullable=True)

    # role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    experiences = relationship("UserExperience", back_populates="user", cascade="all, delete-orphan")
    educations = relationship("UserEducation", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")

    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")
    auth_sessions = relationship("AuthSession", back_populates="user", cascade="all, delete-orphan")


class UserExperience(Base):
    __tablename__ = 'user_experiences'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Может быть пустым, если человек все еще работает
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="experiences")


class UserEducation(Base):
    __tablename__ = 'user_educations'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="educations")


class UserSkill(Base):
    __tablename__ = 'user_skills'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), nullable=True)  # Например, Beginner, Intermediate, Advanced

    user = relationship("User", back_populates="skills")
