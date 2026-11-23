"""
Tahap 3 - Data Profiling (Read-Only Audit Sebelum Preprocessing)
PT YuuukosooVexa Business Intelligence & Data Warehouse Project

Memindai seluruh 5 dataset mentah pada folder data/raw/ tanpa mengubah isi file,
lalu mencatat jumlah baris, kolom, tipe data, missing values, duplikat, encoding,
serta sampel data ke logs/raw_data_profile.json untuk dokumentasi Subbab 3.2.
"""

import json
import os
import time
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILES = [
    ("Flipkart Health Supplements", "Health_Suppliments_Flipkart_02_04_2022.csv"),
    ("Tata 1mg Healthcare Catalog", "1mgData.csv"),
    ("India Air Quality Index (AQI)", "INDIA_AQI_COMPLETE_20251126.csv"),
    ("Gym & Fitness Demand Profile", "GYM.csv"),
    ("Sleep Health & Lifestyle", "Sleep_health_and_lifestyle_dataset.csv"),
]


def detect_delimiter(filepath: Path, encoding: str) -> str:
    """Detect whether the CSV file uses ';' or ',' delimiter from its header line."""
    with open(filepath, "r", encoding=encoding, errors="replace") as f:
        header = f.readline()
    return ";" if header.count(";") > header.count(",") else ","


def read_csv_with_codec_fallback(filepath: Path):
    """Attempt reading CSV with UTF-8 first, falling back to latin-1, with auto delimiter detection."""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            delim = detect_delimiter(filepath, enc)
            df = pd.read_csv(filepath, sep=delim, encoding=enc, low_memory=False)
            return df, enc, delim
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Failed to decode {filepath.name} with supported encodings.")


def profile_all_datasets():
    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_files": len(RAW_FILES),
        "total_raw_rows": 0,
        "datasets": [],
    }

    print("=" * 80)
    print("DATA PROFILING REPORT - BEFORE PREPROCESSING (PT YUUUKOSOOVEXA)")
    print("=" * 80)

    for label, filename in RAW_FILES:
        fpath = RAW_DIR / filename
        if not fpath.exists():
            print(f"[ERROR] File not found: {fpath}")
            continue

        t0 = time.time()
        size_mb = round(os.path.getsize(fpath) / (1024 * 1024), 2)
        df, encoding_used, delim_used = read_csv_with_codec_fallback(fpath)
        elapsed = round(time.time() - t0, 2)

        row_count, col_count = df.shape
        dup_count = int(df.duplicated().sum())
        total_nulls = int(df.isna().sum().sum())

        col_details = []
        for col in df.columns:
            null_cnt = int(df[col].isna().sum())
            null_pct = round((null_cnt / row_count) * 100, 2) if row_count else 0.0
            non_null_sample = df[col].dropna().head(2).astype(str).tolist()
            col_details.append({
                "column": str(col),
                "dtype": str(df[col].dtype),
                "null_count": null_cnt,
                "null_pct": null_pct,
                "nunique": int(df[col].nunique(dropna=True)),
                "sample_values": [s[:60] for s in non_null_sample],
            })

        ds_info = {
            "label": label,
            "filename": filename,
            "size_mb": size_mb,
            "encoding": encoding_used,
            "delimiter": delim_used,
            "rows": int(row_count),
            "columns": int(col_count),
            "duplicate_rows": dup_count,
            "total_missing_cells": total_nulls,
            "read_seconds": elapsed,
            "column_details": col_details,
        }
        summary["datasets"].append(ds_info)
        summary["total_raw_rows"] += int(row_count)

        print(f"\n[{label}] -> {filename}")
        print(f"  Size: {size_mb} MB | Encoding: {encoding_used} | Delimiter: '{delim_used}' | Read: {elapsed}s")
        print(f"  Rows: {row_count:,} | Columns: {col_count} | Duplicates: {dup_count:,} | Total Null Cells: {total_nulls:,}")
        print("  Columns & Top Nulls:")
        for cd in col_details:
            print(
                f"    - {cd['column']:32s} | dtype={cd['dtype']:10s} | "
                f"null={cd['null_count']:>7,} ({cd['null_pct']:>5.1f}%) | "
                f"uniq={cd['nunique']:>7,} | sample={cd['sample_values'][:1]}"
            )

    out_path = LOG_DIR / "raw_data_profile.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"TOTAL RAW ROWS ACROSS 5 FILES: {summary['total_raw_rows']:,}")
    print(f"Profile JSON saved to: {out_path}")
    print("=" * 80)


if __name__ == "__main__":
    profile_all_datasets()
