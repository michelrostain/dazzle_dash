from dash import Dash, html, dcc, Input, Output   # Input/Output servent au callback
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# --- Chargement des données ---
df = pd.read_csv("dazzle_dash/data/life_expectancy_data.csv")
df.columns = df.columns.str.strip()   # enlève les espaces parasites autour des noms (casse conservée)

# --- Graphique : top 5 mortalité adulte ---
moyenne = df.groupby('Country', as_index=False)['Adult Mortality'].mean()
moyenne = moyenne.sort_values('Adult Mortality', ascending=False).head(5)

fig = px.bar(
    moyenne,
    x='Adult Mortality',
    y='Country',
    orientation='h',
    title="5 pays avec la mortalité adulte la plus élevée",
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=700)
fig.update_yaxes(dtick=1)

# --- Données pour les filtres du boxplot ---
# Colonnes numériques proposées (sauf l'année)
colonnes_num = [c for c in df.select_dtypes("number").columns if c != "Year"]
# Liste triée des pays pour le menu déroulant
options_pays = sorted(df["Country"].unique())

# --- Construction du boxplot ---
def construire_boxplot(colonne, pays_choisis):
    # pays_choisis est une LISTE (menu multiple). Liste vide = tous les pays
    if pays_choisis:
        d = df[df["Country"].isin(pays_choisis)]     # garde seulement les pays cochés
    else:
        d = df
    d = d.sort_values("Country")
    # Points individuels (1 point = 1 année) seulement si peu de pays, sinon illisible
    points = "all" if pays_choisis and len(pays_choisis) <= 10 else False
    titre = f"{colonne} : " + (", ".join(pays_choisis) if pays_choisis else "tous les pays")
    return px.box(d, x="Country", y=colonne, points=points,
                  hover_data=["Year"], title=titre)

# --- Application ---
app = Dash()

app.layout = [
    # html.Div(children='My first app with Data'),
    # dag.AgGrid(
    #     rowData=df.astype(object).where(df.notna(), None).to_dict('records'),
    #     columnDefs=[{"field": i} for i in df.columns],
    #     style={"height": "600px"}
    # ),
    # dcc.Graph(figure=fig),

    # Bloc boxplot : deux filtres + graphique
    html.H3("Distribution d'un indicateur"),
    dcc.Dropdown(id="choix-colonne", options=colonnes_num,
                 value=colonnes_num[0], clearable=False),
    dcc.Dropdown(id="choix-pays", options=options_pays,
                 value=[], multi=True,
                 placeholder="Tous les pays (sélectionne-en pour filtrer)"),
    dcc.Graph(id="boxplot"),
]

# Le callback met à jour le boxplot quand l'un des deux filtres change
@app.callback(
    Output("boxplot", "figure"),
    Input("choix-colonne", "value"),
    Input("choix-pays", "value"),
)
def maj_boxplot(colonne, pays):
    return construire_boxplot(colonne, pays)

if __name__ == '__main__':
    app.run(debug=True)