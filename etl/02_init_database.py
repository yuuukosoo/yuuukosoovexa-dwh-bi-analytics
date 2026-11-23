"""
Tahap 4 - Inisialisasi Skema Database PostgreSQL (Staging, Galaxy Schema, & RBAC)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Menjalankan secara berurutan:
  1. sql/01_create_schemas_and_staging.sql
  2. sql/02_create_dwh_galaxy_schema.sql
  3. sql/03_create_rbac_roles.sql
Lalu memverifikasi seluruh skema, tabel, dan peran RBAC yang terbentuk.
"""

import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"
load_dotenv(BASE_DIR / ".env")

SQL_SCRIPTS = [
    ("Langkah 2 - Skema & 5 Tabel Staging", SQL_DIR / "01_create_schemas_and_staging.sql"),
    ("Langkah 3 - 6 Dimensi & 4 Fakta Galaxy Schema", SQL_DIR / "02_create_dwh_galaxy_schema.sql"),
    ("Langkah 4 - 6 Peran Keamanan RBAC", SQL_DIR / "03_create_rbac_roles.sql"),
]


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "yuuukosoovexa_dwh"),
        user=os.getenv("POSTGRES_USER", "dwh_admin"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def init_database():
    print("=" * 78)
    print("TAHAP 4 - INISIALISASI DATABASE POSTGRESQL (PT YUUUKOSOOVEXA)")
    print("=" * 78)

    conn = get_connection()
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            print("[Langkah 1] Koneksi ke database yuuukosoovexa_dwh berhasil dibuka.")
            for step_label, sql_path in SQL_SCRIPTS:
                if not sql_path.exists():
                    raise FileNotFoundError(f"SQL file tidak ditemukan: {sql_path}")
                sql_text = sql_path.read_text(encoding="utf-8")
                cur.execute(sql_text)
                print(f"[{step_label}] SUKSES dieksekusi ({sql_path.name}).")
        conn.commit()

        # Langkah 5: Verifikasi hasil akhir
        print("\n[Langkah 5] Verifikasi Objek yang Terbentuk di PostgreSQL")
        with conn.cursor() as cur:
            cur.execute("""
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name IN ('staging', 'dwh', 'datamart')
                ORDER BY schema_name;
            """)
            schemas = [r[0] for r in cur.fetchall()]
            print(f"  Skema Terbentuk ({len(schemas)}): {', '.join(schemas)}")

            cur.execute("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema IN ('staging', 'dwh', 'datamart')
                  AND table_type = 'BASE TABLE'
                ORDER BY
                    CASE table_schema WHEN 'staging' THEN 1 WHEN 'dwh' THEN 2 ELSE 3 END,
                    table_name;
            """)
            tables = cur.fetchall()
            print(f"\n  Tabel Terbentuk ({len(tables)} total):")
            for sc, tb in tables:
                print(f"    - {sc}.{tb}")

            cur.execute("""
                SELECT rolname
                FROM pg_roles
                WHERE rolname LIKE 'role_%'
                ORDER BY rolname;
            """)
            roles = [r[0] for r in cur.fetchall()]
            print(f"\n  Peran RBAC Terbentuk ({len(roles)}): {', '.join(roles)}")

        print("\n" + "=" * 78)
        print("TAHAP 4 SELESAI 100% - SELURUH STRUKTUR TABEL SIAP DIISI ETL (TAHAP 5)")
        print("=" * 78)

    except Exception as exc:
        conn.rollback()
        print(f"[ERROR] Terjadi kegagalan, transaksi di-rollback: {exc}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
