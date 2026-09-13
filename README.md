# 商铺信息管理系统

> 基于 **FastAPI + Vue 3 + MySQL** 的商铺租赁全生命周期管理系统，覆盖招商、财务、营运、收银、商户、老板六种角色，实现从合同签订到退租归档的完整业务闭环。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-green.svg)
![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [默认账号](#-默认账号)
- [业务流程图](#-业务流程图)
- [API 文档](#-api-文档)
- [部署指南](#-部署指南)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🎯 项目简介

本系统面向商场运营管理场景，解决传统商铺租赁中 **合同分散、租金对账繁琐、账单催收效率低** 等问题。系统采用前后端分离架构，后端基于 FastAPI 提供 RESTful API，前端使用 Vue 3（CDN 引入）实现单页交互，数据库使用 MySQL 8.0。

### 核心价值

- **全生命周期管理**：从招商入驻到退租归档，业务数据完整闭环
- **角色权限隔离**：六种角色各司其职，互不干扰
- **自动化能力**：租金自动计算、欠收金额自动生成、月度账单定时生成
- **轻量部署**：单端口同时服务前端和后端，一条命令即可启动

---

## ✨ 功能特性

### 招商模块

- 租户信息管理（增删改查）
- 合同签订（合同号自动生成，格式：铺位号-三位序号）
- 租金设置（支持固定租金和抽成租金两种模式，自动计算金额）

### 财务模块

- 合同审核（通过 / 不通过）
- 审核通过后自动更新商铺出租状态
- 审核备注记录

### 营运模块

- 租金修改（固定单价 / 抽成比例）
- 商铺退租（自动记录历史租户）

### 收银模块

- 收款单管理
- 发送催收通知
- 修改实收金额（同步更新账单）

### 商户模块

- 自助注册与登录
- 查看个人账单（应收 / 实收 / 欠收 / 结清状态）
- 在线缴费（支持全额 / 部分缴费，多种支付渠道）

### 老板模块

- 商铺总览（只读）
- 注册新员工

### 系统能力

- JWT 无状态认证
- 密码 BCrypt 加密存储
- 定时任务每月自动生成账单
- 数据库生成列自动计算欠收金额

---

## 🛠 技术栈

| 层级 | 技术选型 | 版本 |
|------|----------|------|
| 后端框架 | FastAPI | 0.141.1 |
| ASGI 服务器 | Uvicorn | 0.52.4 |
| ORM | SQLAlchemy | 2.0.52 |
| 数据库驱动 | PyMySQL | 1.2.0 |
| 数据校验 | Pydantic | 2.13.5 |
| 认证 | python-jose (JWT) | 3.5.0 |
| 密码加密 | passlib[bcrypt] | 1.7.4 |
| 定时任务 | APScheduler | 3.11.3 |
| 前端框架 | Vue 3 (CDN) | 3.x |
| HTTP 客户端 | Axios (CDN) | 1.x |
| 数据库 | MySQL | 8.0 |

---

## 📁 项目结构

```text
shop-management/
├── README.md                      # 项目说明文档
├── LICENSE                        # 开源许可证
├── .gitignore                     # Git 忽略配置
│
├── backend/                       # 后端（PyCharm 开发）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI 入口（含静态资源挂载）
│   │   ├── config.py              # 配置管理
│   │   ├── database.py            # 数据库连接
│   │   ├── constants.py           # 角色常量 + 内存会话表
│   │   │
│   │   ├── models/                # SQLAlchemy ORM 模型
│   │   │   ├── shop.py
│   │   │   ├── tenant.py
│   │   │   ├── contract.py
│   │   │   ├── rent.py
│   │   │   ├── receipt.py
│   │   │   ├── bill.py
│   │   │   ├── employee.py
│   │   │   ├── merchant.py
│   │   │   └── history.py
│   │   │
│   │   ├── schemas/               # Pydantic 请求/响应模型
│   │   │   ├── auth.py
│   │   │   ├── tenant.py
│   │   │   ├── contract.py
│   │   │   ├── rent.py
│   │   │   └── employee.py
│   │   │
│   │   ├── routers/               # API 路由
│   │   │   ├── auth.py            # 登录/注册
│   │   │   ├── shop.py
│   │   │   ├── tenant.py
│   │   │   ├── contract.py
│   │   │   ├── rent.py
│   │   │   ├── receipt.py
│   │   │   ├── bill.py
│   │   │   └── employee.py
│   │   │
│   │   ├── services/              # 业务逻辑
│   │   │   ├── contract_service.py
│   │   │   ├── rent_service.py
│   │   │   └── receipt_service.py
│   │   │
│   │   ├── utils/                 # 工具类
│   │   │   ├── security.py        # 密码哈希 + JWT
│   │   │   └── deps.py            # 依赖注入
│   │   │
│   │   └── scheduler/             # 定时任务
│   │       └── monthly_receipt.py
│   │
│   ├── requirements.txt           # 依赖清单
│   ├── .env.example               # 环境变量模板
│   └── run.py                     # 启动脚本
│
├── frontend/                      # 前端（VSCode 开发）
│   ├── index.html                 # 登录页
│   ├── pages/
│   │   ├── register.html          # 商户注册
│   │   ├── employee.html          # 员工工作台
│   │   ├── merchant.html          # 商户工作台
│   │   └── boss.html              # 老板工作台
│   └── static/
│       ├── css/
│       │   ├── common.css         # 全局样式
│       │   ├── login.css          # 登录页样式
│       │   ├── dashboard.css      # 工作台布局
│       │   └── table.css          # 表格样式
│       └── js/
│           ├── api.js             # Axios 封装
│           ├── login.js
│           ├── register.js
│           ├── employee.js
│           ├── merchant.js
│           └── boss.js
│
├── database/                      # 数据库（DataGrip 开发）
│   ├── init.sql                   # 建表 + 初始数据
│   └── README.md
│
├── deploy/                        # 部署配置
│   ├── Dockerfile
│   └── render.yaml
│
└── docs/
    └── 运行说明.md
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+
- 现代浏览器（Chrome / Edge / Firefox）

### 步骤 1：克隆项目

```bash
git clone https://github.com/你的用户名/shop-management-python.git
cd shop-management-python
```

### 步骤 2：初始化数据库

```bash
mysql -u root -p < database/init.sql
```

或在 DataGrip / Navicat 中手动执行 `database/init.sql`。

### 步骤 3：配置后端

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板并修改
cp .env.example .env
# 编辑 .env，把 DB_PASSWORD 改成你的 MySQL 密码
```

### 步骤 4：启动服务

```bash
python run.py
```

启动成功后，控制台会输出：

```text
[调度器] 已启动，下次执行时间：2026-10-01 02:00:00+08:00
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 步骤 5：访问系统

打开浏览器访问：**http://localhost:8000**

> 💡 **提示**：不要访问 `http://0.0.0.0:8000`，`0.0.0.0` 是服务器监听地址，浏览器访问需用 `localhost`。

---

## 👤 默认账号

| 角色 | 用户名 | 密码 | 登录入口 |
|------|--------|------|----------|
| 招商 | `INV001` | `123456` | 员工登录 |
| 财务 | `FIN001` | `123456` | 员工登录 |
| 营运 | `OPE001` | `123456` | 员工登录 |
| 收银 | `CAS001` | `123456` | 员工登录 |
| 商户 | `zhangsan` | `123456` | 商户登录 |
| 老板 | `boss` | `123456` | 老板登录 |

> ⚠️ **首次部署后请立即修改默认密码**，尤其是老板账号。

---

## 🔄 业务流程图

```text
┌─────────────────────────────────────────────────────────────┐
│                    商铺租赁全生命周期                          │
└─────────────────────────────────────────────────────────────┘

  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
  │ 招商 │───▶│ 财务 │───▶│ 系统 │───▶│ 商户 │───▶│ 营运 │
  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘
     │            │            │            │            │
     ▼            ▼            ▼            ▼            ▼
  录入租户     审核合同    自动生成     查看账单      办理退租
  签订合同    通过/不通过  收款单账单   在线缴费      记录历史
  设置租金                 (定时/手动)  (全额/部分)
```

---

## 📡 API 文档

项目启动后，访问 **http://localhost:8000/docs** 可查看 Swagger 交互式文档。

### 主要接口

| 模块 | 方法 | 路径 | 角色 |
|------|------|------|------|
| 认证 | POST | `/api/auth/employee/login` | 公开 |
| 认证 | POST | `/api/auth/merchant/login` | 公开 |
| 认证 | POST | `/api/auth/boss/login` | 公开 |
| 认证 | POST | `/api/auth/merchant/register` | 公开 |
| 商铺 | GET | `/api/shop/list` | 所有登录用户 |
| 租户 | GET | `/api/tenant/list` | 招商 |
| 合同 | GET | `/api/contract/list` | 招商、财务 |
| 合同 | PUT | `/api/contract/audit/{id}` | 财务 |
| 租金 | PUT | `/api/rent/update` | 营运 |
| 收款单 | GET | `/api/receipt/list` | 收银 |
| 收款单 | POST | `/api/receipt/generate` | 招商、收银 |
| 账单 | GET | `/api/bill/list` | 商户 |
| 账单 | POST | `/api/bill/pay/{id}` | 商户 |
| 员工 | POST | `/api/employee/register` | 老板 |

### 认证方式

除登录/注册外，所有请求需在 Header 中携带：

```text
Authorization: Bearer <your-jwt-token>
```

---

## 🌐 部署指南

### 方案一：Railway（推荐，免费额度 $5/月）

1. 访问 https://railway.app ，用 GitHub 登录
2. **New Project** → **Deploy from GitHub repo** → 选择本仓库
3. 点击 **Add Plugin** → **MySQL**
4. 在 **Variables** 中配置：

    ```env
    DB_HOST=${{MySQL.MYSQLHOST}}
    DB_PORT=${{MySQL.MYSQLPORT}}
    DB_USER=${{MySQL.MYSQLUSER}}
    DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
    DB_NAME=${{MySQL.MYSQLDATABASE}}
    JWT_SECRET=<生成一个长随机字符串>
    ```

5. 在 **Settings → Deploy** 中设置启动命令：

    ```bash
    cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```

6. Railway 自动分配公网域名，访问即可

### 方案二：Render + PlanetScale

1. **数据库**：https://planetscale.com 创建免费 MySQL（5GB）
2. **后端**：https://render.com 创建 Web Service，连接 GitHub
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. 配置环境变量（数据库连接、JWT_SECRET）
4. 部署后获得公网域名

### 方案三：本地 Docker

```bash
docker build -t shop-management -f deploy/Dockerfile .
docker run -d -p 8000:8000 --env-file backend/.env shop-management
```

---

## ❓ 常见问题

### 1. 浏览器访问 `0.0.0.0:8000` 打不开？

`0.0.0.0` 是服务器监听地址，浏览器请用 `localhost:8000` 或 `127.0.0.1:8000`。

### 2. 数据库连接失败？

- 检查 MySQL 服务是否启动
- 检查 `.env` 中的 `DB_PASSWORD` 是否正确
- 确认已执行 `database/init.sql` 创建数据库和表

### 3. 登录后页面空白？

- 清除浏览器 `localStorage` 后重新登录
- 检查浏览器控制台是否有红色错误
- 确认后端 `/api/auth/*/login` 接口返回了 token

### 4. 商户看不到账单？

- 需要为商户对应的合同生成收款单和账单
- 可以用招商账号手动调用 `POST /api/receipt/generate`
- 或等待定时任务每月 1 号自动生成

### 5. 定时任务没有按时执行？

- 确认 `app/scheduler/monthly_receipt.py` 中的 cron 表达式正确
- 检查服务器时区是否为 `Asia/Shanghai`
- 查看启动日志是否有 `[调度器] 已启动`

### 6. 密码验证失败？

- 数据库中的密码必须是 bcrypt 哈希
- 用 passlib 重新生成：`python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('123456'))"`
- 把输出更新到数据库

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交改动：`git commit -m "Add some feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 代码规范

- Python 遵循 PEP 8
- 前端保持统一的 CSS 变量命名
- 提交信息使用中文或英文均可，格式：`<类型>: <描述>`

---

## 📄 许可证

本项目采用 **MIT License**，详见 [LICENSE](./LICENSE) 文件。

---

## 📧 联系方式

- 作者：你的名字
- 邮箱：your.email@example.com
- GitHub：[@你的用户名](https://github.com/你的用户名)

---

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [APScheduler](https://apscheduler.readthedocs.io/)

---

**⭐ 如果这个项目对你有帮助，欢迎给个 Star！**