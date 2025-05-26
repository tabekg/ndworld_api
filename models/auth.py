from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base
from utils.http import orm_to_dict


class AuthProvider(Base):
    __tablename__ = 'auth_providers'

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    identifier = Column(String(255), nullable=False)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="auth_providers", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, ['name', 'identifier', 'payload'])


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=True)

    hash = Column(String(255), nullable=False, unique=True)
    fcm_token = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)

    expired_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_action_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="auth_sessions", passive_deletes=True)
    role = relationship("Role", back_populates="auth_sessions", passive_deletes=True)

    def to_dict_item(self):
        return orm_to_dict(self, ['expired_at', 'is_active', 'created_at', 'last_action_at'])
