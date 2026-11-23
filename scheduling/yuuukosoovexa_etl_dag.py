"""
Tahap 6C - Apache Airflow DAG Definitions (Production & Docker Orchestrator)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Selaras dengan Subbab 2.8 dan Tabel 2.12 Laporan UAS:
  1. yuuukosoovexa_daily_etl_pipeline      -> Daily 02:00 WITA (cron: 0 2 * * *)
     Extract -> Transform -> Load Galaxy Schema -> Refresh Data Marts -> Health Check
  2. yuuukosoovexa_weekly_maintenance_dag  -> Weekly Senin 05:00 WITA (cron: 0 5 * * 1)
     Audit Log & Staging Maintenance Verification
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

# Pastikan folder etl/ bisa diimpor baik di dalam kontainer Docker maupun lokal
PROJECT_ETL_DIR = Path("/opt/airflow/project/etl")
if not PROJECT_ETL_DIR.exists():
    PROJECT_ETL_DIR = Path(__file__).resolve().parent.parent / "etl"
if str(PROJECT_ETL_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_ETL_DIR))


def task_extract(**context):
    from extract import run_extract
    run_id = f"AF-{context['ts_nodash']}"
    return run_extract(run_id=run_id)


def task_transform(**context):
    from transform import run_transform
    run_id = f"AF-{context['ts_nodash']}"
    return run_transform(run_id=run_id)


def task_load(**context):
    from load import run_load
    run_id = f"AF-{context['ts_nodash']}"
    return run_load(run_id=run_id)


def task_build_datamarts(**context):
    from importlib import import_module
    dm = import_module("04_build_datamarts")
    dm.build_datamarts()


def task_verify_dwh_health(**context):
    from db_utils import get_pg_connection, get_logger
    log = get_logger("airflow.health_check")
    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            checks = [
                ("dwh.dim_product", 1),
                ("dwh.fact_sales", 1),
                ("dwh.fact_environmental_aqi", 1),
                ("dwh.fact_fitness_demand", 1),
                ("dwh.fact_lifestyle_sleep_health", 1),
                ("datamart.vw_executive_sales", 1),
            ]
            for tbl, min_rows in checks:
                cur.execute(f"SELECT COUNT(*) FROM {tbl};")
                cnt = cur.fetchone()[0]
                if cnt < min_rows:
                    raise ValueError(f"Health check failed: {tbl} has {cnt} rows (< {min_rows})")
                log.info("Health check OK | %s = %s rows", tbl, f"{cnt:,}")
    finally:
        conn.close()


def task_weekly_staging_audit(**context):
    from db_utils import get_pg_connection, get_logger, record_audit
    log = get_logger("airflow.maintenance")
    run_id = f"MAINT-{context['ts_nodash']}"
    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM dwh.etl_audit_log;")
            audit_rows = cur.fetchone()[0]
            log.info("Weekly maintenance audit verified: %s total audit entries.", audit_rows)
        record_audit(conn, run_id, "MAINTENANCE", "dwh.etl_audit_log", audit_rows, audit_rows, 0, "SUCCESS", 0.1, "Weekly audit check OK")
        conn.commit()
    finally:
        conn.close()


DEFAULT_ARGS = {
    "owner": "yuuukosoo_data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# DAG 1: Pipeline ETL Harian Utama (02:00 WITA)
with DAG(
    dag_id="yuuukosoovexa_daily_etl_pipeline",
    description="Daily End-to-End ETL Pipeline (Staging -> Transform -> Galaxy Schema DWH -> Data Marts)",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 11, 1),
    schedule="0 2 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["yuuukosoovexa", "dwh", "etl", "galaxy-schema", "uas-bi"],
) as daily_etl_dag:

    t_extract = PythonOperator(
        task_id="extract_to_staging",
        python_callable=task_extract,
    )

    t_transform = PythonOperator(
        task_id="transform_and_preprocess",
        python_callable=task_transform,
    )

    t_load = PythonOperator(
        task_id="load_galaxy_schema_dwh",
        python_callable=task_load,
    )

    t_datamarts = PythonOperator(
        task_id="refresh_datamart_views",
        python_callable=task_build_datamarts,
    )

    t_verify = PythonOperator(
        task_id="verify_dwh_health",
        python_callable=task_verify_dwh_health,
    )

    t_extract >> t_transform >> t_load >> t_datamarts >> t_verify

# DAG 2: Pemeliharaan & Audit Mingguan (Senin 05:00 WITA)
with DAG(
    dag_id="yuuukosoovexa_weekly_maintenance_dag",
    description="Weekly Staging Audit & Log Verification (Every Monday 05:00 WITA)",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 11, 1),
    schedule="0 5 * * 1",
    catchup=False,
    max_active_runs=1,
    tags=["yuuukosoovexa", "governance", "maintenance"],
) as weekly_maint_dag:

    t_maint = PythonOperator(
        task_id="weekly_staging_and_audit_check",
        python_callable=task_weekly_staging_audit,
    )
