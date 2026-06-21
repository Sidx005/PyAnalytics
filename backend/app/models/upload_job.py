from sqlalchemy import Column, Integer,String, DateTime


from datetime import datetime
from app.database import Base


class UploadJob(Base):

    __tablename__ = "upload_jobs"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    uploaded_at = Column(DateTime, default=datetime.utcnow,nullable=False)

    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)