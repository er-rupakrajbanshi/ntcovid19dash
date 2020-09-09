# Environment used: dash1_8_0_env
import pandas as pd     #
import plotly
import plotly.express as px

import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go

# print(px.data.gapminder()[:15])

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


df = pd.read_json('resources/covid-19-dist.json')
df['District'] = df['District'].apply(lambda x: x.upper())

with open('resources/nepal_district_rs.json') as f:
    geojson = json.load(f)

with open('resources/highlights.json') as f:
    highlights = json.load(f)

#---------------------------------------------------------------
card_total = [
    dbc.CardBody(
        [
            html.H5("Total Cases", className="card-title"),
            html.P(highlights['nepal']['positive'],
                   className="card-text",
                   ),
        ]
    ),
]


card_infected = [
    dbc.CardBody(
        [
            html.H5("Total Infected", className="card-title"),
            html.P(highlights['nepal']['extra1'],
                   className="card-text",
                   ),
        ]
    ),
]

card_recovered = [
    dbc.CardBody(
        [
            html.H5("Recovered", className="card-title"),
            html.P(highlights['nepal']['extra1'],
                   className="card-text",
                   ),
        ]
    ),
]

card_deaths = [
    dbc.CardBody(
        [
            html.H5("Deaths", className="card-title"),
            html.P(highlights['nepal']['deaths'],
                   className="card-text",
                   ),
        ]
    ),
]


app.layout = html.Div([
    html.Div([

        # html.Label(['COVID-19 Current Status']),
        html.Br(),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                {'label': 'Total Cases', 'value': 'Total Cases'},
                {'label': 'Recovered', 'value': 'Recovered'},
                {'label': 'Death', 'value': 'Death'},
                {'label': 'Under Treatment', 'value': 'Under Treatment'},
                # {'label': 'Province', 'value': 'Province'},
            ],
            value='Total Cases',
            multi=False,
            clearable=False,
            style={"width": "45%"}
        ),


    ]),
    html.Br(),

    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(card_total,
                                     color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(card_infected, color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(card_recovered,
                                     color="secondary", inverse=True)),
                    dbc.Col(dbc.Card(card_deaths,
                                     color="secondary", inverse=True)),
                ],
                className="mb-3",
            ),


        ]
    ),


    html.Div([
        dcc.Graph(id='the_graph')
    ]),
])

#---------------------------------------------------------------


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    dff = df

    fig = px.choropleth_mapbox(dff, geojson=geojson, color=my_dropdown,
                               locations="District", featureidkey="properties.District",
                               hover_name='District',
                               hover_data=["Total Cases", "Death", "Recovered", "Under Treatment"], center={"lat": 28.5, "lon": 84},
                               # mapbox_style="carto-positron",
                               zoom=6,
                               color_continuous_scale="YlOrRd")
    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        mapbox_style="white-bg",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return (fig)


if __name__ == '__main__':
    app.run_server(debug=True)
