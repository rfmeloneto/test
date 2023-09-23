from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


def criar_circulos(total, amarelos):
    circulos = []
    for i in range(total):
        if i < amarelos:
            circulo = html.Div(className="circulo branco", style={
                               "background-color": "#FFCD00", "border-radius": "50%", "margin": "5px", "width": "15px", "height": "25px"})
        else:
            circulo = html.Div(className="flex", style={
                               "background-color": "#053F63", "border-radius": "50%", "margin": "5px", "width": "15px", "height": "25px"})
        circulos.append(circulo)
        if (i + 1) % 26 == 0:
            circulos.append(html.Br())
    return circulos


def bus(total_circulos, circulos_amarelos):
    percentual_recebido = round((circulos_amarelos/total_circulos)*100, 2)
    total_a_receber = total_circulos - circulos_amarelos
    percentual_a_receber = 100 - percentual_recebido
    return html.Div(
        children=[
            html.H3("Recebimento de BU's", className="ms-4",
                    style={"color": "#053F63", "fontFamily": "sans-serif", "fontweight": "bold"}),
            dbc.Row(
                id="circulos-container",
                children=criar_circulos(total_circulos, circulos_amarelos),
                className="ms-4",),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row([
                                html.H5("Total Esperado", style={
                                        "color": "#053F63", "fontFamily": "sans-serif", "fontweight": "bold", "text-align": "center"}),
                            ], className="mt-4"),
                            dbc.Row(

                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            total_circulos],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],
                                                className="ms-4",
                                                style={
                                                    "background-color": "#FFCD00", }
                                            )
                                        ],
                                        className="p-0",

                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            "100%"],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],

                                                style={
                                                    "background-color": "#FFFFFF", }
                                            )
                                        ],
                                        className="p-0",
                                    )
                                ],


                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Row([
                                html.H5("Total Recebido", style={
                                        "color": "#053F63", "fontFamily": "sans-serif", "fontweight": "bold", "text-align": "center"}),
                            ], className="mt-4"),
                            dbc.Row(

                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            circulos_amarelos],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],
                                                className="ms-4",
                                                style={
                                                    "background-color": "#FFCD00", }
                                            )
                                        ],
                                        className="p-0",

                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            str(percentual_recebido) + "%"],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],

                                                style={
                                                    "background-color": "#FFFFFF", }
                                            )
                                        ],
                                        className="p-0",
                                    )
                                ],


                            )
                        ]

                    ),
                    dbc.Col(
                        [
                            dbc.Row([
                                html.H5("Total a Receber", style={
                                    "color": "#053F63", "fontFamily": "sans-serif", "fontweight": "bold", "text-align": "center"}),
                            ], className="mt-4"),
                            dbc.Row(

                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            total_a_receber],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],
                                                className="ms-4",
                                                style={
                                                    "background-color": "#FFCD00", }
                                            )
                                        ],
                                        className="p-0",

                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.H4(
                                                        children=[
                                                            str(percentual_a_receber) + "%"],
                                                        className="p-4",
                                                        style={"color": "#053F63",
                                                               "fontWeight": "bold",
                                                               "text-align": "center"})
                                                ],

                                                style={
                                                    "background-color": "#FFFFFF", }
                                            )
                                        ],
                                        className="p-0 me-4",
                                    )
                                ],


                            )
                        ]
                    )

                ]
            )
        ],



    )
