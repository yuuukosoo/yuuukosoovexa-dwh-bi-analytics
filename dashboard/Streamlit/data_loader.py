"""
Data Loader Layer (Live PostgreSQL 16 Data Marts with Cloud Snapshot Fallback)
PT YuuukosooVexa Business Intelligence Dashboard (Streamlit + Plotly)
"""

import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
load_dotenv(ROOT_DIR / ".env")


def _get_sqlalchemy_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "yuuukosoovexa_dwh")
    user = os.getenv("POSTGRES_USER", "dwh_admin")
    pwd = os.getenv("POSTGRES_PASSWORD", "")
    if not pwd:
        return None
    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 3})


@st.cache_data(ttl=300, show_spinner=False)
def load_all_datamarts() -> tuple[dict[str, pd.DataFrame], str]:
    """
    Attempt live PostgreSQL Data Mart queries first (datamart.vw_*).
    Falls back cleanly to data/processed/*.csv if running on Streamlit Cloud without Docker.
    """
    engine = _get_sqlalchemy_engine()
    if engine is not None:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
                data = {
                    "executive_sales": pd.read_sql("SELECT * FROM datamart.vw_executive_sales;", conn),
                    "sales_pricing_sku": pd.read_sql("SELECT * FROM datamart.vw_sales_pricing_sku;", conn),
                    "environmental_aqi_sales": pd.read_sql("SELECT * FROM datamart.vw_environmental_aqi_sales;", conn),
                    "fitness_demand": pd.read_sql("SELECT * FROM datamart.vw_fitness_demand_segmentation;", conn),
                    "sleep_lifestyle": pd.read_sql("SELECT * FROM datamart.vw_sleep_stress_lifestyle;", conn),
                }
            data["executive_sales"]["full_date"] = pd.to_datetime(data["executive_sales"]["full_date"])
            data["environmental_aqi_sales"]["full_date"] = pd.to_datetime(data["environmental_aqi_sales"]["full_date"])
            return data, "PostgreSQL DWH Live"
        except Exception:
            pass

    # Seamless Cloud / Offline Fallback reconstructing identical 5 Data Marts from data/processed/
    dim_date = pd.read_csv(PROCESSED_DIR / "dim_date.csv")
    dim_loc = pd.read_csv(PROCESSED_DIR / "dim_location.csv")
    dim_cat = pd.read_csv(PROCESSED_DIR / "dim_category.csv")
    dim_ch = pd.read_csv(PROCESSED_DIR / "dim_channel.csv")
    dim_prod = pd.read_csv(PROCESSED_DIR / "dim_product.csv")
    dim_up = pd.read_csv(PROCESSED_DIR / "dim_user_profile.csv")
    f_sales = pd.read_csv(PROCESSED_DIR / "fact_sales.csv")
    f_aqi = pd.read_csv(PROCESSED_DIR / "fact_environmental_aqi.csv")
    f_fit = pd.read_csv(PROCESSED_DIR / "fact_fitness_demand.csv")
    f_slp = pd.read_csv(PROCESSED_DIR / "fact_lifestyle_sleep_health.csv")
    f_slp["sleep_disorder"] = f_slp["sleep_disorder"].fillna("None")

    vw_exec = (
        f_sales.merge(dim_date, on="date_key")
        .merge(dim_ch, on="channel_key")
        .merge(dim_cat, on="category_key")
        .merge(dim_loc, on="location_key")
    )
    vw_exec["full_date"] = pd.to_datetime(vw_exec["full_date"])

    sku_agg = (
        f_sales.groupby("product_key", as_index=False)
        .agg(
            total_transactions=("transaction_id", "count"),
            total_units_sold=("units_sold", "sum"),
            total_gross_revenue_inr=("gross_revenue_inr", "sum"),
            total_net_revenue_inr=("net_revenue_inr", "sum"),
            total_discount_given_inr=("discount_amount_inr", "sum"),
        )
    )
    vw_sku = dim_prod.merge(dim_cat[["category_key", "category_name"]], on="category_key").merge(
        sku_agg, on="product_key", how="left"
    )
    for col in ["total_transactions", "total_units_sold", "total_gross_revenue_inr", "total_net_revenue_inr", "total_discount_given_inr"]:
        vw_sku[col] = vw_sku[col].fillna(0)
    vw_sku["discount_tier"] = pd.cut(
        vw_sku["discount_pct"],
        bins=[-0.01, 0.0, 15.0, 30.0, 50.0, 100.0],
        labels=[
            "0% (No Discount)",
            "1-15% (Low Discount)",
            "16-30% (Moderate Discount)",
            "31-50% (High Discount)",
            ">50% (Aggressive Discount)",
        ],
    ).astype(str)

    sales_cat = f_sales.merge(dim_cat[["category_key", "category_name"]], on="category_key")
    sales_cat["vit_units"] = sales_cat["units_sold"].where(sales_cat["category_name"] == "Vitamin Supplement", 0)
    sales_cat["vit_rev"] = sales_cat["net_revenue_inr"].where(sales_cat["category_name"] == "Vitamin Supplement", 0.0)
    daily_city = sales_cat.groupby(["date_key", "location_key"], as_index=False).agg(
        daily_orders=("transaction_id", "count"),
        daily_units_sold=("units_sold", "sum"),
        daily_net_revenue_inr=("net_revenue_inr", "sum"),
        daily_vitamin_units_sold=("vit_units", "sum"),
        daily_vitamin_revenue_inr=("vit_rev", "sum"),
    )
    vw_aqi = (
        f_aqi.merge(dim_date, on="date_key")
        .merge(dim_loc, on="location_key")
        .merge(dim_cat[["category_key", "category_name"]].rename(columns={"category_name": "triggered_supplement_category"}), on="category_key")
        .merge(daily_city, on=["date_key", "location_key"], how="left")
    )
    for col in ["daily_orders", "daily_units_sold", "daily_net_revenue_inr", "daily_vitamin_units_sold", "daily_vitamin_revenue_inr"]:
        vw_aqi[col] = vw_aqi[col].fillna(0)
    vw_aqi["full_date"] = pd.to_datetime(vw_aqi["full_date"])

    vw_fit = (
        f_fit.merge(dim_date[["date_key", "full_date"]].rename(columns={"full_date": "snapshot_date"}), on="date_key")
        .merge(dim_up, on="user_profile_key")
        .merge(dim_cat[["category_key", "category_name", "health_focus"]].rename(columns={"category_name": "recommended_supplement_category"}), on="category_key")
    )

    vw_slp = (
        f_slp.merge(dim_date[["date_key", "full_date", "year_num"]].rename(columns={"full_date": "observation_date"}), on="date_key")
        .merge(dim_loc[["location_key", "city", "region"]], on="location_key")
        .merge(dim_up[["user_profile_key", "gender", "age_group", "bmi_category", "occupation", "fitness_goal"]].rename(columns={"fitness_goal": "wellness_segment"}), on="user_profile_key")
    )

    return {
        "executive_sales": vw_exec,
        "sales_pricing_sku": vw_sku,
        "environmental_aqi_sales": vw_aqi,
        "fitness_demand": vw_fit,
        "sleep_lifestyle": vw_slp,
    }, "Processed DWH Snapshot"
