from sqlalchemy import Column, String, Text, DateTime, event as sa_event, func

from utils.database import Base

from . import user, auth, resume, company, common, worker, agency, category, translation


@sa_event.listens_for(user.User, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()


class Bi(Base):
    __tablename__ = 'bi'

    name = Column(String(55), nullable=False)
    value = Column(Text, nullable=False)
    expired_at = Column(DateTime, default=None)
