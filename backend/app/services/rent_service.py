from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.rent import Rent
from app.models.shop import Shop


def calculate_rent(db: Session, rent: Rent) -> Decimal:
    """根据租金类型计算金额"""
    shop = db.query(Shop).filter(Shop.id == rent.shop_id).first()
    if not shop:
        return Decimal("0")

    area = shop.building_area if rent.area_type == "building" else shop.use_area
    if area is None:
        return Decimal("0")

    if rent.rent_type == "fixed":
        if rent.unit_price is None:
            return Decimal("0")
        return Decimal(area) * Decimal(rent.unit_price)
    elif rent.rent_type == "percent":
        if rent.profit is None or rent.percent_rate is None:
            return Decimal("0")
        return Decimal(rent.profit) * Decimal(rent.percent_rate) / Decimal("100")
    return Decimal("0")