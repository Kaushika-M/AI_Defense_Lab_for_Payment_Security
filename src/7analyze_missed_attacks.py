#print missed attacks rows to analyse
import pandas as pd
import joblib

# Load Blue Team v2
model = joblib.load(
    "models/fraud_detector_v2.pkl"
)

# Load unseen attacks
df = pd.read_csv(
    "data/hard_attacks_test.csv"
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

# Get fraud probability
df["fraud_probability"] = (
    model.predict_proba(X)[:, 1]
)


# Find missed attacks
missed = df[
    df["fraud_probability"] < 0.5
].copy()


print(
    "Total unseen attacks:",
    len(df)
)

print(
    "Missed attacks:",
    len(missed)
)

print(
    "Detected attacks:",
    len(df) - len(missed)
)


# Show hardest attacks
print("\n10 hardest attacks:")

print(
    missed[
        [
            "amount",
            "transaction_velocity",
            "behavior_deviation",
            "device_changed",
            "location_changed",
            "merchant_risk",
            "amount_deviation",
            "fraud_probability"
        ]
    ].head(10)
)


# Average values
print(
    "\nAverage values of missed attacks:"
)

print(
    missed[features].mean()
)


# Average values of detected attacks
detected = df[
    df["fraud_probability"] >= 0.5
]

print(
    "\nAverage values of detected attacks:"
)

print(
    detected[features].mean()
)