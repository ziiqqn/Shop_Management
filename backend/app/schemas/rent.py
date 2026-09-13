from pydantic import BaseModel
from datetime import date
from typing import Optional


class RentCreate(BaseModel):
    tenantId: int
    shopId: int
    contractId: Optional[int] = None
    rentType: str
    areaType: str
    rentLevel: str
    billingCycle: str
    actualStartDate: date
    cycleStartDate: date
    unitPrice: Optional[float] = None
    percentRate: Optional[float] = None
    turnover: Optional[float] = None
    profit: Optional[float] = None


class RentUpdate(RentCreate):
    id: int