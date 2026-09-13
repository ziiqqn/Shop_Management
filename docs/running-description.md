# 商铺信息管理系统 - 运行说明

> 本系统为基于 FastAPI + Vue 3 + MySQL 的商铺租赁全生命周期管理系统。
> 项目采用前后端一体化部署：**一个端口同时提供前端页面和 API 接口**。

---

## 一、环境要求

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.11 或更高 | 后端运行环境 |
| MySQL | 8.0 或更高 | 数据库 |
| pip | 最新版 | 依赖管理 |
| 浏览器 | Chrome / Edge / Firefox | 访问前端 |
| Git | 任意版本 | 拉取代码（可选） |
| Docker | 20.10+ | 使用容器部署时需安装（可选） |

---

## 二、快速开始（本地运行）

### 步骤 1：克隆项目

```bash
git clone https://github.com/你的用户名/shop-management-python.git
cd shop-management-python
```

### 步骤 2：初始化数据库

1. 启动 MySQL 服务
2. 创建数据库并执行初始化脚本：

```bash
mysql -u root -p < database/init.sql
```

脚本会自动完成：
- 创建 `shop_db` 数据库
- 建立 11 张业务表
- 插入 15 个商铺、4 个员工、1 个布局配置

### 步骤 3：配置后端

```bash
cd backend
cp .env.example .env
```

编辑 `.env`，修改数据库密码：

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=shop_db
JWT_SECRET=change-this-to-a-long-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 步骤 4：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 5：启动服务

```bash
python run.py
```

控制台出现以下输出即启动成功：

```
[调度器] 已启动，下次执行时间：2026-10-01 02:00:00+08:00
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 步骤 6：访问系统

浏览器打开：**http://localhost:8000**

> ⚠️ 注意：不要访问 `http://0.0.0.0:8000`，`0.0.0.0` 是服务器监听地址，不是可访问地址。
> 请使用 `localhost` 或 `127.0.0.1`。

---

## 三、默认测试账号

| 角色 | 用户名 | 密码 | 登录入口 |
|------|--------|------|----------|
| 招商 | INV001 | 123456 | 员工登录 |
| 财务 | FIN001 | 123456 | 员工登录 |
| 营运 | OPE001 | 123456 | 员工登录 |
| 收银 | CAS001 | 123456 | 员工登录 |
| 商户 | zhangsan | 123456 | 商户登录 |
| 老板 | boss | 123456 | 老板登录 |

> 商户账号如未预置，可在登录页点击"商户注册"自行创建。

---

## 四、Docker 部署（推荐生产环境）

### 步骤 1：构建镜像

```bash
docker build -f deploy/Dockerfile -t shop-management .
```

### 步骤 2：运行容器

```bash
docker run -d \
  --name shop-mgmt \
  -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=3306 \
  -e DB_USER=root \
  -e DB_PASSWORD=你的密码 \
  -e DB_NAME=shop_db \
  -e JWT_SECRET=your-long-secret-key \
  shop-management
```

### 步骤 3：查看状态

```bash
docker logs -f shop-mgmt
```

### 步骤 4：访问

http://localhost:8000

---

## 五、云端部署（Render + 免费 MySQL）

### 1. 准备免费数据库

推荐使用 **PlanetScale**（免费 5GB）：

1. 注册 https://planetscale.com
2. 创建数据库 `shop_db`
3. 在 DataGrip 中连接该数据库，执行 `database/init.sql`
4. 记录连接信息：`host` / `port` / `user` / `password` / `database`

### 2. 部署到 Render

1. 访问 https://dashboard.render.com ，用 GitHub 登录
2. 点击 `New +` → `Web Service`
3. 选择仓库 `shop-management-python`
4. Render 自动读取 `deploy/render.yaml`（如未自动识别，手动配置）
5. 在 `Environment` 页填入数据库信息
6. 等待 3-5 分钟，部署完成

### 3. 访问

Render 会分配域名：`https://shop-management-xxxx.onrender.com`

> **免费套餐限制**：15 分钟无请求会休眠，下次访问需等待约 30 秒唤醒。

---

## 六、项目目录结构

```
shop-management/
├── backend/                  # 后端（PyCharm）
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 配置
│   │   ├── database.py       # 数据库连接
│   │   ├── constants.py      # 角色常量 + 内存哈希表
│   │   ├── models/           # ORM 模型
│   │   ├── schemas/          # Pydantic 模型
│   │   ├── routers/          # 路由
│   │   ├── services/         # 业务逻辑
│   │   ├── utils/            # JWT / 权限工具
│   │   └── scheduler/        # 定时任务
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/                 # 前端（VSCode）
│   ├── index.html            # 登录页
│   ├── pages/                # 各角色工作台
│   └── static/               # CSS / JS
├── database/                 # 数据库（DataGrip）
│   ├── init.sql
│   └── README.md
├── deploy/                   # 部署配置
│   ├── Dockerfile
│   └── render.yaml
└── docs/
    └── 运行说明.md
```

---

## 七、常见问题

### 1. 浏览器访问 0.0.0.0 打不开

**原因**：`0.0.0.0` 是服务器监听地址，不是可访问的地址。
**解决**：改用 `http://localhost:8000` 或 `http://127.0.0.1:8000`。

### 2. 启动时报"端口被占用"

**原因**：8000 端口被其他程序使用。
**解决**：修改 `run.py` 中的端口：

```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

### 3. 数据库连接失败

**排查**：
- 确认 MySQL 服务已启动
- 确认 `.env` 中的密码正确
- 确认 `shop_db` 数据库已创建
- 确认已执行 `database/init.sql`

### 4. 登录提示"密码错误"

**原因**：数据库中的密码哈希与后端 passlib 生成的不一致。
**解决**：用 Python 重新生成哈希并更新数据库：

```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd.hash("123456"))
```

把输出的哈希复制到 `database/init.sql` 中重新初始化，或直接 `UPDATE` 数据库中的密码字段。

### 5. 商户登录后看不到账单

**原因**：尚未为该商户生成收款单和账单。
**解决**：
- 用招商账号（INV001）为该租户创建合同和租金
- 用财务账号（FIN001）审核通过合同
- 调用 `POST /api/receipt/generate` 手动生成，或等待每月 1 号定时任务

### 6. 定时任务没有触发

**原因**：`main.py` 未正确启动调度器，或时间未到。
**解决**：
- 确认控制台输出 `[调度器] 已启动`
- 测试时可临时把 cron 改为每分钟：
  ```python
  trigger=CronTrigger(minute="*/1")
  ```
- 测试完成后改回 `day=1, hour=2, minute=0`

---

## 八、技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.141.1 |
| ASGI 服务器 | Uvicorn | 0.52.4 |
| ORM | SQLAlchemy | 2.0.52 |
| 数据库驱动 | PyMySQL | 1.2.0 |
| 数据校验 | Pydantic | 2.13.5 |
| 认证 | python-jose (JWT) | 3.5.0 |
| 密码加密 | passlib (bcrypt) | 1.7.4 |
| 定时任务 | APScheduler | 3.11.3 |
| 数据库 | MySQL | 8.0 |
| 前端 | Vue 3 + HTML + CSS + JS | 3.x |

---

## 九、开发约定

- **RESTful 风格**：GET 查询、POST 新增、PUT 更新、DELETE 删除
- **统一前缀**：所有接口以 `/api` 开头
- **统一认证**：除登录/注册外，请求头需带 `Authorization: Bearer <token>`
- **角色隔离**：后端用 `require_role()` 校验，前端按 `role` 动态渲染菜单
- **单端口部署**：前端静态资源由 FastAPI 的 `StaticFiles` 挂载

---

## 十、联系方式

- 项目仓库：https://github.com/ZIIQQN/shop_Management
- 问题反馈：提交 GitHub Issue

---

**文档版本**：1.0
**最后更新**：2026 年 9 月