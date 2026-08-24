#split create model and train them and evaluate
# evaluate with diff attack_types and see the missed one
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Load dataset
df = pd.read_csv("data/payment_transactions.csv")

# Features used by the model
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

# Split data
X_train, X_test, y_train, y_test = train_test_split(X,y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nROC-AUC:")
print(roc_auc_score(y_test, y_proba))

# Evaluate each attack type

results = df.loc[X_test.index].copy()#pull the full original rows

results["prediction"] = y_pred #add y_pred as new column

print("\nAttack-wise detection:")
for attack in results["attack_type"].unique():
    attack_data = results[ #rows belonging to the current attack type
        results["attack_type"] == attack
    ]
    if attack != "legitimate":
        detected = ( #how many rows of this specific attack type were predicted as fraud
            attack_data["prediction"] == 1
        ).sum()

        total = len(attack_data)    #number of transactions belonging to that attack type

        recall = detected / total

        print(f"{attack}: "
            f"{detected}/{total} detected "
            f"({recall:.2%})"
        )

# Find missed fraud attacks
results["fraud_probability"] = y_proba

missed = results[   #rows where the transaction was actually fraud but the model predicted legitimate
    (results["is_fraud"] == 1) &
    (results["prediction"] == 0)
]

print("\nMissed fraud transactions:")
print(
    missed[
        [
            "attack_type",
            "amount",
            "transaction_velocity",
            "device_changed",
            "behavior_deviation",
            "amount_deviation",
            "merchant_risk",
            "fraud_probability"
        ]
    ].sort_values(
        "fraud_probability"
    ).head(10)
)        

import joblib

joblib.dump(model,
    "models/fraud_detector.pkl"
)
print("\nModel saved successfully.")