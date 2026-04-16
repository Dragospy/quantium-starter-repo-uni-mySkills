import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = "./formatted_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"
REGION_OPTIONS = ["all", "north", "east", "south", "west"]

REGION_COLORS = {
    "all": "#ff3385",
    "north": "#1f77b4",
    "east": "#2ca02c",
    "south": "#ff7f0e",
    "west": "#9467bd",
}

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")


def build_figure(region: str):
    filtered = df if region == "all" else df[df["region"] == region]
    daily_sales = filtered.groupby("date", as_index=False)["sales"].sum()

    pretty_region = "All Regions" if region == "all" else region.capitalize()
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time — {pretty_region}",
        labels={"date": "Date", "sales": "Sales ($)"},
        color_discrete_sequence=[REGION_COLORS[region]],
    )

    fig.update_traces(line={"width": 3}, mode="lines")
    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_width=2,
        line_dash="dash",
        line_color="#c2185b",
    )
    if not daily_sales.empty:
        fig.add_annotation(
            x=PRICE_INCREASE_DATE,
            y=daily_sales["sales"].max(),
            text="Price increase<br>15 Jan 2021",
            showarrow=True,
            arrowhead=2,
            ax=50,
            ay=-50,
            font={"color": "#c2185b", "size": 12},
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#c2185b",
            borderwidth=1,
        )

    fig.update_layout(
        plot_bgcolor="#fffafd",
        paper_bgcolor="#ffffff",
        font={"family": "Helvetica Neue, Arial, sans-serif", "color": "#2a1b2e"},
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        margin={"l": 60, "r": 30, "t": 70, "b": 60},
        hovermode="x unified",
        xaxis={"showgrid": True, "gridcolor": "#f3d7e6"},
        yaxis={"showgrid": True, "gridcolor": "#f3d7e6"},
    )
    return fig


app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Pink Morsel Sales Visualiser", id="app-header"),
        html.P(
            "Daily Pink Morsel sales — filter by region to see how the "
            "15 January 2021 price increase moved the needle.",
            id="app-subtitle",
        ),
        html.Div(
            className="control-card",
            children=[
                html.Span("Filter by region", className="control-label"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": r.capitalize(), "value": r}
                        for r in REGION_OPTIONS
                    ],
                    value="all",
                    inline=True,
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[dcc.Graph(id="sales-line-chart")],
        ),
        html.Div(
            "Soul Foods · Pink Morsel sales analysis",
            id="app-footer",
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region):
    return build_figure(region)


if __name__ == "__main__":
    app.run(debug=True)
