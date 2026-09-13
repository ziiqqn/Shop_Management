from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.models.merchant import MerchantAccount
from app.models.tenant import Tenant
from app.schemas.auth import LoginRequest, RegisterRequest, LoginResponse
from app.utils.security import verify_password, hash_password, create_token
from app.constants import BOSS_CREDENTIALS, ROLE_BOSS, ROLE_MERCHANT

router = APIRouter(prefix="/api/auth", tags=["认证"])


# ============================================
# 1. 员工登录
# ============================================
@router.post("/employee/login",  summary="员工登录")
def employee_login(req: LoginRequest, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.job_number == req.username).first()
    if not emp:
        raise HTTPException(status_code=401, detail="工号不存在")
    if not verify_password(req.password, emp.password):
        raise HTTPException(status_code=401, detail="密码错误")

    token = create_token(emp.id, emp.job_number, emp.department)
    return LoginResponse(token=token, role=emp.department, username=emp.job_number)


# ============================================
# 2. 老板登录（硬编码哈希表）
# ============================================
@router.post("/boss/login", response_model=LoginResponse, summary="老板登录")
def boss_login(req: LoginRequest):
    boss = BOSS_CREDENTIALS.get(req.username)
    if not boss:
        raise HTTPException(status_code=401, detail="用户名不存在")
    if not verify_password(req.password, boss["password_hash"]):
        raise HTTPException(status_code=401, detail="密码错误")

    token = create_token(0, req.username, ROLE_BOSS)
    return LoginResponse(token=token, role=ROLE_BOSS, username=req.username)


# ============================================
# 3. 商户登录
# ============================================
@router.post("/merchant/login", response_model=LoginResponse, summary="商户登录")
def merchant_login(req: LoginRequest, db: Session = Depends(get_db)):
    acc = db.query(MerchantAccount).filter(MerchantAccount.username == req.username).first()
    if not acc:
        raise HTTPException(status_code=401, detail="用户名不存在")
    if not verify_password(req.password, acc.password):
        raise HTTPException(status_code=401, detail="密码错误")

    token = create_token(acc.tenant_id, acc.username, ROLE_MERCHANT)
    return LoginResponse(token=token, role=ROLE_MERCHANT, username=acc.username)


# ============================================
# 4. 商户注册
# ============================================
@router.post("/merchant/register", summary="商户注册")
def merchant_register(req: RegisterRequest, db: Session = Depends(get_db)):
    # 检查用户名唯一
    if db.query(MerchantAccount).filter(MerchantAccount.username == req.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 创建租户
    tenant = Tenant(
        name=req.tenantName,
        id_card=req.idCard,
        brand_type=req.brandType,
        brand_name=req.brandName
    )
    db.add(tenant)
    db.flush()  # 获取自增 ID

    # 创建商户账号
    account = MerchantAccount(
        tenant_id=tenant.id,
        username=req.username,
        password=hash_password(req.password)
    )
    db.add(account)
    db.commit()

    return {"message": "注册成功", "tenant_id": tenant.id}