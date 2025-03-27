from sqlalchemy import String, Column, Text, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from utils.database import Base
from utils.http import orm_to_dict


class Candidate(Base):
    __tablename__ = 'candidates'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    summary = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone_number = Column(String(255), nullable=True)
    marital_status = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    about = Column(Text, nullable=True)

    photo_path = Column(String(255), nullable=True)
    photo_id = Column(Integer, nullable=True)

    front_passport_id = Column(Integer, nullable=True)
    back_passport_id = Column(Integer, nullable=True)
    front_passport_path = Column(String(255), nullable=True)
    back_passport_path = Column(String(255), nullable=True)

    experiences = relationship("CandidateExperience", back_populates="candidate", cascade="all, delete-orphan")
    educations = relationship("CandidateEducation", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan")

    user = relationship("User", back_populates="candidate")

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


class CandidateExperience(Base):
    __tablename__ = 'candidate_experiences'

    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Может быть пустым, если человек все еще работает
    description = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="experiences")

    def to_dict_item(self):
        return orm_to_dict(self, ['company', 'position', 'start_date', 'end_date', 'description', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['company', 'position', 'start_date', 'end_date', 'description', 'created_at'])


class CandidateEducation(Base):
    __tablename__ = 'candidate_educations'

    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="educations")

    def to_dict_item(self):
        return orm_to_dict(self, ['institution', 'degree', 'start_date', 'end_date', 'description', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['institution', 'degree', 'start_date', 'end_date', 'description', 'created_at'])


class CandidateSkill(Base):
    __tablename__ = 'candidate_skills'

    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced

    candidate = relationship("Candidate", back_populates="skills")

    def to_dict_item(self):
        return orm_to_dict(self, ['skill_name', 'proficiency', 'created_at'])

    def to_dict_list(self):
        return orm_to_dict(self, ['skill_name', 'proficiency', 'created_at'])
