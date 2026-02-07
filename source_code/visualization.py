import plotly.express as px


def line_chart(df):
    if df is None or df.empty:
        return None
    return px.line(df, x="month", y="total", markers=True)


def bar_chart(df, x, y):
    if df is None or df.empty:
        return None
    return px.bar(df, x=x, y=y)


def hist_chart(df):
    if df is None or df.empty:
        return None
    return px.histogram(df, x="rating", nbins=20)
