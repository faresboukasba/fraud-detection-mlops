from sklearn.model_selection import train_test_split

def clean_transform(df, test_size=0.2, random_state=42):
    """
    Sépare les données en train/test avec stratification.
    """
    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    return X_train, X_test, y_train, y_test
