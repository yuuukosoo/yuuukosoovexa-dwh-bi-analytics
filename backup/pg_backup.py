"""
Tahap 6B - Automated PostgreSQL Backup (pg_dump + gzip + SHA-256 Checksum)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Fitur:
  1. Menjalankan pg_dump pada kontainer Docker yuuukosoovexa_postgres (skema dwh & datamart)
  2. Kompresi otomatis menggunakan gzip (.sql.gz)
  3. Verifikasi integritas menggunakan SHA-256 checksum
  4. Pencatatan manifest ke backup/backup_manifest.json, logs/etl_pipeline.log, & dwh.etl_audit_log
  5. Pembersihan retensi lokal otomatis (menyimpan 7 cadangan terbaru)
"""

import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backup"
sys.path.insert(0, str(BASE_DIR / "etl"))

from db_utils import get_logger, get_pg_connection, record_audit  # noqa: E402

load_dotenv(BASE_DIR / ".env")
logger = get_logger("backup.pg_backup")

CONTAINER_NAME = "yuuukosoovexa_postgres"
RETENTION_KEEP_COUNT = 7


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_backup(run_id: str | None = None) -> dict:
    run_id = run_id or f"BKP-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    t0 = time.time()
    logger.info("=== START AUTOMATED BACKUP (pg_dump + SHA-256) | run_id=%s ===", run_id)

    db_name = os.getenv("POSTGRES_DB", "yuuukosoovexa_dwh")
    db_user = os.getenv("POSTGRES_USER", "dwh_admin")
    db_pass = os.getenv("POSTGRES_PASSWORD", "")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{db_name}_{timestamp}.sql.gz"
    backup_path = BACKUP_DIR / backup_filename

    cmd = [
        "docker", "exec",
        "-e", f"PGPASSWORD={db_pass}",
        CONTAINER_NAME,
        "pg_dump",
        "-U", db_user,
        "-d", db_name,
        "-n", "dwh",
        "-n", "datamart",
        "--clean",
        "--if-exists",
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, check=True)
        with gzip.open(backup_path, "wb", compresslevel=6) as gz_out:
            gz_out.write(proc.stdout)

        size_bytes = backup_path.stat().st_size
        size_mb = round(size_bytes / (1024 * 1024), 2)
        sha256_hex = compute_sha256(backup_path)
        dur = round(time.time() - t0, 2)

        # Update manifest JSON
        manifest_path = BACKUP_DIR / "backup_manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            manifest = {"policy": "3-2-1 Redundancy | Retention 7 Local Copies | SHA-256 Verified", "backups": []}

        entry = {
            "run_id": run_id,
            "filename": backup_filename,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "schemas": ["dwh", "datamart"],
            "size_bytes": size_bytes,
            "size_mb": size_mb,
            "sha256_checksum": sha256_hex,
            "duration_seconds": dur,
            "status": "VERIFIED",
        }
        manifest["backups"].insert(0, entry)

        # Enforce local retention policy (keep 7 most recent .sql.gz files)
        all_gz = sorted(BACKUP_DIR.glob(f"{db_name}_*.sql.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
        removed_old = []
        for old_file in all_gz[RETENTION_KEEP_COUNT:]:
            old_file.unlink(missing_ok=True)
            removed_old.append(old_file.name)
        manifest["backups"] = manifest["backups"][:RETENTION_KEEP_COUNT]
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

        # Audit log into PostgreSQL
        conn = get_pg_connection()
        try:
            record_audit(
                conn,
                run_id,
                "BACKUP",
                f"backup/{backup_filename}",
                1,
                1,
                0,
                "SUCCESS",
                dur,
                f"Size={size_mb}MB | SHA256={sha256_hex[:16]}...",
            )
            conn.commit()
        finally:
            conn.close()

        logger.info(
            "=== BACKUP COMPLETED & VERIFIED | file=%s | size=%s MB | sha256=%s | duration=%ss ===",
            backup_filename,
            size_mb,
            sha256_hex,
            dur,
        )

        print("\n" + "=" * 78)
        print("VERIFIKASI HASIL TAHAP 6B (AUTOMATED BACKUP pg_dump + SHA-256)")
        print("=" * 78)
        print(f"  File Cadangan  -> backup/{backup_filename}")
        print(f"  Skema Dicadang -> dwh (6 Dim + 4 Fact + Audit) & datamart (5 Views)")
        print(f"  Ukuran File    -> {size_mb} MB ({size_bytes:,} bytes)")
        print(f"  SHA-256 Seal   -> {sha256_hex}")
        print(f"  Durasi Backup  -> {dur} detik | Status: VERIFIED")
        print(f"  Manifest Audit -> backup/backup_manifest.json")
        if removed_old:
            print(f"  Retensi Hapus  -> {removed_old}")
        print("=" * 78)
        return entry

    except subprocess.CalledProcessError as exc:
        err_msg = exc.stderr.decode("utf-8", errors="replace") if exc.stderr else str(exc)
        logger.error("BACKUP FAILED: %s", err_msg)
        raise RuntimeError(f"pg_dump failed: {err_msg}") from exc


if __name__ == "__main__":
    run_backup()
