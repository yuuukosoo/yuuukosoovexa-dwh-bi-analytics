-- =============================================================================
-- Tahap 4 (Langkah 4) - Implementasi Role-Based Access Control (RBAC)
-- Prinsip Least Privilege selaras dengan Tabel 2.15 Subbab 2.9 Laporan UAS
-- =============================================================================

-- 1. Membuat 6 peran keamanan (idempotent - aman dijalankan ulang)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_dba') THEN
        CREATE ROLE role_dba NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_data_engineer') THEN
        CREATE ROLE role_data_engineer NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_bi_analyst') THEN
        CREATE ROLE role_bi_analyst NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_store_manager') THEN
        CREATE ROLE role_store_manager NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_inventory_specialist') THEN
        CREATE ROLE role_inventory_specialist NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'role_executive') THEN
        CREATE ROLE role_executive NOLOGIN;
    END IF;
END
$$;

-- 2. Cabut seluruh izin default dari PUBLIC demi keamanan Least Privilege
REVOKE ALL ON SCHEMA staging, dwh, datamart FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA staging, dwh, datamart FROM PUBLIC;

-- 3. Hak Akses role_dba (Full Control pada seluruh skema)
GRANT ALL PRIVILEGES ON SCHEMA staging, dwh, datamart TO role_dba;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging, dwh, datamart TO role_dba;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA staging, dwh, datamart TO role_dba;

-- 4. Hak Akses role_data_engineer (Full Control Staging; Read/Write DWH & Data Mart)
GRANT ALL PRIVILEGES ON SCHEMA staging TO role_data_engineer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO role_data_engineer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA staging TO role_data_engineer;

GRANT USAGE ON SCHEMA dwh, datamart TO role_data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dwh, datamart TO role_data_engineer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA dwh, datamart TO role_data_engineer;

-- 5. Hak Akses role_bi_analyst (Read-Only Staging & DWH; Read/Write Data Mart)
GRANT USAGE ON SCHEMA staging, dwh TO role_bi_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA staging, dwh TO role_bi_analyst;

GRANT USAGE, CREATE ON SCHEMA datamart TO role_bi_analyst;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA datamart TO role_bi_analyst;

-- 6. Hak Akses Pengguna Bisnis (Store Manager, Inventory Specialist, Executive)
-- HANYA boleh Read-Only pada Data Mart (No Access ke Staging & Core DWH)
GRANT USAGE ON SCHEMA datamart TO role_store_manager, role_inventory_specialist, role_executive;
GRANT SELECT ON ALL TABLES IN SCHEMA datamart TO role_store_manager, role_inventory_specialist, role_executive;

-- Pastikan view/tabel baru di skema datamart di masa depan otomatis terbaca oleh peran bisnis
ALTER DEFAULT PRIVILEGES IN SCHEMA datamart
    GRANT SELECT ON TABLES TO role_store_manager, role_inventory_specialist, role_executive, role_bi_analyst;
