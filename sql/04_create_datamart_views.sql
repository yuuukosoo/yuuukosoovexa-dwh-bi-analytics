-- =============================================================================
-- Tahap 6A - Pembuatan Data Mart Views (Siap Tarik ke Microsoft Power BI)
-- Proyek: Data Warehouse & BI Dashboard PT YuuukosooVexa
-- =============================================================================

-- 1. Data Mart Halaman 1: Executive Summary and Multi-Channel Sales
CREATE OR REPLACE VIEW datamart.vw_executive_sales AS
SELECT
    fs.sales_key,
    fs.transaction_id,
    d.date_key,
    d.full_date,
    d.year_num,
    d.quarter_label,
    d.month_num,
    d.month_name,
    d.day_name,
    d.is_weekend,
    d.season_india,
    ch.channel_code,
    ch.channel_name,
    cat.category_code,
    cat.category_name,
    cat.health_focus,
    loc.city,
    loc.state,
    loc.region,
    loc.latitude,
    loc.longitude,
    fs.units_sold,
    fs.unit_mrp_inr,
    fs.unit_selling_price_inr,
    fs.discount_amount_inr,
    fs.discount_pct,
    fs.gross_revenue_inr,
    fs.net_revenue_inr,
    fs.is_simulated_enrichment
FROM dwh.fact_sales fs
JOIN dwh.dim_date     d   ON fs.date_key     = d.date_key
JOIN dwh.dim_channel  ch  ON fs.channel_key  = ch.channel_key
JOIN dwh.dim_category cat ON fs.category_key = cat.category_key
JOIN dwh.dim_location loc ON fs.location_key = loc.location_key;

-- 2. Data Mart Halaman 2: Sales and Pricing Optimization (+ Product SKU Deep-Dive)
CREATE OR REPLACE VIEW datamart.vw_sales_pricing_sku AS
SELECT
    p.product_key,
    p.sku_natural_id,
    p.product_name,
    p.brand,
    p.pack_size,
    p.channel_source,
    cat.category_name,
    p.mrp_inr,
    p.selling_price_inr,
    p.discount_pct,
    CASE
        WHEN p.discount_pct = 0               THEN '0% (No Discount)'
        WHEN p.discount_pct <= 15             THEN '1-15% (Low Discount)'
        WHEN p.discount_pct <= 30             THEN '16-30% (Moderate Discount)'
        WHEN p.discount_pct <= 50             THEN '31-50% (High Discount)'
        ELSE '>50% (Aggressive Discount)'
    END AS discount_tier,
    p.avg_rating,
    p.rating_count,
    p.availability,
    COUNT(fs.sales_key)                           AS total_transactions,
    COALESCE(SUM(fs.units_sold), 0)               AS total_units_sold,
    COALESCE(SUM(fs.gross_revenue_inr), 0.00)     AS total_gross_revenue_inr,
    COALESCE(SUM(fs.net_revenue_inr), 0.00)       AS total_net_revenue_inr,
    COALESCE(SUM(fs.discount_amount_inr), 0.00)   AS total_discount_given_inr
FROM dwh.dim_product p
JOIN dwh.dim_category cat ON p.category_key = cat.category_key
LEFT JOIN dwh.fact_sales fs ON p.product_key = fs.product_key
WHERE p.is_current = TRUE
GROUP BY
    p.product_key, p.sku_natural_id, p.product_name, p.brand, p.pack_size,
    p.channel_source, cat.category_name, p.mrp_inr, p.selling_price_inr,
    p.discount_pct, p.avg_rating, p.rating_count, p.availability;

-- 3. Data Mart Halaman 3: Environmental and Air Quality Correlation (+ City AQI Diagnostic)
CREATE OR REPLACE VIEW datamart.vw_environmental_aqi_sales AS
WITH daily_city_sales AS (
    SELECT
        fs.date_key,
        fs.location_key,
        COUNT(*)                                                                AS total_orders,
        SUM(fs.units_sold)                                                      AS total_units_sold,
        SUM(fs.net_revenue_inr)                                                 AS total_net_revenue_inr,
        SUM(CASE WHEN c.category_name = 'Vitamin Supplement' THEN fs.units_sold ELSE 0 END) AS vitamin_units_sold,
        SUM(CASE WHEN c.category_name = 'Vitamin Supplement' THEN fs.net_revenue_inr ELSE 0 END) AS vitamin_net_revenue_inr
    FROM dwh.fact_sales fs
    JOIN dwh.dim_category c ON fs.category_key = c.category_key
    GROUP BY fs.date_key, fs.location_key
)
SELECT
    aqi.aqi_key,
    d.date_key,
    d.full_date,
    d.year_num,
    d.quarter_label,
    d.month_num,
    d.month_name,
    d.season_india,
    loc.city,
    loc.state,
    loc.region,
    loc.latitude,
    loc.longitude,
    cat.category_name                           AS triggered_supplement_category,
    aqi.avg_us_aqi,
    aqi.max_us_aqi,
    aqi.avg_pm25_ugm3,
    aqi.avg_pm10_ugm3,
    aqi.avg_no2_ugm3,
    aqi.avg_o3_ugm3,
    aqi.avg_temp_c,
    aqi.avg_humidity_pct,
    aqi.dominant_aqi_category,
    aqi.is_festival_period,
    aqi.is_crop_burning_season,
    COALESCE(dcs.total_orders, 0)               AS daily_orders,
    COALESCE(dcs.total_units_sold, 0)           AS daily_units_sold,
    COALESCE(dcs.total_net_revenue_inr, 0.00)   AS daily_net_revenue_inr,
    COALESCE(dcs.vitamin_units_sold, 0)         AS daily_vitamin_units_sold,
    COALESCE(dcs.vitamin_net_revenue_inr, 0.00) AS daily_vitamin_revenue_inr
FROM dwh.fact_environmental_aqi aqi
JOIN dwh.dim_date     d   ON aqi.date_key     = d.date_key
JOIN dwh.dim_location loc ON aqi.location_key = loc.location_key
JOIN dwh.dim_category cat ON aqi.category_key = cat.category_key
LEFT JOIN daily_city_sales dcs
       ON aqi.date_key = dcs.date_key AND aqi.location_key = dcs.location_key;

-- 4A. Data Mart Halaman 4 (Segmen Kebugaran): Fitness Demand Segmentation (80.000 Profil Gym)
CREATE OR REPLACE VIEW datamart.vw_fitness_demand_segmentation AS
SELECT
    ff.fitness_key,
    d.full_date             AS snapshot_date,
    up.gender,
    up.bmi_category,
    up.fitness_goal,
    up.exercise_schedule,
    up.meal_plan,
    cat.category_name       AS recommended_supplement_category,
    cat.health_focus,
    ff.member_count,
    ff.demand_share_pct,
    ff.demand_intensity_score
FROM dwh.fact_fitness_demand ff
JOIN dwh.dim_date         d   ON ff.date_key         = d.date_key
JOIN dwh.dim_user_profile up  ON ff.user_profile_key = up.user_profile_key
JOIN dwh.dim_category     cat ON ff.category_key     = cat.category_key;

-- 4B. Data Mart Halaman 4 (Segmen Gaya Hidup): Sleep Health & Stress Lifestyle (374 Observasi)
CREATE OR REPLACE VIEW datamart.vw_sleep_stress_lifestyle AS
SELECT
    sl.sleep_key,
    sl.person_id,
    d.full_date             AS observation_date,
    d.year_num,
    loc.city,
    loc.region,
    up.gender,
    up.age_group,
    up.bmi_category,
    up.occupation,
    up.fitness_goal         AS wellness_segment,
    sl.age,
    sl.sleep_duration_hrs,
    sl.quality_of_sleep,
    sl.physical_activity_level,
    sl.stress_level,
    sl.systolic_bp,
    sl.diastolic_bp,
    sl.heart_rate_bpm,
    sl.daily_steps,
    sl.sleep_disorder
FROM dwh.fact_lifestyle_sleep_health sl
JOIN dwh.dim_date         d   ON sl.date_key         = d.date_key
JOIN dwh.dim_location     loc ON sl.location_key     = loc.location_key
JOIN dwh.dim_user_profile up  ON sl.user_profile_key = up.user_profile_key;

-- Terapkan ulang izin RBAC Read-Only pada seluruh Data Mart Views untuk peran bisnis
GRANT SELECT ON ALL TABLES IN SCHEMA datamart
    TO role_dba, role_data_engineer, role_bi_analyst,
       role_store_manager, role_inventory_specialist, role_executive;
