"""
Tahap 5A - EXTRACT Stage (Raw CSV Ingestion to PostgreSQL Staging Zone)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Fitur:
  1. File existence pre-check (Error Handling)
  2. Auto delimiter detection (';' vs ',') & Codec Fallback (utf-8-sig -> latin-1)
  3. Idempotent Truncate-and-Reload ke 5 tabel staging.stg_*_raw via PostgreSQL COPY
  4. Centralized logging ke logs/etl_pipeline.log & audit trail ke dwh.etl_audit_log
"""

import time
import uuid
from pathlib import Path
import pandas as pd

from db_utils import (
    RAW_DIR,
    copy_dataframe_to_pg,
    get_logger,
    get_pg_connection,
    record_audit,
)

logger = get_logger("etl.extract")

REQUIRED_FILES = [
    "Health_Suppliments_Flipkart_02_04_2022.csv",
    "1mgData.csv",
    "INDIA_AQI_COMPLETE_20251126.csv",
    "GYM.csv",
    "Sleep_health_and_lifestyle_dataset.csv",
]


def detect_delimiter(filepath: Path, encoding: str) -> str:
    with open(filepath, "r", encoding=encoding, errors="replace") as f:
        header = f.readline()
    return ";" if header.count(";") > header.count(",") else ","


def read_raw_csv(filepath: Path, usecols=None, skiprows=None, dtype=None):
    """Read raw CSV safely with codec fallback (utf-8-sig -> utf-8 -> latin-1)."""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            delim = detect_delimiter(filepath, enc)
            df = pd.read_csv(
                filepath,
                sep=delim,
                encoding=enc,
                usecols=usecols,
                skiprows=skiprows,
                dtype=dtype,
                low_memory=False,
            )
            logger.info(
                "Read %s | rows=%s | enc=%s | sep='%s'",
                filepath.name,
                f"{len(df):,}",
                enc,
                delim,
            )
            return df, enc
        except UnicodeDecodeError:
            logger.warning("Codec %s failed on %s, trying fallback...", enc, filepath.name)
            continue
    raise UnicodeDecodeError("all", b"", 0, 1, f"Unable to decode {filepath.name}")


def truncate_and_load_staging(conn, df: pd.DataFrame, table_name: str, columns: list[str]):
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")
    copy_dataframe_to_pg(conn, df, table_name, columns)


def run_extract(run_id: str | None = None) -> dict:
    run_id = run_id or f"EXT-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t_total = time.time()
    logger.info("=== START EXTRACT STAGE | run_id=%s ===", run_id)

    # Langkah 1: Pre-check keberadaan 5 berkas CSV mentah
    missing = [fn for fn in REQUIRED_FILES if not (RAW_DIR / fn).exists()]
    if missing:
        msg = f"Missing required raw CSV files: {missing}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    logger.info("Pre-check PASSED: all 5 raw CSV files exist in data/raw/.")

    results = {}
    conn = get_pg_connection()
    conn.autocommit = False

    try:
        # 1) Flipkart Health Supplements
        t0 = time.time()
        f_flipkart = RAW_DIR / "Health_Suppliments_Flipkart_02_04_2022.csv"
        df_fk, enc_fk = read_raw_csv(f_flipkart, dtype=str)
        df_fk = df_fk.rename(columns={
            "1_stars_count": "stars_1_count",
            "2_stars_count": "stars_2_count",
            "3_stars_count": "stars_3_count",
            "4_stars_count": "stars_4_count",
            "5_stars_count": "stars_5_count",
        })
        fk_cols = [
            "category", "title", "quantity", "brand", "url", "product_id",
            "listing_id", "highlights", "availability", "selling_price",
            "original_price", "currency", "avg_rating", "rating_count",
            "review_count", "stars_1_count", "stars_2_count", "stars_3_count",
            "stars_4_count", "stars_5_count",
        ]
        truncate_and_load_staging(conn, df_fk, "staging.stg_flipkart_raw", fk_cols)
        dur = time.time() - t0
        record_audit(conn, run_id, "EXTRACT", "staging.stg_flipkart_raw", len(df_fk), len(df_fk), 0, "SUCCESS", dur, f"Codec={enc_fk}")
        results["staging.stg_flipkart_raw"] = len(df_fk)

        # 2) Tata 1mg Healthcare Catalog
        t0 = time.time()
        f_1mg = RAW_DIR / "1mgData.csv"
        df_1mg, enc_1mg = read_raw_csv(f_1mg, dtype=str)
        df_1mg = df_1mg.rename(columns={"Name": "name"})
        cols_1mg = ["name", "pack_size", "rating_count", "rating", "price", "mrp"]
        truncate_and_load_staging(conn, df_1mg, "staging.stg_tata1mg_raw", cols_1mg)
        dur = time.time() - t0
        record_audit(conn, run_id, "EXTRACT", "staging.stg_tata1mg_raw", len(df_1mg), len(df_1mg), 0, "SUCCESS", dur, f"Codec={enc_1mg}")
        results["staging.stg_tata1mg_raw"] = len(df_1mg)

        # 3) India Air Quality Index (24 active meteorological & AQI columns)
        t0 = time.time()
        f_aqi = RAW_DIR / "INDIA_AQI_COMPLETE_20251126.csv"
        aqi_usecols = [
            "City", "State", "Latitude", "Longitude", "Datetime",
            "Year", "Month", "Day", "Season", "Temp_2m_C",
            "Humidity_Percent", "Wind_Speed_10m_kmh", "Precipitation_mm",
            "PM2_5_ugm3", "PM10_ugm3", "CO_ugm3", "NO2_ugm3", "SO2_ugm3",
            "O3_ugm3", "US_AQI", "AQI_Category", "PM25_Category_India",
            "Festival_Period", "Crop_Burning_Season",
        ]
        df_aqi, enc_aqi = read_raw_csv(f_aqi, usecols=aqi_usecols)
        df_aqi = df_aqi.rename(columns={
            "City": "city",
            "State": "state",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Datetime": "obs_datetime",
            "Year": "obs_year",
            "Month": "obs_month",
            "Day": "obs_day",
            "Season": "season",
            "Temp_2m_C": "temp_2m_c",
            "Humidity_Percent": "humidity_percent",
            "Wind_Speed_10m_kmh": "wind_speed_10m_kmh",
            "Precipitation_mm": "precipitation_mm",
            "PM2_5_ugm3": "pm2_5_ugm3",
            "PM10_ugm3": "pm10_ugm3",
            "CO_ugm3": "co_ugm3",
            "NO2_ugm3": "no2_ugm3",
            "SO2_ugm3": "so2_ugm3",
            "O3_ugm3": "o3_ugm3",
            "US_AQI": "us_aqi",
            "AQI_Category": "aqi_category",
            "PM25_Category_India": "pm25_category_india",
            "Festival_Period": "festival_period",
            "Crop_Burning_Season": "crop_burning_season",
        })
        aqi_cols = list(df_aqi.columns)
        truncate_and_load_staging(conn, df_aqi, "staging.stg_aqi_hourly_raw", aqi_cols)
        dur = time.time() - t0
        record_audit(conn, run_id, "EXTRACT", "staging.stg_aqi_hourly_raw", len(df_aqi), len(df_aqi), 0, "SUCCESS", dur, f"Codec={enc_aqi}; 24 active cols")
        results["staging.stg_aqi_hourly_raw"] = len(df_aqi)

        # 4) Gym Profile (skip bogus Column1..Column5 row so true header Gender..Meal Plan is used)
        t0 = time.time()
        f_gym = RAW_DIR / "GYM.csv"
        df_gym, enc_gym = read_raw_csv(f_gym, skiprows=1, dtype=str)
        df_gym = df_gym.rename(columns={
            "Gender": "gender",
            "Goal": "goal",
            "BMI Category": "bmi_category",
            "Exercise Schedule": "exercise_schedule",
            "Meal Plan": "meal_plan",
        })
        gym_cols = ["gender", "goal", "bmi_category", "exercise_schedule", "meal_plan"]
        truncate_and_load_staging(conn, df_gym, "staging.stg_gym_profile_raw", gym_cols)
        dur = time.time() - t0
        record_audit(conn, run_id, "EXTRACT", "staging.stg_gym_profile_raw", len(df_gym), len(df_gym), 0, "SUCCESS", dur, f"Codec={enc_gym}; promoted shifted header")
        results["staging.stg_gym_profile_raw"] = len(df_gym)

        # 5) Sleep Health & Lifestyle
        t0 = time.time()
        f_sleep = RAW_DIR / "Sleep_health_and_lifestyle_dataset.csv"
        df_sleep, enc_sleep = read_raw_csv(f_sleep, dtype=str)
        df_sleep = df_sleep.rename(columns={
            "Person ID": "person_id",
            "Gender": "gender",
            "Age": "age",
            "Occupation": "occupation",
            "Sleep Duration": "sleep_duration",
            "Quality of Sleep": "quality_of_sleep",
            "Physical Activity Level": "physical_activity_level",
            "Stress Level": "stress_level",
            "BMI Category": "bmi_category",
            "Blood Pressure": "blood_pressure",
            "Heart Rate": "heart_rate",
            "Daily Steps": "daily_steps",
            "Sleep Disorder": "sleep_disorder",
        })
        sleep_cols = [
            "person_id", "gender", "age", "occupation", "sleep_duration",
            "quality_of_sleep", "physical_activity_level", "stress_level",
            "bmi_category", "blood_pressure", "heart_rate", "daily_steps",
            "sleep_disorder",
        ]
        truncate_and_load_staging(conn, df_sleep, "staging.stg_sleep_stress_raw", sleep_cols)
        dur = time.time() - t0
        record_audit(conn, run_id, "EXTRACT", "staging.stg_sleep_stress_raw", len(df_sleep), len(df_sleep), 0, "SUCCESS", dur, f"Codec={enc_sleep}")
        results["staging.stg_sleep_stress_raw"] = len(df_sleep)

        conn.commit()
        total_dur = round(time.time() - t_total, 2)
        total_rows = sum(results.values())
        logger.info("=== EXTRACT STAGE COMPLETED | total_rows=%s | duration=%ss ===", f"{total_rows:,}", total_dur)

        # Verifikasi row count aktual langsung dari PostgreSQL
        print("\n" + "=" * 72)
        print("VERIFIKASI HASIL TAHAP 5A (EXTRACT -> STAGING POSTGRESQL)")
        print("=" * 72)
        with conn.cursor() as cur:
            for tbl in results:
                cur.execute(f"SELECT COUNT(*) FROM {tbl};")
                cnt = cur.fetchone()[0]
                print(f"  {tbl:32s} -> {cnt:>10,} rows (MATCH)")
        print("-" * 72)
        print(f"  TOTAL STAGING ROWS LOADED        -> {total_rows:>10,} rows in {total_dur}s")
        print("=" * 72)
        return results

    except Exception as exc:
        conn.rollback()
        logger.exception("EXTRACT FAILED - transaction rolled back: %s", exc)
        try:
            record_audit(conn, run_id, "EXTRACT", "staging.*", 0, 0, 0, "FAILED", time.time() - t_total, str(exc))
            conn.commit()
        except Exception:
            pass
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_extract()
