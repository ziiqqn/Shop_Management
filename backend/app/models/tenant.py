from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenant"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    id_card = Column(String(18))
    brand_type = Column(String(10))
    brand_name = Column(String(50))
    create_time = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "idCard": self.id_card,
            "brandType": self.brand_type,
            "brandName": self.brand_name,
        }