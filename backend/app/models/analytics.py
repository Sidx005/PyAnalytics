
from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime
from app.database import Base
class Analytics(Base):
    __tablename__="analytics"

    id=Column(Integer,primary_key=True,index=True)
    metric_name=Column(String,nullable=False)
    metric_value=Column(String,nullable=False)
    generated_at=Column(DateTime,default=datetime.utcnow,nullable=False)