import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_PATH = "./formatted_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

daily_sales = df.groupby("date", as_index=False)["sales"].sum()

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"},
)

fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_width=2,
    line_dash="dash",
    line_color="red",
)
fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=daily_sales["sales"].max(),
    text="Price increase (15 Jan 2021)",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=-40,
)

app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#ff3385"},
        ),
        html.P(
            "Daily Pink Morsel sales across all regions. "
            "The dashed line marks the price increase on 15 January 2021.",
            style={"textAlign": "center"},
        ),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ],
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
)

if __name__ == "__main__":
    app.run(debug=True)
