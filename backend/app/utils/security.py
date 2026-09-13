from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings
from app.constants import SESSION_TABLE

# 密码哈希上下文（bcrypt 算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """对明文密码进行 bcrypt 哈希"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """校验明文密码与哈希是否匹配"""
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False


def create_token(user_id: int, username: str, role: str) -> str:
    """
    生成 JWT token 并写入内存会话表
    :param user_id: 用户 ID（员工为 employee.id，商户为 tenant_id，老板为 0）
    :param username: 用户名（工号或商户名）
    :param role: 角色（INVESTMENT/FINANCE/OPERATION/CASHIER/MERCHANT/BOSS）
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    # 写入内存哈希表（简单方案，重启清空）
    SESSION_TABLE[token] = {
        "user_id": user_id,
        "username": username,
        "role": role
    }
    return token


def decode_token(token: str) -> dict | None:
    """解析 JWT，失败返回 None"""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None