import pandas as pd

results = [
    {
        "stage": "Blue Team v1",
        "attack": "Hard Velocity",
        "attacks_tested": 500,
        "detected": 197,
        "detection_rate": 39.40
    },
    {
        "stage": "Blue Team v2",
        "attack": "Unseen Hard Velocity",
        "attacks_tested": 500,
        "detected": 348,
        "detection_rate": 69.60
    },
    {
        "stage": "Blue Team v2",
        "attack": "Stealth v1",
        "attacks_tested": 500,
        "detected": 23,
        "detection_rate": 4.60
    },
    {
        "stage": "Blue Team v3",
        "attack": "Unseen Stealth v2",
        "attacks_tested": 500,
        "detected": 444,
        "detection_rate": 88.80
    }
]


df = pd.DataFrame(results)

print("AI DEFENSE LAB - FINAL EXPERIMENT RESULTS")
print(df.to_string(index=False))


print("\n----------------------------------------------")

best = df.loc[
    df["detection_rate"].idxmax()
]

print(
    f"Best result: {best['stage']} "
    f"on {best['attack']}"
)

print(
    f"Detection rate: {best['detection_rate']:.2f}%"
)


print("\n----------------------------------------------")

improvement = (
    88.80 - 4.60
)

print("Adaptive improvement:",
    f"{improvement:.2f} percentage points"
)


df.to_csv(
    "data/final.csv",
    index=False
)

print("\nSaved to data/final.csv")