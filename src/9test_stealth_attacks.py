#train and test them --4.6%
import pandas as pd
import joblib

from sklearn.metrics import confusion_matrix


# Load Blue Team v2
model = joblib.load(
    "models/fraud_detector_v2.pkl"
)


# Load stealth attacks
df = pd.read_csv("data/stealth_attacks.csv"
)


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


# Predict
predictions = model.predict(X)
# Results
detected = (
    predictions == 1
).sum()

missed = (
    predictions == 0
).sum()


print(
    "Stealth attacks:",
    len(df)
)

print(
    f"Detected: {detected}/{len(df)}"
)

print(
    f"Missed: {missed}/{len(df)}"
)

print(
    f"Detection rate: "
    f"{detected / len(df):.2%}"
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y,
        predictions
    )
)