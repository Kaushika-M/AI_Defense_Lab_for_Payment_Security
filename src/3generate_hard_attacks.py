#take 1000 legitimate transactions and make it as fraud with type hard_velocity_attack
#first 500 is hard_train and next 500 is hard_test
#change its velocity , device behavior deviation
#calc amount_deviation
# df_v2---df+hard_train---payment_transactions_v2.csv

import pandas as pd
import numpy as np

np.random.seed(100)

df = pd.read_csv("data/payment_transactions.csv")

templates = df[         #1000 legitimate transactions
    df["is_fraud"] == 0
].sample(
    1000,
    random_state=100
).copy()

hard_attacks = templates.copy()
hard_attacks["transaction_id"] = range(
    10001,
    11001
)
hard_attacks["is_fraud"] = 1
hard_attacks["attack_type"] = (
    "hard_velocity_attack"
)

hard_train = hard_attacks.iloc[:500].copy()
hard_test = hard_attacks.iloc[500:].copy()

hard_train["transaction_velocity"] = np.random.randint(
    4,
    7,
    len(hard_train)
)

hard_train["behavior_deviation"] = np.random.uniform(
    0.5,
    1.5,
    len(hard_train)
)

hard_train["device_changed"] = np.random.choice(
    [0, 1],
    len(hard_train),
    p=[0.95, 0.05]
)

hard_test["transaction_velocity"] = np.random.randint(
    5,
    8,
    len(hard_test)
)

hard_test["behavior_deviation"] = np.random.uniform(
    0.7,
    1.7,
    len(hard_test)
)

hard_test["device_changed"] = np.random.choice(
    [0, 1],
    len(hard_test),
    p=[0.95, 0.05]
)

hard_train["amount_deviation"] = (
    abs(
        hard_train["amount"]
        - hard_train["avg_transaction_amount"]
    )
    / hard_train["avg_transaction_amount"]
)


hard_test["amount_deviation"] = (
    abs(
        hard_test["amount"]
        - hard_test["avg_transaction_amount"]
    )
    / hard_test["avg_transaction_amount"]
)


hard_train.to_csv(
    "data/hard_attacks_train.csv",
    index=False
)

hard_test.to_csv(
    "data/hard_attacks_test.csv",
    index=False
)


df_v2 = pd.concat(
    [
        df,
        hard_train
    ],
    ignore_index=True
)


df_v2.to_csv(
    "data/payment_transactions_v2.csv",
    index=False
)


print(
    "Original transactions:",
    len(df)
)

print(
    "Training hard attacks:",
    len(hard_train)
)

print(
    "Unseen test attacks:",
    len(hard_test)
)

print(
    "Blue Team v2 dataset:",
    len(df_v2)
)


print("\nAttack distribution:")

print(
    df_v2["attack_type"].value_counts()
)