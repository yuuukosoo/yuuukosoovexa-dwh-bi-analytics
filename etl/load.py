"""
Tahap 5C - LOAD Stage (Processed CSVs -> PostgreSQL Core DWH Galaxy Schema)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Fitur:
  1. Pre-check kelengkapan 10 berkas bersih di data/processed/
  2. Atomic Transaction + Automatic Rollback apabila terjadi kegagalan
  3. Urutan pemuatan ketat: 6 Tabel Conformed Dimensions dulu, lalu 4 Tabel Fact
  4. Sinkronisasi otomatis sequence SERIAL PostgreSQL
  5. Pencatatan audit trail ke dwh.etl_audit_log & logs/etl_pipeline.log
"""

import time
import uuid
import pandas as pd

from db_utils import (
    PROCESSED_DIR,
    copy_dataframe_to_pg,
    get_logger,
    get_pg_connection,
    record_audit,
)

logger = get_logger("etl.load")

# Urutan wajib: 6 Dimensi terlebih dahulu (dim_category sebelum dim_product), lalu 4 Fakta
LOAD_PLAN = [
    (
        "dwh.dim_date",
        "dim_date.csv",
        [
            "date_key", "full_date", "day_num", "month_num", "month_name",
            "quarter_num", "quarter_label", "year_num", "day_of_week",
            "day_name", "is_weekend", "season_india",
        ],
        None,
    ),
    (
        "dwh.dim_location",
        "dim_location.csv",
        ["location_key", "city", "state", "region", "latitude", "longitude", "country"],
        "location_key",
    ),
    (
        "dwh.dim_category",
        "dim_category.csv",
        ["category_key", "category_code", "category_name", "health_focus", "target_trigger"],
        "category_key",
    ),
    (
        "dwh.dim_channel",
        "dim_channel.csv",
        ["channel_key", "channel_code", "channel_name", "channel_type", "platform_focus", "currency_code"],
        "channel_key",
    ),
    (
        "dwh.dim_user_profile",
        "dim_user_profile.csv",
        [
            "user_profile_key", "profile_source", "gender", "age_group",
            "bmi_category", "fitness_goal", "occupation",
            "exercise_schedule", "meal_plan",
        ],
        "user_profile_key",
    ),
    (
        "dwh.dim_product",
        "dim_product.csv",
        [
            "product_key", "sku_natural_id", "product_name", "brand", "pack_size",
            "category_key", "channel_source", "mrp_inr", "selling_price_inr",
            "discount_pct", "avg_rating", "rating_count", "availability",
            "effective_date", "expiry_date", "is_current",
        ],
        "product_key",
    ),
    (
        "dwh.fact_environmental_aqi",
        "fact_environmental_aqi.csv",
        [
            "date_key", "location_key", "category_key",
            "avg_us_aqi", "max_us_aqi", "avg_pm25_ugm3", "avg_pm10_ugm3",
            "avg_no2_ugm3", "avg_o3_ugm3", "avg_temp_c", "avg_humidity_pct",
            "dominant_aqi_category", "is_festival_period",
            "is_crop_burning_season", "hourly_obs_count",
        ],
        None,
    ),
    (
        "dwh.fact_fitness_demand",
        "fact_fitness_demand.csv",
        [
            "date_key", "category_key", "user_profile_key",
            "member_count", "demand_share_pct", "demand_intensity_score",
        ],
        None,
    ),
    (
        "dwh.fact_lifestyle_sleep_health",
        "fact_lifestyle_sleep_health.csv",
        [
            "person_id", "date_key", "location_key", "user_profile_key",
            "age", "sleep_duration_hrs", "quality_of_sleep",
            "physical_activity_level", "stress_level", "systolic_bp",
            "diastolic_bp", "heart_rate_bpm", "daily_steps", "sleep_disorder",
        ],
        None,
    ),
    (
        "dwh.fact_sales",
        "fact_sales.csv",
        [
            "transaction_id", "date_key", "location_key", "category_key",
            "product_key", "channel_key", "units_sold", "unit_mrp_inr",
            "unit_selling_price_inr", "discount_amount_inr", "discount_pct",
            "gross_revenue_inr", "net_revenue_inr", "is_simulated_enrichment",
        ],
        None,
    ),
]


def clean_integer_columns_for_copy(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Ensure nullable integer columns do not serialize as floats like '126.0'."""
    int_cols_map = {
        "dwh.dim_product": ["product_key", "category_key", "rating_count"],
        "dwh.fact_lifestyle_sleep_health": [
            "person_id", "date_key", "location_key", "user_profile_key",
            "age", "quality_of_sleep", "physical_activity_level",
            "stress_level", "systolic_bp", "diastolic_bp",
            "heart_rate_bpm", "daily_steps",
        ],
        "dwh.fact_environmental_aqi": ["date_key", "location_key", "category_key", "hourly_obs_count"],
        "dwh.fact_fitness_demand": ["date_key", "category_key", "user_profile_key", "member_count"],
        "dwh.fact_sales": ["date_key", "location_key", "category_key", "product_key", "channel_key", "units_sold"],
    }
    for col in int_cols_map.get(table_name, []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    return df


def run_load(run_id: str | None = None) -> dict:
    run_id = run_id or f"LOD-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t_total = time.time()
    logger.info("=== START LOAD STAGE (GALAXY SCHEMA DWH) | run_id=%s ===", run_id)

    # Langkah 1: Pre-check keberadaan seluruh 10 berkas bersih di data/processed/
    missing = [fname for _, fname, _, _ in LOAD_PLAN if not (PROCESSED_DIR / fname).exists()]
    if missing:
        msg = f"Missing processed CSV files in data/processed/: {missing}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    logger.info("Pre-check PASSED: all 10 processed CSV files exist.")

    conn = get_pg_connection()
    conn.autocommit = False
    loaded_counts = {}

    try:
        # Langkah 3: Idempotent Truncate seluruh tabel DWH (Fact + Dim) dalam 1 transaksi atomik
        logger.info("Truncating existing Core DWH tables inside atomic transaction...")
        with conn.cursor() as cur:
            cur.execute(
                """
                TRUNCATE TABLE
                    dwh.fact_sales,
                    dwh.fact_environmental_aqi,
                    dwh.fact_fitness_demand,
                    dwh.fact_lifestyle_sleep_health,
                    dwh.dim_product,
                    dwh.dim_user_profile,
                    dwh.dim_channel,
                    dwh.dim_category,
                    dwh.dim_location,
                    dwh.dim_date
                RESTART IDENTITY CASCADE;
                """
            )

        # Langkah 4 & 5: Muat 6 Dimensi dulu, kemudian 4 Fakta
        for table_name, filename, cols, seq_col in LOAD_PLAN:
            t0 = time.time()
            df = pd.read_csv(PROCESSED_DIR / filename, keep_default_na=True, low_memory=False)
            # Keep literal 'None' in sleep_disorder (prevent pandas converting 'None' to NaN)
            if table_name == "dwh.fact_lifestyle_sleep_health":
                df["sleep_disorder"] = df["sleep_disorder"].fillna("None")
            df = clean_integer_columns_for_copy(df, table_name)

            copy_dataframe_to_pg(conn, df, table_name, cols)

            if seq_col:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT setval(pg_get_serial_sequence('{table_name}', '{seq_col}'), "
                        f"COALESCE((SELECT MAX({seq_col}) FROM {table_name}), 1), true);"
                    )

            dur = time.time() - t0
            loaded_counts[table_name] = len(df)
            record_audit(conn, run_id, "LOAD", table_name, len(df), len(df), 0, "SUCCESS", dur, f"Source={filename}")
            logger.info("Loaded %-34s -> %8s rows in %.2fs", table_name, f"{len(df):,}", dur)

        # Langkah 6: Commit permanen apabila seluruh 10 tabel sukses tanpa error
        conn.commit()
        total_dur = round(time.time() - t_total, 2)
        total_rows = sum(loaded_counts.values())
        logger.info("=== LOAD STAGE COMPLETED | total_rows=%s | duration=%ss ===", f"{total_rows:,}", total_dur)

        # Verifikasi langsung dari PostgreSQL
        print("\n" + "=" * 76)
        print("VERIFIKASI HASIL TAHAP 5C (LOAD -> CORE DWH GALAXY SCHEMA POSTGRESQL)")
        print("=" * 76)
        with conn.cursor() as cur:
            for tbl in loaded_counts:
                cur.execute(f"SELECT COUNT(*) FROM {tbl};")
                actual = cur.fetchone()[0]
                status = "MATCH" if actual == loaded_counts[tbl] else "MISMATCH"
                print(f"  {tbl:34s} -> {actual:>10,} rows ({status})")
        print("-" * 76)
        print(f"  TOTAL CORE DWH ROWS LOADED         -> {total_rows:>10,} rows in {total_dur}s")
        print("=" * 76)
        return loaded_counts

    except Exception as exc:
        conn.rollback()
        logger.exception("LOAD FAILED - ALL CHANGES ROLLED BACK: %s", exc)
        try:
            record_audit(conn, run_id, "LOAD", "dwh.*", 0, 0, 0, "FAILED", time.time() - t_total, str(exc))
            conn.commit()
        except Exception:
            pass
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_load()
