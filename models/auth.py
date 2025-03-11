from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class AuthProvider(Base):
    __tablename__ = 'auth_providers'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    identity = Column(String(255), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="auth_providers")
