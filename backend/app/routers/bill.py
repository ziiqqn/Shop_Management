from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bill import Bill
from app.models.receipt import Receipt
from app.utils.deps import require_role
from app.constants import ROLE_MERCHANT

router = APIRouter(prefix="/api/bill", tags=["账单"])


@router.get("/list", summary="商户查看自己的账单")
def list_bills(db: Session = Depends(get_db),
               user=Depends(require_role(ROLE_MERCHANT))):
    tenant_id = user["user_id"]
    bills = db.query(Bill).filter(Bill.tenant_id == tenant_id) \
        .order_by(Bill.bill_month.desc()).all()
    return [b.to_dict() for b in bills]


@router.post("/pay/{bill_id}", summary="商户缴费")
def pay_bill(bill_id: int, amount: float, channel: str = "wechat",
             db: Session = Depends(get_db),
             user=Depends(require_role(ROLE_MERCHANT))):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(404, "账单不存在")
    if bill.tenant_id != user["user_id"]:
        raise HTTPException(403, "无权操作此账单")
    if bill.is_paid == 1:
        raise HTTPException(400, "账单已结清")

    new_paid = float(bill.paid_amount) + amount
    if new_paid > float(bill.receivable_amount):
        raise HTTPException(400, "缴费金额超过应收金额")

    bill.paid_amount = new_paid
    bill.payment_channel = channel
    if new_paid == float(bill.receivable_amount):
        bill.is_paid = 1

    # 同步更新收款单
    receipt = db.query(Receipt).filter(Receipt.id == bill.receipt_id).first()
    if receipt:
        receipt.paid_amount = float(receipt.paid_amount) + amount

    db.commit()
    return {"message": "缴费成功", "paidAmount": new_paid, "isPaid": bill.is_paid}