-- =============================================================================
-- Tahap 7 - Kueri Validasi & Rekonsiliasi Data (Source -> Staging -> DWH -> Data Mart)
-- Proyek: Data Warehouse & BI Dashboard PT YuuukosooVexa
-- Dapat dijalankan langsung di pgAdmin Query Tool maupun oleh etl/05_validate_dwh.py
-- =============================================================================

-- 1. REKONSILIASI JUMLAH BARIS (STAGING vs CORE DWH vs DATA MART)
SELECT 'Staging: Flipkart Raw'               AS layer_table, COUNT(*) AS row_count FROM staging.stg_flipkart_raw
UNION ALL
SELECT 'Staging: Tata 1mg Raw'               AS layer_table, COUNT(*) AS row_count FROM staging.stg_tata1mg_raw
UNION ALL
SELECT 'Staging: India AQI Hourly Raw'       AS layer_table, COUNT(*) AS row_count FROM staging.stg_aqi_hourly_raw
UNION ALL
SELECT 'Staging: Gym Profile Raw'            AS layer_table, COUNT(*) AS row_count FROM staging.stg_gym_profile_raw
UNION ALL
SELECT 'Staging: Sleep Stress Raw'           AS layer_table, COUNT(*) AS row_count FROM staging.stg_sleep_stress_raw
UNION ALL
SELECT 'DWH Dim: dim_product (Unique SKU)'   AS layer_table, COUNT(*) AS row_count FROM dwh.dim_product
UNION ALL
SELECT 'DWH Fact: fact_sales'                AS layer_table, COUNT(*) AS row_count FROM dwh.fact_sales
UNION ALL
SELECT 'DWH Fact: fact_environmental_aqi'    AS layer_table, COUNT(*) AS row_count FROM dwh.fact_environmental_aqi
UNION ALL
SELECT 'DWH Fact: fact_fitness_demand'       AS layer_table, COUNT(*) AS row_count FROM dwh.fact_fitness_demand
UNION ALL
SELECT 'DWH Fact: fact_lifestyle_sleep'      AS layer_table, COUNT(*) AS row_count FROM dwh.fact_lifestyle_sleep_health
UNION ALL
SELECT 'DataMart: vw_executive_sales'        AS layer_table, COUNT(*) AS row_count FROM datamart.vw_executive_sales
UNION ALL
SELECT 'DataMart: vw_sales_pricing_sku'      AS layer_table, COUNT(*) AS row_count FROM datamart.vw_sales_pricing_sku
UNION ALL
SELECT 'DataMart: vw_environmental_aqi_sales' AS layer_table, COUNT(*) AS row_count FROM datamart.vw_environmental_aqi_sales
UNION ALL
SELECT 'DataMart: vw_fitness_demand_seg'     AS layer_table, COUNT(*) AS row_count FROM datamart.vw_fitness_demand_segmentation
UNION ALL
SELECT 'DataMart: vw_sleep_stress_lifestyle' AS layer_table, COUNT(*) AS row_count FROM datamart.vw_sleep_stress_lifestyle;

-- 2. REKONSILIASI AGREGAT FINANSIAL & METRIK (CORE DWH vs DATA MART - HARUS SELISIH 0.00)
SELECT
    'Sales Net Revenue (INR)' AS metric_name,
    (SELECT ROUND(SUM(net_revenue_inr), 2) FROM dwh.fact_sales) AS dwh_value,
    (SELECT ROUND(SUM(net_revenue_inr), 2) FROM datamart.vw_executive_sales) AS datamart_value,
    (SELECT ROUND(SUM(net_revenue_inr), 2) FROM dwh.fact_sales)
      - (SELECT ROUND(SUM(net_revenue_inr), 2) FROM datamart.vw_executive_sales) AS diff_value
UNION ALL
SELECT
    'Sales Units Sold' AS metric_name,
    (SELECT SUM(units_sold)::numeric FROM dwh.fact_sales),
    (SELECT SUM(units_sold)::numeric FROM datamart.vw_executive_sales),
    (SELECT SUM(units_sold)::numeric FROM dwh.fact_sales)
      - (SELECT SUM(units_sold)::numeric FROM datamart.vw_executive_sales)
UNION ALL
SELECT
    'SKU DataMart Net Revenue (INR)' AS metric_name,
    (SELECT ROUND(SUM(net_revenue_inr), 2) FROM dwh.fact_sales),
    (SELECT ROUND(SUM(total_net_revenue_inr), 2) FROM datamart.vw_sales_pricing_sku),
    (SELECT ROUND(SUM(net_revenue_inr), 2) FROM dwh.fact_sales)
      - (SELECT ROUND(SUM(total_net_revenue_inr), 2) FROM datamart.vw_sales_pricing_sku)
UNION ALL
SELECT
    'Total Gym Members Represented' AS metric_name,
    (SELECT COUNT(*)::numeric FROM staging.stg_gym_profile_raw),
    (SELECT SUM(member_count)::numeric FROM datamart.vw_fitness_demand_segmentation),
    (SELECT COUNT(*)::numeric FROM staging.stg_gym_profile_raw)
      - (SELECT SUM(member_count)::numeric FROM datamart.vw_fitness_demand_segmentation)
UNION ALL
SELECT
    'Average Daily US_AQI' AS metric_name,
    (SELECT ROUND(AVG(avg_us_aqi), 4) FROM dwh.fact_environmental_aqi),
    (SELECT ROUND(AVG(avg_us_aqi), 4) FROM datamart.vw_environmental_aqi_sales),
    (SELECT ROUND(AVG(avg_us_aqi), 4) FROM dwh.fact_environmental_aqi)
      - (SELECT ROUND(AVG(avg_us_aqi), 4) FROM datamart.vw_environmental_aqi_sales);

-- 3. UJI INTEGRITAS REFERENSIAL (ZERO ORPHAN FOREIGN KEYS)
SELECT 'Orphan fact_sales -> dim_product' AS integrity_check,
       COUNT(*) AS invalid_rows
FROM dwh.fact_sales f LEFT JOIN dwh.dim_product d ON f.product_key = d.product_key
WHERE d.product_key IS NULL
UNION ALL
SELECT 'Orphan fact_sales -> dim_date', COUNT(*)
FROM dwh.fact_sales f LEFT JOIN dwh.dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL
UNION ALL
SELECT 'Orphan fact_environmental_aqi -> dim_location', COUNT(*)
FROM dwh.fact_environmental_aqi f LEFT JOIN dwh.dim_location d ON f.location_key = d.location_key
WHERE d.location_key IS NULL
UNION ALL
SELECT 'Orphan fact_fitness_demand -> dim_user_profile', COUNT(*)
FROM dwh.fact_fitness_demand f LEFT JOIN dwh.dim_user_profile d ON f.user_profile_key = d.user_profile_key
WHERE d.user_profile_key IS NULL
UNION ALL
SELECT 'Orphan fact_lifestyle_sleep -> dim_user_profile', COUNT(*)
FROM dwh.fact_lifestyle_sleep_health f LEFT JOIN dwh.dim_user_profile d ON f.user_profile_key = d.user_profile_key
WHERE d.user_profile_key IS NULL;

-- 4. UJI ATURAN MUTU DATA (DATA QUALITY & BUSINESS RULES)
SELECT 'Invalid selling_price <= 0 in dim_product' AS quality_rule,
       COUNT(*) AS violations FROM dwh.dim_product WHERE selling_price_inr <= 0
UNION ALL
SELECT 'Inverted price (selling_price > mrp) in dim_product',
       COUNT(*) FROM dwh.dim_product WHERE selling_price_inr > mrp_inr
UNION ALL
SELECT 'Null sleep_disorder in fact_lifestyle_sleep_health',
       COUNT(*) FROM dwh.fact_lifestyle_sleep_health WHERE sleep_disorder IS NULL OR TRIM(sleep_disorder) = ''
UNION ALL
SELECT 'Unlabeled simulated rows in fact_sales',
       COUNT(*) FROM dwh.fact_sales WHERE is_simulated_enrichment IS DISTINCT FROM TRUE;

-- 5. UJI KEAMANAN RBAC (LEAST PRIVILEGE VERIFICATION)
SELECT
    rolname,
    has_schema_privilege(rolname, 'staging', 'USAGE')  AS can_access_staging,
    has_schema_privilege(rolname, 'dwh', 'USAGE')      AS can_access_dwh,
    has_schema_privilege(rolname, 'datamart', 'USAGE') AS can_access_datamart,
    has_table_privilege(rolname, 'datamart.vw_executive_sales', 'SELECT') AS can_select_datamart
FROM pg_roles
WHERE rolname IN (
    'role_dba', 'role_data_engineer', 'role_bi_analyst',
    'role_store_manager', 'role_inventory_specialist', 'role_executive'
)
ORDER BY rolname;
