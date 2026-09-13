from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate, AuditRequest
from app.services.contract_service import generate_contract_no, audit_contract
from app.utils.deps import require_role
from app.constants import ROLE_INVESTMENT, ROLE_FINANCE

router = APIRouter(prefix="/api/contract", tags=["合同"])


@router.get("/list", summary="合同列表")
def list_contracts(db: Session = Depends(get_db),
                   user=Depends(require_role(ROLE_INVESTMENT, ROLE_FINANCE))):
    return [c.to_dict() for c in db.query(Contract).all()]


@router.get("/{contract_id}", summary="合同详情")
def get_contract(contract_id: int, db: Session = Depends(get_db),
                 user=Depends(require_role(ROLE_INVESTMENT, ROLE_FINANCE))):
    c = db.query(Contract).filter(Contract.id == contract_id).first()
    if not c:
        raise HTTPException(404, "合同不存在")
    return c.to_dict()


@router.post("/add", summary="新增合同")
def add_contract(data: ContractCreate, db: Session = Depends(get_db),
                 user=Depends(require_role(ROLE_INVESTMENT))):
    contract_no = generate_contract_no(db, data.shopId)
    contract = Contract(
        contract_no=contract_no,
        shop_id=data.shopId,
        tenant_id=data.tenantId,
        pic_url=data.picUrl,
        start_date=data.startDate,
        end_date=data.endDate,
        audit_status=0
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return {"message": "新增成功", "contractNo": contract_no, "id": contract.id}


@router.put("/update", summary="更新合同")
def update_contract(data: ContractUpdate, db: Session = Depends(get_db),
                    user=Depends(require_role(ROLE_INVESTMENT))):
    contract = db.query(Contract).filter(Contract.id == data.id).first()
    if not contract:
        raise HTTPException(404, "合同不存在")
    contract.shop_id = data.shopId
    contract.tenant_id = data.tenantId
    contract.pic_url = data.picUrl
    contract.start_date = data.startDate
    contract.end_date = data.endDate
    db.commit()
    return {"message": "更新成功"}


@router.delete("/{contract_id}", summary="删除合同")
def delete_contract(contract_id: int, db: Session = Depends(get_db),
                    user=Depends(require_role(ROLE_INVESTMENT))):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(404, "合同不存在")
    db.delete(contract)
    db.commit()
    return {"message": "删除成功"}


@router.put("/audit/{contract_id}", summary="财务审核合同")
def audit(contract_id: int, req: AuditRequest, db: Session = Depends(get_db),
          user=Depends(require_role(ROLE_FINANCE))):
    try:
        audit_contract(db, contract_id, req.approved, req.remark)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"message": "审核完成"}