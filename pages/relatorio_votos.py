import dash_bootstrap_components as dbc
from dash import html


def relatorio_votos(uf, municipio, grid, eleitores_aptos, brancos, comparecimento, nulos, nominais, apurado):
    header = html.Div([
        dbc.Row([
            dbc.Col([
                html.img(src="assets/integravoto.svg"),
            ]),
            dbc.Col([
                dbc.Row(html.H6("Sistema de Gerenciamento de Totalização")),
                dbc.Row(html.H6("Eleição de Conselho Tutelar - 2023")),
                dbc.Row(html.H6(str(municipio) + " - " + str(uf))),
            ])

        ]
        )
    ])

    footer = html.Div([
        dbc.Row([

            dbc.Col([
                dbc.Row([
                    dbc.Card(
                      dbc.Row([
                          html.H6("Eleitores Aptos"),
                      ]),
                      dbc.Row([
                          eleitores_aptos
                      ])
                      )
                ]),
                dbc.Row([
                    dbc.Card(
                        dbc.Row([
                            html.H6("Votos em Branco"),
                        ]),
                        dbc.Row([
                            brancos
                        ])
                    )
                ]),
            ]),
            dbc.Col([
                dbc.Row([
                    dbc.Card(
                        dbc.Row([
                            html.H6("Comparecimento"),
                        ]),
                        dbc.Row([
                            comparecimento
                        ])
                    )
                ]),
                dbc.Row([
                    dbc.Card(
                        dbc.Row([
                            html.H6("Votos nulo"),
                        ]),
                        dbc.Row([
                            nulos
                        ])
                    )
                ]),
            ]),
            dbc.Col([
                dbc.Row([
                    dbc.Card(
                        dbc.Row([
                            html.H6("Votos Nominais"),
                        ]),
                        dbc.Row([
                            nominais
                        ])
                    )
                ]),
                dbc.Row([
                    dbc.Card(
                        dbc.Row([
                            html.H6("Total Apurado"),
                        ]),
                        dbc.Row([
                            apurado
                        ])
                    )
                ]),
            ]),

        ])
    ])

    html.Div([dbc.ModalHeader(dbc.Button("Imprimir", id="grid-browser-print-btn")),
              dbc.ModalBody(

        [
            header,
            grid,
            footer,
        ],
        id="grid-print-area",
    ),
        html.Div(id="dummy"), ],)
