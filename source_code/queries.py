import pandas as pd


def build_where(spec, date_range, regions, products):
    clauses = []
    params = []

    # Date range
    if spec.date_col and date_range:
        d1 = pd.Timestamp(date_range[0])
        d2 = pd.Timestamp(date_range[1])
        clauses.append(f"{spec.date_col} BETWEEN ? AND ?")
        params.extend([d1, d2])

    # Region filter
    if spec.region_col and regions:
        clauses.append(f"{spec.region_col} IN (SELECT * FROM UNNEST(?))")
        params.append(regions)

    # Product filter
    if spec.product_col and products:
        clauses.append(f"{spec.product_col} IN (SELECT * FROM UNNEST(?))")
        params.append(products)

    where_sql = " WHERE " + " AND ".join(clauses) if clauses else ""
    return where_sql, params


def _extra_where_or_and(where_sql: str) -> str:
   
    return " AND " if where_sql.strip().startswith("WHERE") else " WHERE "


def get_summary_kpis(con, table, spec, where_sql, params):
    """
    KPIs en cartes:
    - nb lignes
    - total (SUM)
    - moyenne (AVG)
    - note moyenne (AVG rating)
    """
    n = con.execute(f"SELECT COUNT(*) FROM {table}{where_sql}", params).fetchone()[0]

    total = avg = None
    if spec.amount_col:
        total, avg = con.execute(
            f"SELECT SUM({spec.amount_col}), AVG({spec.amount_col}) FROM {table}{where_sql}",
            params,
        ).fetchone()

    rating = None
    if spec.rating_col:
        rating = con.execute(
            f"SELECT AVG({spec.rating_col}) FROM {table}{where_sql}",
            params,
        ).fetchone()[0]

    return n, total, avg, rating


def get_time_kpi(con, table, spec, where_sql, params):
   
    if not spec.date_col or not spec.amount_col:
        return None

    agg = "AVG" if spec.name == "airbnb" else "SUM"
    extra = _extra_where_or_and(where_sql)

    q = f"""
    SELECT DATE_TRUNC('month', {spec.date_col}) AS month,
           {agg}({spec.amount_col}) AS total
    FROM {table}
    {where_sql}
    {extra}{spec.amount_col} IS NOT NULL
    GROUP BY 1
    ORDER BY 1
    """
    return con.execute(q, params).df()


def get_top_regions(con, table, spec, where_sql, params, top_n: int = 10):
    """
    Top régions selon:
    - SUM(amount_col) si disponible
    - sinon COUNT(*)
    """
    if not spec.region_col:
        return None

    metric = f"SUM({spec.amount_col})" if spec.amount_col else "COUNT(*)"

    q = f"""
    SELECT {spec.region_col} AS region,
           {metric} AS value
    FROM {table}
    {where_sql}
    GROUP BY 1
    ORDER BY value DESC
    LIMIT {int(top_n)}
    """
    return con.execute(q, params).df()


def get_top_products(con, table, spec, where_sql, params, top_n: int = 10):
    """
    Top produits selon:
    - SUM(amount_col) si disponible
    - sinon COUNT(*)
    Le nombre de lignes est piloté par top_n (slider).
    """
    if not spec.product_col:
        return None

    metric = f"SUM({spec.amount_col})" if spec.amount_col else "COUNT(*)"

    q = f"""
    SELECT {spec.product_col} AS product,
           {metric} AS value
    FROM {table}
    {where_sql}
    GROUP BY 1
    ORDER BY value DESC
    LIMIT {int(top_n)}
    """
    return con.execute(q, params).df()


def get_rating_distribution(con, table, spec, where_sql, params):
    """
    Distribution des notes (histogramme).
    """
    if not spec.rating_col:
        return None

    extra = _extra_where_or_and(where_sql)

    q = f"""
    SELECT {spec.rating_col} AS rating
    FROM {table}
    {where_sql}
    {extra}{spec.rating_col} IS NOT NULL
    """
    return con.execute(q, params).df()
