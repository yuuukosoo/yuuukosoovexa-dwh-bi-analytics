-- =============================================================================
-- Tahap 4 (Langkah 2) - Pembuatan 3 Skema & 5 Tabel Raw Staging
-- Proyek: Data Warehouse & BI Dashboard PT YuuukosooVexa
-- =============================================================================

-- 1. Membuat 3 skema pemisah lapisan arsitektur DWH
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dwh;
CREATE SCHEMA IF NOT EXISTS datamart;

-- 2. Tabel Staging 1: Katalog Suplemen Flipkart Health (3.076 baris mentah)
DROP TABLE IF EXISTS staging.stg_flipkart_raw CASCADE;
CREATE TABLE staging.stg_flipkart_raw (
    raw_id              BIGSERIAL PRIMARY KEY,
    category            TEXT,
    title               TEXT,
    quantity            TEXT,
    brand               TEXT,
    url                 TEXT,
    product_id          TEXT,
    listing_id          TEXT,
    highlights          TEXT,
    availability        TEXT,
    selling_price       TEXT,
    original_price      TEXT,
    currency            TEXT,
    avg_rating          TEXT,
    rating_count        TEXT,
    review_count        TEXT,
    stars_1_count       TEXT,
    stars_2_count       TEXT,
    stars_3_count       TEXT,
    stars_4_count       TEXT,
    stars_5_count       TEXT,
    source_file         TEXT DEFAULT 'Health_Suppliments_Flipkart_02_04_2022.csv',
    ingested_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabel Staging 2: Katalog Farmasi Tata 1mg (16.944 baris mentah)
DROP TABLE IF EXISTS staging.stg_tata1mg_raw CASCADE;
CREATE TABLE staging.stg_tata1mg_raw (
    raw_id              BIGSERIAL PRIMARY KEY,
    name                TEXT,
    pack_size           TEXT,
    rating_count        TEXT,
    rating              TEXT,
    price               TEXT,
    mrp                 TEXT,
    source_file         TEXT DEFAULT '1mgData.csv',
    ingested_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabel Staging 3: Observasi Kualitas Udara & Cuaca India (AQI Hourly/Daily)
DROP TABLE IF EXISTS staging.stg_aqi_hourly_raw CASCADE;
CREATE TABLE staging.stg_aqi_hourly_raw (
    raw_id                  BIGSERIAL PRIMARY KEY,
    city                    TEXT,
    state                   TEXT,
    latitude                DOUBLE PRECISION,
    longitude               DOUBLE PRECISION,
    obs_datetime            TEXT,
    obs_year                INTEGER,
    obs_month               INTEGER,
    obs_day                 INTEGER,
    season                  TEXT,
    temp_2m_c               DOUBLE PRECISION,
    humidity_percent        DOUBLE PRECISION,
    wind_speed_10m_kmh      DOUBLE PRECISION,
    precipitation_mm        DOUBLE PRECISION,
    pm2_5_ugm3              DOUBLE PRECISION,
    pm10_ugm3               DOUBLE PRECISION,
    co_ugm3                 DOUBLE PRECISION,
    no2_ugm3                DOUBLE PRECISION,
    so2_ugm3                DOUBLE PRECISION,
    o3_ugm3                 DOUBLE PRECISION,
    us_aqi                  DOUBLE PRECISION,
    aqi_category            TEXT,
    pm25_category_india     TEXT,
    festival_period         INTEGER,
    crop_burning_season     INTEGER,
    source_file             TEXT DEFAULT 'INDIA_AQI_COMPLETE_20251126.csv',
    ingested_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabel Staging 4: Profil Kebugaran & Diet Anggota Gym (80.000 baris bersih setelah koreksi header)
DROP TABLE IF EXISTS staging.stg_gym_profile_raw CASCADE;
CREATE TABLE staging.stg_gym_profile_raw (
    raw_id              BIGSERIAL PRIMARY KEY,
    gender              TEXT,
    goal                TEXT,
    bmi_category        TEXT,
    exercise_schedule   TEXT,
    meal_plan           TEXT,
    source_file         TEXT DEFAULT 'GYM.csv',
    ingested_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabel Staging 5: Survei Kualitas Tidur & Gaya Hidup (374 baris mentah)
DROP TABLE IF EXISTS staging.stg_sleep_stress_raw CASCADE;
CREATE TABLE staging.stg_sleep_stress_raw (
    raw_id                      BIGSERIAL PRIMARY KEY,
    person_id                   TEXT,
    gender                      TEXT,
    age                         TEXT,
    occupation                  TEXT,
    sleep_duration              TEXT,
    quality_of_sleep            TEXT,
    physical_activity_level     TEXT,
    stress_level                TEXT,
    bmi_category                TEXT,
    blood_pressure              TEXT,
    heart_rate                  TEXT,
    daily_steps                 TEXT,
    sleep_disorder              TEXT,
    source_file                 TEXT DEFAULT 'Sleep_health_and_lifestyle_dataset.csv',
    ingested_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
