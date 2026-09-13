from sqlalchemy import Column, BigInteger, String, Date, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Rent(Base):
    __tablename__ = "rent"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(BigInteger, nullable=False)
    shop_id = Column(BigInteger, nullable=False)
    contract_id = Column(BigInteger)
    rent_type = Column(String(10), nullable=False)
    area_type = Column(String(10), nullable=False)
    rent_level = Column(String(20), nullable=False)
    billing_cycle = Column(String(10), nullable=False)
    actual_start_date = Column(Date, nullable=False)
    cycle_start_date = Column(Date, nullable=False)
    unit_price = Column(DECIMAL(10, 2))
    rent_amount_fixed = Column(DECIMAL(10, 2))
    percent_rate = Column(DECIMAL(5, 2))
    turnover = Column(DECIMAL(12, 2))
    profit = Column(DECIMAL(12, 2))
    rent_amount_percent = Column(DECIMAL(12, 2))
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "tenantId": self.tenant_id,
            "shopId": self.shop_id,
            "contractId": self.contract_id,
            "rentType": self.rent_type,
            "areaType": self.area_type,
            "rentLevel": self.rent_level,
            "billingCycle": self.billing_cycle,
            "unitPrice": float(self.unit_price) if self.unit_price else None,
            "rentAmountFixed": float(self.rent_amount_fixed) if self.rent_amount_fixed else None,
            "percentRate": float(self.percent_rate) if self.percent_rate else None,
            "profit": float(self.profit) if self.profit else None,
            "rentAmountPercent": float(self.rent_amount_percent) if self.rent_amount_percent else None,
        }