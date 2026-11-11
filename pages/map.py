from dash import register_page, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from src.data import load_data

register_page(__name__, path="/map", name="Carte", order=1)

df = load_data(clean=True).sort_values("Year")  # slider goes 2000 -> 2015
df_2015 = df[df["Year"] == 2015]

# --- Carte du monde ---
carte = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Life expectancy",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale="Viridis",
    range_color=(df["Life expectancy"].min(), df["Life expectancy"].max()),
    projection="natural earth",
)
carte.update_layout(height=600, margin=dict(l=0, r=0, t=0, b=0))


# --- 10 meilleurs / 10 pires en 2015 (graph du notebook) ---
def barres(valeurs, couleur, titre):
    fig = go.Figure(go.Bar(x=valeurs.values, y=valeurs.index, orientation="h", marker_color=couleur))
    fig.update_layout(title=titre, height=300, margin=dict(l=0, r=0, t=30, b=0),
                      template="plotly_white", yaxis=dict(autorange="reversed", dtick=1))
    return fig


esperance_2015 = df_2015.groupby("Country")["Life expectancy"].mean()
top_10 = barres(esperance_2015.nlargest(10), "steelblue", "10 meilleurs (2015)")
bottom_10 = barres(esperance_2015.nsmallest(10), "indianred", "10 pires (2015)")
moyenne_2015 = df_2015["Life expectancy"].mean()
colonnes_y = [c for c in df.select_dtypes("number").columns if c != "Year"]


def courbe(pays, y):
    fig = go.Figure()
    status = df.groupby(["Year", "Status"], as_index=False)[y].mean()
    for nom, label, couleur in [("Developed", "Pays développés", "seagreen"),
                                ("Developing", "Pays en développement", "darkorange")]:
        d = status[status["Status"] == nom]
        fig.add_trace(go.Scatter(x=d["Year"], y=d[y], mode="lines",
                                 name=label, line=dict(color=couleur, width=3)))
    if pays:
        d = df[df["Country"] == pays]
        fig.add_trace(go.Scatter(x=d["Year"], y=d[y], mode="lines+markers",
                                 name=pays, line=dict(color="royalblue", width=4)))
    fig.update_layout(title=f"L'évolution de {y} (2000–2015)",
                      xaxis_title="Année", yaxis_title=y,
                      template="plotly_white", hovermode="x unified", xaxis=dict(dtick=1))
    if y in ["Total expenditure", "Diphtheria"]:
        fig.update_yaxes(range=[0, 100], ticksuffix="%")
    return fig


layout = html.Div([
    html.H1("Espérance de vie dans le monde"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=carte), md=8),
        dbc.Col([
            dcc.Graph(figure=top_10),
            dcc.Graph(figure=bottom_10),
        ], md=4),
    ]),
    html.Div([
        html.H5("Espérance de vie mondiale 2015"),
        html.H2(f"{moyenne_2015:.1f} ans"),
    ], className="text-center my-4"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="pays-courbe", options=sorted(df["Country"].unique()),
                             value="France", placeholder="Aucun pays"), md=6),
        dbc.Col(dcc.Dropdown(id="y-courbe", options=colonnes_y,
                             value="Life expectancy", clearable=False), md=6),
    ]),
    dcc.Graph(id="courbe"),
])


@callback(Output("courbe", "figure"), Input("pays-courbe", "value"), Input("y-courbe", "value"))
def maj_courbe(pays, y):
    return courbe(pays, y)
