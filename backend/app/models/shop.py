from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Shop(Base):
    __tablename__ = "shop"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    shop_number = Column(String(20), unique=True, nullable=False)
    floor = Column(String(20), nullable=False)
    floor_index = Column(Integer, nullable=False)
    building_area = Column(DECIMAL(10, 2), default=50.00)
    use_area = Column(DECIMAL(10, 2), default=40.00)
    is_rented = Column(Integer, default=0)
    current_tenant_id = Column(BigInteger, nullable=True)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "shopNumber": self.shop_number,
            "floor": self.floor,
            "floorIndex": self.floor_index,
            "buildingArea": float(self.building_area) if self.building_area else None,
            "useArea": float(self.use_area) if self.use_area else None,
            "isRented": self.is_rented,
            "currentTenantId": self.current_tenant_id,
        }