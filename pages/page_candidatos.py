from dash import html, dcc
import dash_bootstrap_components as dbc


def candidatos():
    return html.Div([dbc.Col([

        html.H4(id="nome_cidade"),
    ]),

        dbc.Col([

            html.H5("Candidatos"),


        ]),

        dbc.Row(
        [
            dbc.Col(
                [

                    dbc.Row(
                        dcc.Graph(
                            id="resultado",
                            style={
                                "height": "300px",
                                "overflowY": "scroll"},
                        ),
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
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
                                                    id="total_urnas",
                                                    style={"color": "#053F63", "fontWeight": "bold"})
                                            )
                                        ],
                                        style={
                                            "backgroundColor": "#FFCD00", },
                                        className="p-4 mb-2 text-center shadow-sm",
                                    ),
                                ],
                            ),
                            dbc.Col([
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
                                                id="total_secoes",
                                                style={"color": "#053F63", "fontWeight": "bold"})
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "#FFCD00", },
                                    className="p-4 text-center shadow-sm",
                                ),
                            ]),
                            dbc.Col([
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
                                                id="total_votos",
                                                style={"color": "#053F63", "fontWeight": "bold"})
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "#FFCD00", },
                                    className="p-4 text-center shadow-sm",
                                ),
                            ])
                        ],
                    ),

                ],
            ),
        ],
    )])
