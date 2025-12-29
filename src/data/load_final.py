import os

def load_final(X_train, X_test, y_train, y_test, output_dir="data_final"):
    """
    Sauvegarde les données finales en format Parquet.
    """
    os.makedirs(output_dir, exist_ok=True)

    X_train.to_parquet(f"{output_dir}/X_train.parquet")
    X_test.to_parquet(f"{output_dir}/X_test.parquet")
    y_train.to_frame().to_parquet(f"{output_dir}/y_train.parquet")
    y_test.to_frame().to_parquet(f"{output_dir}/y_test.parquet")

    print("Final data saved!")
