from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel

from app.database import get_db
from app.models.receipt import Receipt
from app.services.receipt_service import (
    generate_receipt_and_bill,
    generate_all_monthly_receipts
)
from app.utils.deps import require_role
from app.constants import ROLE_CASHIER, ROLE_INVESTMENT

router = APIRouter(prefix="/api/receipt", tags=["收款单"])


class GenerateRequest(BaseModel):
    contractId: int
    receiptTime: date


# ============================================
# 原有接口
# ============================================
@router.get("/list", summary="收款单列表")
def list_receipts(db: Session = Depends(get_db),
                  user=Depends(require_role(ROLE_CASHIER))):
    return [r.to_dict() for r in db.query(Receipt).all()]


@router.put("/remind/{receipt_id}", summary="发送催收")
def send_reminder(receipt_id: int, db: Session = Depends(get_db),
                  user=Depends(require_role(ROLE_CASHIER))):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(404, "收款单不存在")
    receipt.reminder_sent = 1
    db.commit()
    return {"message": "催收已发送"}


@router.put("/paid/{receipt_id}", summary="修改实收金额")
def update_paid(receipt_id: int, amount: float, db: Session = Depends(get_db),
                user=Depends(require_role(ROLE_CASHIER))):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(404, "收款单不存在")
    receipt.paid_amount = amount
    db.commit()
    return {"message": "修改成功"}


# ============================================
# 新增：手动为单份合同生成
# ============================================
@router.post("/generate", summary="手动为指定合同生成收款单和账单")
def manual_generate(req: GenerateRequest, db: Session = Depends(get_db),
                    user=Depends(require_role(ROLE_INVESTMENT, ROLE_CASHIER))):
    result = generate_receipt_and_bill(db, req.contractId, req.receiptTime)
    if not result["success"]:
        raise HTTPException(400, result["message"])
    return result


# ============================================
# 新增：批量生成（测试用，或月度手动触发）
# ============================================
@router.post("/generate-batch", summary="批量生成当月收款单和账单")
def manual_generate_batch(db: Session = Depends(get_db),
                          user=Depends(require_role(ROLE_INVESTMENT, ROLE_CASHIER))):
    result = generate_all_monthly_receipts(db)
    return result