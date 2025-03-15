from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


class AuthProvider(Base):
    __tablename__ = 'auth_providers'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    identity = Column(String(255), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="auth_providers")

    def to_dict_item(self):
        return orm_to_dict(self, ['name', 'identity', 'payload'])


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hash = Column(String(255), nullable=False, unique=True)
    fcm_token = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    expired_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="auth_sessions")

    def to_dict_item(self):
        return orm_to_dict(self, ['expired_at', 'is_active', 'created_at'])
