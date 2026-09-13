CREATE DATABASE IF NOT EXISTS shop_db;

-- ============================================
-- 商铺信息管理系统 - 数据库初始化脚本
-- 数据库：shop_db（已创建）
-- 数据库版本：MySQL 8.0+
-- ============================================

USE shop_db;

-- ============================================
-- 1. 老板配置表
-- ============================================
DROP TABLE IF EXISTS boss_config;
CREATE TABLE boss_config (
                             id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                             username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                             password VARCHAR(100) NOT NULL COMMENT '密码（BCrypt加密）',
                             name VARCHAR(50) COMMENT '姓名',
                             phone VARCHAR(20) COMMENT '联系电话',
                             create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
                         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='老板配置表';

-- ============================================
-- 2. 商场布局配置表
-- ============================================
DROP TABLE IF EXISTS mall_layout;
CREATE TABLE mall_layout (
                             id BIGINT AUTO_INCREMENT PRIMARY KEY,
                             floor_count INT NOT NULL DEFAULT 3 COMMENT '层数',
                             shops_per_floor INT NOT NULL DEFAULT 5 COMMENT '每层商铺数',
                             floor_names JSON COMMENT '楼层名称映射，如{"1":"负一层","2":"一层","3":"二层"}',
                             update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商场布局配置表';

-- ============================================
-- 3. 商铺表
-- ============================================
DROP TABLE IF EXISTS shop;
CREATE TABLE shop (
                      id BIGINT AUTO_INCREMENT PRIMARY KEY,
                      shop_number VARCHAR(20) NOT NULL UNIQUE COMMENT '铺位号，如 AA-B1-0001',
                      floor VARCHAR(20) NOT NULL COMMENT '楼层名称',
                      floor_index INT NOT NULL COMMENT '楼层序号（1,2,3...）',
                      building_area DECIMAL(10,2) NOT NULL DEFAULT 50.00 COMMENT '建筑面积',
                      use_area DECIMAL(10,2) NOT NULL DEFAULT 40.00 COMMENT '使用面积',
                      is_rented TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0-未出租，1-已出租',
                      current_tenant_id BIGINT DEFAULT NULL COMMENT '当前租户ID',
                      create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                      update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      INDEX idx_shop_number (shop_number),
                      INDEX idx_floor (floor_index),
                      INDEX idx_is_rented (is_rented)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商铺表';

-- ============================================
-- 4. 租户表
-- ============================================
DROP TABLE IF EXISTS tenant;
CREATE TABLE tenant (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL COMMENT '租户名称',
                        id_card VARCHAR(18) COMMENT '身份证号',
                        brand_type VARCHAR(10) COMMENT '品牌类型：连锁/个体',
                        brand_name VARCHAR(50) COMMENT '品牌名',
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_id_card (id_card),
                        INDEX idx_brand_type (brand_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='租户信息表';

-- ============================================
-- 5. 合同表
-- ============================================
DROP TABLE IF EXISTS contract;
CREATE TABLE contract (
                          id BIGINT AUTO_INCREMENT PRIMARY KEY,
                          contract_no VARCHAR(50) NOT NULL UNIQUE COMMENT '合同号，格式：铺位号-三位序号',
                          shop_id BIGINT NOT NULL COMMENT '商铺ID',
                          tenant_id BIGINT NOT NULL COMMENT '租户ID',
                          pic_url VARCHAR(200) COMMENT '合同电子图片路径',
                          start_date DATE NOT NULL COMMENT '合同开始日期',
                          end_date DATE NOT NULL COMMENT '合同结束日期',
                          audit_status TINYINT(1) DEFAULT 0 COMMENT '0-待审核，1-通过，2-不通过',
                          audit_remark VARCHAR(255) COMMENT '审核备注',
                          create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                          FOREIGN KEY (shop_id) REFERENCES shop(id) ON DELETE RESTRICT,
                          FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE RESTRICT,
                          INDEX idx_shop_id (shop_id),
                          INDEX idx_tenant_id (tenant_id),
                          INDEX idx_dates (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合同表';

-- ============================================
-- 6. 租金表
-- ============================================
DROP TABLE IF EXISTS rent;
CREATE TABLE rent (
                      id BIGINT AUTO_INCREMENT PRIMARY KEY,
                      tenant_id BIGINT NOT NULL COMMENT '租户ID',
                      shop_id BIGINT NOT NULL COMMENT '商铺ID',
                      contract_id BIGINT COMMENT '关联合同ID',
                      rent_type VARCHAR(10) NOT NULL COMMENT 'fixed-固定，percent-抽成',
                      area_type VARCHAR(10) NOT NULL COMMENT 'building-建筑面积，use-使用面积',
                      rent_level VARCHAR(20) NOT NULL COMMENT 'chain_high-连锁高，individual_low-个体低',
                      billing_cycle VARCHAR(10) NOT NULL COMMENT 'month-月，quarter-季',
                      actual_start_date DATE NOT NULL COMMENT '实际使用开始时间',
                      cycle_start_date DATE NOT NULL COMMENT '合同周期开始时间',
                      unit_price DECIMAL(10,2) COMMENT '单价（元/平米）',
                      rent_amount_fixed DECIMAL(10,2) COMMENT '固定租金金额',
                      percent_rate DECIMAL(5,2) COMMENT '抽成比（%）',
                      turnover DECIMAL(12,2) COMMENT '营业额',
                      profit DECIMAL(12,2) COMMENT '利润',
                      rent_amount_percent DECIMAL(12,2) COMMENT '抽成租金金额',
                      create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                      update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      FOREIGN KEY (tenant_id) REFERENCES tenant(id),
                      FOREIGN KEY (shop_id) REFERENCES shop(id),
                      FOREIGN KEY (contract_id) REFERENCES contract(id) ON DELETE SET NULL,
                      INDEX idx_tenant_shop (tenant_id, shop_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='租金表';

-- ============================================
-- 7. 收款单表
-- ============================================
DROP TABLE IF EXISTS receipt;
CREATE TABLE receipt (
                         id BIGINT AUTO_INCREMENT PRIMARY KEY,
                         tenant_id BIGINT NOT NULL COMMENT '租户ID',
                         contract_id BIGINT NOT NULL COMMENT '合同ID',
                         receipt_time DATE NOT NULL COMMENT '收款时间（当期）',
                         receivable_amount DECIMAL(12,2) NOT NULL COMMENT '应收金额',
                         paid_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00 COMMENT '实收金额',
                         unpaid_amount DECIMAL(12,2) GENERATED ALWAYS AS (receivable_amount - paid_amount) STORED COMMENT '欠收金额（自动计算）',
                         reminder_sent TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0-未催收，1-已催收',
                         create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                         FOREIGN KEY (tenant_id) REFERENCES tenant(id),
                         FOREIGN KEY (contract_id) REFERENCES contract(id),
                         INDEX idx_receipt_time (receipt_time),
                         INDEX idx_tenant_unpaid (tenant_id, unpaid_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收款单表';

-- ============================================
-- 8. 账单表
-- ============================================
DROP TABLE IF EXISTS bill;
CREATE TABLE bill (
                      id BIGINT AUTO_INCREMENT PRIMARY KEY,
                      tenant_id BIGINT NOT NULL COMMENT '租户ID',
                      receipt_id BIGINT NOT NULL COMMENT '收款单ID',
                      receivable_amount DECIMAL(12,2) NOT NULL COMMENT '应收金额',
                      paid_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00 COMMENT '实收金额',
                      unpaid_amount DECIMAL(12,2) GENERATED ALWAYS AS (receivable_amount - paid_amount) STORED COMMENT '欠收金额（自动计算）',
                      payment_channel VARCHAR(20) COMMENT 'wechat/alipay/bank/offline',
                      bill_month DATE NOT NULL COMMENT '账单月份',
                      is_paid TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0-未结清，1-已结清',
                      create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (tenant_id) REFERENCES tenant(id),
                      FOREIGN KEY (receipt_id) REFERENCES receipt(id),
                      INDEX idx_bill_month (bill_month),
                      INDEX idx_tenant_paid (tenant_id, is_paid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='账单表';

-- ============================================
-- 9. 商铺历史租户表
-- ============================================
DROP TABLE IF EXISTS shop_history_tenant;
CREATE TABLE shop_history_tenant (
                                     id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                     shop_id BIGINT NOT NULL COMMENT '商铺ID',
                                     tenant_id BIGINT NOT NULL COMMENT '租户ID',
                                     contract_id BIGINT NOT NULL COMMENT '合同ID',
                                     start_date DATE COMMENT '租期开始日期',
                                     end_date DATE COMMENT '租期结束日期',
                                     create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                                     FOREIGN KEY (shop_id) REFERENCES shop(id) ON DELETE CASCADE,
                                     FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE,
                                     FOREIGN KEY (contract_id) REFERENCES contract(id) ON DELETE CASCADE,
                                     INDEX idx_shop_id (shop_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商铺历史租户表';

-- ============================================
-- 10. 员工表
-- ============================================
DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
                          id BIGINT AUTO_INCREMENT PRIMARY KEY,
                          name VARCHAR(50) NOT NULL COMMENT '姓名',
                          job_number VARCHAR(20) NOT NULL UNIQUE COMMENT '工号',
                          department VARCHAR(20) NOT NULL COMMENT '部门：INVESTMENT/FINANCE/OPERATION/CASHIER',
                          `rank` VARCHAR(10) NOT NULL COMMENT '职级：员工/经理',
                          password VARCHAR(100) NOT NULL COMMENT '密码（BCrypt加密）',
                          create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                          INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

-- ============================================
-- 11. 商户账号表
-- ============================================
DROP TABLE IF EXISTS merchant_account;
CREATE TABLE merchant_account (
                                  id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                  tenant_id BIGINT NOT NULL UNIQUE COMMENT '关联租户ID',
                                  username VARCHAR(50) NOT NULL UNIQUE COMMENT '登录用户名',
                                  password VARCHAR(100) NOT NULL COMMENT '密码（BCrypt加密）',
                                  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                                  FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE,
                                  INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商户账号表';


-- ============================================
-- 初始数据
-- ============================================

-- 1. 老板账号（密码 123456 的 BCrypt 哈希）
INSERT INTO boss_config (username, password, name, phone) VALUES
    ('boss', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju', '张老板', '13800000000');

# 修改老板密码
UPDATE boss_config SET password = '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju' WHERE username = 'boss';

-- 2. 商场布局配置（3层，每层5户）
INSERT INTO mall_layout (floor_count, shops_per_floor, floor_names) VALUES
    (3, 5, '{"1":"负一层","2":"一层","3":"二层"}');

-- 3. 商铺数据（15条）
INSERT INTO shop (shop_number, floor, floor_index, building_area, use_area, is_rented) VALUES
                                                                                           ('AA-B1-0001', '负一层', 1, 50.00, 40.00, 0),
                                                                                           ('AA-B1-0002', '负一层', 1, 55.00, 44.00, 0),
                                                                                           ('AA-B1-0003', '负一层', 1, 48.00, 38.00, 0),
                                                                                           ('AA-B1-0004', '负一层', 1, 60.00, 50.00, 0),
                                                                                           ('AA-B1-0005', '负一层', 1, 52.00, 42.00, 0),
                                                                                           ('AA-F1-0001', '一层', 2, 70.00, 60.00, 0),
                                                                                           ('AA-F1-0002', '一层', 2, 75.00, 65.00, 0),
                                                                                           ('AA-F1-0003', '一层', 2, 68.00, 58.00, 0),
                                                                                           ('AA-F1-0004', '一层', 2, 80.00, 70.00, 0),
                                                                                           ('AA-F1-0005', '一层', 2, 72.00, 62.00, 0),
                                                                                           ('AA-F2-0001', '二层', 3, 65.00, 55.00, 0),
                                                                                           ('AA-F2-0002', '二层', 3, 70.00, 60.00, 0),
                                                                                           ('AA-F2-0003', '二层', 3, 62.00, 52.00, 0),
                                                                                           ('AA-F2-0004', '二层', 3, 78.00, 68.00, 0),
                                                                                           ('AA-F2-0005', '二层', 3, 68.00, 58.00, 0);

-- 4. 员工账号（密码均为 123456 的 BCrypt 哈希）
INSERT INTO employee (name, job_number, department, `rank`, password) VALUES
                                                                          ('招商专员', 'INV001', 'INVESTMENT', '员工', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju'),
                                                                          ('财务经理', 'FIN001', 'FINANCE',    '经理', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju'),
                                                                          ('营运专员', 'OPE001', 'OPERATION',  '员工', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju'),
                                                                          ('收银员',   'CAS001', 'CASHIER',    '员工', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju');


-- 查看所有表
SHOW TABLES;

-- 验证商铺数量（应为 15）
SELECT COUNT(*) FROM shop;

-- 验证员工数量（应为 4）
SELECT COUNT(*) FROM employee;

-- 验证布局配置（应为 1）
SELECT * FROM mall_layout;

-- 验证老板账号（应为 1）
SELECT * FROM boss_config;

-- ============================================
-- 5. 预置测试商户
-- ============================================

-- 插入租户（张三）
INSERT INTO tenant (name, id_card, brand_type, brand_name) VALUES
    ('张三', '123456199001011234', '个体', '张记面馆');

-- 插入商户账号，tenant_id 使用上面刚插入的 ID
-- 假设上面 tenant 的 id 为 1
INSERT INTO merchant_account (tenant_id, username, password) VALUES
    (1, 'zhangsan', '$2b$12$qDUazkK8D9XKkUBxltiDE.M3DC77ddd2gbymc.CZJJBG1PqOVZ/Ju');





