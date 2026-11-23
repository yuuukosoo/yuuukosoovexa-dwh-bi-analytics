"""
Tahap 7 - Automated Data Validation & Reconciliation Runner
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Menjalankan 5 rangkaian pengujian otomatis:
  1. Row Count Reconciliation (Raw CSV -> Staging -> Core DWH -> Data Mart)
  2. Aggregate Financial & KPI Accuracy (Core DWH vs Data Mart; tolerance = 0.00)
  3. Referential Integrity (Zero Orphan Foreign Keys across 4 Fact Tables)
  4. Data Quality & Business Rules (Zero negative/inverted prices, zero nulls, labeled simulation)
  5. RBAC Least Privilege Security Verification

Menyimpan laporan bukti terstruktur ke logs/validation_report.json & dwh.etl_audit_log.
"""

import json
import time
import uuid

from db_utils import LOG_DIR, get_logger, get_pg_connection, record_audit

logger = get_logger("etl.validate")


def run_validation():
    run_id = f"VAL-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t0 = time.time()
    logger.info("=== START TAHAP 7 - AUTOMATED DATA VALIDATION | run_id=%s ===", run_id)

    # Load Tahap 3 raw profile for Source CSV baseline comparison
    raw_profile_path = LOG_DIR / "raw_data_profile.json"
    raw_counts = {}
    if raw_profile_path.exists():
        prof = json.loads(raw_profile_path.read_text(encoding="utf-8"))
        for ds in prof.get("datasets", []):
            raw_counts[ds["filename"]] = ds["rows"]

    conn = get_pg_connection()
    checks = []

    def add_check(suite: str, name: str, expected, actual, passed: bool, note: str = ""):
        checks.append({
            "suite": suite,
            "check_name": name,
            "expected": str(expected),
            "actual": str(actual),
            "status": "PASS" if passed else "FAIL",
            "note": note,
        })

    try:
        with conn.cursor() as cur:
            # --------------------------------------------------------------
            # SUITE 1: ROW COUNT RECONCILIATION (SOURCE -> STAGING -> DWH -> DATAMART)
            # --------------------------------------------------------------
            cur.execute("SELECT COUNT(*) FROM staging.stg_flipkart_raw;")
            stg_fk = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "Flipkart CSV -> Staging", raw_counts.get("Health_Suppliments_Flipkart_02_04_2022.csv", 3076), stg_fk, stg_fk == 3076)

            cur.execute("SELECT COUNT(*) FROM staging.stg_tata1mg_raw;")
            stg_1mg = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "Tata 1mg CSV -> Staging", raw_counts.get("1mgData.csv", 16944), stg_1mg, stg_1mg == 16944)

            cur.execute("SELECT COUNT(*) FROM staging.stg_aqi_hourly_raw;")
            stg_aqi = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "India AQI CSV -> Staging", raw_counts.get("INDIA_AQI_COMPLETE_20251126.csv", 842160), stg_aqi, stg_aqi == 842160)

            cur.execute("SELECT COUNT(*) FROM staging.stg_gym_profile_raw;")
            stg_gym = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "GYM CSV (-1 shifted header) -> Staging", 80000, stg_gym, stg_gym == 80000)

            cur.execute("SELECT COUNT(*) FROM staging.stg_sleep_stress_raw;")
            stg_sleep = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "Sleep Health CSV -> Staging", raw_counts.get("Sleep_health_and_lifestyle_dataset.csv", 374), stg_sleep, stg_sleep == 374)

            # Staging -> DWH SKU reconciliation (3,076 + (16,944 - 996 dups) = 19,024)
            cur.execute("SELECT COUNT(*) FROM dwh.dim_product;")
            dwh_prod = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "Staging Products (-996 dups) -> dim_product", 19024, dwh_prod, dwh_prod == 19024)

            cur.execute("SELECT COUNT(*) FROM dwh.fact_sales;")
            dwh_sales = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM datamart.vw_executive_sales;")
            dm_sales = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "fact_sales -> vw_executive_sales", dwh_sales, dm_sales, dwh_sales == dm_sales == 50000)

            cur.execute("SELECT COUNT(*) FROM dwh.fact_environmental_aqi;")
            dwh_aqi = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM datamart.vw_environmental_aqi_sales;")
            dm_aqi = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "fact_environmental_aqi -> vw_environmental_aqi_sales", dwh_aqi, dm_aqi, dwh_aqi == dm_aqi == 35090)

            cur.execute("SELECT SUM(member_count) FROM datamart.vw_fitness_demand_segmentation;")
            dm_gym_sum = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "Staging 80,000 GYM -> SUM(member_count) DataMart", 80000, dm_gym_sum, dm_gym_sum == 80000)

            cur.execute("SELECT COUNT(*) FROM datamart.vw_sleep_stress_lifestyle;")
            dm_sleep = cur.fetchone()[0]
            add_check("1. Row Reconciliation", "fact_lifestyle_sleep -> vw_sleep_stress_lifestyle", 374, dm_sleep, dm_sleep == 374)

            # --------------------------------------------------------------
            # SUITE 2: AGGREGATE FINANCIAL & KPI ACCURACY (ZERO DOUBLE COUNTING)
            # --------------------------------------------------------------
            cur.execute("SELECT ROUND(SUM(net_revenue_inr), 2), SUM(units_sold), ROUND(SUM(gross_revenue_inr), 2) FROM dwh.fact_sales;")
            dwh_net, dwh_units, dwh_gross = cur.fetchone()
            cur.execute("SELECT ROUND(SUM(net_revenue_inr), 2), SUM(units_sold), ROUND(SUM(gross_revenue_inr), 2) FROM datamart.vw_executive_sales;")
            dm_net, dm_units, dm_gross = cur.fetchone()
            cur.execute("SELECT ROUND(SUM(total_net_revenue_inr), 2), SUM(total_units_sold) FROM datamart.vw_sales_pricing_sku;")
            sku_net, sku_units = cur.fetchone()

            add_check("2. Aggregate Accuracy", "Net Revenue (DWH vs vw_executive_sales)", dwh_net, dm_net, dwh_net == dm_net, "Diff = 0.00")
            add_check("2. Aggregate Accuracy", "Net Revenue (DWH vs vw_sales_pricing_sku)", dwh_net, sku_net, dwh_net == sku_net, "Diff = 0.00")
            add_check("2. Aggregate Accuracy", "Units Sold (DWH vs DataMarts)", dwh_units, dm_units, dwh_units == dm_units == sku_units, "Diff = 0")

            cur.execute("SELECT ROUND(AVG(avg_us_aqi), 4) FROM dwh.fact_environmental_aqi;")
            dwh_avg_aqi = cur.fetchone()[0]
            cur.execute("SELECT ROUND(AVG(avg_us_aqi), 4) FROM datamart.vw_environmental_aqi_sales;")
            dm_avg_aqi = cur.fetchone()[0]
            add_check("2. Aggregate Accuracy", "Mean Daily US_AQI (DWH vs DataMart)", dwh_avg_aqi, dm_avg_aqi, dwh_avg_aqi == dm_avg_aqi, "Diff = 0.0000")

            # --------------------------------------------------------------
            # SUITE 3: REFERENTIAL INTEGRITY (ZERO ORPHAN FOREIGN KEYS)
            # --------------------------------------------------------------
            orphan_queries = [
                ("Orphan fact_sales -> dim_product", "SELECT COUNT(*) FROM dwh.fact_sales f LEFT JOIN dwh.dim_product d ON f.product_key = d.product_key WHERE d.product_key IS NULL;"),
                ("Orphan fact_sales -> dim_date", "SELECT COUNT(*) FROM dwh.fact_sales f LEFT JOIN dwh.dim_date d ON f.date_key = d.date_key WHERE d.date_key IS NULL;"),
                ("Orphan fact_environmental_aqi -> dim_location", "SELECT COUNT(*) FROM dwh.fact_environmental_aqi f LEFT JOIN dwh.dim_location d ON f.location_key = d.location_key WHERE d.location_key IS NULL;"),
                ("Orphan fact_fitness_demand -> dim_user_profile", "SELECT COUNT(*) FROM dwh.fact_fitness_demand f LEFT JOIN dwh.dim_user_profile d ON f.user_profile_key = d.user_profile_key WHERE d.user_profile_key IS NULL;"),
                ("Orphan fact_lifestyle_sleep -> dim_user_profile", "SELECT COUNT(*) FROM dwh.fact_lifestyle_sleep_health f LEFT JOIN dwh.dim_user_profile d ON f.user_profile_key = d.user_profile_key WHERE d.user_profile_key IS NULL;"),
            ]
            for label, q in orphan_queries:
                cur.execute(q)
                orphans = cur.fetchone()[0]
                add_check("3. Referential Integrity", label, 0, orphans, orphans == 0)

            # --------------------------------------------------------------
            # SUITE 4: DATA QUALITY & BUSINESS RULES
            # --------------------------------------------------------------
            dq_queries = [
                ("Zero selling_price <= 0 (dim_product)", "SELECT COUNT(*) FROM dwh.dim_product WHERE selling_price_inr <= 0;"),
                ("Zero inverted selling_price > mrp (dim_product)", "SELECT COUNT(*) FROM dwh.dim_product WHERE selling_price_inr > mrp_inr;"),
                ("Zero null/empty sleep_disorder", "SELECT COUNT(*) FROM dwh.fact_lifestyle_sleep_health WHERE sleep_disorder IS NULL OR TRIM(sleep_disorder) = '';"),
                ("Zero null avg_us_aqi (fact_environmental_aqi)", "SELECT COUNT(*) FROM dwh.fact_environmental_aqi WHERE avg_us_aqi IS NULL;"),
                ("100% simulated enrichment labeled (UAS Rule C)", "SELECT COUNT(*) FROM dwh.fact_sales WHERE is_simulated_enrichment IS DISTINCT FROM TRUE;"),
            ]
            for label, q in dq_queries:
                cur.execute(q)
                viol = cur.fetchone()[0]
                add_check("4. Data Quality Rules", label, 0, viol, viol == 0)

            # --------------------------------------------------------------
            # SUITE 5: RBAC LEAST PRIVILEGE VERIFICATION
            # --------------------------------------------------------------
            for biz_role in ("role_executive", "role_store_manager", "role_inventory_specialist"):
                cur.execute(
                    """
                    SELECT
                        has_schema_privilege(%s, 'staging', 'USAGE'),
                        has_schema_privilege(%s, 'dwh', 'USAGE'),
                        has_schema_privilege(%s, 'datamart', 'USAGE'),
                        has_table_privilege(%s, 'datamart.vw_executive_sales', 'SELECT');
                    """,
                    (biz_role, biz_role, biz_role, biz_role),
                )
                s_priv, d_priv, dm_priv, sel_priv = cur.fetchone()
                ok = (not s_priv) and (not d_priv) and dm_priv and sel_priv
                add_check(
                    "5. RBAC Security",
                    f"Least Privilege ({biz_role})",
                    "staging=False, dwh=False, datamart=True",
                    f"staging={s_priv}, dwh={d_priv}, datamart={dm_priv & sel_priv}",
                    ok,
                )

            # Golden Benchmark KPIs for Power BI Dashboard Verification (Point 28 PDF)
            cur.execute("""
                SELECT
                    COUNT(*) AS total_transactions,
                    SUM(units_sold) AS total_units_sold,
                    ROUND(SUM(gross_revenue_inr), 2) AS total_gross_revenue_inr,
                    ROUND(SUM(net_revenue_inr), 2) AS total_net_revenue_inr,
                    ROUND(AVG(net_revenue_inr), 2) AS avg_order_value_inr,
                    ROUND(AVG(discount_pct), 2) AS avg_discount_pct
                FROM datamart.vw_executive_sales;
            """)
            g_tx, g_units, g_gross, g_net, g_aov, g_disc = cur.fetchone()

            cur.execute("""
                SELECT channel_name, COUNT(*), SUM(units_sold), ROUND(SUM(net_revenue_inr), 2)
                FROM datamart.vw_executive_sales
                GROUP BY channel_name ORDER BY 4 DESC;
            """)
            channel_breakdown = [
                {"channel": r[0], "transactions": int(r[1]), "units": int(r[2]), "net_revenue_inr": float(r[3])}
                for r in cur.fetchall()
            ]

        passed_cnt = sum(1 for c in checks if c["status"] == "PASS")
        failed_cnt = sum(1 for c in checks if c["status"] == "FAIL")
        dur = round(time.time() - t0, 2)

        report = {
            "run_id": run_id,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": dur,
            "summary": {
                "total_checks": len(checks),
                "passed": passed_cnt,
                "failed": failed_cnt,
                "overall_status": "ALL PASSED" if failed_cnt == 0 else "HAS FAILURES",
            },
            "golden_kpi_benchmarks_for_powerbi": {
                "total_transactions": int(g_tx),
                "total_units_sold": int(g_units),
                "total_gross_revenue_inr": float(g_gross),
                "total_net_revenue_inr": float(g_net),
                "avg_order_value_inr": float(g_aov),
                "avg_discount_pct": float(g_disc),
                "channel_breakdown": channel_breakdown,
            },
            "checks": checks,
        }

        out_path = LOG_DIR / "validation_report.json"
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        record_audit(
            conn,
            run_id,
            "VALIDATION",
            "ALL_LAYERS (CSV->Staging->DWH->DataMart)",
            len(checks),
            passed_cnt,
            failed_cnt,
            "SUCCESS" if failed_cnt == 0 else "FAILED",
            dur,
            f"Passed={passed_cnt}/{len(checks)}",
        )
        conn.commit()

        logger.info("=== TAHAP 7 VALIDATION COMPLETED | passed=%d/%d | duration=%ss ===", passed_cnt, len(checks), dur)

        print("\n" + "=" * 92)
        print("HASIL UJI VALIDASI & REKONSILIASI TAHAP 7 (SOURCE -> STAGING -> DWH -> DATA MART)")
        print("=" * 92)
        cur_suite = None
        for c in checks:
            if c["suite"] != cur_suite:
                cur_suite = c["suite"]
                print(f"\n[{cur_suite}]")
            print(f"  [{c['status']}] {c['check_name']:48s} | Expected: {c['expected']:>14s} | Actual: {c['actual']:>14s}")
        print("\n" + "-" * 92)
        print(f"  SKOR AKHIR VALIDASI : {passed_cnt}/{len(checks)} PASSED ({failed_cnt} FAILED) dalam {dur} detik")
        print("  ANGKA PATOKAN EMAS (GOLDEN BENCHMARK) UNTUK REKONSILIASI DASHBOARD POWER BI:")
        print(f"    - Total Transactions : {g_tx:,}")
        print(f"    - Total Units Sold   : {g_units:,}")
        print(f"    - Gross Revenue      : INR {g_gross:,.2f}")
        print(f"    - Net Revenue        : INR {g_net:,.2f}")
        print(f"    - Avg Order Value    : INR {g_aov:,.2f} | Avg Discount: {g_disc}%")
        for cb in channel_breakdown:
            print(f"    - Channel {cb['channel']:16s} : {cb['transactions']:,} tx | {cb['units']:,} units | INR {cb['net_revenue_inr']:,.2f}")
        print(f"  Laporan JSON disimpan ke: {out_path}")
        print("=" * 92)

        if failed_cnt > 0:
            raise AssertionError(f"Validation failed with {failed_cnt} failed checks!")
        return report

    finally:
        conn.close()


if __name__ == "__main__":
    run_validation()
