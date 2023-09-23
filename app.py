import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from dash import dcc, html
from dash.dependencies import Input, Output, State

from pages.page_candidatos import candidatos
from pages.bus import bus

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.FLATLY], suppress_callback_exceptions=True)

df = pd.read_csv("urnas.csv")
dft = pd.read_csv("resultado.csv")
dfbu = pd.read_csv("bu_recebido.csv")
filejson = open("geodata/to.json")
geojson = json.load(filejson)

total_circulos = 200
circulos_amarelos = 30

components = [candidatos(), bus(total_circulos, circulos_amarelos)]


app.layout = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Col([

                    ], width=1),
                    dbc.Col([
                        html.Img(
                            src="assets/integravoto_deitado.svg",
                            style={"height": "100px"},
                        ),

                    ], width=3, className="ms-20"),
                    dbc.Col([

                    ], width=1),
                    dbc.Col([
                        html.H2(
                            "Painel de Resultados das Eleições - Conselho Tutelar",
                            style={"color": "white",
                                   "fontFamily": "Roboto", "fontSize": "35px",
                                   "fontWeight": "900"},
                        )
                    ])

                ],
                fluid=True,
                style={"width": "100%"},
            ),
            color="#004A7C",
            className="shadow-sm",

        ),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="dropdown-estado",
                    options=[
                        {"label": "Tocantins", "value": "TO"},
                        {"label": "Pernabuco", "value": "PE"},
                        {"label": "Rio Grande do Norte", "value": "RN"},
                    ],

                    className="p-4",
                    value="TO",),
            ]),
            dbc.Col([
                dcc.Dropdown(
                    id="dropdown-cidade",
                    options=[
                        {"label": cidade, "value": cidade}
                        for cidade in df["cidade"].unique()
                    ],
                    value="Palmas",
                    className="p-4",
                ),
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id="dropdown-regiao",
                    options=[
                        {"label": "Única", "value": 1},
                        {"label": "Sul", "value": 2},
                        {"label": "Norte", "value": 3},
                    ],
                    placeholder="Região",
                    value="Única",
                    className="p-4",
                ),
            ]),


        ]),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [dbc.RadioItems(
                        id="radio",
                        options=[
                            {"label": "Candidatos", "value": 0},
                            {"label": "Bu's", "value": 1},
                        ],
                        value=0,
                        inline=True
                    ),
                        dbc.Card(
                            [
                                html.Div(id="components", children=[]),

                            ],
                            style={"height": "500px",
                                   "background-color": "#D9D9D9"},
                    ),
                    ],
                    className="p-3",
                ),
                dbc.Col(
                    [
                        html.Div(dcc.Graph(id="map")),


                    ]
                ),
            ],
        ),
        dbc.Navbar(
            dbc.Container(
                dbc.Row(
                    [
                        html.Img(src="assets/bandeira_branca.svg"),
                    ],
                    className="justify-content-end align-items-center ms-auto",
                ),
            ),
            color="#004A7C",
            className="shadow-sm fixed-bottom",
        ),
    ],
    style={
        "background-color": "#f5f5f5",
        "height": "100vh",
        "width": "100%",
        "margin": 0,
        "padding": 0,
    },


)


@app.callback(Output("components", "children"), Input("radio", "value"))
def update_components(value):
    return components[value]


@app.callback(Output("map", "figure"), Input("dropdown-estado", "value"))
def update_map(estado):
    maps = {"TO": "geodata/to.json",
            "PE": "geodata/pe.json", "RN": "geodata/rn.json"}
    center = {"TO": {"lat": -10.1837, "lon": -48.3338}, "PE": {"lat":
                                                               -7.1173, "lon": -34.8631}, "RN": {"lat": -5.7793, "lon": -35.2009}}
    filejson = open(maps[estado])
    geojson = json.load(filejson)
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="cidade",
        featureidkey="properties.name",
        color="urnas",
        hover_name="cidade",
        title="Mapa do Tocantins",
        color_continuous_scale="Viridis",
        opacity=1,
        mapbox_style="carto-positron",
        zoom=4.8,
        center=center[estado],
    )

    fig.update_geos(
        visible=True,
        resolution=110,
        showcountries=False,
        showcoastlines=False,
        showland=False,
        fitbounds="locations",
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Contagem de Urnas"),

    )

    return fig


@app.callback(Output("nome_cidade", "children"), Input("dropdown-cidade", "value"))
def update_nome_cidade(value):
    return value


@app.callback(
    Output("total_urnas", "children"),
    Input("dropdown-cidade", "value"),
)
def update_total_urnas(value):
    return (dft[dft["cidade"] == value]["urnas_apuradas"].sum(),)


@app.callback(
    Output("total_secoes", "children"),
    Input("dropdown-cidade", "value"),
)
def update_total_secoes(value):
    return (dft[dft["cidade"] == value]["secoes_apuradas"].sum(),)


@app.callback(
    Output("total_votos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_total_votos(value):
    return (dft[dft["cidade"] == value]["votos_apurados"].sum(),)


@app.callback(Output("resultado", "figure"), Input("dropdown-cidade", "value"))
def update_resultado(value):
    df_filtered = dft.drop(
        ["urnas_apuradas", "secoes_apuradas", "votos_apurados"], axis=1
    )
    df_city = df_filtered[df_filtered["cidade"] == value]
    non_empty_values = df_city.iloc[0].dropna()

    sorted_values = non_empty_values[non_empty_values != ""].astype(
        str).sort_values(ascending=True)
    sorted_values = sorted_values.drop(columns=["cidade"])
    df_sorted = pd.DataFrame({
        "Candidato": sorted_values.index,
        "Votos": sorted_values.values
    })

    fig = px.bar(
        x=sorted_values.index,
        y=sorted_values.values,
        color=sorted_values.index,
        text="Candidato "+df_sorted['Candidato'] + " / " +
        df_sorted['Votos'].astype(str) + " votos",
        orientation="h",
        height=300,
        template="plotly_dark"

    )
    fig.update_layout(showlegend=False, xaxis_visible=False,
                      yaxis_visible=False,
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
