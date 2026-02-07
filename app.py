import streamlit as st
import duckdb
import pandas as pd

from source_code.data_loader import load_and_store
from source_code.queries import (
    build_where,
    kpi_cards,
    kpi_time,
    kpi_region,
    kpi_product,
    kpi_rating,
)
from source_code.visualization import line_chart, bar_chart, hist_chart


st.set_page_config(page_title="KPI App", layout="wide")
st.title("📊 Application KPI — Streamlit + DuckDB")

DB_PATH = "database/app.duckdb"
TABLE = "fact"

con = duckdb.connect(DB_PATH)

uploaded = st.sidebar.file_uploader("📤 Téléverser un CSV", type=["csv"])

if not uploaded:
    st.info("Ajoute un CSV pour démarrer.")
    st.stop()

df, spec = load_and_store(con, uploaded, table=TABLE)

if spec.name == "unknown":
    st.error("Dataset non reconnu.")
    st.write(df.columns.tolist())
    st.stop()

st.sidebar.success(f"Dataset détecté : {spec.name}")

# Filters
date_range = None
regions = None
products = None

if spec.date_col and spec.date_col in df.columns:
    min_d = pd.to_datetime(df[spec.date_col]).min()
    max_d = pd.to_datetime(df[spec.date_col]).max()
    if pd.notna(min_d) and pd.notna(max_d):
        date_range = st.sidebar.date_input(
            "📅 Filtrer par date",
            value=(min_d.date(), max_d.date()),
        )

if spec.region_col and spec.region_col in df.columns:
    regions = st.sidebar.multiselect(
        "🌍 Région",
        sorted(df[spec.region_col].dropna().astype(str).unique()),
    )

if spec.product_col and spec.product_col in df.columns:
    products = st.sidebar.multiselect(
        "🧾 Produit",
        sorted(df[spec.product_col].dropna().astype(str).unique()),
    )

where_sql, params = build_where(spec, date_range, regions, products)

# KPI cards
n, total, avg, rating = kpi_cards(con, TABLE, spec, where_sql, params)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Lignes", n)
c2.metric("💰 Total", "N/A" if total is None else round(total, 2))
c3.metric("📈 Moyenne", "N/A" if avg is None else round(avg, 2))
c4.metric("⭐ Note moyenne", "N/A" if rating is None else round(rating, 2))

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("1) Évolution")
    fig = line_chart(kpi_time(con, TABLE, spec, where_sql, params))
    if fig:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("2) Par région")
    fig = bar_chart(kpi_region(con, TABLE, spec, where_sql, params), "region", "value")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("3) Par produit")
    fig = bar_chart(kpi_product(con, TABLE, spec, where_sql, params), "product", "value")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("4) Distribution des notes")
    fig = hist_chart(kpi_rating(con, TABLE, spec, where_sql, params))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
