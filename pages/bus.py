from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


def criar_circulos(total, brancos):
    circulos = []
    for i in range(total):
        if i < brancos:
            circulo = html.Div(className="circulo branco", style={
                               "background-color": "#053F85", "border-radius": "50%", "margin": "5px", "width": "15px", "height": "15px"})
        else:
            circulo = html.Div(className="flex", style={
                               "background-color": "#053F63", "border-radius": "50%", "margin": "5px", "width": "15px", "height": "25px"})
        circulos.append(circulo)
        if (i + 1) % 25 == 0:
            circulos.append(html.Br())
    return circulos


def bus(total_circulos, circulos_brancos):
    return html.Div(
        children=[
            html.H1("Círculos"),
            dbc.Row(
                id="circulos-container",
                children=criar_circulos(total_circulos, circulos_brancos),
                className="ms-4",),
        ],

    )
