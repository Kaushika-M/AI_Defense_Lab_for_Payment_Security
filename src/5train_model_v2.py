#train the model for df+hard_train
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)
# Load Blue Team training dataset
# v2 should train on df+hard_train 10500
#test will be done speparately
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


X = df[features]
y = df["is_fraud"]

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    min_samples_leaf=2
)
model.fit(X, y)


print("\nBlue Team v2 trained.")


# Save model
joblib.dump(
    model,
    "models/fraud_detector_v2.pkl"
)

print(
    "Model saved to "
    "models/fraud_detector_v2.pkl"
)