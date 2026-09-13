from pydantic import BaseModel
from typing import Optional


class ShopResponse(BaseModel):
    id: int
    shopNumber: str
    floor: str
    floorIndex: int
    buildingArea: Optional[float]
    useArea: Optional[float]
    isRented: int
    currentTenantId: Optional[int]

    class Config:
        from_attributes = True