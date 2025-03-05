from sqlalchemy import create_engine, Column, Integer, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(object):
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=text("(timezone('utc', now()))"), nullable=False)
    updated_at = Column(DateTime, default=None)


Base = declarative_base(cls=BaseModel)
