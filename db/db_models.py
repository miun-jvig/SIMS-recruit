from sqlalchemy import Column, Integer, String, LargeBinary, Text, DateTime
from db.db import base
from sqlalchemy.sql import func

class CVJobPair(base):
    __tablename__ = 'cv_job_pair'

    id = Column(Integer, primary_key=True, index=True)
    cv_filename = Column(String, index=True)
    cv_content = Column(LargeBinary)  # Store cv as blob
    job_filename = Column(String, index=True)
    job_content = Column(LargeBinary)  # Store job as blob
    grade = Column(Integer)  # Store grade from LLM
    insights = Column(Text)  # Store reasoning as text
    status = Column(String, default='uploaded')  # Track status of the pair
    matching = Column(Text)  # Store matching details as text
    not_matching = Column(Text)  # Store not matching details as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
