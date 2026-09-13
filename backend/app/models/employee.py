from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    job_number = Column(String(20), unique=True, nullable=False)
    department = Column(String(20), nullable=False)
    rank = Column(String(10), nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "jobNumber": self.job_number,
            "department": self.department,
            "rank": self.rank,
        }