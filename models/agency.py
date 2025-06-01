from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class Agency(Base):
    __tablename__ = 'agencies'

    title = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)

    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)

    roles = relationship("Role", back_populates="agency", passive_deletes=True)
    resumes = relationship("Resume", back_populates="agency", passive_deletes=True)
