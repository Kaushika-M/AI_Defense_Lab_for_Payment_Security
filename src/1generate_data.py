#create legitimate transactions then create synthetic fraud samples--1000
import pandas as pd
import numpy as np

np.random.seed(42) #same random every time
n = 10000#no of transactions

data = {
    "transaction_id": range(1, n + 1),

    "amount": np.random.uniform(100, 5000, n),

    "account_age": np.random.randint(30, 2000, n),

    "transaction_hour": np.random.randint(0, 24, n),

    "device_changed": np.random.choice([0, 1], n, p=[0.95, 0.05]),#0-same device

    "location_changed": np.random.choice([0, 1], n, p=[0.90, 0.10]),

    "transaction_velocity": np.random.randint(1, 6, n),

    "avg_transaction_amount": np.random.uniform(100, 3000, n),

    "merchant_risk": np.random.uniform(0, 1, n),

    "behavior_deviation": np.random.uniform(0, 2, n),

    "is_fraud": 0,

    "attack_type": "legitimate"
}

df = pd.DataFrame(data)

# Calculate how different the transaction amount
# is from the customer's normal amount

df["amount_deviation"] = (
    abs(df["amount"] - df["avg_transaction_amount"])
    / df["avg_transaction_amount"]
)

# Generate synthetic fraud
fraud_count = 1000
fraud_indices = np.random.choice(   #select transaction
    df.index,
    size=fraud_count,
    replace=False
)

attack_types = np.random.choice([
        "velocity_attack",
        "device_anomaly",
        "behavior_anomaly"
    ],
    size=fraud_count
)

df.loc[fraud_indices, "is_fraud"] = 1   #marking as fraud
df.loc[fraud_indices, "attack_type"] = attack_types


# Modify features according
# to attack type
# Velocity attack
velocity_mask = df["attack_type"] == "velocity_attack"

df.loc[velocity_mask, "transaction_velocity"] = \
    np.random.randint(4, 10, velocity_mask.sum())   #moderately high velocity

df.loc[velocity_mask, "behavior_deviation"] = \
    np.random.uniform(1.0, 3.5, velocity_mask.sum())    #unusual behavior

# Device anomaly
device_mask = df["attack_type"] == "device_anomaly"

df.loc[device_mask, "device_changed"] = 1   #new device

df.loc[device_mask, "behavior_deviation"] = \
    np.random.uniform(0.8, 3.0, device_mask.sum())  # behavioral abnormality


# Behavior anomaly
behavior_mask = df["attack_type"] == "behavior_anomaly"

df.loc[behavior_mask, "behavior_deviation"] = \
    np.random.uniform(1.5, 4.0, behavior_mask.sum())

df.loc[behavior_mask, "amount"] = (
    df.loc[behavior_mask, "avg_transaction_amount"]
    * np.random.uniform(2, 4, behavior_mask.sum())
)
df["amount_deviation"] = (
    abs(df["amount"] - df["avg_transaction_amount"])
    / df["avg_transaction_amount"]
)
print(df.head())
print("\nShape:", df.shape)
print("\nFraud count:")
print(df["is_fraud"].value_counts())
print(df["attack_type"].value_counts())

df.to_csv("data/payment_transactions.csv", index=False)

