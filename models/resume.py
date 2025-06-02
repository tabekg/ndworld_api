import enum

from sqlalchemy import String, Column, Text, Date, Integer, ForeignKey, Enum, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from models.common import resume_categories
from utils.database import Base
from utils.http import orm_to_dict


class ResumeStatusEnum(str, enum.Enum):
    draft = 'DRAFT'
    available = 'AVAILABLE'
    archived = 'ARCHIVED'
    unavailable = 'UNAVAILABLE'


class Resume(Base):
    __tablename__ = 'resumes'

    agency_id = Column(Integer, ForeignKey('agencies.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(ResumeStatusEnum), nullable=False)

    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=True)

    summary = Column(Text, nullable=True)
    marital_status = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    about = Column(Text, nullable=True)
    residential_address = Column(String(255), nullable=True)
    registered_address = Column(String(255), nullable=True)

    instagram = Column(String(255), nullable=True)
    telegram = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    phone_numbers = Column(ARRAY(String(30)), nullable=True)

    photo = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    photos = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    passport_front = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    passport_back = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    birth_certificate = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    experiences = relationship("ResumeExperience", back_populates="resume", passive_deletes=True)
    educations = relationship("ResumeEducation", back_populates="resume", passive_deletes=True)
    skills = relationship("ResumeSkill", back_populates="resume", passive_deletes=True)

    agency = relationship("Agency", back_populates="resumes")
    role = relationship("Role", back_populates="resumes")
    workers = relationship("Worker", back_populates="resume", passive_deletes=True)
    categories = relationship("Category", secondary=resume_categories, back_populates="resumes")

    @hybrid_property
    def is_active(self):
        return self.status == ResumeStatusEnum.available

    @is_active.expression
    def is_active(cls):
        return cls.status == ResumeStatusEnum.available

    def to_dict_item(self):
        return orm_to_dict(self, [
            'status',

            'name',
            'surname',
            'patronymic',

            'summary',
            'marital_status',
            'birth_date',
            'about',
            'residential_address',
            'registered_address',

            'instagram',
            'telegram',
            'email',
            'linkedin',
            'phone_number',
            'phone_numbers',

            'photo',
            'photos',
            'passport_front',
            'passport_back',
            'birth_certificate',
        ], additional_fields={
            'experiences': lambda a: orm_to_dict(a.experiences),
            'educations': lambda a: orm_to_dict(a.educations),
            'skills': lambda a: orm_to_dict(a.skills),
        })


class ResumeExperience(Base):
    __tablename__ = 'resume_experiences'

    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)

    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Может быть пустым, если человек все еще работает
    description = Column(Text, nullable=True)

    resume = relationship("Resume", back_populates="experiences", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, ['company', 'position', 'start_date', 'end_date', 'description', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['company', 'position', 'start_date', 'end_date', 'description', 'created_at'])


class ResumeEducation(Base):
    __tablename__ = 'resume_educations'

    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)

    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    resume = relationship("Resume", back_populates="educations", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, ['institution', 'degree', 'start_date', 'end_date', 'description', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['institution', 'degree', 'start_date', 'end_date', 'description', 'created_at'])


class ResumeSkill(Base):
    __tablename__ = 'resume_skills'

    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced

    resume = relationship("Resume", back_populates="skills", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, ['skill_name', 'proficiency', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['skill_name', 'proficiency', 'created_at'])
