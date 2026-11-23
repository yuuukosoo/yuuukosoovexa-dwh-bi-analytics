"""
Shared Database, Logging, and Audit Trail Utilities
PT YuuukosooVexa Business Intelligence & Data Warehouse Project
"""

import io
import logging
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
LOG_DIR = BASE_DIR / "logs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")


def get_logger(name: str = "yuuukosoovexa_etl") -> logging.Logger:
    """Configure centralized file + console logger writing to logs/etl_pipeline.log."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(LOG_DIR / "etl_pipeline.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


def get_pg_connection():
    """Create PostgreSQL connection using isolated .env credentials."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "yuuukosoovexa_dwh"),
        user=os.getenv("POSTGRES_USER", "dwh_admin"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def copy_dataframe_to_pg(conn, df, full_table_name: str, columns: list[str], chunk_size: int = 100_000):
    """High-speed PostgreSQL COPY bulk loader in chunks."""
    col_sql = ", ".join(columns)
    copy_sql = f"COPY {full_table_name} ({col_sql}) FROM STDIN WITH (FORMAT CSV, NULL '')"
    total_rows = len(df)
    with conn.cursor() as cur:
        for start in range(0, total_rows, chunk_size):
            chunk = df.iloc[start : start + chunk_size][columns]
            buf = io.StringIO()
            chunk.to_csv(buf, index=False, header=False, na_rep="")
            buf.seek(0)
            cur.copy_expert(copy_sql, buf)


def record_audit(
    conn,
    run_id: str,
    stage_name: str,
    table_target: str,
    rows_input: int,
    rows_loaded: int,
    rows_rejected: int,
    status: str,
    duration_seconds: float,
    message: str = "",
):
    """Insert an audit trail entry into dwh.etl_audit_log."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dwh.etl_audit_log (
                pipeline_run_id, stage_name, table_target,
                rows_input, rows_loaded, rows_rejected,
                status, duration_seconds, message
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                run_id,
                stage_name,
                table_target,
                int(rows_input),
                int(rows_loaded),
                int(rows_rejected),
                status,
                round(float(duration_seconds), 2),
                message,
            ),
        )
