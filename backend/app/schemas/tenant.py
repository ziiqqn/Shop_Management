from pydantic import BaseModel, Field
from typing import Optional


class TenantCreate(BaseModel):
    name: str = Field(..., max_length=50)
    idCard: str = Field(..., min_length=18, max_length=18)
    brandType: str = Field(..., description="连锁 / 个体")
    brandName: Optional[str] = None


class TenantUpdate(TenantCreate):
    id: int