from dash import register_page, html
import dash_bootstrap_components as dbc

register_page(__name__, path="/", name="Accueil", order=0)


def carte(titre, texte, lien):
    return dbc.Card(dbc.CardBody([
        html.H4(titre),
        html.P(texte),
        dbc.Button("Ouvrir", href=lien, color="primary"),
    ]))


layout = html.Div([
    html.H1("Espérance de vie dans le monde"),
    html.P("Analyse des données de l'OMS (2000-2015).", className="lead"),
    dbc.Row([
        dbc.Col(carte("Carte", "L'espérance de vie par pays et par année.", "/map")),
        dbc.Col(carte("Boxplot", "La distribution d'un indicateur.", "/boxplot")),
    ]),
])
