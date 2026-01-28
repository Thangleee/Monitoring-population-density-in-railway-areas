
from sqlalchemy import Column, Integer, DateTime
from database import Base
from datetime import datetime

class PeopleCount(Base):
    __tablename__ = "people_density"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    density = Column(Integer)
