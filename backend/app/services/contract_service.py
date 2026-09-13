from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.models.shop import Shop
from app.models.rent import Rent
from datetime import date


def generate_contract_no(db: Session, shop_id: int) -> str:
    """生成合同号：铺位号-三位序号"""
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise ValueError("商铺不存在")

    last = db.query(Contract).filter(Contract.shop_id == shop_id) \
        .order_by(Contract.id.desc()).first()

    seq = 1
    if last:
        suffix = last.contract_no.split("-")[-1]
        try:
            seq = int(suffix) + 1
        except ValueError:
            seq = 1
    return f"{shop.shop_number}-{seq:03d}"


def audit_contract(db: Session, contract_id: int, approved: bool, remark: str = None):
    """财务审核合同"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise ValueError("合同不存在")
    if contract.audit_status != 0:
        raise ValueError("该合同已审核")

    contract.audit_status = 1 if approved else 2
    contract.audit_remark = remark

    if approved:
        # 更新商铺状态
        shop = db.query(Shop).filter(Shop.id == contract.shop_id).first()
        if shop:
            shop.is_rented = 1
            shop.current_tenant_id = contract.tenant_id

    db.commit()
    return True