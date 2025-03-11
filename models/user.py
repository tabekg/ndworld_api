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

    # provider_name = Column(String(255), nullable=False)
    # provider_uid = Column(String(255), nullable=True)
    # provider_id = Column(String(255), nullable=False)
    # number = Column(String(35), nullable=True)
    # encrypted_password = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    contact_email = Column(String(255), nullable=True)
    contact_phone_number = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    about = Column(Text, nullable=True)

    # role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)
    fcm_token = Column(String(255), nullable=True)
    # warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=True)
    # selected_warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=True)

    experiences = relationship("UserExperience", back_populates="user", cascade="all, delete-orphan")
    educations = relationship("UserEducation", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")

    # warehouse = relationship('Warehouse', foreign_keys=[warehouse_id])
    # selected_warehouse = relationship('Warehouse', foreign_keys=[selected_warehouse_id])
    # codes = relationship('UserCode', back_populates='user')


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
