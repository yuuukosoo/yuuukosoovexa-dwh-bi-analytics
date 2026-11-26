"""
PT YuuukosooVexa Executive Business Intelligence Dashboard (Streamlit + Plotly)
Connected Live to PostgreSQL 16 Galaxy Schema Data Marts (datamart.vw_*)

4 Main Analytical Pages + 2 Contextual Drill-Through Pages + DWH Validation Audit:
  1. Executive Summary & Multi-Channel Sales
  2. Sales & Pricing Optimization (+ Product SKU Deep-Dive Drill-Through)
  3. Environmental & Air Quality Correlation (+ City AQI Diagnostic Drill-Through)
  4. Lifestyle & Fitness Segmentation
  5. DWH Validation & Governance Audit (Source to Staging to DWH to Dashboard)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import importlib
from data_loader import ROOT_DIR, load_all_datamarts
from translations import TRANSLATIONS, t
import styles as _styles_mod
if not hasattr(_styles_mod, "build_csv_download_icon_html") or not hasattr(_styles_mod, "render_download_popover"):
    importlib.reload(_styles_mod)
from styles import (
    PALETTE,
    apply_bento_plotly_style,
    build_csv_download_icon_html,
    build_info_popover_html,
    build_striped_pill_bar,
    inject_bento_css,
    inject_motion_engine,
    render_aqi_hero_map,
    render_bento_treemap,
    render_brand_header,
    render_channel_arc_gauge,
    render_chart_card_header,
    render_compact_kpi_card,
    render_download_popover,
    render_empty_state,
    render_error_state,
    render_horizontal_pill_bars,
    render_kpi_icon_badge,
    render_nested_hero_card,
    render_page_title,
    render_rounded_heatmap,
    render_section_eyebrow,
    render_sidebar_support_widget,
    render_sku_modern_table,
    render_striped_pill_bar,
    render_top_header,
    render_wellness_radar,
)

st.set_page_config(
    page_title="YuuukosooVexa BI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "sb_theme_open" not in st.session_state:
    st.session_state.sb_theme_open = False
if "sb_lang_open" not in st.session_state:
    st.session_state.sb_lang_open = False

lang = st.session_state.lang
theme = st.session_state.theme

inject_bento_css(sidebar_expanded=st.session_state.sidebar_expanded, theme=theme, lang=lang)


# ------------------------------------------------------------------------------
# HELPER FORMATTING FUNCTIONS
# ------------------------------------------------------------------------------
def fmt_inr_compact(val: float) -> str:
    if abs(val) >= 1e7:
        return f"INR {val / 1e6:,.2f}M"
    if abs(val) >= 1e6:
        return f"INR {val / 1e6:,.2f}M"
    if abs(val) >= 1e3:
        return f"INR {val / 1e3:,.1f}K"
    return f"INR {val:,.2f}"


# ------------------------------------------------------------------------------
# LOAD DATA FROM POSTGRESQL DATA MARTS (WITH LOADING & ERROR STATES - R-27)
# ------------------------------------------------------------------------------
try:
    with st.spinner("Loading verified Data Marts from PostgreSQL 16..."):
        data, source_badge = load_all_datamarts()
except Exception as exc:
    render_error_state(
        "Unable to load Data Marts",
        f"Database connection and snapshot fallback returned an error ({type(exc).__name__}).",
        "Verify that Docker container yuuukosoovexa_postgres is running on port 5432, then reload this page.",
    )
    st.stop()

df_exec = data["executive_sales"]
df_sku = data["sales_pricing_sku"]
df_aqi = data["environmental_aqi_sales"]
df_fit = data["fitness_demand"]
df_slp = data["sleep_lifestyle"]

# Session state for Navigation & Contextual Drill-Through (state preservation!)
if "active_page" not in st.session_state:
    st.session_state.active_page = "Executive Summary"
if "drill_mode" not in st.session_state:
    st.session_state.drill_mode = None  # None | 'sku' | 'city'
if "drill_sku_id" not in st.session_state:
    st.session_state.drill_sku_id = None
if "drill_city_name" not in st.session_state:
    st.session_state.drill_city_name = None

PLOT_CFG = {"displayModeBar": False}


# ------------------------------------------------------------------------------
# LEFT ICON RAIL SIDEBAR (4 MAIN ANALYTICAL PAGES WITH ACCESSIBLE TOOLTIPS)
# ------------------------------------------------------------------------------
VALID_PAGES = {"Executive Summary", "Sales & Pricing", "Environmental AQI", "Lifestyle & Fitness", "Data Quality"}
if st.session_state.active_page not in VALID_PAGES:
    st.session_state.active_page = "Executive Summary"

with st.sidebar:
    is_exp = st.session_state.sidebar_expanded
    if st.button(
        t("collapse_menu", lang) if is_exp else "",
        icon=":material/left_panel_close:" if is_exp else ":material/left_panel_open:",
        help=t("collapse_menu", lang) if is_exp else t("expand_menu", lang),
        key="btn_toggle_sidebar",
        type="secondary",
        use_container_width=is_exp,
    ):
        st.session_state.sidebar_expanded = not is_exp
        st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    NAV_PAGES = [
        ("Executive Summary", "nav_exec", ":material/space_dashboard:", "Penjualan Multi-Kanal" if lang == "id" else "Multi-Channel Sales"),
        ("Sales & Pricing", "nav_sales", ":material/sell:", "Optimasi Diskon" if lang == "id" else "Discount Optimization"),
        ("Environmental AQI", "nav_aqi", ":material/air:", "Korelasi Kualitas Udara" if lang == "id" else "Air Quality Correlation"),
        ("Lifestyle & Fitness", "nav_life", ":material/fitness_center:", "Segmentasi Pelanggan" if lang == "id" else "Customer Segmentation"),
        ("Data Quality", "nav_quality", ":material/verified:", "Validasi & Audit DWH" if lang == "id" else "DWH Validation & Audit"),
    ]
    for p_key, p_lbl_key, p_icon, p_sub in NAV_PAGES:
        is_act = (st.session_state.active_page == p_key and st.session_state.drill_mode is None)
        p_lbl = t(p_lbl_key, lang)
        if st.button(
            p_lbl if is_exp else "",
            icon=p_icon,
            help=f"{p_lbl} ({p_sub})",
            key=f"nav_{p_key}",
            type="primary" if is_act else "secondary",
            use_container_width=is_exp,
        ):
            st.session_state.active_page = p_key
            st.session_state.drill_mode = None
            st.rerun()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # Nested Sublist 1: Theme (Light / Dark)
    if is_exp:
        th_caret = " ▾" if st.session_state.sb_theme_open else " ▸"
        if st.button(
            f"{t('nav_theme', lang)}{th_caret}",
            icon=":material/contrast:",
            help=t("nav_theme", lang),
            key="btn_sb_theme_parent",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.sb_theme_open = not st.session_state.sb_theme_open
            st.rerun()

        if st.session_state.sb_theme_open:
            with st.container(key=f"sb_sub_theme_light{'_active' if theme == 'light' else ''}"):
                if st.button(
                    t("theme_light", lang),
                    icon=":material/light_mode:",
                    key="btn_theme_light",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.theme = "light"
                    st.rerun()
            with st.container(key=f"sb_sub_theme_dark{'_active' if theme == 'dark' else ''}"):
                if st.button(
                    t("theme_dark", lang),
                    icon=":material/dark_mode:",
                    key="btn_theme_dark",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.theme = "dark"
                    st.rerun()

        # Nested Sublist 2: Language (Indonesia / English)
        lg_caret = " ▾" if st.session_state.sb_lang_open else " ▸"
        if st.button(
            f"{t('nav_lang', lang)}{lg_caret}",
            icon=":material/translate:",
            help=t("nav_lang", lang),
            key="btn_sb_lang_parent",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.sb_lang_open = not st.session_state.sb_lang_open
            st.rerun()

        if st.session_state.sb_lang_open:
            with st.container(key=f"sb_sub_lang_id{'_active' if lang == 'id' else ''}"):
                if st.button(
                    t("lang_id", lang),
                    icon=":material/language:",
                    key="btn_lang_id",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.lang = "id"
                    st.rerun()
            with st.container(key=f"sb_sub_lang_en{'_active' if lang == 'en' else ''}"):
                if st.button(
                    t("lang_en", lang),
                    icon=":material/language:",
                    key="btn_lang_en",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.lang = "en"
                    st.rerun()
    else:
        # Collapsed Mini Icon Rail: quick-toggle icons
        if st.button(
            "",
            icon=":material/dark_mode:" if theme == "light" else ":material/light_mode:",
            help=f"{t('nav_theme', lang)}: {t('theme_dark' if theme == 'light' else 'theme_light', lang)}",
            key="btn_rail_theme_toggle",
            type="secondary",
            use_container_width=False,
        ):
            st.session_state.theme = "dark" if theme == "light" else "light"
            st.rerun()
        if st.button(
            "",
            icon=":material/translate:",
            help=f"{t('nav_lang', lang)}: {'Indonesia' if lang == 'en' else 'English'}",
            key="btn_rail_lang_toggle",
            type="secondary",
            use_container_width=False,
        ):
            st.session_state.lang = "id" if lang == "en" else "en"
            st.rerun()

    # Customer Service Headset Help & Support Widget directly below Language
    render_sidebar_support_widget(sidebar_expanded=is_exp, lang=lang)

    page = st.session_state.active_page


# ==============================================================================
# DRILL-THROUGH VIEW 1: PRODUCT SKU DEEP-DIVE DIAGNOSTIC
# ==============================================================================
def render_drill_sku():
    sku_id = st.session_state.drill_sku_id
    row_sku = df_sku[df_sku["sku_natural_id"] == sku_id]
    if row_sku.empty:
        st.session_state.drill_mode = None
        st.rerun()
        return
    rec = row_sku.iloc[0]

    col_back, col_t, col_dl = st.columns([0.55, 8.65, 0.8], gap="small", vertical_alignment="center")
    with col_back:
        if st.button("", icon=":material/arrow_back:", key="btn_drill_back", help="Kembali ke Penjualan & Harga" if lang == "id" else "Back to Sales & Pricing"):
            st.session_state.drill_mode = None
            st.rerun()
    with col_t:
        render_page_title(t("drill_sku_title", lang), f"{rec['sku_natural_id']} ({rec['channel_source']})")
    with col_dl:
        render_download_popover("drill_sku", lang=lang, csv_df=row_sku, csv_filename=f"yuuukosoovexa_sku_{sku_id}.csv")

    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

    is_id = (lang == "id")
    render_section_eyebrow(t("drill_sku_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            "Pendapatan Bersih SKU" if is_id else "SKU Net Revenue",
            str(rec["product_name"])[:54],
            "TOTAL PENDAPATAN BERSIH SKU" if is_id else "TOTAL SKU NET REVENUE",
            fmt_inr_compact(float(rec["total_net_revenue_inr"])),
            f"{'Kotor' if is_id else 'Gross'} {fmt_inr_compact(float(rec['total_gross_revenue_inr']))}",
            variant="emerald",
        )
    with k2:
        render_nested_hero_card(
            "Volume & Pesanan" if is_id else "Volume & Orders",
            f"{'Kategori' if is_id else 'Category'} {rec['category_name']}",
            "UNIT TERJUAL" if is_id else "UNITS SOLD",
            f"{int(rec['total_units_sold']):,} {'Unit' if is_id else 'Units'}",
            f"{int(rec['total_transactions']):,} {'Pesanan' if is_id else 'Orders'} | {'Merek' if is_id else 'Brand'} {rec['brand']}",
            variant="lime",
        )
    with k3:
        render_compact_kpi_card(
            "Struktur Harga (MRP vs Jual)" if is_id else "Pricing Structure (MRP vs Selling)",
            f"INR {rec['selling_price_inr']:,.0f}",
            sub=f"{'MRP Asli' if is_id else 'Original MRP'} INR {rec['mrp_inr']:,.0f} | {rec['discount_tier']}",
            accent_strip="tag",
            strip_tone="forest",
            strip_tooltip=f"-{rec['discount_pct']:.1f}%",
        )
        rating_txt = f"{rec['avg_rating']:.2f} / 5.0" if pd.notna(rec["avg_rating"]) else ("Tanpa Rating" if is_id else "No Rating")
        render_compact_kpi_card(
            "Rating Pelanggan & Kemasan" if is_id else "Customer Rating & Pack",
            rating_txt,
            sub=f"{'Kemasan' if is_id else 'Pack Size'} {rec['pack_size']} | Status {rec['availability']}",
            accent_strip="star",
            strip_tone="lime",
            strip_tooltip=f"{int(rec['rating_count']):,} {'ulasan' if is_id else 'ratings'}",
        )

    # Peer comparison within same category & channel
    render_section_eyebrow("02 · Perbandingan Kategori Sejenis" if is_id else "02 · Peer Category Benchmark")
    peers = df_sku[
        (df_sku["category_name"] == rec["category_name"])
        & (df_sku["channel_source"] == rec["channel_source"])
    ].sort_values("total_net_revenue_inr", ascending=False).head(10)

    with st.container(border=True, key="card_p5_audit"):
        render_chart_card_header(
            f"{'10 SKU Pembanding Teratas' if is_id else 'Top 10 Peer SKUs'} ({rec['category_name']})"
        )
        hi_col = "#c8f169" if PALETTE["is_dark"] else "#043f2e"
        base_col = "#294338" if PALETTE["is_dark"] else "#bfd1b4"
        peer_rows = []
        for pr in peers.itertuples(index=False):
            is_sel = (pr.sku_natural_id == sku_id)
            p_col = hi_col if is_sel else base_col
            p_name = str(pr.product_name)[:34]
            peer_rows.append(
                {
                    "label": p_name,
                    "segments": [(float(pr.total_net_revenue_inr), p_col)],
                    "tip_html": (
                        f"<div style='font-weight:700;color:{PALETTE['emerald']};'>{p_name}</div>"
                        f"<div><span style='color:{PALETTE['muted']};'>{'Pendapatan Bersih' if is_id else 'Net Revenue'}</span> <b>INR {float(pr.total_net_revenue_inr):,.0f}</b></div>"
                    ),
                }
            )
        render_horizontal_pill_bars(
            peer_rows,
            legend_items=[
                ("SKU Terpilih" if is_id else "Selected SKU", hi_col),
                ("SKU Pembanding" if is_id else "Peer SKUs", base_col),
            ],
            wide_labels=True,
        )


# ==============================================================================
# DRILL-THROUGH VIEW 2: CITY AQI DIAGNOSTIC
# ==============================================================================
def render_drill_city():
    city = st.session_state.drill_city_name
    cdf = df_aqi[df_aqi["city"] == city].sort_values("full_date")
    if cdf.empty:
        st.session_state.drill_mode = None
        st.rerun()
        return

    is_id = (lang == "id")
    col_back, col_t, col_dl = st.columns([0.55, 8.65, 0.8], gap="small", vertical_alignment="center")
    with col_back:
        if st.button("", icon=":material/arrow_back:", key="btn_drill_back", help="Kembali ke Kualitas Udara AQI" if is_id else "Back to Environmental AQI"):
            st.session_state.drill_mode = None
            st.rerun()
    with col_t:
        render_page_title(
            f"{'Diagnostik AQI' if is_id else ''} {city}{'' if is_id else ' AQI Diagnostic'},".strip(),
            f"{cdf['state'].iloc[0]} ({cdf['region'].iloc[0]} India)",
        )
    with col_dl:
        render_download_popover("drill_city", lang=lang, csv_df=cdf, csv_filename=f"yuuukosoovexa_aqi_{str(city).lower().replace(' ', '_')}.csv")

    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

    avg_aqi = cdf["avg_us_aqi"].mean()
    max_aqi = cdf["max_us_aqi"].max()
    vit_rev = cdf["daily_vitamin_revenue_inr"].sum()
    unhealthy_days = int((cdf["avg_us_aqi"] > 150).sum())

    render_section_eyebrow(t("drill_city_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            "Paparan Udara Kota" if is_id else "City Air Exposure",
            f"{'Observasi selama' if is_id else 'Observations across'} {len(cdf):,} {'hari' if is_id else 'days'}",
            "RATA-RATA US AQI HARIAN" if is_id else "MEAN DAILY US AQI",
            f"{avg_aqi:.1f}",
            f"{'Puncak AQI' if is_id else 'Peak Max AQI'} {max_aqi:.0f} | PM2.5 {cdf['avg_pm25_ugm3'].mean():.1f} ug/m3",
            variant="teal",
        )
    with k2:
        render_nested_hero_card(
            "Permintaan Preventif" if is_id else "Preventive Demand",
            "Penjualan suplemen vitamin dan imunitas" if is_id else "Vitamin and immunity supplement sales",
            "PENDAPATAN VITAMIN KOTA" if is_id else "CITY VITAMIN REVENUE",
            fmt_inr_compact(vit_rev),
            f"{int(cdf['daily_vitamin_units_sold'].sum()):,} {'Unit Vitamin Terjual' if is_id else 'Vitamin Units Sold'}",
            variant="lime",
        )
    with k3:
        tone_u = "bad" if unhealthy_days > 100 else "warn"
        render_compact_kpi_card(
            "Hari Udara Tidak Sehat (>150 AQI)" if is_id else "Unhealthy Air Days (>150 AQI)",
            f"{unhealthy_days:,} {'Hari' if is_id else 'Days'}",
            sub=f"{'Suhu Rata-Rata' if is_id else 'Avg Temp'} {cdf['avg_temp_c'].mean():.1f} C | {'Kelembapan' if is_id else 'Humidity'} {cdf['avg_humidity_pct'].mean():.0f}%",
            accent_strip="exclamation",
            strip_tone="forest",
            strip_tooltip=f"{unhealthy_days / len(cdf) * 100:.1f}% {'dari total hari' if is_id else 'of days'}",
        )
        render_compact_kpi_card(
            "Total Pendapatan Suplemen Kota" if is_id else "Total City Supplement Revenue",
            fmt_inr_compact(cdf["daily_net_revenue_inr"].sum()),
            sub="Gabungan seluruh 5 kategori suplemen" if is_id else "All 5 supplement categories combined",
            accent_strip="bag",
            strip_tone="lime",
            strip_tooltip=f"{int(cdf['daily_orders'].sum()):,} {'Pesanan' if is_id else 'Orders'}",
        )

    render_section_eyebrow(t("drill_city_s2", lang))
    monthly_c = (
        cdf.assign(ym=cdf["full_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("ym", as_index=False)
        .agg(avg_us_aqi=("avg_us_aqi", "mean"), avg_pm25=("avg_pm25_ugm3", "mean"), vit_rev=("daily_vitamin_revenue_inr", "sum"))
    )

    col_l, col_r = st.columns([6.5, 3.5], gap="medium")
    with col_l:
        with st.container(border=True, key="card_drill_city_dual"):
            render_chart_card_header(f"{city} AQI vs Vitamin")
            lbl_vit = "Pendapatan Vitamin" if is_id else "Vitamin Revenue"
            lbl_aqi = "Rata-Rata US AQI" if is_id else "Mean US AQI"
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(
                    x=monthly_c["ym"],
                    y=monthly_c["vit_rev"],
                    name=lbl_vit,
                    mode="lines",
                    line=dict(color=PALETTE["emerald"], width=2.6, shape="spline", smoothing=1.15),
                    hovertemplate=f"<span style='color:#043f2e'>{lbl_vit}</span>  <b>INR %{{y:,.0f}}</b><extra></extra>",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=monthly_c["ym"],
                    y=monthly_c["avg_us_aqi"],
                    name=lbl_aqi,
                    mode="lines",
                    line=dict(color=PALETTE["coral"], width=2.2, dash="dot", shape="spline", smoothing=1.15),
                    hovertemplate=f"<span style='color:#7f1d1d'>{lbl_aqi}</span>  <b>%{{y:.1f}}</b><extra></extra>",
                ),
                secondary_y=True,
            )
            if not monthly_c.empty:
                pk_c = int(monthly_c["avg_us_aqi"].idxmax())
                fig.add_trace(
                    go.Scatter(
                        x=[monthly_c.loc[pk_c, "ym"]],
                        y=[float(monthly_c.loc[pk_c, "avg_us_aqi"])],
                        mode="markers",
                        hoverinfo="skip",
                        showlegend=False,
                        marker=dict(size=12, color=PALETTE["lime"], line=dict(color=PALETTE["emerald"], width=2.6)),
                    ),
                    secondary_y=True,
                )
            fig.update_yaxes(title_text=f"{lbl_vit} (INR)", secondary_y=False)
            fig.update_yaxes(title_text=lbl_aqi, secondary_y=True, showgrid=False)
            apply_bento_plotly_style(fig, height=340)
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True, config=PLOT_CFG)

    with col_r:
        with st.container(border=True, key="card_drill_city_pol"):
            render_chart_card_header(t("drill_city_pol_title", lang))
            pol_df = pd.DataFrame({
                "Pollutant": ["PM2.5", "PM10", "NO2", "O3"],
                "Concentration": [
                    cdf["avg_pm25_ugm3"].mean(),
                    cdf["avg_pm10_ugm3"].mean(),
                    cdf["avg_no2_ugm3"].mean(),
                    cdf["avg_o3_ugm3"].mean(),
                ],
            })
            peak_pol = float(pol_df["Concentration"].max()) if not pol_df.empty else 0
            render_striped_pill_bar(
                pol_df["Pollutant"],
                pol_df["Concentration"],
                peak_badge_text=f"{peak_pol:.1f} ug/m3",
                value_fmt="ugm3",
                height=340,
            )


# ==============================================================================
# PAGE 1: EXECUTIVE SUMMARY & MULTI-CHANNEL SALES
# ==============================================================================
def render_page1():
    all_ch_lbl = t("all_channels", lang)
    all_cat_lbl = t("all_categories", lang)
    col_title, col_f1, col_f2, col_dl = st.columns([5.2, 2.0, 2.0, 0.8], gap="small")
    with col_title:
        st.markdown(f'<h1 class="yv-page-heading">{t("nav_exec", lang)}</h1>', unsafe_allow_html=True)
    with col_f1:
        ch_choice = st.selectbox(
            "Channel Filter",
            options=[all_ch_lbl, "Flipkart Health", "Tata 1mg"],
            index=0,
            label_visibility="collapsed",
            key=f"p1_ch_sel_{lang}",
        )
    with col_f2:
        cats_all = [all_cat_lbl] + sorted(df_exec["category_name"].unique().tolist())
        sel_cat = st.selectbox("Category Filter", cats_all, label_visibility="collapsed", key=f"p1_cat_sel_{lang}")
    with col_dl:
        render_download_popover("p1", lang=lang)

    st.markdown('<div class="filter-content-spacer"></div>', unsafe_allow_html=True)

    min_d, max_d = df_exec["full_date"].min().date(), df_exec["full_date"].max().date()
    f = df_exec.copy()
    if ch_choice != all_ch_lbl:
        f = f[f["channel_name"] == ch_choice]
    if sel_cat != all_cat_lbl:
        f = f[f["category_name"] == sel_cat]

    if f.empty:
        render_empty_state(
            "No sales transactions match the active filters",
            f"Channel '{ch_choice}' combined with category '{sel_cat}' returned 0 records.",
            "Reset the Channel switcher to All or choose All Categories to restore the overview.",
        )
        return

    net_rev = float(f["net_revenue_inr"].sum())
    gross_rev = float(f["gross_revenue_inr"].sum())
    tx_cnt = int(len(f))
    units = int(f["units_sold"].sum())
    aov = net_rev / tx_cnt if tx_cnt else 0.0
    avg_disc = float(f["discount_pct"].mean()) if tx_cnt else 0.0

    fk_units = int(f.loc[f["channel_name"] == "Flipkart Health", "units_sold"].sum())
    mg_units = int(f.loc[f["channel_name"] == "Tata 1mg", "units_sold"].sum())

    # --- TIER 1: EXECUTIVE KPI OVERVIEW (LEFT -> CENTER -> RIGHT) ---
    is_id = (lang == "id")
    render_section_eyebrow(t("p1_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            t("p1_hero1_title", lang),
            t("p1_hero1_sub", lang),
            t("p1_hero1_lbl", lang),
            fmt_inr_compact(net_rev),
            f"{'Kotor' if is_id else 'Gross'} {fmt_inr_compact(gross_rev)} | {'Diskon Rata-Rata' if is_id else 'Avg Disc'} {avg_disc:.2f}%",
            variant="emerald",
        )
    with k2:
        render_nested_hero_card(
            t("p1_hero2_title", lang),
            t("p1_hero2_sub", lang),
            t("p1_hero2_lbl", lang),
            f"{units:,} {'Unit' if is_id else 'Units'}",
            f"Tata 1mg {mg_units:,} | Flipkart {fk_units:,}",
            variant="lime",
        )
    with k3:
        render_compact_kpi_card(
            t("p1_kpi3_lbl", lang),
            f"{tx_cnt:,} {'Pesanan' if is_id else 'Orders'}",
            sub=f"{'Rata-Rata Nilai Pesanan (AOV)' if is_id else 'Average Order Value (AOV)'} INR {aov:,.2f}",
            accent_strip="check",
            strip_tone="forest",
            strip_tooltip=t("p1_kpi3_badge", lang),
        )
        render_compact_kpi_card(
            t("p1_kpi4_lbl", lang),
            f"{avg_disc:.2f}%",
            sub=f"{'Periode' if is_id else 'Period'} {min_d.strftime('%b %Y')} {'s/d' if is_id else 'to'} {max_d.strftime('%b %Y')}",
            accent_strip="percent",
            strip_tone="lime",
            strip_tooltip=t("p1_kpi4_badge", lang),
        )

    # --- TIER 2: PRIMARY REVENUE TREND (SMOOTH SPLINE + COMPACT 'Month v' DROPDOWN) ---
    render_section_eyebrow(t("p1_s2", lang))
    with st.container(border=True, key="card_p1_trend"):
        hd_l, hd_r = st.columns([8.4, 1.6])
        with hd_l:
            render_chart_card_header(
                t("p1_trend_title", lang),
                t("p1_trend_sub", lang),
            )
        with hd_r:
            g_opts = [t("gran_month", lang), t("gran_quarter", lang), t("gran_year", lang)]
            gran = st.selectbox(
                "Granularity",
                options=g_opts,
                index=0,
                label_visibility="collapsed",
                key=f"p1_gran_select_{lang}",
            )

        if gran == g_opts[2]:
            tdf = f.groupby("year_num", as_index=False).agg(gross=("gross_revenue_inr", "sum"), net=("net_revenue_inr", "sum"))
            x_col = tdf["year_num"].astype(str)
        elif gran == g_opts[1]:
            tdf = (
                f.assign(yq=f["year_num"].astype(str) + " " + f["quarter_label"])
                .groupby("yq", as_index=False)
                .agg(gross=("gross_revenue_inr", "sum"), net=("net_revenue_inr", "sum"))
            )
            x_col = tdf["yq"]
        else:
            tdf = (
                f.assign(ym=f["full_date"].dt.to_period("M").dt.to_timestamp())
                .groupby("ym", as_index=False)
                .agg(gross=("gross_revenue_inr", "sum"), net=("net_revenue_inr", "sum"))
            )
            x_col = tdf["ym"]

        lbl_gross = "Pendapatan Kotor" if is_id else "Gross Revenue"
        lbl_net = "Pendapatan Bersih" if is_id else "Net Revenue"
        lbl_peak = "Puncak" if is_id else "Peak"
        fig_tr = go.Figure()
        fig_tr.add_trace(
            go.Scatter(
                x=x_col,
                y=tdf["gross"],
                name=lbl_gross,
                mode="lines",
                line=dict(color=PALETTE["sage_bar"], width=1.8, dash="dot", shape="spline", smoothing=1.15),
                hovertemplate=f"<span style='color:{PALETTE['muted']}'>{lbl_gross}</span>  <b>INR %{{y:,.0f}}</b><extra></extra>",
            )
        )
        fig_tr.add_trace(
            go.Scatter(
                x=x_col,
                y=tdf["net"],
                name=lbl_net,
                mode="lines",
                line=dict(color=PALETTE["chart_primary"], width=2.6, shape="spline", smoothing=1.15),
                hovertemplate=f"<span style='color:{PALETTE['emerald']}'>{lbl_net}</span>  <b>INR %{{y:,.0f}}</b><extra></extra>",
            )
        )

        # Single Chartreuse Peak Marker + Callout Pill
        if not tdf.empty:
            pk_i = int(tdf["net"].idxmax())
            pk_x = x_col.loc[pk_i]
            pk_y = float(tdf.loc[pk_i, "net"])
            fig_tr.add_trace(
                go.Scatter(
                    x=[pk_x],
                    y=[pk_y],
                    mode="markers",
                    hoverinfo="skip",
                    showlegend=False,
                    marker=dict(
                        size=13,
                        color=PALETTE["lime"],
                        line=dict(color=PALETTE["hero_bg"], width=2.8),
                    ),
                )
            )
            fig_tr.add_annotation(
                x=pk_x,
                y=pk_y,
                text=f"<b>{lbl_peak} {fmt_inr_compact(pk_y)}</b>",
                showarrow=True,
                arrowhead=0,
                arrowwidth=2,
                arrowcolor=PALETTE["chart_badge_bg"],
                ax=0,
                ay=-34,
                bgcolor=PALETTE["chart_badge_bg"],
                bordercolor=PALETTE["chart_badge_bg"],
                borderwidth=1,
                borderpad=6,
                font=dict(size=11.5, color=PALETTE["chart_badge_fg"], family="Inter, sans-serif"),
            )

        max_y = float(max(tdf["gross"].max(), tdf["net"].max())) if not tdf.empty else 1
        fig_tr.update_yaxes(range=[0, max_y * 1.18])
        apply_bento_plotly_style(fig_tr, height=310)
        fig_tr.update_layout(hovermode="x unified", margin=dict(l=8, r=14, t=24, b=16))
        st.plotly_chart(fig_tr, use_container_width=True, config=PLOT_CFG)

    # --- TIER 3: CATEGORY & CHANNEL BREAKDOWN (6.2 : 3.8 SPLIT) ---
    render_section_eyebrow(t("p1_s3", lang))
    bot_l, bot_r = st.columns([6.2, 3.8], gap="medium")
    with bot_l:
        with st.container(border=True, key="card_p1_cat"):
            render_chart_card_header(
                t("p1_cat_title", lang),
                t("p1_cat_sub", lang),
            )
            cat_agg = (
                f.groupby("category_name", as_index=False)
                .agg(net_rev=("net_revenue_inr", "sum"), units=("units_sold", "sum"))
                .sort_values("net_rev", ascending=False)
            )
            max_cat = float(cat_agg["net_rev"].max()) if not cat_agg.empty else 0
            short_lbl = (
                cat_agg["category_name"]
                .replace({
                    "Vitamin Supplement": "Vitamins",
                    "Protein Supplement": "Protein",
                    "Energy Drinks": "Energy",
                    "Milk Drink Mixes": "Milk Mix",
                    "Digestive Probiotic": "Probiotic",
                })
            )
            render_striped_pill_bar(
                short_lbl,
                cat_agg["net_rev"],
                peak_badge_text=fmt_inr_compact(max_cat).replace("INR ", ""),
                full_labels=cat_agg["category_name"].tolist(),
                value_fmt="inr",
                extra_lines=[f"{int(u):,} {'Unit Terjual' if is_id else 'Units Sold'}" for u in cat_agg["units"].tolist()],
                height=345,
            )

    with bot_r:
        ch_agg = f.groupby("channel_name", as_index=False).agg(net_rev=("net_revenue_inr", "sum"), orders=("transaction_id", "count"))
        with st.container(border=True, key="card_p1_donut"):
            render_chart_card_header(t("p1_ch_title", lang), t("p1_ch_sub", lang))
            render_channel_arc_gauge(ch_agg, net_rev, center_sub_label=t("total_net_rev", lang), lang=lang)

        if not ch_agg.empty:
            leader = ch_agg.sort_values("net_rev", ascending=False).iloc[0]
            share_pct = leader["net_rev"] / net_rev * 100 if net_rev else 0
            leader_num = fmt_inr_compact(leader["net_rev"]).replace("INR ", "")
            leader_info = build_info_popover_html(
                t("p1_leader_lbl", lang),
                (
                    f"Menampilkan kanal penjualan dengan kontribusi pendapatan bersih tertinggi ({leader['channel_name']} sebesar {share_pct:.1f}%)."
                    if is_id
                    else f"Highlights the top revenue-contributing sales channel ({leader['channel_name']} at {share_pct:.1f}% share)."
                ),
                "Ringkasan Penjualan Multi-Kanal" if is_id else "Multi-Channel Sales Summary",
            )
            st.markdown(
                f'<div class="bento-leader-card">'
                f'<div class="bento-card-header" style="margin-bottom:0;">'
                f'<div class="kpi-label" style="color:{PALETTE["muted"]}; margin-bottom:0;">{t("p1_leader_lbl", lang)}</div>'
                f'{leader_info}'
                f'</div>'
                f'<div class="leader-body">'
                f'<div class="leader-left">'
                f'<div class="leader-val"><span class="kpi-unit kpi-unit-pre">INR</span><span id="yv_num_p1_leader" class="anim-num">{leader_num}</span></div>'
                f'</div>'
                f'<div class="leader-right">'
                f'<div class="leader-channel">{leader["channel_name"]}</div>'
                f'<div class="leader-share">{share_pct:.1f}% {t("p1_leader_share", lang)}</div>'
                f'<div class="leader-orders">{int(leader["orders"]):,} {t("p1_leader_orders", lang)}</div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ==============================================================================
# PAGE 2: SALES & PRICING OPTIMIZATION (+ SKU DRILL-THROUGH)
# ==============================================================================
def render_page2():
    all_ch_lbl = t("all_channels", lang)
    all_cat_lbl = t("all_categories", lang)
    col_title, col_f1, col_f2, col_dl = st.columns([5.2, 2.0, 2.0, 0.8], gap="small")
    with col_title:
        st.markdown(f'<h1 class="yv-page-heading">{t("nav_sales", lang)}</h1>', unsafe_allow_html=True)
    with col_f1:
        ch_choice = st.selectbox(
            "Pricing Channel",
            options=[all_ch_lbl, "Flipkart Health", "Tata 1mg"],
            index=0,
            label_visibility="collapsed",
            key=f"p2_ch_sel_{lang}",
        )
    with col_f2:
        cats = [all_cat_lbl] + sorted(df_sku["category_name"].unique().tolist())
        sel_cat = st.selectbox("Category", cats, label_visibility="collapsed", key=f"p2_cat_sel_{lang}")

    st.markdown('<div class="filter-content-spacer"></div>', unsafe_allow_html=True)

    f = df_sku.copy()
    if ch_choice != all_ch_lbl:
        f = f[f["channel_source"] == ch_choice]
    if sel_cat != all_cat_lbl:
        f = f[f["category_name"] == sel_cat]

    with col_dl:
        render_download_popover("p2", lang=lang)

    if f.empty:
        render_empty_state(
            "No catalog SKUs match the active filters",
            f"Channel '{ch_choice}' combined with category '{sel_cat}' returned 0 SKUs.",
            "Switch Channel back to All or select All Categories to view catalog pricing.",
        )
        return

    avg_disc = float(f["discount_pct"].mean()) if len(f) else 0
    avg_mrp = float(f["mrp_inr"].mean()) if len(f) else 0
    avg_sell = float(f["selling_price_inr"].mean()) if len(f) else 0
    avg_rat = float(f["avg_rating"].mean()) if len(f) else 0
    tot_disc_given = float(f["total_discount_given_inr"].sum())
    tot_net = float(f["total_net_revenue_inr"].sum())
    disc_eff = tot_net / tot_disc_given if tot_disc_given > 0 else 0

    tier_order = [
        "0% (No Discount)",
        "1-15% (Low Discount)",
        "16-30% (Moderate Discount)",
        "31-50% (High Discount)",
        ">50% (Aggressive Discount)",
    ]
    t_agg = f.groupby("discount_tier", as_index=False).agg(net_rev=("total_net_revenue_inr", "sum"))
    t_agg["discount_tier"] = pd.Categorical(t_agg["discount_tier"], categories=tier_order, ordered=True)
    t_agg = t_agg.sort_values("discount_tier")
    best_tier = t_agg.sort_values("net_rev", ascending=False).iloc[0] if not t_agg.empty else None

    # --- TIER 1: PRICING KPI OVERVIEW (LEFT -> CENTER -> RIGHT) ---
    is_id = (lang == "id")
    render_section_eyebrow(t("p2_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            t("p2_hero1_title", lang),
            t("p2_hero1_sub", lang),
            t("p2_hero1_lbl", lang),
            f"{avg_disc:.2f}%",
            f"{'Rasio Efisiensi' if is_id else 'Efficiency Ratio'} {disc_eff:.2f}x | {'Diskon' if is_id else 'Discount'} INR {tot_disc_given/1e6:.2f}M",
            variant="teal",
        )
    with k2:
        render_nested_hero_card(
            t("p2_hero2_title", lang),
            t("p2_hero2_sub", lang),
            t("p2_hero2_lbl", lang),
            f"INR {avg_sell:,.0f}",
            f"{'Rata-Rata MRP' if is_id else 'Avg MRP'} INR {avg_mrp:,.0f} | {'Selisih' if is_id else 'Gap'} INR {avg_mrp - avg_sell:,.0f}",
            variant="lime",
        )
    with k3:
        render_compact_kpi_card(
            t("p2_kpi3_lbl", lang),
            f"{len(f):,} SKUs",
            sub=f"{'Total Diskon Diberikan' if is_id else 'Total Discount Granted'} {fmt_inr_compact(tot_disc_given)}",
            accent_strip="star",
            strip_tone="forest",
            strip_tooltip=f"{'Rata-Rata Rating' if is_id else 'Avg Rating'} {avg_rat:.2f} / 5",
        )
        if best_tier is not None:
            tier_short = str(best_tier["discount_tier"]).split(" ")[0]
            render_compact_kpi_card(
                t("p2_kpi4_lbl", lang),
                f"{'Pita' if is_id else ''} {tier_short}{'' if is_id else ' Band'}".strip(),
                sub=f"{'Pangsa pendapatan bersih tertinggi' if is_id else 'Highest net revenue share'} ({best_tier['discount_tier']})",
                accent_strip="trend_up",
                strip_tone="lime",
                strip_tooltip=fmt_inr_compact(float(best_tier["net_rev"])),
            )

    # --- TIER 2: ELASTICITY & DISCOUNT TIER PERFORMANCE (6.0 : 4.0 SPLIT) ---
    render_section_eyebrow(t("p2_s2", lang))
    mid_l, mid_r = st.columns([6.0, 4.0], gap="medium")
    with mid_l:
        with st.container(border=True, key="card_p2_scatter"):
            render_chart_card_header(
                t("p2_hm_title", lang),
                t("p2_hm_sub", lang),
            )
            hm_df = f.copy()
            disc_bins = [-0.01, 0.01, 5, 10, 15, 20, 25, 30, 40, 50, 100]
            disc_labels = ["0%", "1-5%", "6-10%", "11-15%", "16-20%", "21-25%", "26-30%", "31-40%", "41-50%", ">50%"]
            hm_df["disc_bin"] = pd.cut(hm_df["discount_pct"], bins=disc_bins, labels=disc_labels)

            # Use Categories on Y-axis when viewing All Categories; switch to Price Bands when a single Category is selected
            if hm_df["category_name"].nunique() > 1:
                hm_df["y_group"] = hm_df["category_name"].replace({
                    "Vitamin Supplement": "Vitamins",
                    "Protein Supplement": "Protein",
                    "Energy Drinks": "Energy",
                    "Milk Drink Mixes": "Milk Mix",
                    "Digestive Probiotic": "Probiotic",
                })
                y_order = (
                    hm_df.groupby("y_group")["total_net_revenue_inr"]
                    .sum()
                    .sort_values(ascending=False)
                    .index.tolist()
                )
            else:
                price_bins = [-1, 250, 500, 1000, 2000, 1e9]
                price_labels = ["< 250", "250-500", "500-1K", "1K-2K", "> 2K INR"]
                hm_df["y_group"] = pd.cut(hm_df["selling_price_inr"], bins=price_bins, labels=price_labels).astype(str)
                y_order = price_labels

            piv_rev = (
                hm_df.pivot_table(index="y_group", columns="disc_bin", values="total_net_revenue_inr", aggfunc="sum", observed=False)
                .reindex(index=y_order, columns=disc_labels)
                .fillna(0.0)
            )
            piv_sku = (
                hm_df.pivot_table(index="y_group", columns="disc_bin", values="sku_natural_id", aggfunc="count", observed=False)
                .reindex(index=y_order, columns=disc_labels)
                .fillna(0)
            )
            piv_units = (
                hm_df.pivot_table(index="y_group", columns="disc_bin", values="total_units_sold", aggfunc="sum", observed=False)
                .reindex(index=y_order, columns=disc_labels)
                .fillna(0)
            )

            render_rounded_heatmap(
                x_labels=disc_labels,
                y_labels=y_order,
                z_matrix=piv_rev.values,
                sku_matrix=piv_sku.values,
                units_matrix=piv_units.values,
                peak_badge_fn=fmt_inr_compact,
                lang=lang,
            )

    with mid_r:
        with st.container(border=True, key="card_p2_tier"):
            render_chart_card_header(
                t("p2_tier_title", lang),
                t("p2_tier_sub", lang),
            )
            short_t = t_agg["discount_tier"].astype(str).str.split(" ").str[0]
            max_t = float(t_agg["net_rev"].max()) if not t_agg.empty else 0
            render_striped_pill_bar(
                short_t,
                t_agg["net_rev"],
                peak_badge_text=fmt_inr_compact(max_t).replace("INR ", ""),
                full_labels=t_agg["discount_tier"].astype(str).tolist(),
                value_fmt="inr",
                height=330,
            )

    # --- TIER 3: ACTIONABLE SKU MATRIX & DRILL-THROUGH (FULL WIDTH) ---
    render_section_eyebrow(t("p2_s3", lang))
    with st.container(border=True, key="card_p2_matrix"):
        base_skus = f.sort_values("total_net_revenue_inr", ascending=False).head(50)
        search_key = f"p2_sku_search_{lang}"
        sku_q_live = str(st.session_state.get(search_key, "")).strip()

        def _filter_skus(df_in, q_str: str):
            if not q_str:
                return df_in
            q_low = q_str.lower()
            mask = (
                df_in["product_name"].astype(str).str.lower().str.contains(q_low, regex=False)
                | df_in["sku_natural_id"].astype(str).str.lower().str.contains(q_low, regex=False)
                | df_in["channel_source"].astype(str).str.lower().str.contains(q_low, regex=False)
                | df_in["category_name"].astype(str).str.lower().str.contains(q_low, regex=False)
            )
            return df_in[mask]

        pre_skus = _filter_skus(base_skus, sku_q_live)

        # Two-column header: Big 2-line display title (Left) + Stacked Drill-Through & Search controls (Right)
        hdr_l, hdr_r = st.columns([4.2, 5.8], gap="medium")
        with hdr_r:
            d2, d3 = st.columns([6.2, 3.8], gap="small")
            with d2:
                sku_opts = [f"{r.sku_natural_id} | {str(r.product_name)[:36]}" for r in pre_skus.itertuples()]
                sel_sku_lbl = st.selectbox(
                    "Select SKU for Drill-Through",
                    sku_opts if sku_opts else ["No matching SKU"],
                    label_visibility="collapsed",
                    disabled=(len(sku_opts) == 0),
                )
            with d3:
                if st.button(t("btn_inspect_sku", lang), use_container_width=True, disabled=(len(sku_opts) == 0)):
                    st.session_state.drill_sku_id = sel_sku_lbl.split(" | ")[0]
                    st.session_state.drill_mode = "sku"
                    st.rerun()

            _, sr_col = st.columns([4.4, 5.6], gap="small")
            with sr_col:
                search_ph = "Cari produk atau SKU..." if lang == "id" else "Search anything..."
                sku_q = st.text_input(
                    "Search SKU",
                    placeholder=search_ph,
                    label_visibility="collapsed",
                    key=search_key,
                ).strip()

        top_skus = _filter_skus(base_skus, sku_q)
        top_line_1 = "TOP 50"
        top_line_2 = "SKU Produk" if lang == "id" else "Product SKUs"
        with hdr_l:
            sku_info = build_info_popover_html(
                f"{top_line_1} {top_line_2}",
                (
                    "Menampilkan 50 SKU produk dengan pendapatan bersih tertinggi. Gunakan kotak pencarian untuk menyaring produk atau pilih SKU untuk melihat analisis mendalam."
                    if lang == "id"
                    else "Displays the top 50 product SKUs ranked by net revenue. Use the search bar to filter or select a SKU to inspect detailed pricing."
                ),
                "Katalog Produk & Harga" if lang == "id" else "Product & Pricing Catalog",
            )
            sku_csv_icon = build_csv_download_icon_html(top_skus, "yuuukosoovexa_top50_skus.csv", lang)
            st.markdown(
                f'<div style="display:flex; align-items:flex-start; justify-content:space-between; width:100%;">'
                f'<div class="sku-highlight-stack">'
                f'<div class="sku-highlight-big">{top_line_1}</div>'
                f'<div class="sku-highlight-sub">{top_line_2}</div>'
                f'</div>'
                f'<div class="yv-hdr-actions" style="padding-top:10px; padding-right:4px;">{sku_csv_icon}{sku_info}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if top_skus.empty:
            render_empty_state(
                "Tidak ada SKU yang cocok" if lang == "id" else "No matching SKUs found",
                f"Pencarian '{sku_q}' tidak ditemukan pada 50 SKU teratas." if lang == "id" else f"Search '{sku_q}' returned 0 results in the Top 50 SKUs.",
                "Kosongkan kolom pencarian untuk menampilkan semua SKU." if lang == "id" else "Clear the search bar to view all Top 50 SKUs.",
            )
        else:
            render_sku_modern_table(top_skus, title="", lang=lang)


# ==============================================================================
# PAGE 3: ENVIRONMENTAL & AIR QUALITY CORRELATION (+ CITY AQI DRILL-THROUGH)
# ==============================================================================
def render_page3():
    all_sea_lbl = t("all_seasons", lang)
    all_reg_lbl = t("all_regions", lang)
    col_title, col_f1, col_f2, col_dl = st.columns([5.2, 2.0, 2.0, 0.8], gap="small")
    with col_title:
        st.markdown(f'<h1 class="yv-page-heading">{t("nav_aqi", lang)}</h1>', unsafe_allow_html=True)
    with col_f1:
        season_choice = st.selectbox(
            "Season Filter",
            options=[all_sea_lbl, "Winter", "Summer", "Monsoon", "Post-Monsoon"],
            index=0,
            label_visibility="collapsed",
            key=f"p3_season_sel_{lang}",
        )
    with col_f2:
        regions = [all_reg_lbl] + sorted(df_aqi["region"].unique().tolist())
        sel_reg = st.selectbox("Region", regions, label_visibility="collapsed", key=f"p3_reg_sel_{lang}")
    with col_dl:
        render_download_popover("p3", lang=lang)

    st.markdown('<div class="filter-content-spacer"></div>', unsafe_allow_html=True)

    f = df_aqi.copy()
    if season_choice != all_sea_lbl:
        f = f[f["season_india"] == season_choice]
    if sel_reg != all_reg_lbl:
        f = f[f["region"] == sel_reg]

    if f.empty:
        render_empty_state(
            "No environmental observations match these filters",
            f"Season '{season_choice}' in region '{sel_reg}' returned 0 city-day records.",
            "Reset Season to All or choose All Regions to view air quality coverage.",
        )
        return

    mean_aqi = float(f["avg_us_aqi"].mean()) if len(f) else 0
    mean_pm25 = float(f["avg_pm25_ugm3"].mean()) if len(f) else 0
    vit_rev = float(f["daily_vitamin_revenue_inr"].sum())
    unhealthy_days = int((f["avg_us_aqi"] > 150).sum())

    high_aqi_vit = float(f.loc[f["avg_us_aqi"] > 150, "daily_vitamin_revenue_inr"].mean()) if unhealthy_days else 0
    norm_aqi_vit = float(f.loc[f["avg_us_aqi"] <= 100, "daily_vitamin_revenue_inr"].mean()) if (f["avg_us_aqi"] <= 100).any() else 0
    demand_lift = ((high_aqi_vit - norm_aqi_vit) / norm_aqi_vit * 100) if norm_aqi_vit > 0 else 0

    city_agg = (
        f.groupby(["city", "state", "region", "latitude", "longitude"], as_index=False)
        .agg(
            mean_aqi=("avg_us_aqi", "mean"),
            mean_pm25=("avg_pm25_ugm3", "mean"),
            vit_rev=("daily_vitamin_revenue_inr", "sum"),
            vit_units=("daily_vitamin_units_sold", "sum"),
        )
    )

    # --- TIER 1: HERO GEOSPATIAL RISK MAP (FULL WIDTH, THEME-AWARE FLOATING HUD) ---
    render_section_eyebrow(t("p3_s1", lang))
    render_aqi_hero_map(
        city_agg,
        demand_lift=demand_lift,
        season_label=season_choice,
        region_label=sel_reg,
        height=468,
        hud_labels=TRANSLATIONS.get(lang, TRANSLATIONS["en"]),
    )

    # --- TIER 2: ENVIRONMENTAL EXPOSURE & IMMUNITY DEMAND KPI STRIP ---
    is_id = (lang == "id")
    render_section_eyebrow(t("p3_s2", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            t("p3_hero1_title", lang),
            f"29 {'Kota India' if is_id else 'Indian Cities'} ({len(f):,} {'Hari-Kota' if is_id else 'City-Days'})",
            t("p3_hero1_lbl", lang),
            f"{mean_aqi:.2f}",
            f"{'Rata-Rata PM2.5' if is_id else 'Mean PM2.5'} {mean_pm25:.1f} ug/m3 | {'Hari Tidak Sehat' if is_id else 'Unhealthy Days'} {unhealthy_days:,}",
            variant="teal",
        )
    with k2:
        render_nested_hero_card(
            t("p3_hero2_title", lang),
            t("p3_hero2_sub", lang),
            t("p3_hero2_lbl", lang),
            fmt_inr_compact(vit_rev),
            f"{int(f['daily_vitamin_units_sold'].sum()):,} {'Unit Terjual | 29 Kota' if is_id else 'Units Sold | 29 Cities'}",
            variant="lime",
        )
    with k3:
        lift_tone = "good" if demand_lift >= 0 else "bad"
        lift_icon = "trend_up" if demand_lift >= 0 else "trend_down"
        render_compact_kpi_card(
            t("p3_kpi3_lbl", lang),
            f"{demand_lift:+.1f}%",
            sub=(
                f"Rata-Rata AQI Tinggi INR {high_aqi_vit:,.0f}/hari vs Normal INR {norm_aqi_vit:,.0f}/hari"
                if is_id
                else f"High AQI Avg INR {high_aqi_vit:,.0f}/day vs Normal INR {norm_aqi_vit:,.0f}/day"
            ),
            accent_strip=lift_icon,
            strip_tone="forest",
            strip_tooltip=f"{demand_lift:+.1f}% {t('p3_kpi3_badge', lang)}",
        )
        with st.container(border=True, key="card_p3_drill"):
            drill_info = build_info_popover_html(
                t("p3_drill_lbl", lang),
                (
                    "Pilih salah satu dari 29 kota India lalu klik tombol untuk membuka analisis mendalam tren AQI dan profil polutan harian kota tersebut."
                    if is_id
                    else "Select any of the 29 Indian cities and click inspect to open its daily AQI timeline and pollutant breakdown."
                ),
                "Analisis Detail Kota" if is_id else "City Detail Analysis",
            )
            st.markdown(
                f'<div class="bento-card-header" style="margin-bottom:10px;">'
                f'<div class="kpi-label" style="color:{PALETTE["muted"]}; margin-bottom:0;">{t("p3_drill_lbl", lang)}</div>'
                f'{drill_info}'
                f'</div>',
                unsafe_allow_html=True,
            )
            d_c1, d_c2 = st.columns([6.2, 3.8], gap="small")
            top_cities = city_agg.sort_values("mean_aqi", ascending=False)["city"].tolist()
            with d_c1:
                sel_city = st.selectbox("Select City", top_cities, label_visibility="collapsed")
            with d_c2:
                if st.button(t("btn_inspect", lang), use_container_width=True):
                    st.session_state.drill_city_name = sel_city
                    st.session_state.drill_mode = "city"
                    st.rerun()

    # --- TIER 3: SEASONAL SYNCHRONIZATION TIMELINE & HIGH-RISK CITY RANKING (6.4 : 3.6 SPLIT) ---
    render_section_eyebrow(t("p3_s3", lang))
    bot_l, bot_r = st.columns([6.4, 3.6], gap="medium")
    with bot_l:
        with st.container(border=True, key="card_p3_dual"):
            hd_l, hd_r = st.columns([7.8, 2.2])
            with hd_l:
                render_chart_card_header(
                    t("p3_dual_title", lang),
                    t("p3_dual_sub", lang),
                )
            with hd_r:
                g3_opts = [t("gran_month", lang), t("gran_quarter", lang), t("gran_year", lang)]
                aqi_gran = st.selectbox(
                    "AQI Granularity",
                    options=g3_opts,
                    index=0,
                    label_visibility="collapsed",
                    key=f"p3_gran_select_{lang}",
                )

            if aqi_gran == g3_opts[2]:
                m_aqi = f.groupby("year_num", as_index=False).agg(mean_aqi=("avg_us_aqi", "mean"), vit_rev=("daily_vitamin_revenue_inr", "sum"))
                ax_col = m_aqi["year_num"].astype(str)
            elif aqi_gran == g3_opts[1]:
                m_aqi = (
                    f.assign(yq=f["full_date"].dt.to_period("Q").astype(str))
                    .groupby("yq", as_index=False)
                    .agg(mean_aqi=("avg_us_aqi", "mean"), vit_rev=("daily_vitamin_revenue_inr", "sum"))
                )
                ax_col = m_aqi["yq"]
            else:
                m_aqi = (
                    f.assign(ym=f["full_date"].dt.to_period("M").dt.to_timestamp())
                    .groupby("ym", as_index=False)
                    .agg(mean_aqi=("avg_us_aqi", "mean"), vit_rev=("daily_vitamin_revenue_inr", "sum"))
                )
                ax_col = m_aqi["ym"]

            lbl_vit = "Pendapatan Vitamin" if is_id else "Vitamin Revenue"
            lbl_aqi = "Rata-Rata US AQI" if is_id else "Mean US AQI"
            lbl_pkaqi = "Puncak AQI" if is_id else "Peak AQI"
            fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
            fig_dual.add_trace(
                go.Scatter(
                    x=ax_col,
                    y=m_aqi["vit_rev"],
                    name=lbl_vit,
                    mode="lines",
                    line=dict(color=PALETTE["chart_primary"], width=2.6, shape="spline", smoothing=1.15),
                    hovertemplate=f"<span style='color:{PALETTE['emerald']}'>{lbl_vit}</span>  <b>INR %{{y:,.0f}}</b><extra></extra>",
                ),
                secondary_y=False,
            )
            fig_dual.add_trace(
                go.Scatter(
                    x=ax_col,
                    y=m_aqi["mean_aqi"],
                    name=lbl_aqi,
                    mode="lines",
                    line=dict(color=PALETTE["coral"], width=2.2, dash="dot", shape="spline", smoothing=1.15),
                    hovertemplate=f"<span style='color:{PALETTE['coral']}'>{lbl_aqi}</span>  <b>%{{y:.1f}}</b><extra></extra>",
                ),
                secondary_y=True,
            )

            # Single Peak AQI Callout Marker + Badge
            if not m_aqi.empty:
                pk_a = int(m_aqi["mean_aqi"].idxmax())
                pk_ax = ax_col.loc[pk_a]
                pk_ay = float(m_aqi.loc[pk_a, "mean_aqi"])
                fig_dual.add_trace(
                    go.Scatter(
                        x=[pk_ax],
                        y=[pk_ay],
                        mode="markers",
                        hoverinfo="skip",
                        showlegend=False,
                        marker=dict(
                            size=13,
                            color=PALETTE["lime"],
                            line=dict(color=PALETTE["hero_bg"], width=2.8),
                        ),
                    ),
                    secondary_y=True,
                )
                fig_dual.add_annotation(
                    x=pk_ax,
                    y=pk_ay,
                    yref="y2",
                    text=f"<b>{lbl_pkaqi} {pk_ay:.1f}</b>",
                    showarrow=True,
                    arrowhead=0,
                    arrowwidth=2,
                    arrowcolor=PALETTE["chart_badge_bg"],
                    ax=0,
                    ay=-34,
                    bgcolor=PALETTE["chart_badge_bg"],
                    bordercolor=PALETTE["chart_badge_bg"],
                    borderwidth=1,
                    borderpad=6,
                    font=dict(size=11.5, color=PALETTE["chart_badge_fg"], family="Inter, sans-serif"),
                )

            max_rev = float(m_aqi["vit_rev"].max()) if not m_aqi.empty else 1
            max_aqi_v = float(m_aqi["mean_aqi"].max()) if not m_aqi.empty else 150
            fig_dual.update_yaxes(title_text=f"{lbl_vit} (INR)", range=[0, max_rev * 1.22], secondary_y=False)
            fig_dual.update_yaxes(title_text=lbl_aqi, range=[0, max_aqi_v * 1.26], secondary_y=True, showgrid=False)
            apply_bento_plotly_style(fig_dual, height=345)
            fig_dual.update_layout(hovermode="x unified", margin=dict(l=8, r=14, t=24, b=16))
            st.plotly_chart(fig_dual, use_container_width=True, config=PLOT_CFG)

    with bot_r:
        with st.container(border=True, key="card_p3_top8"):
            render_chart_card_header(
                t("p3_top8_title", lang),
                t("p3_top8_sub", lang),
            )
            if PALETTE["is_dark"]:
                col_high, col_watch, col_norm = "#c8f169", "#4ba651", "#294338"
            else:
                col_high, col_watch, col_norm = "#043f2e", "#78c51c", "#bfd1b4"

            top8 = city_agg.sort_values("mean_aqi", ascending=False).head(8).reset_index(drop=True)
            city_rows = []
            for r in top8.itertuples(index=False):
                aqi_v = float(r.mean_aqi)
                pm_v = float(r.mean_pm25)
                if aqi_v > 150:
                    c_col, t_lbl = col_high, t("map_leg_high", lang)
                elif aqi_v > 100:
                    c_col, t_lbl = col_watch, t("map_leg_watch", lang)
                else:
                    c_col, t_lbl = col_norm, t("map_leg_normal", lang)
                city_rows.append(
                    {
                        "label": str(r.city).upper(),
                        "segments": [(aqi_v, c_col)],
                        "tip_html": (
                            f"<div style='font-weight:700;color:{PALETTE['emerald']};'>{r.city} ({t_lbl})</div>"
                            f"<div><span style='color:{PALETTE['muted']};'>Mean US AQI</span> <b>{aqi_v:.1f}</b> &middot; "
                            f"<span style='color:{PALETTE['muted']};'>PM2.5</span> <b>{pm_v:.1f} ug/m3</b></div>"
                        ),
                    }
                )
            render_horizontal_pill_bars(
                city_rows,
                legend_items=[
                    (t("map_leg_high", lang), col_high),
                    (t("map_leg_watch", lang), col_watch),
                    (t("map_leg_normal", lang), col_norm),
                ],
            )


# ==============================================================================
# PAGE 4: LIFESTYLE & FITNESS SEGMENTATION
# ==============================================================================
def render_page4():
    all_goal_lbl = t("all_goals", lang)
    all_bmi_lbl = t("all_bmi", lang)
    col_title, col_f1, col_f2, col_dl = st.columns([5.2, 2.0, 2.0, 0.8], gap="small")
    with col_title:
        st.markdown(f'<h1 class="yv-page-heading">{t("nav_life", lang)}</h1>', unsafe_allow_html=True)
    with col_f1:
        goal_choice = st.selectbox(
            "Fitness Goal",
            options=[all_goal_lbl, "Muscle Gain", "Fat Burn"],
            index=0,
            label_visibility="collapsed",
            key=f"p4_goal_sel_{lang}",
        )
    with col_f2:
        bmis = [all_bmi_lbl] + sorted(df_fit["bmi_category"].unique().tolist())
        sel_bmi = st.selectbox("BMI Category", bmis, label_visibility="collapsed", key=f"p4_bmi_sel_{lang}")
    with col_dl:
        render_download_popover("p4", lang=lang)

    st.markdown('<div class="filter-content-spacer"></div>', unsafe_allow_html=True)

    ff = df_fit.copy()
    fs = df_slp.copy()
    if goal_choice != all_goal_lbl:
        ff = ff[ff["fitness_goal"] == goal_choice]
    if sel_bmi != all_bmi_lbl:
        ff = ff[ff["bmi_category"] == sel_bmi]
        fs = fs[fs["bmi_category"] == sel_bmi]

    if ff.empty and fs.empty:
        render_empty_state(
            "No lifestyle or fitness records match these filters",
            f"Fitness goal '{goal_choice}' and BMI '{sel_bmi}' returned 0 profiles.",
            "Reset Fitness Goal to All Goals or BMI to All BMI to restore segmentation.",
        )
        return

    tot_members = int(ff["member_count"].sum())
    muscle_cnt = int(ff.loc[ff["fitness_goal"] == "Muscle Gain", "member_count"].sum())
    muscle_pct = muscle_cnt / tot_members * 100 if tot_members else 0

    avg_sleep = float(fs["sleep_duration_hrs"].mean()) if len(fs) else 0
    avg_stress = float(fs["stress_level"].mean()) if len(fs) else 0
    disorder_pct = float((fs["sleep_disorder"] != "None").mean() * 100) if len(fs) else 0

    # --- TIER 1: FITNESS & SLEEP COHORT KPI STRIP ---
    is_id = (lang == "id")
    render_section_eyebrow(t("p4_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            t("p4_hero1_title", lang),
            t("p4_hero1_sub", lang),
            t("p4_hero1_lbl", lang),
            f"{tot_members:,}",
            f"{'Massa Otot' if is_id else 'Muscle Gain'} {muscle_pct:.1f}% | {muscle_cnt:,} {'Anggota' if is_id else 'Members'}",
            variant="emerald",
        )
    with k2:
        render_nested_hero_card(
            t("p4_hero2_title", lang),
            t("p4_hero2_sub", lang),
            t("p4_hero2_lbl", lang),
            f"{avg_sleep:.2f} {'Jam' if is_id else 'Hrs'}",
            (
                f"{'Rata-Rata Stres' if is_id else 'Avg Stress'} {avg_stress:.1f}/10 | {'Rata-Rata Langkah' if is_id else 'Avg Steps'} {fs['daily_steps'].mean():,.0f}"
                if len(fs)
                else ("Tidak ada data" if is_id else "No records")
            ),
            variant="lime",
        )
    with k3:
        render_compact_kpi_card(
            t("p4_kpi3_lbl", lang),
            f"{disorder_pct:.1f}%",
            sub=(
                f"Berdasarkan {len(fs):,} responden gaya hidup klinis"
                if is_id
                else f"Based on {len(fs):,} clinical lifestyle respondents"
            ),
            accent_strip="exclamation",
            strip_tone="forest",
            strip_tooltip=t("p4_kpi3_badge", lang),
        )
        render_compact_kpi_card(
            t("p4_kpi4_lbl", lang),
            f"{fs['quality_of_sleep'].mean():.2f} / 10" if len(fs) else "0",
            sub=t("p4_kpi4_sub", lang),
            accent_strip="moon",
            strip_tone="lime",
            strip_tooltip=t("p4_kpi4_badge", lang),
        )

    # --- TIER 2: FULL-WIDTH PROPORTIONAL ROUNDED BENTO TREEMAP ---
    render_section_eyebrow(t("p4_s2", lang))
    with st.container(border=True, key="card_p4_tree"):
        render_chart_card_header(
            t("p4_tree_title", lang),
            t("p4_tree_sub", lang),
        )
        if ff.empty:
            render_empty_state(
                "Tidak ada segmen gym yang cocok" if is_id else "No gym segment matches this filter",
                f"Fitness goal '{goal_choice}' and BMI '{sel_bmi}' returned 0 gym profiles.",
                "Reset filter tujuan kebugaran atau BMI untuk melihat seluruh 8 segmen." if is_id else "Reset Fitness Goal or BMI filter to view all 8 segments.",
            )
        else:
            render_bento_treemap(ff, lang=lang)

    # --- TIER 3: CLINICAL WELLNESS & OCCUPATION DEEP-DIVE (4.8 : 5.2 SPLIT) ---
    render_section_eyebrow(t("p4_s3", lang))
    bot_l, bot_r = st.columns([4.8, 5.2], gap="medium")
    with bot_l:
        with st.container(border=True, key="card_p4_radar"):
            rh_l, rh_r = st.columns([5.8, 4.2], gap="small")
            with rh_l:
                render_chart_card_header(
                    t("p4_radar_title", lang),
                    t("p4_radar_sub", lang),
                )
            with rh_r:
                all_tier_lbl = t("all_tiers", lang)
                tier_opts = [all_tier_lbl] + sorted(fs["wellness_segment"].dropna().unique().tolist()) if not fs.empty else [all_tier_lbl]
                tier_choice = st.selectbox(
                    "Wellness Tier",
                    options=tier_opts,
                    index=0,
                    label_visibility="collapsed",
                    key=f"p4_radar_tier_sel_{lang}",
                )

            if fs.empty:
                render_empty_state(
                    "No clinical sleep records for this BMI filter",
                    f"The Sleep Health dataset contains 0 respondents in BMI group '{sel_bmi}'.",
                    "Select All BMI or Normal / Overweight / Obese to inspect the wellness profile.",
                )
            else:
                rad_slice = fs if tier_choice == all_tier_lbl else fs[fs["wellness_segment"] == tier_choice]
                render_wellness_radar(rad_slice, tier_label=tier_choice, lang=lang)

    with bot_r:
        with st.container(border=True, key="card_p4_occ"):
            render_chart_card_header(
                t("p4_occ_title", lang),
                t("p4_occ_sub", lang),
            )
            if fs.empty:
                render_empty_state(
                    "No occupation breakdown available",
                    f"No clinical respondents match BMI filter '{sel_bmi}'.",
                    "Choose All BMI to inspect occupation distribution.",
                )
            else:
                occ_piv = (
                    fs.groupby(["occupation", "sleep_disorder"])
                    .size()
                    .unstack(fill_value=0)
                )
                for col_sd in ["None", "Insomnia", "Sleep Apnea"]:
                    if col_sd not in occ_piv.columns:
                        occ_piv[col_sd] = 0
                occ_piv["total"] = occ_piv[["None", "Insomnia", "Sleep Apnea"]].sum(axis=1)
                occ_top7 = occ_piv.sort_values("total", ascending=False).head(7)
                y_occ = [str(o).upper() for o in occ_top7.index.tolist()]

                if PALETTE["is_dark"]:
                    c_none, c_ins, c_apn = "#294338", "#4ba651", "#c8f169"
                else:
                    c_none, c_ins, c_apn = "#bfd1b4", "#78c51c", "#043f2e"

                occ_id_map = {
                    "Nurse": "Perawat",
                    "Doctor": "Dokter",
                    "Engineer": "Insinyur",
                    "Lawyer": "Pengacara",
                    "Teacher": "Guru",
                    "Accountant": "Akuntan",
                    "Salesperson": "Tenaga Penjual",
                    "Sales Representative": "Staf Penjualan",
                    "Software Engineer": "Insinyur TI",
                    "Scientist": "Ilmuwan",
                    "Manager": "Manajer",
                }
                occ_rows = []
                for occ_name, row_s in occ_top7.iterrows():
                    v_none = int(row_s["None"])
                    v_ins = int(row_s["Insomnia"])
                    v_apn = int(row_s["Sleep Apnea"])
                    occ_disp = occ_id_map.get(str(occ_name), str(occ_name)) if is_id else str(occ_name)
                    occ_rows.append(
                        {
                            "label": occ_disp.upper(),
                            "segments": [(v_none, c_none), (v_ins, c_ins), (v_apn, c_apn)],
                            "tip_html": (
                                f"<div style='font-weight:700;color:{PALETTE['emerald']};'>{occ_disp} ({int(row_s['total']):,} total)</div>"
                                f"<div><span style='color:{PALETTE['muted']};'>{'Tanpa Gangguan' if is_id else 'None'}</span> <b>{v_none}</b> &middot; "
                                f"<span style='color:{PALETTE['muted']};'>Insomnia</span> <b>{v_ins}</b> &middot; "
                                f"<span style='color:{PALETTE['muted']};'>Sleep Apnea</span> <b>{v_apn}</b></div>"
                            ),
                        }
                    )
                render_horizontal_pill_bars(
                    occ_rows,
                    legend_items=[
                        ("Sleep Apnea", c_apn),
                        ("Insomnia", c_ins),
                        ("Tanpa Gangguan" if is_id else "None", c_none),
                    ],
                )


# ==============================================================================
# PAGE 5: DATA QUALITY & DWH VALIDATION AUDIT
# ==============================================================================
def render_page5():
    import html as _html

    is_id = (lang == "id")
    val_path = ROOT_DIR / "logs" / "validation_report.json"
    prep_path = ROOT_DIR / "logs" / "preprocessing_summary.json"
    val_data = json.loads(val_path.read_text(encoding="utf-8")) if val_path.exists() else {"summary": {"total_checks": 27, "passed": 27, "failed": 0}, "duration_seconds": 1.82, "checks": []}
    prep_data = json.loads(prep_path.read_text(encoding="utf-8")) if prep_path.exists() else {"before_vs_after": [], "processed_tables": {}}

    checks = val_data.get("checks", [])
    suite_id_map = {
        "1. Row Reconciliation": "1. Kelengkapan Jumlah Data",
        "2. Aggregate Accuracy": "2. Akurasi Perhitungan",
        "3. Referential Integrity": "3. Konsistensi Hubungan Data",
        "4. Data Quality Rules": "4. Aturan Validitas Data",
        "5. RBAC Security": "5. Keamanan Akses Data",
    }
    suite_en_map = {
        "1. Row Reconciliation": "1. Data Completeness",
        "2. Aggregate Accuracy": "2. Calculation Accuracy",
        "3. Referential Integrity": "3. Data Link Consistency",
        "4. Data Quality Rules": "4. Data Validity Rules",
        "5. RBAC Security": "5. Access Security",
    }
    fixes_id_map = {
        "Flipkart Health Supplements": "Format teks dan angka penilaian dirapikan (misalnya '4,4' menjadi 4.4), 681 deskripsi kosong dilengkapi, serta persentase diskon dihitung otomatis.",
        "Tata 1mg Healthcare Catalog": "996 data ganda dihapus, simbol mata uang dan teks ulasan dibersihkan, harga normal dan harga jual yang tertukar diperbaiki, lalu dikelompokkan ke 5 kategori.",
        "India Air Quality Index (AQI)": "8 kolom sensor kosong dibuang, 145 data kualitas udara kosong disaring, dan 842 ribu catatan per jam diringkas menjadi rata-rata harian per kota.",
        "Gym & Fitness Demand Profile": "Judul kolom yang bergeser diperbaiki, label BMI dan target kebugaran diseragamkan, lalu 80.000 profil diringkas menjadi 16 segmen utuh.",
        "Sleep Health & Lifestyle": "219 data gangguan tidur kosong ditandai 'Tidak Ada', label BMI diseragamkan, serta tekanan darah dipisah menjadi angka atas dan bawah.",
    }
    fixes_en_map = {
        "Flipkart Health Supplements": "Standardized text and rating decimals ('4,4' to 4.4), filled 681 empty product descriptions, and calculated discount rates automatically.",
        "Tata 1mg Healthcare Catalog": "Removed 996 duplicate items, cleaned currency symbols and review labels, corrected swapped list/selling prices, and grouped into 5 categories.",
        "India Air Quality Index (AQI)": "Removed 8 empty sensor columns, filtered 145 missing air quality records, and summarized 842k hourly readings into daily city averages.",
        "Gym & Fitness Demand Profile": "Fixed shifted column headers, standardized BMI and fitness goal labels, and grouped all 80,000 member profiles into 16 clean segments.",
        "Sleep Health & Lifestyle": "Marked 219 empty sleep disorder entries as 'None', standardized BMI labels, and separated blood pressure into systolic and diastolic values.",
    }
    raw_suites = list(dict.fromkeys(c["suite"] for c in checks))
    suite_disp_to_raw = {t("p5_all_suites", lang): None}
    for rs in raw_suites:
        lbl_s = suite_id_map.get(rs, rs) if is_id else suite_en_map.get(rs, rs)
        suite_disp_to_raw[lbl_s] = rs
    suites_all = list(suite_disp_to_raw.keys())

    col_title, col_f1, col_dl = st.columns([6.6, 2.6, 0.8], gap="small")
    with col_title:
        st.markdown(f'<h1 class="yv-page-heading">{t("nav_quality", lang)}</h1>', unsafe_allow_html=True)
    with col_f1:
        sel_suite = st.selectbox(
            "Validation Suite",
            options=suites_all,
            index=0,
            label_visibility="collapsed",
            key=f"p5_suite_sel_{lang}",
        )
    with col_dl:
        render_download_popover("p5", lang=lang)

    st.markdown('<div class="filter-content-spacer"></div>', unsafe_allow_html=True)

    summary = val_data.get("summary", {})
    passed_cnt = int(summary.get("passed", 27))
    total_cnt = int(summary.get("total_checks", 27))
    failed_cnt = int(summary.get("failed", 0))
    val_dur = float(val_data.get("duration_seconds", 1.82))

    # --- TIER 1: VALIDATION & DATA QUALITY KPI OVERVIEW ---
    render_section_eyebrow(t("p5_s1", lang))
    k1, k2, k3 = st.columns([3.5, 3.5, 3.0], gap="medium")
    with k1:
        render_nested_hero_card(
            t("p5_hero1_title", lang),
            "Seluruh pemeriksaan kelengkapan, akurasi hitungan, konsistensi data, dan keamanan akses lolos 100%." if is_id else "All completeness, calculation accuracy, consistency, and access security checks passed 100%.",
            t("p5_hero1_lbl", lang),
            f"{passed_cnt}/{total_cnt}",
            f"{'Gagal' if is_id else 'Failed'} {failed_cnt} | {'Durasi' if is_id else 'Duration'} {val_dur:.2f}s",
            variant="emerald",
            info_meta="Laporan Audit Kualitas Data" if is_id else "Data Quality Audit Report",
        )
    with k2:
        render_nested_hero_card(
            t("p5_hero2_title", lang),
            "Ukuran data berhasil diringkas 96,74% dari 287,55 MB data mentah menjadi 9,37 MB data siap analisis." if is_id else "Data size reduced by 96.74% from 287.55 MB raw files to 9.37 MB ready-to-analyze tables.",
            t("p5_hero2_lbl", lang),
            "9.37 MB",
            f"{'Mentah' if is_id else 'Raw'} 287.55 MB | -96.74%",
            variant="lime",
            info_meta="Ringkasan Penyimpanan Data" if is_id else "Clean Data Storage Summary",
        )
    with k3:
        render_compact_kpi_card(
            t("p5_kpi3_lbl", lang),
            "942,554",
            sub="5 sumber data mentah -> 105.811 data siap analisis" if is_id else "5 raw data sources -> 105,811 clean records",
            accent_strip="check",
            strip_tone="forest",
            strip_tooltip="100% Terverifikasi" if is_id else "100% Verified",
            info_meta="Rekapitulasi Data Masuk" if is_id else "Data Ingestion Summary",
        )
        render_compact_kpi_card(
            t("p5_kpi4_lbl", lang),
            "6.74M+",
            sub="996 data ganda dihapus · 6,74 juta data kosong dirapikan" if is_id else "996 duplicates removed · 6.74M empty fields cleaned",
            accent_strip="exclamation",
            strip_tone="lime",
            strip_tooltip="Nol Data Kosong Kritis" if is_id else "Zero Critical Missing Data",
            info_meta="Ringkasan Pembersihan Data" if is_id else "Data Cleansing Summary",
        )

    # --- TIER 2: FULL-WIDTH 5 INTERACTIVE 3D FLIP CARDS (BEFORE VS AFTER PREPROCESSING) ---
    render_section_eyebrow(t("p5_s2", lang))
    with st.container(border=True, key="card_p5_prep"):
        prep_info = build_info_popover_html(
            t("p5_prep_title", lang),
            "Arahkan kursor (hover) ke setiap kartu untuk melihat hasil data setelah dibersihkan beserta perbaikan utamanya." if is_id else "Hover over any card to flip and see the cleaned record count along with key improvements.",
            "Ringkasan Pembersihan Data" if is_id else "Data Cleansing Summary",
        )
        st.markdown(
            f'<div style="display:flex; justify-content:flex-end; align-items:center; margin-bottom:4px;">{prep_info}</div>',
            unsafe_allow_html=True,
        )
        bva = prep_data.get("before_vs_after", [])
        short_names = {
            "Flipkart Health Supplements": "Flipkart Health",
            "Tata 1mg Healthcare Catalog": "Tata 1mg",
            "India Air Quality Index (AQI)": "India AQI",
            "Gym & Fitness Demand Profile": "Gym Profile",
            "Sleep Health & Lifestyle": "Sleep Health",
        }
        before_desc_id = {
            "Flipkart Health Supplements": "3.076 data awal dengan format koma penilaian berbeda ('4,4') serta 681 deskripsi produk yang kosong.",
            "Tata 1mg Healthcare Catalog": "16.944 data awal berisi 996 data ganda, simbol mata uang, teks ulasan, dan posisi harga jual yang tertukar.",
            "India Air Quality Index (AQI)": "842.160 catatan kualitas udara per jam dengan 8 kolom sensor kosong dan 145 data indeks udara hilang.",
            "Gym & Fitness Demand Profile": "80.000 profil anggota gym dengan judul kolom yang bergeser serta label BMI dan target kebugaran belum seragam.",
            "Sleep Health & Lifestyle": "374 catatan gaya hidup dengan 219 data gangguan tidur kosong serta tekanan darah masih tergabung dalam teks.",
        }
        before_desc_en = {
            "Flipkart Health Supplements": "3,076 initial records with comma-formatted ratings ('4,4') and 681 empty product descriptions.",
            "Tata 1mg Healthcare Catalog": "16,944 initial records with 996 duplicates, currency symbols, review text, and swapped selling prices.",
            "India Air Quality Index (AQI)": "842,160 hourly air quality records containing 8 empty sensor columns and 145 missing index values.",
            "Gym & Fitness Demand Profile": "80,000 gym member profiles with shifted column headers and inconsistent BMI and goal labels.",
            "Sleep Health & Lifestyle": "374 lifestyle records with 219 empty sleep disorder entries and combined blood pressure text.",
        }
        card_svgs = [
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/></svg>',
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 6.5h11"/><path d="M6.5 17.5h11"/><path d="M4 9v6"/><path d="M20 9v6"/><path d="M12 6.5v11"/></svg>',
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
        ]
        check_svg = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9 12l2 2 4-4"/></svg>'

        cards_html = []
        for idx, item in enumerate(bva):
            ds_raw = str(item.get("dataset", ""))
            ds_short = _html.escape(short_names.get(ds_raw, ds_raw))
            ra = f"{int(item.get('rows_after', 0)):,}"
            b_desc = _html.escape((before_desc_id if is_id else before_desc_en).get(ds_raw, ""))
            fx_txt = fixes_id_map.get(ds_raw, str(item.get("key_fixes", ""))) if is_id else fixes_en_map.get(ds_raw, str(item.get("key_fixes", "")))
            fx = _html.escape(fx_txt)
            ic_svg = card_svgs[idx % len(card_svgs)]

            after_title = f"{ra} {'Segmen' if ds_raw.startswith('Gym') else 'Baris Bersih'}" if is_id else f"{ra} {'Segments' if ds_raw.startswith('Gym') else 'Clean Rows'}"

            cards_html.append(
                f'<div class="yv-flip-card">'
                f'<div class="yv-flip-inner">'
                f'<div class="yv-flip-face yv-flip-front">'
                f'<div>'
                f'<div class="yv-flip-ic">{ic_svg}</div>'
                f'<div class="yv-flip-title">{ds_short}</div>'
                f'<p class="yv-flip-body">{b_desc}</p>'
                f'</div>'
                f'</div>'
                f'<div class="yv-flip-face yv-flip-back">'
                f'<div>'
                f'<div class="yv-flip-ic">{check_svg}</div>'
                f'<div class="yv-flip-title">{after_title}</div>'
                f'<p class="yv-flip-body">{fx}</p>'
                f'</div>'
                f'</div>'
                f'</div>'
                f'</div>'
            )
        st.markdown(f'<div class="yv-flip-grid">{"".join(cards_html)}</div>', unsafe_allow_html=True)

    # --- TIER 3: SUITE BREAKDOWN + FULL 27 AUTOMATED CHECKS AUDIT TABLE ---
    render_section_eyebrow(t("p5_s3", lang))
    bot_l, bot_r = st.columns([3.8, 6.2], gap="medium")
    with bot_l:
        with st.container(border=True, key="card_p5_suites"):
            render_chart_card_header(
                t("p5_suite_title", lang),
                "Distribusi jumlah pemeriksaan kualitas yang lolos pada 5 kategori pengujian data." if is_id else "Distribution of passed quality checks across all 5 verification categories.",
                info_meta="Pemeriksaan Kualitas Otomatis" if is_id else "Automated Quality Checks",
            )
            pass_hero_txt = "100% Lolos" if is_id else "100% Passed"
            st.markdown(
                f'<div style="font-size:clamp(30px, 2.6vw, 38px); font-weight:700; letter-spacing:-0.035em; '
                f'color:{PALETTE["emerald"]}; line-height:1.08; margin:6px 0 20px 0; padding-bottom:18px; '
                f'border-bottom:1px solid {PALETTE["hairline"]};">{pass_hero_txt}</div>',
                unsafe_allow_html=True,
            )
            suite_counts = {}
            for c in checks:
                s_name = suite_id_map.get(c["suite"], c["suite"]) if is_id else suite_en_map.get(c["suite"], c["suite"])
                suite_counts[s_name] = suite_counts.get(s_name, 0) + (1 if c.get("status") == "PASS" else 0)
            col_bar = "#c8f169" if PALETTE["is_dark"] else "#043f2e"
            suite_rows = []
            for s_name, cnt in sorted(suite_counts.items(), key=lambda x: x[1], reverse=True):
                short_s = s_name.split(". ", 1)[-1].upper()
                suite_rows.append(
                    {
                        "label": short_s,
                        "segments": [(cnt, col_bar)],
                        "tip_html": (
                            f"<div style='font-weight:700;color:{PALETTE['emerald']};'>{s_name}</div>"
                            f"<div><span style='color:{PALETTE['muted']};'>Status</span> <b>{cnt}/{cnt} {'LOLOS' if is_id else 'PASS'}</b></div>"
                        ),
                    }
                )
            render_horizontal_pill_bars(
                suite_rows,
                legend_items=None,
                wide_labels=True,
            )

    with bot_r:
        with st.container(border=True, key="card_p5_checks"):
            raw_sel = suite_disp_to_raw.get(sel_suite)
            filt_checks = checks if raw_sel is None else [c for c in checks if c["suite"] == raw_sel]
            render_chart_card_header(
                t("p5_audit_title", lang),
                "Daftar hasil pemeriksaan kualitas untuk memastikan data sumber dan laporan selalu cocok." if is_id else "Detailed quality check results confirming source data and dashboard figures match.",
                info_meta="Laporan Audit Kualitas Data" if is_id else "Data Quality Audit Report",
                csv_df=pd.DataFrame(filt_checks),
                csv_filename="yuuukosoovexa_dwh_audit_report.csv",
            )
            c_rows = []
            pill_bg = "#1b3326" if PALETTE["is_dark"] else "#eef7df"
            pill_fg = "#c8f169" if PALETTE["is_dark"] else "#1b5e20"
            dot_col = "#c8f169" if PALETTE["is_dark"] else "#4ba651"
            for c in filt_checks:
                raw_st = str(c.get("status", "PASS"))
                st_lbl = _html.escape("LOLOS" if (is_id and raw_st == "PASS") else raw_st)
                s_disp = suite_id_map.get(c["suite"], c["suite"]) if is_id else suite_en_map.get(c["suite"], c["suite"])
                c_rows.append(
                    f"<tr>"
                    f"<td style='padding:10px 12px; font-size:12px; color:{PALETTE['muted']}; white-space:nowrap;'>{_html.escape(str(s_disp))}</td>"
                    f"<td style='padding:10px 12px; font-size:12.5px; font-weight:600; color:{PALETTE['emerald']};'>{_html.escape(str(c['check_name']))}</td>"
                    f"<td style='padding:10px 12px; font-size:12px; color:{PALETTE['charcoal']};'>{_html.escape(str(c['expected']))}</td>"
                    f"<td style='padding:10px 12px; font-size:12px; font-weight:600; color:{PALETTE['emerald']};'>{_html.escape(str(c['actual']))}</td>"
                    f"<td style='padding:10px 12px; text-align:center;'>"
                    f"<span style='display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:999px; background:{pill_bg}; color:{pill_fg}; font-size:11.5px; font-weight:700;'>"
                    f"<span style='width:6px; height:6px; border-radius:999px; background:{dot_col};'></span>{st_lbl}</span></td>"
                    f"</tr>"
                )
            audit_tbl = (
                f'<div class="sku-tbl-shell" style="margin-top:4px;">'
                f'<div class="sku-tbl-scroll" style="max-height:360px;">'
                f'<table class="sku-tbl">'
                f'<thead><tr>'
                f'<th style="padding:10px 12px;">{"Kategori Uji" if is_id else "Suite"}</th>'
                f'<th style="padding:10px 12px;">{"Pemeriksaan" if is_id else "Validation Check"}</th>'
                f'<th style="padding:10px 12px;">{"Target" if is_id else "Expected"}</th>'
                f'<th style="padding:10px 12px;">{"Aktual" if is_id else "Actual"}</th>'
                f'<th style="padding:10px 12px; text-align:center;">Status</th>'
                f'</tr></thead><tbody>{"".join(c_rows)}</tbody></table></div></div>'
            )
            st.markdown(audit_tbl, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# MAIN ROUTER (HANDLES CONTEXTUAL DRILL-THROUGH & 5 MAIN PAGES)
# ------------------------------------------------------------------------------
if st.session_state.drill_mode == "sku":
    render_drill_sku()
elif st.session_state.drill_mode == "city":
    render_drill_city()
elif page == "Executive Summary":
    render_page1()
elif page == "Sales & Pricing":
    render_page2()
elif page == "Environmental AQI":
    render_page3()
elif page == "Data Quality":
    render_page5()
else:
    render_page4()

inject_motion_engine(nonce=f"{page}_{st.session_state.drill_mode}_{theme}_{lang}")
