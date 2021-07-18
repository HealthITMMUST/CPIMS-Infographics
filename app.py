import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Output, Input

data = pd.read_csv("kakamega.csv")
data["case_date"] = pd.to_datetime(data["case_date"], format='%d/%m/%y')
data.sort_values("case_date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets= [external_stylesheets,dbc.themes.BOOTSTRAP])

app.title = "CPMIS INFOGRAPHICS!"

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "absolute",
    "top":"18rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}



sidebar = html.Div(
    [
        html.Hr(),
        html.P(
            "Navigation", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Registry", href="/page-1", active="exact"),
                dbc.NavLink("Forms", href="/page-2", active="exact"),
                dbc.NavLink("Reports", href="/page-3", active="exact"),
                dbc.NavLink("Gallary", href="/page-4", active="exact"),
                dbc.NavLink("Import", href="/page-5", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)



app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children= html.Img(src='venv/assets/shield.svg'), className="header-emoji"),
                html.H1(
                    children="CPIMS INFOGRAPHICS", className="header-title"
                ),
                html.P(
                    children="Analyze the reported child cases"
                    " within a given county in a specific county",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="county", className="menu-title"),
                        dcc.Dropdown(
                            id="county-filter",
                            options=[
                                {"label": county, "value": county}
                                for county in np.sort(data.county.unique())
                            ],
                            value="kakamega",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
               html.Div(
                    children=[
                        html.Div(children="sub county", className="menu-title"),
                        dcc.Dropdown(
                            id="sub-filter",
                            options=[
                                {"label": sub_county, "value": sub_county}
                                for sub_county in data.sub_county.unique()
                            ],
                            value="Malava",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.case_date.min().date(),
                            max_date_allowed=data.case_date.max().date(),
                            start_date=data.case_date.min().date(),
                            end_date=data.case_date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        sidebar,
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="Bar-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

fig = px.bar(data, x = "case_status", y = "sex", color = "sex")


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure"), Output("Bar-chart", "figure")],
    [
        Input("county-filter", "value"),
        Input("sub-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(county, sub_county, start_date, end_date):
    mask = (
        (data.county == county)
        & (data.sub_county == sub_county)
        & (data.case_date >= start_date)
        & (data.case_date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["case_date"],
                "y": filtered_data["age"],
                "type": "lines",
                "hovertemplate": "{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["case_date"],
                "y": filtered_data["sex"],
                "type": "line",
            },
        ],
        "layout": {
            "title": {"text": "", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    Bar_chart_figure = {

    
        "data": [
            {
                "x": filtered_data["case_status"],
                "y": filtered_data["sex"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": False},
            'color': ['sex'],
            "colorway": ["#0000FF", "#17B897"],
        },
    }
    

    return price_chart_figure, volume_chart_figure, Bar_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
    
    
    