from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class Category(Base):
    __tablename__ = 'categories'

    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    title_ky = Column(String(255), nullable=False)
    title_tr = Column(String(255), nullable=False)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    resume_fields = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)

    parent = relationship("Category", passive_deletes=True)
    companies = relationship("Company", back_populates='category', passive_deletes=True)
