from download_data import download_data
from clean_transform import clean_transform
from load_final import load_final

def run_data_pipeline():
    """
    Pipeline complet pour préparer les données.
    """
    df = download_data()
    X_train, X_test, y_train, y_test = clean_transform(df)
    load_final(X_train, X_test, y_train, y_test)
