import os
import streamlit as st
import duckdb
import pandas as pd

from source_code.data_loader import load_and_store
from source_code.queries import (
    build_where,
    get_summary_kpis,
    get_time_kpi,
    get_top_regions,
    get_top_products,
    get_rating_distribution,
)
from source_code.visualization import line_month, bar_top, hist_rating


# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Dataset-analytics", page_icon="📊", layout="wide")


def fmt_money(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "N/A"
    return f"{x:,.2f}".replace(",", " ")


def fmt_int(x):
    return f"{x:,}".replace(",", " ")


# -------------------- HEADER --------------------
st.markdown(
    """
    <div style="display:flex;align-items:center;justify-content:space-between;">
        <div>
            <h1 style="margin-bottom:0;">📊 Dataset-analytics</h1>
            <p style="margin-top:6px;opacity:0.85;">
                 → KPI & Visualisations
            </p>
        </div>
        <div style="text-align:right; opacity:0.9;">
            <span style="padding:8px 12px;border-radius:999px;background:#161B22;border:1px solid #2d333b;">
                Streamlit • DuckDB • SQL • Plotly
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# -------------------- DB --------------------
DB_PATH = "database/app.duckdb"
TABLE = "fact"

try:
    con = duckdb.connect(DB_PATH)
except Exception:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = duckdb.connect(DB_PATH)


# -------------------- SIDEBAR --------------------
st.sidebar.header("⚙️ Contrôles")
st.sidebar.caption("upload +filtres")
st.sidebar.divider()

uploaded = st.sidebar.file_uploader("📤 Téléverser un CSV", type=["csv"])

reset = st.sidebar.button("🔄 Reset filtres", use_container_width=True)
st.sidebar.divider()

if reset:
    st.session_state.clear()

if not uploaded:
    st.info("➡️ Téléverse un CSV (dataset Shopping ou Airbnb) pour démarrer.")
    st.stop()


# -------------------- LOAD DATA --------------------
df, spec = load_and_store(con, uploaded, table=TABLE)

if spec.name == "unknown":
    st.error("Dataset non reconnu.")
    st.write("Colonnes détectées :", df.columns.tolist())
    st.stop()

badge = "🛒 Shopping Trends" if spec.name == "shopping" else "🏠 Airbnb"
st.success(f"Dataset détecté : **{badge}**")


# -------------------- FILTERS --------------------
date_range = None
regions = None
products = None

# Date filter
if spec.date_col and spec.date_col in df.columns:
    min_d = pd.to_datetime(df[spec.date_col]).min()
    max_d = pd.to_datetime(df[spec.date_col]).max()
    if pd.notna(min_d) and pd.notna(max_d):
        date_range = st.sidebar.date_input(
            "📅 Filtrer par date",
            value=(min_d.date(), max_d.date()),
        )

# Region filter
if spec.region_col and spec.region_col in df.columns:
    region_options = sorted(df[spec.region_col].dropna().astype(str).unique().tolist())
    regions = st.sidebar.multiselect(
        "🌍 Filtrer par région",
        region_options,
        default=region_options[:5] if len(region_options) > 5 else region_options,
    )

# Product filter
if spec.product_col and spec.product_col in df.columns:
    product_options = sorted(df[spec.product_col].dropna().astype(str).unique().tolist())
    products = st.sidebar.multiselect(
        "🧾 Filtrer par produit",
        product_options,
        default=product_options[:5] if len(product_options) > 5 else product_options,
    )

where_sql, params = build_where(spec, date_range, regions, products)


# -------------------- KPI CARDS --------------------
n, total, avg, rating = get_summary_kpis(con, TABLE, spec, where_sql, params)

with st.container(border=True):
    st.subheader("📌 KPIs ")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Lignes", fmt_int(n))
    c2.metric("💰 Total", fmt_money(total))
    c3.metric("📈 Moyenne", fmt_money(avg))
    c4.metric("⭐ Note moyenne", "N/A" if rating is None else f"{rating:.2f}")

st.divider()


# -------------------- VISUALS --------------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Évolution", "🌍 Régions", "🧾 Produits", "⭐ Notes"])

with tab1:
    df_time = get_time_kpi(con, TABLE, spec, where_sql, params)
    fig = line_month(df_time)  
    if fig:
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Graph indisponible (il faut une date + un montant/prix).")

with tab2:
    df_reg = get_top_regions(con, TABLE, spec, where_sql, params, top_n=10)
    fig = bar_top(df_reg, "region", "value", "Top régions", "Top 10")
    if fig:
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Graph indisponible (pas de région détectée).")


with tab3:
    df_prod = get_top_products(con, TABLE, spec, where_sql, params, top_n=10)
    fig = bar_top(df_prod, "product", "value", "Top produits", "Top 10")
    if fig:
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Graph indisponible (pas de produit détecté).")


with tab4:
    df_rat = get_rating_distribution(con, TABLE, spec, where_sql, params)
    fig = hist_rating(df_rat)
    if fig:
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Graph indisponible (pas de colonne note).")

with st.expander("🔎 Aperçu des données (max 200 lignes)"):
    st.dataframe(
        con.execute(f"SELECT * FROM {TABLE}{where_sql} LIMIT 200", params).df(),
        width="stretch"
    )

