from sqlalchemy import String, Column, Text, UniqueConstraint, Index

from utils.database import Base


class Translation(Base):
    __tablename__ = 'translations'

    source_language = Column(String(255), nullable=True)
    target_language = Column(String(255), nullable=False)

    source_text = Column(Text, nullable=False)
    target_text = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint('source_language', 'target_language', 'source_text', name='uq_translation_key'),
        Index('ix_translation_lookup', 'source_language', 'target_language', 'source_text'),
    )
