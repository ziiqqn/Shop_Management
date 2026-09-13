# 角色常量
ROLE_INVESTMENT = "INVESTMENT"
ROLE_FINANCE = "FINANCE"
ROLE_OPERATION = "OPERATION"
ROLE_CASHIER = "CASHIER"
ROLE_BOSS = "BOSS"
ROLE_MERCHANT = "MERCHANT"

# 内存会话哈希表：{token: {user_id, username, role}}
# 简单方案，重启后端会清空
SESSION_TABLE: dict = {}

# 老板硬编码账号（哈希表）
# password_hash 是 "123456" 的 bcrypt 哈希，请用 Python 生成后替换
BOSS_CREDENTIALS = {
    "boss": {
        "password_hash": "$2b$12$SaZ0vmzVqpgEtizaXq.mc.nbXZdvOV29n3sYyChbycEBMn7Wt56Je",
        "role": ROLE_BOSS
    }
}

# 各角色允许访问的模块（路由前缀）
ROLE_PERMISSIONS = {
    ROLE_INVESTMENT: ["/api/tenant", "/api/contract", "/api/rent"],
    ROLE_FINANCE:    ["/api/contract/audit"],
    ROLE_OPERATION:  ["/api/rent/update", "/api/shop/exit"],
    ROLE_CASHIER:    ["/api/receipt"],
    ROLE_BOSS:       ["/api/shop", "/api/employee/register"],
}