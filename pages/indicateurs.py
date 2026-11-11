from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px

from src.data import load_data

register_page(__name__, path="/indicateurs", name="Indicateurs", order=2)

df = load_data(clean=True)

INDICATEURS = {
    "GDP": "PIB",
    "Schooling": "Scolarité",
    "Total expenditure": "Dépenses de santé (T.E.)",
    "Income composition of resources": "Income composition",
}


def nuage(data, colonne, titre):
    d = data[[colonne, "Life expectancy"]].dropna()
    fig = px.scatter(d, x=colonne, y="Life expectancy", opacity=0.5)
    if len(d) > 1:
        a, b = np.polyfit(d[colonne], d["Life expectancy"], 1)  # droite y = a*x + b
        r = np.corrcoef(d[colonne], d["Life expectancy"])[0, 1]
        x = np.sort(d[colonne])
        fig.add_scatter(x=x, y=a * x + b, mode="lines", line=dict(color="red"), showlegend=False)
        titre += f"   R = {r:.2f}"
    fig.update_layout(title=titre, template="plotly_white", height=350)
    if colonne in ["Total expenditure", "Diphtheria"]:
        fig.update_xaxes(range=[0, 100], ticksuffix="%")
    return fig


layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="pays-indic", options=sorted(df["Country"].unique()),
                             placeholder="Tous les pays"), md=6),
        dbc.Col(dcc.Dropdown(id="status-indic",
                             options=[{"label": "Pays développés", "value": "Developed"},
                                      {"label": "Pays en développement", "value": "Developing"}],
                             placeholder="Tous"), md=6),
    ]),
    dbc.Row([dbc.Col(dcc.Graph(id=f"indic-{i}"), md=6) for i in range(4)]),
])


@callback([Output(f"indic-{i}", "figure") for i in range(4)],
          Input("pays-indic", "value"), Input("status-indic", "value"))
def maj_indicateurs(pays, status):
    data = df
    if pays:
        data = data[data["Country"] == pays]
    if status:
        data = data[data["Status"] == status]
    return [nuage(data, col, titre) for col, titre in INDICATEURS.items()]
