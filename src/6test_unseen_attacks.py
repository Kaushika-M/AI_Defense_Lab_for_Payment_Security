#test on unseen dataset with 500 rows
import pandas as pd
import joblib

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

#load v2 model
model = joblib.load(
    "models/fraud_detector_v2.pkl"
)

df = pd.read_csv(
    "data/hard_attacks_test.csv"
)
print(df.shape)

features = [
    "amount",
    "account_age",
    "transaction_hour",
    "device_changed",
    "location_changed",
    "transaction_velocity",
    "avg_transaction_amount",
    "merchant_risk",
    "behavior_deviation",
    "amount_deviation"
]


X = df[features]
y = df["is_fraud"]


predictions = model.predict(X)

print("Unseen attacks:", len(df))


print("\nClassification Report:")

print(
    classification_report(
        y,
        predictions
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y,
        predictions
    )
)


# -----------------------------------
# Detection rate
# -----------------------------------

detected = (
    predictions == 1
).sum()


detection_rate = (
    detected / len(df)
)


print(
    f"\nUnseen attack detection: "
    f"{detected}/{len(df)} "
    f"({detection_rate:.2%})"
)