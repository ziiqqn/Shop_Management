from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.contract import Contract
from app.models.rent import Rent
from app.models.receipt import Receipt
from app.models.bill import Bill
from app.models.shop import Shop


def calculate_rent_amount(db: Session, rent: Rent) -> Decimal:
    """
    根据租金记录计算应收金额：
    - 固定租金：面积 × 单价
    - 抽成租金：利润 × 抽成比 / 100
    """
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

    if rent.rent_type == "percent":
        if rent.profit is None or rent.percent_rate is None:
            return Decimal("0")
        return Decimal(rent.profit) * Decimal(rent.percent_rate) / Decimal("100")

    return Decimal("0")


def generate_receipt_and_bill(db: Session, contract_id: int, receipt_time: date) -> dict:
    """
    为指定合同生成当期收款单和账单。
    返回：{"success": bool, "message": str}
    """
    # 1. 查询合同
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return {"success": False, "message": f"合同 {contract_id} 不存在"}

    if contract.audit_status != 1:
        return {"success": False, "message": f"合同 {contract_id} 未审核通过"}

    # 2. 检查是否已生成本期收款单
    existing = db.query(Receipt).filter(
        Receipt.contract_id == contract_id,
        Receipt.receipt_time == receipt_time
    ).first()
    if existing:
        return {"success": False, "message": f"合同 {contract_id} 在 {receipt_time} 已生成过收款单"}

    # 3. 查询关联租金
    rent = db.query(Rent).filter(Rent.contract_id == contract_id) \
        .order_by(Rent.id.desc()).first()
    if not rent:
        return {"success": False, "message": f"合同 {contract_id} 未找到租金信息"}

    # 4. 计算应收金额
    receivable = calculate_rent_amount(db, rent)
    if receivable <= 0:
        return {"success": False, "message": f"合同 {contract_id} 应收金额无效"}

    # 5. 创建收款单
    receipt = Receipt(
        tenant_id=contract.tenant_id,
        contract_id=contract.id,
        receipt_time=receipt_time,
        receivable_amount=receivable,
        paid_amount=Decimal("0"),
        reminder_sent=0
    )
    db.add(receipt)
    db.flush()  # 获取 receipt.id

    # 6. 创建账单
    bill = Bill(
        tenant_id=contract.tenant_id,
        receipt_id=receipt.id,
        receivable_amount=receivable,
        paid_amount=Decimal("0"),
        bill_month=receipt_time.replace(day=1),
        is_paid=0
    )
    db.add(bill)
    db.commit()

    return {
        "success": True,
        "message": f"合同 {contract_id} 生成成功，应收 {receivable} 元",
        "receipt_id": receipt.id,
        "bill_id": bill.id
    }


def generate_all_monthly_receipts(db: Session, target_date: date = None) -> dict:
    """
    扫描所有有效合同，生成本期收款单/账单。
    由定时任务或手动接口调用。
    """
    if target_date is None:
        target_date = date.today()

    receipt_time = target_date.replace(day=1)

    # 查询所有有效合同（已审核通过且在当前日期范围内）
    contracts = db.query(Contract).filter(
        Contract.audit_status == 1,
        Contract.start_date <= target_date,
        Contract.end_date >= target_date
    ).all()

    total = len(contracts)
    success = 0
    skipped = 0
    failed = 0
    details = []

    for c in contracts:
        result = generate_receipt_and_bill(db, c.id, receipt_time)
        if result["success"]:
            success += 1
        elif "已生成过" in result["message"]:
            skipped += 1
        else:
            failed += 1
        details.append({"contract_id": c.id, **result})

    return {
        "target_date": str(target_date),
        "total_contracts": total,
        "success": success,
        "skipped": skipped,
        "failed": failed,
        "details": details
    }