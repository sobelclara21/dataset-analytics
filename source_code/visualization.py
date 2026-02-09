import plotly.express as px

def _layout(fig, title: str, subtitle: str | None = None):
    fig.update_layout(
        title={"text": f"{title}<br><sup>{subtitle or ''}</sup>", "x": 0.02},
        margin=dict(l=20, r=20, t=70, b=20),
        height=430,
        hovermode="x unified",
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    return fig


def line_month(df):
    if df is None or df.empty:
        return None

    fig = px.line(df, x="month", y="total", markers=True)
    fig.update_traces(
        mode="lines+markers+text",
        text=df["total"].round(2),
        textposition="top center"
    )
    fig.update_xaxes(tickformat="%b %Y")
    fig.update_yaxes(tickformat=",.0f")
    return _layout(fig, "Évolution mensuelle", "Somme des montants / prix")


def bar_top(df, x, y, title, subtitle=None):
    if df is None or df.empty:
        return None

    fig = px.bar(df, x=x, y=y, text=df[y].round(2))
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_xaxes(tickangle=-25)
    fig.update_yaxes(tickformat=",.0f")
    return _layout(fig, title, subtitle)


def hist_rating(df):
    if df is None or df.empty:
        return None

    fig = px.histogram(df, x="rating", nbins=20)
    fig.update_traces(texttemplate="%{y}", textposition="outside", cliponaxis=False)
    return _layout(fig, "Distribution des notes", "Répartition des ratings")
