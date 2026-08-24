#train and test the model--88.8%
import pandas as pd
import joblib

from sklearn.metrics import confusion_matrix


# Load Blue Team v3
model = joblib.load(
    "models/fraud_detector_v3.pkl"
)


# Load unseen Stealth v2 attacks
df = pd.read_csv(
    "data/stealth_attacks_v2.csv"
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


# Calculate results
detected = (predictions == 1).sum()
missed = (predictions == 0).sum()

detection_rate = detected / len(df)


print("Unseen Stealth v2 attacks:", len(df))

print(
    f"Detected: {detected}/{len(df)}"
)

print(
    f"Missed: {missed}/{len(df)}"
)

print(
    f"Detection rate: {detection_rate:.2%}"
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y,
        predictions
    )
)