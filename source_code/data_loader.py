import re
from datetime import datetime
import pandas as pd
import duckdb

from source_code.schema import detect_dataset


def snake_case(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "_", text)
    return text.lower()


def parse_money(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .replace({"nan": None, "None": None, "": None, "NA": None, "N/A": None})
    )
    return pd.to_numeric(cleaned, errors="coerce")



def season_to_date(season: str):

    if not isinstance(season, str):
        return pd.NaT
    season = season.strip().lower()
    mapping = {"spring": (3, 15), "summer": (6, 15), "autumn": (9, 15), "fall": (9, 15), "winter": (12, 15)}
    if season not in mapping:
        return pd.NaT
    return datetime(2024, *mapping[season])


def load_and_store(con: duckdb.DuckDBPyConnection, uploaded_file, table="fact"):
    df = pd.read_csv(uploaded_file)

    # 1) normalisation colonnes
    df.columns = [snake_case(c) for c in df.columns]

    # 2) détecter dataset
    spec = detect_dataset(set(df.columns))

    # 3) nettoyage selon dataset
    if spec.name == "shopping":
        # renomme si nécessaire
        if "purchase_amount_(usd)" in df.columns and "purchase_amount_usd" not in df.columns:
            df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount_usd"})

        if "purchase_amount_usd" in df.columns:
            df["purchase_amount_usd"] = parse_money(df["purchase_amount_usd"])

        # date synthétique
        if "season" in df.columns:
            df["purchase_date"] = pd.to_datetime(df["season"].apply(season_to_date), errors="coerce")
        else:
            df["purchase_date"] = pd.NaT

        if "review_rating" in df.columns:
            df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")

    elif spec.name == "airbnb":
        if "price" in df.columns:
            df["price"] = parse_money(df["price"])

        if "last_review" in df.columns:
            df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

        if "review_rate_number" in df.columns:
            df["review_rate_number"] = pd.to_numeric(df["review_rate_number"], errors="coerce")

    # 4) stockage DuckDB
    con.execute(f"DROP TABLE IF EXISTS {table}")
    con.register("tmp", df)
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM tmp")
    con.unregister("tmp")

    return df, spec
