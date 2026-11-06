import plotly.graph_objects as go
import pandas as pd

# --------------Graphes à courbe

'''Code pour plusieurs colonnes, seul le seuil est à adapter. 
Les colonnes concernées sont : 
- Adult Mortality, seuil : 0,5
- Alcohol : 0,3
- Hepatitis B: 0,5
- Measles : on garde sans rien changer
- under-five deaths : 
- polio : 2,5
- Total expenditure : 0,3
- Diphtheria : 0,3
- GDP : 0,3
- Thinness 1-19 years : 0,3
- Thinness 5-9 years : 0,4
'''

def calculer_traces(d, colonne, seuil):
    """Calcule les 4 traces du graphique pour un seuil donné.
    d : lignes d'UN seul pays, triées par année."""
    # Une valeur est suspecte si elle est < seuil x médiane du pays
    flag = d[colonne] < seuil * d[colonne].median()

    # Valeurs d'origine indexées par année
    origine = d.set_index("Year")[colonne]

    # Valeurs suspectes effacées (NaN), année en index pour l'interpolation
    valeurs = d[colonne].where(~flag)
    valeurs.index = d["Year"].values

    # Interpolation linéaire uniquement ENTRE deux valeurs retenues
    interpolees = valeurs.interpolate(method="index", limit_area="inside")

    # Années flaggées : interpolables (rouge) ou non (orange, bord de série)
    annees_suspectes = d.loc[flag, "Year"]
    points_rouges = interpolees.reindex(annees_suspectes).dropna()
    non_interpolables = annees_suspectes[~annees_suspectes.isin(points_rouges.index)]
    retenues = valeurs.dropna()

    # Années où la valeur d'origine est ABSENTE (NaN) mais remplie par l'interpolation
    annees_nan = d.loc[d[colonne].isna(), "Year"]
    points_nan = interpolees.reindex(annees_nan).dropna()  # dropna : on retire les NaN non interpolables

    bleu = "#636EFA"
    return [
        # Trace 1 : la ligne seule, sans marqueurs ni infobulle
        go.Scatter(x=interpolees.index, y=interpolees.values, mode="lines",
                   line=dict(color=bleu), hoverinfo="skip", showlegend=False),
        # Trace 2 : marqueurs bleus uniquement sur les valeurs retenues
        go.Scatter(x=retenues.index, y=retenues.values, mode="markers",
                   name="Valeurs retenues", marker=dict(color=bleu)),
        # Trace 3 : points rouges, avec la valeur d'origine dans l'infobulle
        go.Scatter(x=points_rouges.index, y=points_rouges.values, mode="markers",
                   name="Valeurs interpolées", marker=dict(color="red", size=10),
                   customdata=origine.loc[points_rouges.index].values,
                   hovertemplate=("Année : %{x}<br>"
                                  "Valeur interpolée : %{y:.1f}<br>"
                                  "Valeur d'origine : %{customdata}<extra></extra>")),
        # Trace 4 : suspectes non remplaçables, laissées à leur valeur d'origine
        go.Scatter(x=non_interpolables.values, y=origine.loc[non_interpolables].values,
                   mode="markers", name="Suspectes non remplacées (bord de série)",
                   marker=dict(color="orange", size=10, symbol="x"),
                   hovertemplate="Année : %{x}<br>Valeur d'origine : %{y}<extra></extra>"),
    
        # Trace 5 : valeurs absentes (NaN) comblées par interpolation (losanges violets)
        go.Scatter(x=points_nan.index, y=points_nan.values, mode="markers",
                   name="Valeurs absentes interpolées",
                   marker=dict(color="purple", size=10, symbol="diamond"),
                   hovertemplate=("Année : %{x}<br>"
                                  "Valeur interpolée : %{y:.1f}<br>"
                                  "Valeur d'origine : absente<extra></extra>")),     
        ] 

def courbe_avec_outliers(df, pays, colonne, titre, seuil):
    """Courbe d'un pays avec un seuil fixe (pas de curseur)."""
    d = df[df["Country"] == pays].sort_values("Year").copy()

    # Axe des ordonnées : de 0 à 10 % au-dessus du maximum de la colonne pour ce pays
    maximum = d[colonne].max()  # NaN si le pays n'a aucune valeur
    plage_y = [0, maximum * 1.1] if pd.notna(maximum) and maximum > 0 else None  # None = automatique

    # On ajoute simplement les 5 traces calculées avec le seuil fixe
    fig = go.Figure()
    for t in calculer_traces(d, colonne, seuil):
        fig.add_trace(t)

    fig.update_layout(
        title=titre, xaxis_title="Année",
        yaxis=dict(title=colonne, range=plage_y),
        width=1100, height=500, margin=dict(r=380),   # marge droite pour la légende
        legend=dict(x=1.02, y=1, xanchor="left", yanchor="top"),
    )
    return fig