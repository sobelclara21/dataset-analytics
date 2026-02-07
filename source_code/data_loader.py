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


def parse_money(series: pd.Series):
    return (
        series.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .astype(float)
    )


def season_to_date(season):
    if not isinstance(season, str):
        return pd.NaT
    season = season.lower()
    mapping = {
        "spring": (3, 15),
        "summer": (6, 15),
        "autumn": (9, 15),
        "fall": (9, 15),
        "winter": (12, 15),
    }
    if season not in mapping:
        return pd.NaT
    return datetime(2024, *mapping[season])


def load_and_store(con, uploaded_file, table="fact"):
    df = pd.read_csv(uploaded_file)

    df.columns = [snake_case(c) for c in df.columns]

    spec = detect_dataset(set(df.columns))

    # Dataset 11
    if spec.name == "shopping":
        if "purchase_amount_(usd)" in df.columns:
            df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount_usd"})

        if "purchase_amount_usd" in df.columns:
            df["purchase_amount_usd"] = parse_money(df["purchase_amount_usd"])

        if "season" in df.columns:
            df["purchase_date"] = df["season"].apply(season_to_date)

    # Dataset 12
    if spec.name == "airbnb":
        if "price" in df.columns:
            df["price"] = parse_money(df["price"])
        if "last_review" in df.columns:
            df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    con.execute(f"DROP TABLE IF EXISTS {table}")
    con.register("tmp", df)
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM tmp")
    con.unregister("tmp")

    return df, spec
