from sqlalchemy import Column, Integer, String, LargeBinary, Text, DateTime
from sqlalchemy.sql import func
from db.db_base import Base

class CVJobPair(Base):
    __tablename__ = 'cv_job_pair'

    id = Column(Integer, primary_key=True, index=True)
    cv_filename = Column(String, index=True)
    cv_content = Column(LargeBinary)
    job_filename = Column(String, index=True)
    job_content = Column(LargeBinary)
    grade = Column(Integer)
    insights = Column(Text)
    status = Column(String, default='pending')
    matching = Column(Text)
    not_matching = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
