"""
End-to-End ETL Pipeline Orchestrator (1-Click Shortcut: Extract -> Transform -> Load)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Fitur:
  - Menjalankan seluruh pipeline secara berurutan (Extract -> Transform -> Load)
  - Automated Retry Mechanism (maksimal 3 kali percobaan dengan jeda 5 detik)
  - Satu Pipeline Run ID terpadu untuk jejak audit penuh di dwh.etl_audit_log
"""

import time
import uuid

from db_utils import get_logger
from extract import run_extract
from transform import run_transform
from load import run_load

logger = get_logger("etl.orchestrator")


def execute_with_retry(stage_label: str, fn, run_id: str, max_retries: int = 3, delay_sec: int = 5):
    for attempt in range(1, max_retries + 1):
        try:
            logger.info("[%s] Attempt %d/%d...", stage_label, attempt, max_retries)
            return fn(run_id=run_id)
        except Exception as exc:
            logger.error("[%s] Attempt %d failed: %s", stage_label, attempt, exc)
            if attempt == max_retries:
                raise
            logger.warning("[%s] Retrying in %d seconds...", stage_label, delay_sec)
            time.sleep(delay_sec)


def run_full_pipeline():
    run_id = f"ETL-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t0 = time.time()
    logger.info("===================================================================")
    logger.info("STARTING FULL END-TO-END ETL PIPELINE | run_id=%s", run_id)
    logger.info("===================================================================")

    execute_with_retry("STAGE 1 - EXTRACT", run_extract, run_id)
    execute_with_retry("STAGE 2 - TRANSFORM", run_transform, run_id)
    execute_with_retry("STAGE 3 - LOAD", run_load, run_id)

    total_sec = round(time.time() - t0, 2)
    logger.info("===================================================================")
    logger.info("FULL END-TO-END ETL PIPELINE SUCCEEDED in %ss | run_id=%s", total_sec, run_id)
    logger.info("===================================================================")


if __name__ == "__main__":
    run_full_pipeline()
