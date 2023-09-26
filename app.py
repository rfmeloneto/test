import json
import requests
import os
import ast

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag

from dash import dcc, html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

from pages.page_candidatos import candidatos
from pages.bus import bus


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.FLATLY], suppress_callback_exceptions=True)

app.title = 'IntegraVoto'
app._favicon = "asserts/favicon.ico"

load_dotenv()


def update_estado():
    url_pleitos = os.getenv("PLEITOS_ATIVOS")
    pleitos = requests.get(url_pleitos).json()
    df_pleitos = pd.DataFrame(pleitos)
    opcoes = [{"label": e, "value": uf} for e, uf in zip(
        df_pleitos["estado"].unique(), df_pleitos["uf"].unique())]
    return opcoes, df_pleitos["uf"].unique()[0]


def update_cidade(uf):
    url_pleitos = os.getenv("PLEITOS_ATIVOS")
    pleitos = requests.get(url_pleitos).json()
    df_pleitos = pd.DataFrame(pleitos)
    cidades = df_pleitos[df_pleitos['uf'] == uf]['cidade'].unique()
    id = df_pleitos[df_pleitos['uf'] == uf]['id'].unique()
    options = [{"label": cidades[i], "value": id[i]}
               for i in range(len(cidades))]
    return options, id[0]


def update_cidade_title(cidade):
    url_pleitos = os.getenv("PLEITOS_ATIVOS")
    pleitos = requests.get(url_pleitos).json()
    df_pleitos = pd.DataFrame(pleitos)
    cidades = df_pleitos[df_pleitos['id'] == cidade]['cidade'].unique()
    return cidades[0]


def update_regiao(cidade):
    url_pleitos = os.getenv("PLEITOS_ATIVOS")
    pleitos = requests.get(url_pleitos).json()
    df_pleitos = pd.DataFrame(pleitos)
    regioes = df_pleitos.loc[df_pleitos['id'] == cidade, 'regiao']
    regiao = ast.literal_eval(regioes.iloc[0])
    options = [{"label": r, "value": r} for r in regiao]
    return options, regiao[0]


def update_table(cidade, regiao):
    url_resultado = os.getenv("RESULTADOS")+str(cidade)+"/"
    resultato = requests.get(url_resultado).json()
    dft = pd.DataFrame(resultato)
    cidade_str = dft["cidade"].unique()
    df_city = dft[(dft["cidade"] == cidade_str[0]) & (dft["regiao"] == regiao)].sort_values(
        by="votos", ascending=False)
    colocados = [i+1 for i in range(0, len(df_city["candidato"].unique()))]
    df_city['colocacao'] = colocados
    return dag.AgGrid(
        columnDefs=[
            {"headerName": "Posição", "field": "colocacao"},
            {"headerName": "Nome", "field": "nome_candidato"},
            {"headerName": "Número", "field": "candidato"},
            {"headerName": "Votos", "field": "votos"},
        ],
        rowData=df_city.to_dict(orient="records"),
        columnSize="sizeToFit",
        style={"height": "360px", "width": "100%", "justify": "center"},


    )


def map(estado):
    url_mapa = os.getenv("MAPA")
    response = requests.get(url_mapa).json()
    df = pd.DataFrame(response)
    maps = {"TO": "geodata/to.json", }
    center = {"TO": {"lat": -10.1837, "lon": -48.3338}, }
    filejson = open(maps[estado])
    geojson = json.load(filejson)
    df["percentual"] = round((df["bu_recebidos"]/df["qtd_total_urnas"])*100, 2)
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="cod_ibge",
        featureidkey="properties.id",
        color="percentual",
        hover_name="cidade",
        title="Mapa do Tocantins",
        color_continuous_scale="Viridis",
        opacity=1,
        mapbox_style="carto-positron",
        zoom=4.8,
        center=center[estado],
        range_color=[0, 100],
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


def bus_page(cidade):
    env_bu = os.getenv("BU")
    url_bus = env_bu.format(
        cidade=cidade
    )
    response = requests.get(url_bus).json()
    df = pd.DataFrame(response)
    qtd_urna = df["qtd_total_urnas"].values
    bu_recebidos = df["bu_recebidos"].values
    return bus(qtd_urna[0], bu_recebidos[0])


def brancos(cidade):
    url_brancos = os.getenv("BRANCOS_NULOS")
    brancos = requests.get(url_brancos).json()
    df_brancos = pd.DataFrame(brancos)
    brancos = df_brancos.loc[df_brancos["cidade"] == cidade, "brancos"].sum()
    return brancos


def nulos(cidade):
    url_nulos = os.getenv("BRANCOS_NULOS")
    nulos = requests.get(url_nulos).json()
    df_nulos = pd.DataFrame(nulos)
    nulos = df_nulos.loc[df_nulos["cidade"] == cidade, "nulos"].sum()
    return nulos


def validos(cidade):
    url_validos = os.getenv("BRANCOS_NULOS")
    validos = requests.get(url_validos).json()
    df_validos = pd.DataFrame(validos)
    validos = df_validos.loc[df_validos["cidade"] == cidade, "validos"].sum()
    return validos


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


app.layout = html.Div(
    [

        html.Div([dbc.Modal(
            [

                dbc.ModalHeader(html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="assets/integravoto_preto.svg"),
                        ]),
                        dbc.Col([
                            dbc.Row(
                                html.H6("Sistema de Gerenciamento de Totalização")),
                            dbc.Row(
                                html.H6("Eleição de Conselho Tutelar - 2023")),

                        ]),
                    ]
                    )
                ])),
                dbc.ModalBody([], id="grid-modal"),
            ],
            id="modal-xl",
            # fullscreen=True,
            size="lg",
            is_open=False,
        ), ]),
        html.Script(
            id="script"
        ),
        html.Div([], id="dummy"),
        dcc.Interval(
            id='interval-component',
            interval=60 * 1000,
            n_intervals=0
        ),
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Col([

                    ], width=1),
                    dbc.Col([
                        html.Img(
                            src="assets/integravoto.svg",
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
                    className="p-4",
                ),
            ]),
            dbc.Col([
                    dcc.Dropdown(
                        id="dropdown-cidade",
                        placeholder="Cidade",
                        className="p-4",
                    ),
                    ]),

            dbc.Col([

                dcc.Dropdown(
                    id="dropdown-regiao",
                    placeholder="Região",
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
                        html.Div(dcc.Graph(id="map"),
                                 style={"height": "500px",
                                        "width": "700px", "margin-left": "10%",
                                        "margin-top": "5%"},
                                 ),


                    ],

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


@app.callback(
    Output("dropdown-estado", "options"),
    Output("dropdown-estado", "value"),
    Input('interval-component', 'n_intervals'))
def load_estado(n):
    return update_estado()


# Atualização das cidades de acordo com o estado
@app.callback(
    Output('dropdown-cidade', 'options'),
    Output('dropdown-cidade', 'value'),
    Input('dropdown-estado', 'value'),
)
def load_city(uf):
    return update_cidade(uf)


@app.callback(
    Output('dropdown-regiao', 'options'),
    Output('dropdown-regiao', 'value'),
    Input('dropdown-cidade', 'value')
)
def load_regiao(cidade):
    return update_regiao(cidade)


@app.callback(Output("components", "children"), Input("radio", "value"),
              Input("dropdown-cidade", "value"),  Input('interval-component', 'n_intervals'))
def update_components(value, cidade, n):
    if value == 0:
        return candidatos()
    if value == 1:
        return bus_page(cidade)


@app.callback(Output("map", "figure"), Input("dropdown-estado", "value"),
              Input('interval-component', 'n_intervals'))
def update_map(estado, n):
    return map(estado)


@app.callback(Output("nome_cidade", "children"), Input("dropdown-cidade", "value"))
def update_nome_cidade(value):
    return update_cidade_title(value)


@app.callback(
    Output("votos_brancos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_brancos(value):
    return brancos(value),


@app.callback(
    Output("votos_nulos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_nulos(value):
    return nulos(value),


@app.callback(
    Output("votos_validos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_validos(value):
    return validos(value),


@app.callback(Output("grid", "children"), Input("dropdown-cidade", "value"),
              Input("dropdown-regiao", "value"),
              Input('interval-component', 'n_intervals'))
def update_resultado(cidade, regiao, n):
    return update_table(cidade, regiao)


@app.callback(
    Output("modal-xl", "is_open"),
    Output("grid-modal", "children"),
    Input("open-xl", "n_clicks"),
    State("dropdown-cidade", "value"),
    State("dropdown-regiao", "value"),
    State("modal-xl", "is_open"),
    prevent_initial_call=True
)
def open_modal(n1, cidade, regiao, is_open):
    return toggle_modal(n1, is_open), update_table(cidade, regiao)


@app.callback(Output("script", "children"), Input("print-btn", "n_clicks"),)
def print(n):
    if n:
        return """
            <script>
                    window.print();
            </script>
        """
    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)
