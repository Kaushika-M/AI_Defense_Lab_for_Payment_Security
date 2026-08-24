# 🛡️ AI Defense Lab

## GenAI-Powered Payment Fraud Detection

AI Defense Lab is a Red Team / Blue Team system for detecting evolving payment fraud attacks.

The system follows:

**Identify → Generate → Defend → Adapt**

---
## 🌐 Live Demo

Try the working prototype:

[AI Defense Lab - Live Demo](https://ai-defense-lab.streamlit.app/)
## 🎯 What I Built

### 🔴 Red Team
Identifies and generates synthetic payment fraud attacks.

Implemented attacks:

- Velocity Attack
- Device Anomaly
- Behavior Anomaly
- Hard Velocity Attack
- Stealth Velocity Attack

I identified **10 attack types** in total, with 5 currently implemented.

### 🔵 Blue Team
Uses a **Random Forest machine-learning model** to detect fraudulent transactions.

The model uses 10 features:

- Transaction amount
- Account age
- Transaction hour
- Device change
- Location change
- Transaction velocity
- Average transaction amount
- Merchant risk
- Behavior deviation
- Amount deviation

### 🔄 Adaptive Defense

The attacks that the model struggles to detect are used to create harder attacks and improve the next version of the model.

---

## 📊 Results

| Stage | Attack | Detection |
|---|---|---:|
| Blue Team v1 | Hard Velocity | 39.4% |
| Blue Team v2 | Unseen Hard Velocity | 69.6% |
| Blue Team v2 | Stealth v1 | 4.6% |
| Blue Team v3 | Unseen Stealth v2 | **88.8%** |

### 🏆 Best Result

**Unseen Stealth v2: 88.8% detection**

Detection improved from:

**4.6% → 88.8%**

That's an improvement of **84.2 percentage points**.

---

## 🖥️ Dashboard

The Streamlit dashboard provides:

### Blue Team
Enter a transaction and get:

- Fraud / Legitimate prediction
- Fraud probability
- Risk level

### Red Team
Select an attack type and generate a synthetic attack.

The generated attack is immediately tested by the Blue Team detector.

---

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- Joblib
- Streamlit

---

## 🚀 How to Run

### 1. Create virtual environment

python -m venv venv

### 2. Activate environment

.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run dashboard

streamlit run dashboard.py
