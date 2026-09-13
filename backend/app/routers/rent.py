from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rent import Rent
from app.schemas.rent import RentCreate, RentUpdate
from app.services.rent_service import calculate_rent
from app.utils.deps import require_role
from app.constants import ROLE_INVESTMENT, ROLE_OPERATION

router = APIRouter(prefix="/api/rent", tags=["租金"])


@router.get("/list", summary="租金列表")
def list_rents(db: Session = Depends(get_db),
               user=Depends(require_role(ROLE_INVESTMENT, ROLE_OPERATION))):
    return [r.to_dict() for r in db.query(Rent).all()]


@router.get("/{rent_id}", summary="租金详情")
def get_rent(rent_id: int, db: Session = Depends(get_db),
             user=Depends(require_role(ROLE_INVESTMENT, ROLE_OPERATION))):
    r = db.query(Rent).filter(Rent.id == rent_id).first()
    if not r:
        raise HTTPException(404, "租金不存在")
    return r.to_dict()


@router.post("/add", summary="新增租金")
def add_rent(data: RentCreate, db: Session = Depends(get_db),
             user=Depends(require_role(ROLE_INVESTMENT))):
    rent = Rent(
        tenant_id=data.tenantId,
        shop_id=data.shopId,
        contract_id=data.contractId,
        rent_type=data.rentType,
        area_type=data.areaType,
        rent_level=data.rentLevel,
        billing_cycle=data.billingCycle,
        actual_start_date=data.actualStartDate,
        cycle_start_date=data.cycleStartDate,
        unit_price=data.unitPrice,
        percent_rate=data.percentRate,
        turnover=data.turnover,
        profit=data.profit,
    )
    db.add(rent)
    db.flush()
    # 自动计算金额
    amount = calculate_rent(db, rent)
    if rent.rent_type == "fixed":
        rent.rent_amount_fixed = amount
    else:
        rent.rent_amount_percent = amount
    db.commit()
    return {"message": "新增成功", "id": rent.id}


@router.put("/update", summary="修改租金（营运专属）")
def update_rent(data: RentUpdate, db: Session = Depends(get_db),
                user=Depends(require_role(ROLE_OPERATION))):
    rent = db.query(Rent).filter(Rent.id == data.id).first()
    if not rent:
        raise HTTPException(404, "租金不存在")
    rent.unit_price = data.unitPrice
    rent.percent_rate = data.percentRate
    rent.turnover = data.turnover
    rent.profit = data.profit
    # 重新计算金额
    amount = calculate_rent(db, rent)
    if rent.rent_type == "fixed":
        rent.rent_amount_fixed = amount
    else:
        rent.rent_amount_percent = amount
    db.commit()
    return {"message": "修改成功"}


@router.delete("/{rent_id}", summary="删除租金")
def delete_rent(rent_id: int, db: Session = Depends(get_db),
                user=Depends(require_role(ROLE_INVESTMENT))):
    rent = db.query(Rent).filter(Rent.id == rent_id).first()
    if not rent:
        raise HTTPException(404, "租金不存在")
    db.delete(rent)
    db.commit()
    return {"message": "删除成功"}