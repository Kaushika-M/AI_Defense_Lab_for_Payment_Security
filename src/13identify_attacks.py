#created taxonomy families with attack type=10
import pandas as pd

attacks = [{
        "attack_id": "A01",
        "attack_name": "Velocity Attack",
        "category": "Transaction",
        "description":
            "Rapid sequence of transactions designed to exploit "
            "transaction velocity limits.",
        "signals":
            "High transaction velocity, repeated transactions",
        "simulation":
            "Increase transaction_velocity",
        "implemented": True
    },

    {
        "attack_id": "A02",
        "attack_name": "Device Anomaly",
        "category": "Device / Identity",
        "description":
            "Fraudulent transaction originating from a previously "
            "unseen or changed device.",
        "signals":
            "device_changed, unusual device behavior",
        "simulation":
            "Set device_changed = 1",
        "implemented": True
    },

    {
        "attack_id": "A03",
        "attack_name": "Behavior Anomaly",
        "category": "Behavioral",
        "description":
            "Transaction behavior differs significantly from "
            "the customer's historical behavior.",
        "signals":
            "High behavior deviation, unusual amount",
        "simulation":
            "Increase behavior_deviation and amount",
        "implemented": True
    },

    {
        "attack_id": "A04",
        "attack_name": "Hard Velocity Attack",
        "category": "Adaptive",
        "description":
            "Velocity attack designed to remain close to legitimate "
            "transaction behavior.",
        "signals":
            "Moderately elevated velocity",
        "simulation":
            "Velocity around 5-7 with normal supporting features",
        "implemented": True
    },

    {
        "attack_id": "A05",
        "attack_name": "Stealth Velocity Attack",
        "category": "Adaptive",
        "description":
            "Velocity attack that intentionally mimics legitimate "
            "device, location and behavioral characteristics.",
        "signals":
            "Moderate velocity with minimal anomalies",
        "simulation":
            "Velocity around 5 while keeping other features normal",
        "implemented": True
    },

    {
        "attack_id": "A06",
        "attack_name": "AI Phishing",
        "category": "Social Engineering",
        "description":
            "AI-generated messages designed to convince users "
            "to reveal payment credentials or approve transactions.",
        "signals":
            "Suspicious links, unusual communication patterns",
        "simulation":
            "Future extension",
        "implemented": False
    },

    {
        "attack_id": "A07",
        "attack_name": "Deepfake Impersonation",
        "category": "Social Engineering",
        "description":
            "AI-generated voice or video impersonation used to "
            "convince victims or support agents to authorize payments.",
        "signals":
            "Identity inconsistencies, unusual authorization behavior",
        "simulation":
            "Future extension",
        "implemented": False
    },

    {
        "attack_id": "A08",
        "attack_name": "Synthetic Identity",
        "category": "Identity",
        "description":
            "Combination of fabricated and legitimate identity "
            "attributes to create fraudulent accounts.",
        "signals":
            "Inconsistent identity and account history",
        "simulation":
            "Future extension",
        "implemented": False
    },

    {
        "attack_id": "A09",
        "attack_name": "Low-and-Slow Fraud",
        "category": "Adaptive",
        "description":
            "Small fraudulent transactions spread over time to "
            "avoid velocity-based detection.",
        "signals":
            "Subtle repeated deviations",
        "simulation":
            "Future extension",
        "implemented": False
    },

    {
        "attack_id": "A10",
        "attack_name": "Multi-Feature Mimicry",
        "category": "Adaptive",
        "description":
            "Attacker modifies multiple transaction features "
            "to resemble legitimate customer behavior.",
        "signals":
            "Weak individual signals but correlated anomalies",
        "simulation":
            "Future extension",
        "implemented": False
    }
]

df = pd.DataFrame(attacks)

print("\n=== GenAI Payment Fraud Attack Taxonomy ===\n")
print(df[
    [
        "attack_id",
        "attack_name",
        "category",
        "implemented"
    ]
].to_string(index=False)
)


print("\nTotal attack types:", len(df))

print(
    "Implemented:",
    df["implemented"].sum()
)

print(
    "Future extensions:",
    (~df["implemented"]).sum()
)


df.to_csv(
    "data/attack_taxonomy.csv",
    index=False
)

print(
    "\nSaved to data/attack_taxonomy.csv"
)