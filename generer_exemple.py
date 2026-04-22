"""
Génère un fichier Excel exemple avec Code ISIN — format recommandé.
Exécute : python generer_exemple.py
"""
import pandas as pd

# Format recommandé : Code ISIN (accepte aussi Ticker ou nom)
donnees = {
    "Code ISIN":  [
        "MA0000012445",  # ATTIJARIWAFA BANK
        "MA0000011488",  # ITISSALAT AL-MAGHRIB (Maroc Telecom)
        "MA0000012320",  # LafargeHolcim Maroc
        "MA0000011058",  # MANAGEM
        "MA0000012247",  # COSUMAR
        "MA0000011884",  # BCP
        "MA0000012262",  # TOTALENERGIES MARKETING MAROC
        "MA0000010928",  # WAFA ASSURANCE
        "MA0000010506",  # CIMENTS DU MAROC
        "MA0000012437",  # BANK OF AFRICA
    ],
    "Quantité":   [200,   500,   50,    100,   300,   150,   80,    30,    60,    400],
    "Prix Achat": [420.0, 118.0, 1750.0,1580.0,270.0, 240.0, 1200.0,3800.0,1500.0,175.0],
}

df = pd.DataFrame(donnees)
df.to_excel("portefeuille_exemple.xlsx", index=False)
print("✅ portefeuille_exemple.xlsx créé !")
print("   Colonnes : Code ISIN | Quantité | Prix Achat")
print("   → Importez ce fichier dans le tableau de bord")
