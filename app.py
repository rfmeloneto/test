import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag

from dash import dcc, html
from dash.dependencies import Input, Output

from pages.page_candidatos import candidatos
from pages.bus import bus

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.FLATLY], suppress_callback_exceptions=True)

app.title = 'IntegraVoto'
app._favicon = "asserts/favicon.ico"

df = pd.read_csv("urnas.csv")
dft = pd.read_csv("resultado.csv")
df_brancos_nulos = pd.read_csv("brancos_nulos.csv")
filejson = open("geodata/to.json")
geojson = json.load(filejson)

total_circulos = 150
circulos_amarelos = 28

components = [candidatos(), bus(
    total_circulos, circulos_amarelos)]


app.layout = html.Div(
    [
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
    Output('table', 'data'),
    Input('cidade-dropdown', 'value')
)
def update_table(cidade):
    # Filtra o DataFrame com base na cidade selecionada
    filtered_df = df[df['Cidade'] == cidade]

    # Remove as colunas dos candidatos que não têm votos na cidade filtrada
    filtered_df = filtered_df.loc[:, (filtered_df != 0).any()]

    # Converte o DataFrame filtrado em uma lista de dicionários para uso no AgGrid
    data = filtered_df.to_dict('records')

    return data


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
    Output("votos_brancos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_brancos(value):
    return (df_brancos_nulos[df_brancos_nulos["cidade"] == value]["votos_brancos"].sum(),)


@app.callback(
    Output("votos_nulos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_nulos(value):
    return (df_brancos_nulos[df_brancos_nulos["cidade"] == value]["votos_nulos"].sum(),)


@app.callback(
    Output("votos_validos", "children"),
    Input("dropdown-cidade", "value"),
)
def update_votos_validos(value):
    return (dft[dft["cidade"] == value]["votos"].sum(),)


@app.callback(Output("grid", "children"), Input("dropdown-cidade", "value"))
def update_resultado(value):
    df_city = dft[dft["cidade"] == value].sort_values(
        by="votos", ascending=False)
    colocados = [i+1 for i in range(0, len(df_city["candidato"].unique()))]
    df_city['colocacao'] = colocados
    return dag.AgGrid(
        columnDefs=[
            {"headerName": "Posição", "field": "colocacao"},
            {"headerName": "Candidato", "field": "candidato"},
            {"headerName": "Votos", "field": "votos"},
        ],
        rowData=df_city.to_dict(orient="records"),
        columnSize="sizeToFit",
        style={"height": "360px", "width": "100%", "justify": "center"},



    )


if __name__ == "__main__":
    app.run_server(debug=True)
