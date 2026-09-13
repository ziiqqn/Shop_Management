from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import SessionLocal
from app.services.receipt_service import generate_all_monthly_receipts

# 全局调度器实例
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")


def monthly_receipt_job():
    """每月1号凌晨2点执行：为所有有效合同生成收款单与账单"""
    print("=" * 50)
    print("[定时任务] 开始生成月度收款单与账单...")

    db = SessionLocal()
    try:
        result = generate_all_monthly_receipts(db)
        print(f"[定时任务] 完成：共 {result['total_contracts']} 份合同，"
              f"成功 {result['success']}，跳过 {result['skipped']}，失败 {result['failed']}")
        for d in result["details"]:
            print(f"  - {d['message']}")
    except Exception as e:
        print(f"[定时任务] 执行出错：{e}")
    finally:
        db.close()

    print("=" * 50)


def start_scheduler():
    """在应用启动时调用，注册并启动定时任务"""
    if scheduler.running:
        print("[调度器] 已在运行，跳过启动")
        return

    # 每月1号凌晨2点执行
    scheduler.add_job(
        monthly_receipt_job,
        trigger=CronTrigger(day=1, hour=2, minute=0),
        id="monthly_receipt",
        name="月度账单生成",
        replace_existing=True
    )

    scheduler.start()
    print("[调度器] 已启动，下次执行时间：", scheduler.get_job("monthly_receipt").next_run_time)


def shutdown_scheduler():
    """应用关闭时优雅停止调度器"""
    if scheduler.running:
        scheduler.shutdown()
        print("[调度器] 已停止")