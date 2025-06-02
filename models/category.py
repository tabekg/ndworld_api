from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from models.common import resume_categories
from utils.database import Base
from utils.http import orm_to_dict


class Category(Base):
    __tablename__ = 'categories'

    parent_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=True)

    title = Column(String(255), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    parent = relationship("Category", back_populates="parent", passive_deletes=True)
    resumes = relationship("Resume", secondary=resume_categories, back_populates="categories")

    def to_dict_item(self):
        return orm_to_dict(self, [
            'title',
            'payload', 'is_disabled',
            'created_at',
        ])
