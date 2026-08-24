import streamlit as st
import pandas as pd
import numpy as np
import joblib


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("models/fraud_detector_v3.pkl")


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Defense Lab",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🛡️ AI Defense Lab")
st.subheader("GenAI Payment Fraud Detection")

st.caption("Identify → Generate → Defend → Adapt")


# ==========================================
# BLUE TEAM
# ==========================================

st.header("🔵 Blue Team")

st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=100.0,
    max_value=20000.0,
    value=2500.0
)

account_age = st.sidebar.number_input(
    "Account Age (days)",
    min_value=30,
    max_value=2000,
    value=1000
)

transaction_hour = st.sidebar.slider(
    "Transaction Hour",
    0,
    23,
    12
)

device_changed = st.sidebar.selectbox(
    "Device Changed?",
    [0, 1],
    format_func=lambda x: "No" if x == 0 else "Yes"
)

location_changed = st.sidebar.selectbox(
    "Location Changed?",
    [0, 1],
    format_func=lambda x: "No" if x == 0 else "Yes"
)

transaction_velocity = st.sidebar.slider(
    "Transaction Velocity",
    1,
    10,
    3
)

avg_transaction_amount = st.sidebar.number_input(
    "Average Transaction Amount",
    min_value=100.0,
    max_value=10000.0,
    value=2000.0
)

merchant_risk = st.sidebar.slider(
    "Merchant Risk",
    0.0,
    1.0,
    0.5
)

behavior_deviation = st.sidebar.slider(
    "Behavior Deviation",
    0.0,
    5.0,
    1.0
)

amount_deviation = (
    abs(amount - avg_transaction_amount)
    / avg_transaction_amount
)

st.sidebar.metric(
    "Amount Deviation",
    f"{amount_deviation:.2f}"
)


# ==========================================
# BLUE TEAM ANALYSIS
# ==========================================

if st.button(
    "🔍 Analyze Transaction",
    use_container_width=True
):

    transaction = pd.DataFrame([{
        "amount": amount,
        "account_age": account_age,
        "transaction_hour": transaction_hour,
        "device_changed": device_changed,
        "location_changed": location_changed,
        "transaction_velocity": transaction_velocity,
        "avg_transaction_amount": avg_transaction_amount,
        "merchant_risk": merchant_risk,
        "behavior_deviation": behavior_deviation,
        "amount_deviation": amount_deviation
    }])

    prediction = model.predict(transaction)[0]

    probability = model.predict_proba(
        transaction
    )[0][1]

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        if prediction == 1:
            st.error("🚨 FRAUD DETECTED")
        else:
            st.success("✅ LEGITIMATE")

    with col2:

        st.metric(
            "Fraud Probability",
            f"{probability * 100:.2f}%"
        )

    with col3:

        if probability >= 0.75:
            risk = "HIGH"
        elif probability >= 0.40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        st.metric(
            "Risk Level",
            risk
        )


# ==========================================
# RED TEAM
# ==========================================

st.divider()

st.header("🔴 Red Team Attack Simulator")

attack_type = st.selectbox(
    "Choose Attack",
    [
        "Velocity Attack",
        "Device Anomaly",
        "Behavior Anomaly",
        "Hard Velocity Attack",
        "Stealth Velocity Attack"
    ]
)


if st.button(
    "⚔️ Generate Attack",
    use_container_width=True
):

    # Load legitimate transactions

    data = pd.read_csv(
        "data/payment_transactions.csv"
    )

    legitimate = data[
        data["is_fraud"] == 0
    ]

    # Pick legitimate transaction as template

    attack = legitimate.sample(
        1,
        random_state=np.random.randint(
            0,
            100000
        )
    ).copy()


    # ======================================
    # ATTACK GENERATION
    # ======================================

    if attack_type == "Velocity Attack":

        attack["transaction_velocity"] = np.random.randint(
            6,
            10
        )

        attack["behavior_deviation"] = np.random.uniform(
            1.5,
            3.5
        )


    elif attack_type == "Device Anomaly":

        attack["device_changed"] = 1


    elif attack_type == "Behavior Anomaly":

        attack["behavior_deviation"] = np.random.uniform(
            2.5,
            4.0
        )

        attack["amount"] = (
            attack["avg_transaction_amount"]
            * np.random.uniform(2, 4)
        )


    elif attack_type == "Hard Velocity Attack":

        attack["transaction_velocity"] = np.random.randint(
            5,
            8
        )

        attack["behavior_deviation"] = np.random.uniform(
            0.7,
            1.7
        )

        attack["device_changed"] = np.random.choice(
            [0, 1],
            p=[0.95, 0.05]
        )


    elif attack_type == "Stealth Velocity Attack":

        attack["transaction_velocity"] = 5

        attack["behavior_deviation"] = np.random.uniform(
            0.7,
            1.5
        )

        attack["device_changed"] = 0

        attack["location_changed"] = 0

        attack["merchant_risk"] = np.random.uniform(
            0.3,
            0.6
        )


    # ======================================
    # AMOUNT DEVIATION
    # ======================================

    attack["amount_deviation"] = (
        abs(
            attack["amount"]
            - attack["avg_transaction_amount"]
        )
        / attack["avg_transaction_amount"]
    )


    # ======================================
    # MODEL FEATURES
    # ======================================

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

    attack_features = attack[features]


    # ======================================
    # BLUE TEAM DETECTION
    # ======================================

    prediction = model.predict(
        attack_features
    )[0]

    probability = model.predict_proba(
        attack_features
    )[0][1]


    # ======================================
    # RESULT
    # ======================================

    st.subheader(
        f"⚔️ {attack_type}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Fraud Probability",
            f"{probability * 100:.2f}%"
        )

    with col2:

        if prediction == 1:

            st.success(
                "🛡️ ATTACK DETECTED"
            )

        else:

            st.error(
                "🚨 ATTACK MISSED"
            )


# ==========================================
# ADAPTIVE DEFENSE
# ==========================================

st.divider()

st.header("🔄 Adaptive Defense")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Stealth v1",
        "4.6%"
    )

with col2:
    st.metric(
        "Stealth v2",
        "88.8%"
    )

with col3:
    st.metric(
        "Improvement",
        "+84.2 pp"
    )