import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

CSV_PATH = "/home/pi/sensor_log.csv"
MODEL_PATH = "/home/pi/aq_model.joblib"

def main():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = ["temp_c", "hum_pct", "mq2", "mq135"]
    for col in required_cols:
        if col not in df.columns:
            raise SystemExit(f"Missing column: {col}")

    # Ensure numeric
    for c in required_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=required_cols)

    # Percentile thresholds (auto, data-driven)
    mq2_p33, mq2_p66 = df["mq2"].quantile([0.33, 0.66]).values
    mq135_p33, mq135_p66 = df["mq135"].quantile([0.33, 0.66]).values

    def label_from_value(v, p33, p66):
        if v < p33:
            return 0  # Good
        if v < p66:
            return 1  # Moderate
        return 2      # Bad

    # Label each sample using the worse of MQ2 and MQ135 labels
    labels_mq2 = df["mq2"].apply(lambda v: label_from_value(v, mq2_p33, mq2_p66))
    labels_mq135 = df["mq135"].apply(lambda v: label_from_value(v, mq135_p33, mq135_p66))
    df["label"] = pd.concat([labels_mq2, labels_mq135], axis=1).max(axis=1).astype(int)

    # Print label distribution
    print("Label distribution:")
    print(df["label"].value_counts().sort_index())
    print("\nThresholds:")
    print(f"mq2:   p33={mq2_p33:.2f}, p66={mq2_p66:.2f}")
    print(f"mq135: p33={mq135_p33:.2f}, p66={mq135_p66:.2f}")

    X = df[["temp_c", "hum_pct", "mq2", "mq135"]].astype(float)
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=400))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=3))

    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
