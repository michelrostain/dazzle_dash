"""Point d'entrée unique pour charger les données.

Le chemin est construit à partir de l'emplacement de CE fichier,
donc ça marche quel que soit le dossier depuis lequel on lance le script.
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_CSV = DATA_DIR / "raw" / "life_expectancy_data.csv"
CLEAN_CSV = DATA_DIR / "clean" / "life_expectancy_clean.csv"


def load_data(clean=False):
    """Charge le CSV brut (par défaut) ou nettoyé, noms de colonnes sans espaces parasites."""
    df = pd.read_csv(CLEAN_CSV if clean else RAW_CSV)
    df.columns = df.columns.str.strip()
    return df

def load_data_brut(clean=False):
    """Charge le CSV brut (par défaut) ou nettoyé, noms de colonnes sans espaces parasites."""
    df = pd.read_csv(RAW_CSV)
    df.columns = df.columns.str.strip()
    return df



