from pydantic import BaseModel
from datetime import date
from typing import Optional


class ContractCreate(BaseModel):
    shopId: int
    tenantId: int
    picUrl: Optional[str] = None
    startDate: date
    endDate: date


class ContractUpdate(ContractCreate):
    id: int


class AuditRequest(BaseModel):
    approved: bool
    remark: Optional[str] = None