from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_ag_grid as dag


def candidatos():
    return html.Div([dbc.Col([

        html.H4(id="nome_cidade"),
    ]),

        dbc.Col([

            html.H5("Candidatos"),
        ]),
        dbc.Col([

        ]),

        dbc.Row(
        [
            dbc.Col(
                [

                    dbc.Row([

                        html.Div(
                            id="grid",
                        )
                    ]),
                    dbc.Button("Tabela", id="open-xl",
                               n_clicks=0, className="mt-4"),
                ],

                width=9),

            dbc.Col(
                [
                    dbc.Row([
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.H5(
                                            "Votos Válidos",
                                            style={
                                                "color": "#053F63", "fontWeight": "bold"}
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    html.H5(
                                        id="votos_validos",
                                        style={"color": "#053F63", "fontWeight": "bold"}),

                                ),
                            ],
                            style={
                                "backgroundColor": "#FFCD00", "width": "95%"},
                            className="p-4 mb-2 text-center shadow-sm",
                        ),
                    ]),
                    dbc.Row(
                        [
                            dbc.Card(
                                [
                                    dbc.Row(
                                        [
                                            html.H5(
                                                "Votos Brancos",
                                                style={
                                                    "color": "#053F63", "fontWeight": "bold"}
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        html.H5(
                                            id="votos_brancos",
                                            style={"color": "#053F63", "fontWeight": "bold"})
                                    )
                                ],
                                style={
                                    "backgroundColor": "#FFCD00", "width": "95%"},
                                className="p-4 mb-2 text-center shadow-sm",
                            ),
                        ],
                    ),
                    dbc.Row([
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        html.H5(
                                            "Votos Nulos",
                                            style={
                                                "color": "#053F63", "fontWeight": "bold"}
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    html.H5(
                                        id="votos_nulos",
                                        style={"color": "#053F63", "fontWeight": "bold"})
                                ),
                            ],
                            style={
                                "backgroundColor": "#FFCD00", "width": "95%"},
                            className="p-4 text-center shadow-sm",
                        ),
                    ]),
                ]
            )
        ],
    )])
