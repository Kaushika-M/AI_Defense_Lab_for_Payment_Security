#take og dataset and 500 as fraud and its attack is stealth_velocity_v2
#modify features
import pandas as pd
import numpy as np

np.random.seed(300)

# Load legitimate transactions
df = pd.read_csv(
    "data/payment_transactions.csv"
)

# Select legitimate templates
templates = df[
    df["is_fraud"] == 0
].sample(
    500,
    random_state=300
).copy()


# Create new unseen stealth attacks
attacks = templates.copy()

attacks["transaction_id"] = range(
    30001,
    30501
)

attacks["is_fraud"] = 1

attacks["attack_type"] = (
    "stealth_velocity_v2"
)


# -----------------------------------
# Slightly different from Stealth v1
# -----------------------------------

# Instead of exactly 5
attacks["transaction_velocity"] = np.random.randint(
    5,
    7,
    len(attacks)
)


# Keep device normal
attacks["device_changed"] = 0


# Keep location mostly normal
attacks["location_changed"] = np.random.choice(
    [0, 1],
    len(attacks),
    p=[0.95, 0.05]
)


# Normal-ish behavior
attacks["behavior_deviation"] = np.random.uniform(
    0.8,
    1.6,
    len(attacks)
)


# Moderate merchant risk
attacks["merchant_risk"] = np.random.uniform(
    0.25,
    0.75,
    len(attacks)
)


# Moderate amount deviation
attacks["amount_deviation"] = np.random.uniform(
    0.3,
    2.2,
    len(attacks)
)


# Save
attacks.to_csv(
    "data/stealth_attacks_v2.csv",
    index=False
)


print(
    "Stealth v2 attacks:",
    len(attacks)
)

print("\nAverage values:")

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