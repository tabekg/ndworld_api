from sqlalchemy import String, Column, Text, Date, Integer, ForeignKey, Float, Boolean, Time, DateTime, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class User(Base):
    __tablename__ = 'users'

    attributes = relationship("UserAttribute", back_populates="user", cascade="all, delete-orphan")
    data = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)


class UserAttribute(Base):
    __tablename__ = "user_attributes"

    user_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)

    value_string = Column(String, nullable=True)
    value_integer = Column(Integer, nullable=True)
    value_float = Column(Float, nullable=True)
    value_text = Column(Text, nullable=True)
    value_boolean = Column(Boolean, nullable=True)
    value_date = Column(Date, nullable=True)
    value_time = Column(Time, nullable=True)
    value_datetime = Column(DateTime, nullable=True)
    value_interval = Column(Interval, nullable=True)
    value_data = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)

    user = relationship("User", back_populates="attributes")
