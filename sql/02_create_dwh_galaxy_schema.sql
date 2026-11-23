-- =============================================================================
-- Tahap 4 (Langkah 3) - Pembuatan Core Data Warehouse (Galaxy Schema)
-- Urutan Wajib: 6 Tabel Conformed Dimensions Terlebih Dahulu, Lalu 4 Tabel Fact
-- Selaras 100% dengan Subbab 2.6 dan Tabel 2.10 Matriks Bus Laporan UAS
-- =============================================================================

-- Bersihkan tabel lama secara berurutan (Fact dulu baru Dimension karena FK)
DROP TABLE IF EXISTS dwh.fact_sales CASCADE;
DROP TABLE IF EXISTS dwh.fact_environmental_aqi CASCADE;
DROP TABLE IF EXISTS dwh.fact_fitness_demand CASCADE;
DROP TABLE IF EXISTS dwh.fact_lifestyle_sleep_health CASCADE;
DROP TABLE IF EXISTS dwh.etl_audit_log CASCADE;

DROP TABLE IF EXISTS dwh.dim_product CASCADE;
DROP TABLE IF EXISTS dwh.dim_channel CASCADE;
DROP TABLE IF EXISTS dwh.dim_user_profile CASCADE;
DROP TABLE IF EXISTS dwh.dim_category CASCADE;
DROP TABLE IF EXISTS dwh.dim_location CASCADE;
DROP TABLE IF EXISTS dwh.dim_date CASCADE;

-- =============================================================================
-- BAGIAN A: 6 TABEL CONFORMED DIMENSIONS
-- =============================================================================

-- 1. dim_date (Conformed Dimension universal untuk seluruh 4 tabel fakta)
CREATE TABLE dwh.dim_date (
    date_key        INTEGER PRIMARY KEY,         -- Format YYYYMMDD (contoh: 20240115)
    full_date       DATE NOT NULL UNIQUE,
    day_num         SMALLINT NOT NULL,
    month_num       SMALLINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    quarter_num     SMALLINT NOT NULL,
    quarter_label   VARCHAR(10) NOT NULL,        -- Q1, Q2, Q3, Q4
    year_num        SMALLINT NOT NULL,
    day_of_week     SMALLINT NOT NULL,           -- 1=Mon .. 7=Sun
    day_name        VARCHAR(15) NOT NULL,
    is_weekend      BOOLEAN NOT NULL DEFAULT FALSE,
    season_india    VARCHAR(20) NOT NULL         -- Winter, Summer, Monsoon, Post-Monsoon
);

-- 2. dim_location (Penghubung fact_sales, fact_environmental_aqi, fact_lifestyle_sleep_health)
CREATE TABLE dwh.dim_location (
    location_key    SERIAL PRIMARY KEY,
    city            VARCHAR(100) NOT NULL,
    state           VARCHAR(100) NOT NULL,
    region          VARCHAR(50) NOT NULL,        -- North, South, East, West, Central, Northeast
    latitude        NUMERIC(9, 6),
    longitude       NUMERIC(9, 6),
    country         VARCHAR(50) NOT NULL DEFAULT 'India',
    UNIQUE (city, state)
);

-- 3. dim_category (5 Kategori Standar Suplemen - penghubung sales, AQI, dan fitness)
CREATE TABLE dwh.dim_category (
    category_key        SERIAL PRIMARY KEY,
    category_code       VARCHAR(30) NOT NULL UNIQUE,
    category_name       VARCHAR(100) NOT NULL UNIQUE,
    health_focus        VARCHAR(150) NOT NULL,
    target_trigger      VARCHAR(150) NOT NULL
);

-- 4. dim_user_profile (Penghubung fact_fitness_demand dan fact_lifestyle_sleep_health)
CREATE TABLE dwh.dim_user_profile (
    user_profile_key    SERIAL PRIMARY KEY,
    profile_source      VARCHAR(30) NOT NULL,    -- 'GYM' atau 'SLEEP_STUDY'
    gender              VARCHAR(20) NOT NULL,
    age_group           VARCHAR(30) NOT NULL,
    bmi_category        VARCHAR(40) NOT NULL,
    fitness_goal        VARCHAR(60) NOT NULL,
    occupation          VARCHAR(80) NOT NULL,
    exercise_schedule   TEXT,
    meal_plan           TEXT
);

-- 5. dim_channel (Saluran Penjualan Multi-Kanal: Flipkart Health & Tata 1mg)
CREATE TABLE dwh.dim_channel (
    channel_key         SERIAL PRIMARY KEY,
    channel_code        VARCHAR(30) NOT NULL UNIQUE,
    channel_name        VARCHAR(100) NOT NULL UNIQUE,
    channel_type        VARCHAR(50) NOT NULL,
    platform_focus      VARCHAR(150) NOT NULL,
    currency_code       VARCHAR(10) NOT NULL DEFAULT 'INR'
);

-- 6. dim_product (Katalog Produk 20.020 SKU dengan dukungan SCD Type 2)
CREATE TABLE dwh.dim_product (
    product_key         SERIAL PRIMARY KEY,
    sku_natural_id      VARCHAR(100) NOT NULL,
    product_name        TEXT NOT NULL,
    brand               VARCHAR(150) NOT NULL,
    pack_size           VARCHAR(120),
    category_key        INTEGER NOT NULL REFERENCES dwh.dim_category(category_key),
    channel_source      VARCHAR(50) NOT NULL,
    mrp_inr             NUMERIC(12, 2) NOT NULL,
    selling_price_inr   NUMERIC(12, 2) NOT NULL,
    discount_pct        NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    avg_rating          NUMERIC(3, 2),
    rating_count        INTEGER DEFAULT 0,
    availability        VARCHAR(40) DEFAULT 'IN_STOCK',
    -- Atribut SCD Type 2 (Slowly Changing Dimension)
    effective_date      DATE NOT NULL DEFAULT CURRENT_DATE,
    expiry_date         DATE,
    is_current          BOOLEAN NOT NULL DEFAULT TRUE
);

-- =============================================================================
-- BAGIAN B: 4 TABEL FAKTA (GALAXY SCHEMA / FACT CONSTELLATION)
-- =============================================================================

-- 1. fact_sales (Transaksi Penjualan Multi-Kanal)
CREATE TABLE dwh.fact_sales (
    sales_key               BIGSERIAL PRIMARY KEY,
    transaction_id          VARCHAR(60) NOT NULL UNIQUE,
    date_key                INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    location_key            INTEGER NOT NULL REFERENCES dwh.dim_location(location_key),
    category_key            INTEGER NOT NULL REFERENCES dwh.dim_category(category_key),
    product_key             INTEGER NOT NULL REFERENCES dwh.dim_product(product_key),
    channel_key             INTEGER NOT NULL REFERENCES dwh.dim_channel(channel_key),
    units_sold              INTEGER NOT NULL CHECK (units_sold > 0),
    unit_mrp_inr            NUMERIC(12, 2) NOT NULL,
    unit_selling_price_inr  NUMERIC(12, 2) NOT NULL,
    discount_amount_inr     NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    discount_pct            NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    gross_revenue_inr       NUMERIC(14, 2) NOT NULL,
    net_revenue_inr         NUMERIC(14, 2) NOT NULL,
    is_simulated_enrichment BOOLEAN NOT NULL DEFAULT TRUE,
    etl_loaded_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. fact_environmental_aqi (Agregasi Harian Kualitas Udara & Meteorologi per Kota)
CREATE TABLE dwh.fact_environmental_aqi (
    aqi_key                 BIGSERIAL PRIMARY KEY,
    date_key                INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    location_key            INTEGER NOT NULL REFERENCES dwh.dim_location(location_key),
    category_key            INTEGER NOT NULL REFERENCES dwh.dim_category(category_key),
    avg_us_aqi              NUMERIC(8, 2) NOT NULL,
    max_us_aqi              NUMERIC(8, 2) NOT NULL,
    avg_pm25_ugm3           NUMERIC(8, 2),
    avg_pm10_ugm3           NUMERIC(8, 2),
    avg_no2_ugm3            NUMERIC(8, 2),
    avg_o3_ugm3             NUMERIC(8, 2),
    avg_temp_c              NUMERIC(6, 2),
    avg_humidity_pct        NUMERIC(6, 2),
    dominant_aqi_category   VARCHAR(40) NOT NULL,
    is_festival_period      BOOLEAN NOT NULL DEFAULT FALSE,
    is_crop_burning_season  BOOLEAN NOT NULL DEFAULT FALSE,
    hourly_obs_count        INTEGER NOT NULL DEFAULT 24,
    etl_loaded_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (date_key, location_key)
);

-- 3. fact_fitness_demand (Permintaan Segmen Kebugaran & Nutrisi Olahraga)
CREATE TABLE dwh.fact_fitness_demand (
    fitness_key             BIGSERIAL PRIMARY KEY,
    date_key                INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    category_key            INTEGER NOT NULL REFERENCES dwh.dim_category(category_key),
    user_profile_key        INTEGER NOT NULL REFERENCES dwh.dim_user_profile(user_profile_key),
    member_count            INTEGER NOT NULL CHECK (member_count > 0),
    demand_share_pct        NUMERIC(6, 2) NOT NULL,
    demand_intensity_score  NUMERIC(6, 2) NOT NULL,
    etl_loaded_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. fact_lifestyle_sleep_health (Observasi Kualitas Tidur, Stres & Kesehatan Gaya Hidup)
CREATE TABLE dwh.fact_lifestyle_sleep_health (
    sleep_key               BIGSERIAL PRIMARY KEY,
    person_id               INTEGER NOT NULL UNIQUE,
    date_key                INTEGER NOT NULL REFERENCES dwh.dim_date(date_key),
    location_key            INTEGER NOT NULL REFERENCES dwh.dim_location(location_key),
    user_profile_key        INTEGER NOT NULL REFERENCES dwh.dim_user_profile(user_profile_key),
    age                     SMALLINT NOT NULL,
    sleep_duration_hrs      NUMERIC(4, 2) NOT NULL,
    quality_of_sleep        SMALLINT NOT NULL,
    physical_activity_level SMALLINT NOT NULL,
    stress_level            SMALLINT NOT NULL,
    systolic_bp             SMALLINT,
    diastolic_bp            SMALLINT,
    heart_rate_bpm          SMALLINT NOT NULL,
    daily_steps             INTEGER NOT NULL,
    sleep_disorder          VARCHAR(50) NOT NULL DEFAULT 'None',
    etl_loaded_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- BAGIAN C: TABEL AUDIT TRAIL EKSEKUSI ETL (DATA GOVERNANCE & LINEAGE)
-- =============================================================================
CREATE TABLE dwh.etl_audit_log (
    audit_id            SERIAL PRIMARY KEY,
    pipeline_run_id     VARCHAR(64) NOT NULL,
    stage_name          VARCHAR(80) NOT NULL,
    table_target        VARCHAR(100) NOT NULL,
    rows_input          INTEGER DEFAULT 0,
    rows_loaded         INTEGER DEFAULT 0,
    rows_rejected       INTEGER DEFAULT 0,
    status              VARCHAR(20) NOT NULL,    -- SUCCESS, FAILED, WARNING
    duration_seconds    NUMERIC(10, 2) DEFAULT 0.00,
    message             TEXT,
    executed_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- BAGIAN D: PERFORMANCE INDEXES PADA FOREIGN KEYS
-- =============================================================================
CREATE INDEX idx_fact_sales_date        ON dwh.fact_sales(date_key);
CREATE INDEX idx_fact_sales_location    ON dwh.fact_sales(location_key);
CREATE INDEX idx_fact_sales_category    ON dwh.fact_sales(category_key);
CREATE INDEX idx_fact_sales_product     ON dwh.fact_sales(product_key);
CREATE INDEX idx_fact_sales_channel     ON dwh.fact_sales(channel_key);

CREATE INDEX idx_fact_aqi_date          ON dwh.fact_environmental_aqi(date_key);
CREATE INDEX idx_fact_aqi_location      ON dwh.fact_environmental_aqi(location_key);
CREATE INDEX idx_fact_aqi_category      ON dwh.fact_environmental_aqi(category_key);

CREATE INDEX idx_fact_fitness_date      ON dwh.fact_fitness_demand(date_key);
CREATE INDEX idx_fact_fitness_category  ON dwh.fact_fitness_demand(category_key);
CREATE INDEX idx_fact_fitness_profile   ON dwh.fact_fitness_demand(user_profile_key);

CREATE INDEX idx_fact_sleep_date        ON dwh.fact_lifestyle_sleep_health(date_key);
CREATE INDEX idx_fact_sleep_location    ON dwh.fact_lifestyle_sleep_health(location_key);
CREATE INDEX idx_fact_sleep_profile     ON dwh.fact_lifestyle_sleep_health(user_profile_key);

CREATE INDEX idx_dim_product_sku        ON dwh.dim_product(sku_natural_id);
CREATE INDEX idx_dim_product_category   ON dwh.dim_product(category_key);
