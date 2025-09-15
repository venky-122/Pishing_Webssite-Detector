# train_model.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from detector.feature_extraction import extract_features_from_url, FEATURE_COLUMNS


def prepare_feature_dataframe(url_series: pd.Series) -> pd.DataFrame:
    rows = [extract_features_from_url(u) for u in url_series]
    df = pd.DataFrame(rows)
    # ensure column order
    return df[FEATURE_COLUMNS]

def main():
    # The CSV should have two columns: url,label
    # label: 0=legit, 1=phishing
    df = pd.read_csv("phishing_urls.csv")
    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("phishing_urls.csv must contain 'url' and 'label' columns")

    X = prepare_feature_dataframe(df["url"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"  # helps with imbalanced data
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save both model and the feature columns
    bundle = {"model": model, "feature_columns": FEATURE_COLUMNS}
    joblib.dump(bundle, "phishing_model_bundle.pkl")
    print("Saved model bundle to phishing_model_bundle.pkl")

if __name__ == "__main__":
    main()
