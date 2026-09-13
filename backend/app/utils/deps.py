from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.constants import SESSION_TABLE

# 定义 Bearer 安全方案，auto_error=False 表示没带 token 时不自动报错，交给我们自己处理
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    从 Authorization: Bearer <token> 中提取 token，
    查内存会话表获取当前用户信息。
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="未登录或 token 缺失")
    token = credentials.credentials
    user = SESSION_TABLE.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="token 无效或已过期，请重新登录")
    return user


def require_role(*roles: str):
    def checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="无权限访问该接口")
        return user
    return checker