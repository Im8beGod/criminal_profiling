import streamlit as st
import time
import numpy as np

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# =========================
# 🎮 UI
# =========================
st.markdown("""
<style>
.stApp {background:#04060c;color:#e6f1ff;font-family:monospace;}
.panel {background:#0b1220;padding:12px;border-radius:8px;margin:8px;border:1px solid #1f2a44;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Investigation Console")

# =========================
# 🧠 PROFILE GENERATOR
# =========================
def generate_profile(traits):
    mapping = {
        "admin_access": "Has administrative system access",
        "internal_access": "Can access internal network",
        "direct_access": "Direct system access",
        "technical": "Technically skilled",
        "low_technical": "Limited technical ability",
        "social": "Highly trusted socially",
        "revenge": "Possible emotional motive",
        "low_access": "Limited permissions",
        "works_late": "Active during late hours"
    }
    return [mapping.get(t, t) for t in traits]

# =========================
# 🟢 FEATURE ENGINEERING
# =========================
def extract_features(suspect):
    return np.array([
        int("admin_access" in suspect["traits"]),
        int("internal_access" in suspect["traits"]),
        int("direct_access" in suspect["traits"]),
        int("technical" in suspect["traits"]),
        int("social" in suspect["traits"]),
        int("revenge" in suspect["traits"]),
        int("low_access" in suspect["traits"])
    ])

# =========================
# 🟢 SIMPLE LOGISTIC MODEL
# =========================
def logistic(x):
    return 1 / (1 + np.exp(-x))

def train_production_model(case, clues):
    weights = np.array([0.8, 0.7, 0.9, 0.5, 0.3, 0.2, -0.6])

    # adjust weights dynamically using clues
    for clue in clues:
        if clue["type"] == "constraint":
            for rule in clue["rules"]:
                if rule == "admin_access":
                    weights[0] += 0.5
                if rule == "internal_access":
                    weights[1] += 0.5
                if rule == "direct_access":
                    weights[2] += 0.5

    return weights

def predict_production(case, weights):
    results = {}

    for s in case["suspects"]:
        x = extract_features(s)
        score = np.dot(weights, x)
        prob = logistic(score)
        results[s["name"]] = prob

    return results

# =========================
# 🎯 DIFFICULTY
# =========================
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# =========================
# 🏆 LEADERBOARD
# =========================
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# =========================
# CASE
# =========================
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

st.markdown("## 📁 Case")
st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

# =========================
# EVIDENCE
# =========================
st.markdown("## 🔍 Evidence")

clues = case["clues"]

if difficulty == "Medium":
    clues = clues[:-1]
elif difficulty == "Hard":
    clues = clues[:-2]

for c in clues:
    st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS
# =========================
st.markdown("## 🧑 Suspects")
st.warning("Capability determines feasibility.")

for s in case["suspects"]:
    profile = generate_profile(s["traits"])

    st.markdown(f"""
    <div class='panel'>
    <b>{s['name']}</b><br>
    {"<br>".join("• " + p for p in profile)}
    </div>
    """, unsafe_allow_html=True)

# =========================
# QUESTIONS
# =========================
st.markdown("## 🧠 Your Reasoning")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

# =========================
# FINAL GUESS
# =========================
user_guess = st.selectbox("Your suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("🚨 Run Investigation"):

    st.markdown("## 🧠 Constraint Analysis")

    ai_scores = {}

    for s in case["suspects"]:
        score = 0

        for clue in clues:
            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                else:
                    score += 10

        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # 🟢 PRODUCTION ML
    # =========================
    weights = train_production_model(case, clues)
    ml_results = predict_production(case, weights)

    ml_top = max(ml_results, key=ml_results.get)

    st.markdown("## 🧠 Predictive Model")

    for name, prob in ml_results.items():
        percent = int(prob * 100)
        st.write(f"{name}: {percent}%")
        st.progress(percent)

    st.write(f"Most Likely: {ml_top}")

    # =========================
    # RESULTS
    # =========================
    st.markdown("## ⚖️ Results")
    st.write("You:", user_guess)
    st.write("System:", ai_top)
    st.write("Model:", ml_top)
    st.write("Actual:", true)

    # =========================
    # SCORE
    # =========================
    score = 50 if user_guess == true else -20

    if difficulty == "Medium":
        score *= 1.5
    elif difficulty == "Hard":
        score *= 2

    st.markdown(f"## 🎮 Score: {int(score)}")

    # =========================
    # LEADERBOARD
    # =========================
    name = st.text_input("Enter name:")

    if st.button("Submit Score"):
        st.session_state.leaderboard.append((name, int(score)))

    st.markdown("## 🏆 Leaderboard")

    board = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)

    for i, (n, s) in enumerate(board[:5]):
        st.write(f"{i+1}. {n} — {s}")
