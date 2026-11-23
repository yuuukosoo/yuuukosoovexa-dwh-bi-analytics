"""
Tahap 6B - Disaster Recovery Restore Utility (Verifikasi SHA-256 + psql Restore)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Cara pakai:
  python backup/pg_restore.py                    (otomatis pilih backup terbaru di manifest)
  python backup/pg_restore.py <nama_file.sql.gz> (pulihkan dari file backup tertentu)
"""

import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backup"
sys.path.insert(0, str(BASE_DIR / "etl"))

from db_utils import get_logger  # noqa: E402

load_dotenv(BASE_DIR / ".env")
logger = get_logger("backup.pg_restore")

CONTAINER_NAME = "yuuukosoovexa_postgres"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_restore(target_filename: str | None = None):
    manifest_path = BACKUP_DIR / "backup_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError("backup_manifest.json tidak ditemukan. Jalankan pg_backup.py terlebih dahulu.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not manifest.get("backups"):
        raise ValueError("Daftar backup di manifest masih kosong.")

    if target_filename:
        matched = [b for b in manifest["backups"] if b["filename"] == target_filename]
        if not matched:
            raise ValueError(f"File {target_filename} tidak terdaftar di backup_manifest.json.")
        entry = matched[0]
    else:
        entry = manifest["backups"][0]

    backup_path = BACKUP_DIR / entry["filename"]
    if not backup_path.exists():
        raise FileNotFoundError(f"File backup fisik tidak ditemukan: {backup_path}")

    # 1. Verifikasi integritas SHA-256 sebelum restore
    actual_sha = compute_sha256(backup_path)
    expected_sha = entry["sha256_checksum"]
    if actual_sha != expected_sha:
        msg = f"SHA-256 MISMATCH! Expected={expected_sha}, Actual={actual_sha}. Restore dibatalkan demi keamanan."
        logger.error(msg)
        raise RuntimeError(msg)
    logger.info("SHA-256 Checksum VERIFIED for %s", entry["filename"])

    # 2. Decompress dan jalankan restore ke PostgreSQL via psql
    db_name = os.getenv("POSTGRES_DB", "yuuukosoovexa_dwh")
    db_user = os.getenv("POSTGRES_USER", "dwh_admin")
    db_pass = os.getenv("POSTGRES_PASSWORD", "")

    t0 = time.time()
    with gzip.open(backup_path, "rb") as gz_in:
        sql_bytes = gz_in.read()

    cmd = [
        "docker", "exec", "-i",
        "-e", f"PGPASSWORD={db_pass}",
        CONTAINER_NAME,
        "psql", "-v", "ON_ERROR_STOP=1",
        "-U", db_user,
        "-d", db_name,
    ]
    subprocess.run(cmd, input=sql_bytes, capture_output=True, check=True)
    dur = round(time.time() - t0, 2)
    logger.info("RESTORE COMPLETED in %ss from %s", dur, entry["filename"])
    print(f"[SUCCESS] Database {db_name} berhasil dipulihkan dari {entry['filename']} dalam {dur} detik.")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_restore(arg)
