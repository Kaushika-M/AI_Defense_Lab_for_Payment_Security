#combine df+hard_train--payment_transactions_v2.csv with stealth_attacks.csv
#form df_v3
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier


# -----------------------------------
# Load existing Blue Team v2 data
# -----------------------------------

df = pd.read_csv(
    "data/payment_transactions_v2.csv"
)


# -----------------------------------
# Load stealth attacks
# -----------------------------------

stealth = pd.read_csv(
    "data/stealth_attacks.csv"
)


# -----------------------------------
# Combine training data
# -----------------------------------

df_v3 = pd.concat(
    [
        df,
        stealth
    ],
    ignore_index=True
)


print(
    "Blue Team v3 training data:",
    df_v3.shape
)


print("\nAttack distribution:")

print(
    df_v3["attack_type"].value_counts()
)


# -----------------------------------
# Features
# -----------------------------------

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


X = df_v3[features]

y = df_v3["is_fraud"]


# -----------------------------------
# Train
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=400,
    random_state=42,
    class_weight="balanced",
    min_samples_leaf=2
)


model.fit(X, y)


# -----------------------------------
# Save
# -----------------------------------

joblib.dump(
    model,
    "models/fraud_detector_v3.pkl"
)


print(
    "\nBlue Team v3 saved!"
)