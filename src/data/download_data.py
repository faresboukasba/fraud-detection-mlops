import kagglehub
import pandas as pd
import os

def download_data():
    """
    Télécharge la dataset via kagglehub et charge automatiquement le CSV.
    """
    # Téléchargement
    path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    print("Fichiers téléchargés dans :", path)

    # Chercher le CSV téléchargé
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans le dossier KaggleHub.")

    csv_path = os.path.join(path, csv_files[0])
    print("CSV détecté :", csv_path)

    df = pd.read_csv(csv_path)
    print("Shape data:", df.shape)

    return df


df = download_data()
