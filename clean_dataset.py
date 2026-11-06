import pandas as pd
import numpy as np


def corriger_seuil(df, colonne, seuil):
    """Remplace les valeurs < seuil x médiane du pays.

    Celles encadrées par deux valeurs retenues sont interpolées.
    Celles en bord de série deviennent NaN (aucune valeur inventée).
    """
    df = df.copy()

    # Médiane de chaque pays, ramenée sur chaque ligne
    mediane = df.groupby("Country")[colonne].transform("median")

    # On efface les valeurs suspectes : elles deviennent NaN
    df[colonne] = df[colonne].where(df[colonne] >= seuil * mediane)

    # Interpolation par pays, dans l'ordre chronologique, uniquement ENTRE
    # deux valeurs retenues (limit_area="inside" interdit d'extrapoler)
    ordre = df.sort_values(["Country", "Year"])
    df[colonne] = (ordre.groupby("Country")[colonne]
                        .transform(lambda s: s.interpolate(limit_area="inside")))
    return df


def nettoyer(df):
    """Renvoie une copie nettoyée de df. Le DataFrame d'origine n'est pas modifié."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)
    nan_avant = df.isna().sum()

    # ---------- Colonnes supprimées ----------
    df = df.drop(columns=["Population", "BMI", "HIV/AIDS", "percentage expenditure"],
                 errors="ignore")

    # ---------- Zéros = codes manquants ----------
    df["Schooling"] = df["Schooling"].replace(0, np.nan)
    df["Income composition of resources"] = (
        df["Income composition of resources"].replace(0, np.nan))

    # ---------- Seuils (ratio valeur / médiane du pays) ----------
    df = corriger_seuil(df, "Adult Mortality", 0.5)
    df = corriger_seuil(df, "Alcohol", 0.3)
    df = corriger_seuil(df, "Hepatitis B", 0.2)
    df = corriger_seuil(df, "Polio", 0.25)
    df = corriger_seuil(df, "Diphtheria", 0.3)
    df = corriger_seuil(df, "Total expenditure", 0.35)
    df = corriger_seuil(df, "GDP", 0.5)
    df = corriger_seuil(df, "thinness 1-19 years", 0.35)
    df = corriger_seuil(df, "thinness 5-9 years", 0.4)

    # ---------- Bilan ----------
    nan_apres = df.isna().sum()
    communes = nan_apres.index.intersection(nan_avant.index)
    ajoutes = nan_apres[communes] - nan_avant[communes]
    ajoutes = ajoutes[ajoutes != 0]
    supprimees = nan_avant.index.difference(nan_apres.index)
    print("Colonnes supprimées :", list(supprimees) if len(supprimees) else "aucune")
    print("NaN ajoutés par le nettoyage :")
    print(ajoutes.to_string() if len(ajoutes) else "aucun")
    return df

# Ce bloc ne s'exécute QUE si on lance le fichier directement,
# jamais quand le notebook fait "from nettoyage_par_colonne import nettoyer"
if __name__ == "__main__":
    brut = pd.read_csv("/home/michel/Documents/LaPlateforme/Projets/annee2/Data_Wiz_Dash/dazzle_dash/data/life_expectancy_data.csv")
    propre = nettoyer(brut)
    propre.to_csv("data/life_expectancy_clean.csv", index=False)
    print("Fichier écrit.")