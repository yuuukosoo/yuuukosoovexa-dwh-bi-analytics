"""
Tahap 6A - Eksekusi Pembuatan Data Mart Views di PostgreSQL
PT YuuukosooVexa Business Intelligence & Data Warehouse Project
"""

import time
import uuid
from pathlib import Path

from db_utils import BASE_DIR, get_logger, get_pg_connection, record_audit

logger = get_logger("etl.datamart")
SQL_PATH = BASE_DIR / "sql" / "04_create_datamart_views.sql"

DATAMART_VIEWS = [
    ("datamart.vw_executive_sales", "Halaman 1 - Executive Summary & Multi-Channel Sales"),
    ("datamart.vw_sales_pricing_sku", "Halaman 2 - Sales & Pricing Optimization (+ SKU Deep-Dive)"),
    ("datamart.vw_environmental_aqi_sales", "Halaman 3 - Environmental & Air Quality Correlation"),
    ("datamart.vw_fitness_demand_segmentation", "Halaman 4A - Gym & Fitness Demand Segmentation"),
    ("datamart.vw_sleep_stress_lifestyle", "Halaman 4B - Clinical Sleep & Stress Lifestyle"),
]


def build_datamarts():
    run_id = f"DM-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t0 = time.time()
    logger.info("=== START TAHAP 6A - BUILD DATA MART VIEWS | run_id=%s ===", run_id)

    conn = get_pg_connection()
    conn.autocommit = False

    try:
        sql_text = SQL_PATH.read_text(encoding="utf-8")
        with conn.cursor() as cur:
            cur.execute(sql_text)
        conn.commit()

        print("\n" + "=" * 84)
        print("VERIFIKASI HASIL TAHAP 6A (DATA MART VIEWS DI POSTGRESQL - SIAP POWER BI)")
        print("=" * 84)

        total_views = 0
        with conn.cursor() as cur:
            for view_name, desc in DATAMART_VIEWS:
                cur.execute(f"SELECT COUNT(*) FROM {view_name};")
                cnt = cur.fetchone()[0]
                total_views += 1
                print(f"  {view_name:42s} -> {cnt:>8,} rows | {desc}")
                record_audit(conn, run_id, "DATAMART", view_name, cnt, cnt, 0, "SUCCESS", 0.0, desc)

            # Quick business KPI preview from Data Marts
            cur.execute("""
                SELECT
                    COUNT(*) AS tx_cnt,
                    SUM(units_sold) AS total_units,
                    ROUND(SUM(net_revenue_inr), 2) AS total_net_rev,
                    ROUND(AVG(discount_pct), 2) AS avg_disc_pct
                FROM datamart.vw_executive_sales;
            """)
            tx_cnt, total_units, total_net_rev, avg_disc = cur.fetchone()
            print("-" * 84)
            print(f"  KPI Preview (vw_executive_sales): Tx={tx_cnt:,} | Units={total_units:,} | NetRev=INR {total_net_rev:,.2f} | AvgDisc={avg_disc}%")

        dur = round(time.time() - t0, 2)
        conn.commit()
        logger.info("=== TAHAP 6A COMPLETED | views=%d | duration=%ss ===", total_views, dur)
        print(f"  Total {total_views} Data Mart Views aktif dalam {dur}s (RBAC Read-Only diterapkan)")
        print("=" * 84)

    except Exception as exc:
        conn.rollback()
        logger.exception("TAHAP 6A FAILED: %s", exc)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    build_datamarts()
