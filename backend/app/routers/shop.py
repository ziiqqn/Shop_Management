from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.shop import Shop
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/shop", tags=["商铺"])


@router.get("/list", summary="获取所有商铺")
def list_shops(db: Session = Depends(get_db), user=Depends(get_current_user)):
    shops = db.query(Shop).order_by(Shop.floor_index, Shop.shop_number).all()
    return [s.to_dict() for s in shops]


@router.get("/{shop_id}", summary="获取单个商铺")
def get_shop(shop_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="商铺不存在")
    return shop.to_dict()