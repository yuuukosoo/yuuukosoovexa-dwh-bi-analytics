"""
Tahap 6C - Lightweight Local Python Scheduler (Fallback Non-Docker)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Menjalankan jadwal harian yang selaras dengan Tabel 2.12:
  - 01:00 WITA -> Automated Backup (pg_dump + SHA-256)
  - 02:00 WITA -> Full ETL Pipeline (Extract -> Transform -> Load -> Data Mart)
"""

import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "etl"))
sys.path.insert(0, str(BASE_DIR / "backup"))

from db_utils import get_logger  # noqa: E402
from pg_backup import run_backup  # noqa: E402
from run_etl_pipeline import run_full_pipeline  # noqa: E402

logger = get_logger("scheduling.local")


def job_daily_backup():
    logger.info("[SCHEDULER] Triggering 01:00 WITA Daily Backup...")
    run_backup()


def job_daily_etl():
    logger.info("[SCHEDULER] Triggering 02:00 WITA Daily Full ETL Pipeline...")
    run_full_pipeline()


def start_scheduler():
    try:
        import schedule
    except ImportError:
        print("Library 'schedule' belum terinstal. Jalankan: pip install schedule")
        return

    schedule.every().day.at("01:00").do(job_daily_backup)
    schedule.every().day.at("02:00").do(job_daily_etl)

    logger.info("Local Python Scheduler AKTIF (01:00 WITA Backup | 02:00 WITA ETL). Tekan Ctrl+C untuk berhenti.")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    start_scheduler()
