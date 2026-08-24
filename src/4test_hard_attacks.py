#test the df+hard_train dataset
#get only hard_velocity_attacks and train the model---39.4%
import pandas as pd
import joblib

from sklearn.metrics import classification_report, confusion_matrix

# Load trained model
model = joblib.load("models/fraud_detector.pkl")


# Load new dataset
# df_v2---df+hard_train---payment_transactions_v2.csv
df = pd.read_csv("data/payment_transactions_v2.csv")


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


# Select ONLY hard attacks
hard_attacks = df[df["attack_type"] == "hard_velocity_attack"].copy()


X_hard = hard_attacks[features]
y_hard = hard_attacks["is_fraud"]


# Predict
predictions = model.predict(X_hard)


print("Hard attacks:", len(hard_attacks))

print("\nDetection results:")
print(
    classification_report(
        y_hard,
        predictions
    )
)


print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_hard,
        predictions
    )
)


detected = (predictions == 1).sum()

recall = detected / len(hard_attacks)

print(
    f"\nHard attack detection: "
    f"{detected}/{len(hard_attacks)} "
    f"({recall:.2%})"
)