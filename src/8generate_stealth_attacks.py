# create 500 legitimate as fraud and chagne to stealth_velocity_attack.modify features
#as per missed.

import pandas as pd
import numpy as np

np.random.seed(200)

# Load legitimate transactions
df = pd.read_csv(
    "data/payment_transactions.csv"
)

# Select legitimate templates
templates = df[
    df["is_fraud"] == 0
].sample(
    500,
    random_state=200
).copy()


# -----------------------------------
# Create stealth velocity attacks
# -----------------------------------

attacks = templates.copy()

attacks["transaction_id"] = range(
    20001,
    20501
)

attacks["is_fraud"] = 1

attacks["attack_type"] = (
    "stealth_velocity_attack"
)


# -----------------------------------
# Target the discovered weakness
# -----------------------------------

# Moderate velocity
# as missed attacks have velocity as 5
attacks["transaction_velocity"] = 5


# Keep device normal
attacks["device_changed"] = 0


# Keep location normal
attacks["location_changed"] = 0


# Keep behavior close to normal
attacks["behavior_deviation"] = np.random.uniform(
    0.7,
    1.5,
    len(attacks)
)


# Keep merchant risk relatively normal
attacks["merchant_risk"] = np.random.uniform(
    0.2,
    0.7,
    len(attacks)
)


# Keep amount deviation relatively moderate
attacks["amount_deviation"] = np.random.uniform(
    0.2,
    2.0,
    len(attacks)
)


# -----------------------------------
# Save
# -----------------------------------

attacks.to_csv(
    "data/stealth_attacks.csv",
    index=False
)


print(
    "Stealth attacks generated:",
    len(attacks)
)

print(
    "\nAverage values:"
)

print(
    attacks[
        [
            "amount",
            "transaction_velocity",
            "behavior_deviation",
            "device_changed",
            "location_changed",
            "merchant_risk",
            "amount_deviation"
        ]
    ].mean()
)