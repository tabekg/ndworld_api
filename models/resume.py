import enum

from sqlalchemy import String, Column, Text, Date, Integer, ForeignKey, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from models.common import job_offer_resumes
from utils.database import Base
from utils.http import orm_to_dict


class ResumeStatusEnum(str, enum.Enum):
    draft = 'DRAFT'
    available = 'AVAILABLE'
    archived = 'ARCHIVED'
    unavailable = 'UNAVAILABLE'


class Resume(Base):
    __tablename__ = 'resumes'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)

    status = Column(Enum(ResumeStatusEnum), nullable=False)
    summary = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone_number = Column(String(255), nullable=True)
    contact_whatsapp = Column(String(255), nullable=True)
    marital_status = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    about = Column(Text, nullable=True)

    photo_path = Column(String(255), nullable=True)
    photo_id = Column(Integer, nullable=True)
    front_passport_id = Column(Integer, nullable=True)
    back_passport_id = Column(Integer, nullable=True)
    front_passport_path = Column(String(255), nullable=True)
    back_passport_path = Column(String(255), nullable=True)

    experiences = relationship("ResumeExperience", back_populates="resume", passive_deletes=True)
    educations = relationship("ResumeEducation", back_populates="resume", passive_deletes=True)
    skills = relationship("ResumeSkill", back_populates="resume", passive_deletes=True)

    company = relationship("Company", back_populates="resumes")
    job_offers = relationship("JobOffer", secondary=job_offer_resumes, back_populates="resumes")
    workers = relationship("Worker", back_populates="resume", passive_deletes=True)

    @hybrid_property
    def is_active(self):
        return self.status == ResumeStatusEnum.available

    @is_active.expression
    def is_active(cls):
        return cls.status == ResumeStatusEnum.available

    def to_dict_item(self):
        return orm_to_dict(self, [
            'summary',
            'contact_email', 'contact_phone_number',
            'marital_status',
            'birth_date', 'about',
            'photo_path',
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
