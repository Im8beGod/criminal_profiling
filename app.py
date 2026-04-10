import streamlit as st
import time
import numpy as np
from sklearn.tree import DecisionTreeClassifier

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
        "direct_access": "Direct access without mediation",
        "technical": "Strong technical capability",
        "low_technical": "Limited technical ability",
        "social": "Highly trusted and social",
        "revenge": "Possible emotional motive",
        "low_access": "Limited system permissions",
        "works_late": "Active during late hours"
    }
    return [mapping.get(t, t) for t in traits]

# =========================
# 🟢 ML MODEL
# =========================
def train_model(case):
    X, y = [], []

    for s in case["suspects"]:
        features = [
            int("admin_access" in s["traits"]),
            int("technical" in s["traits"]),
            int("social" in s["traits"]),
            int("revenge" in s["traits"]),
            int("internal_access" in s["traits"])
        ]
        X.append(features)
        y.append(s["name"])

    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

def predict_model(model, case):
    results = {}

    for s in case["suspects"]:
        features = [
            int("admin_access" in s["traits"]),
            int("technical" in s["traits"]),
            int("social" in s["traits"]),
            int("revenge" in s["traits"]),
            int("internal_access" in s["traits"])
        ]

        prob = model.predict_proba([features])[0]
        results[s["name"]] = max(prob)

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

if case.get("complexity") == "hard":
    st.warning("⚠️ Complex case: misleading evidence present")

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
st.warning("Motive alone is not enough. Capability determines feasibility.")

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

    ai_scores = {}
    elimination_log = {}

    st.markdown("## 🧠 System Analysis")

    for s in case["suspects"]:
        score = 0
        reasons = []

        st.markdown(f"### Evaluating {s['name']}")

        for clue in clues:
            time.sleep(0.3)

            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                    msg = f"Failed: {clue['text']}"
                    st.error(msg)
                    reasons.append(msg)
                else:
                    score += 10
                    msg = f"Valid: {clue['text']}"
                    st.success(msg)
                    reasons.append(msg)

        ai_scores[s["name"]] = score
        elimination_log[s["name"]] = reasons

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # 🟢 ML MODEL OUTPUT
    # =========================
    model = train_model(case)
    ml_results = predict_model(model, case)
    ml_top = max(ml_results, key=ml_results.get)

    st.markdown("## 🧠 Predictive Model")

    for name, prob in ml_results.items():
        st.write(f"{name}: {round(prob*100,2)}%")
        st.progress(int(prob*100))

    st.write(f"Most Likely (ML): {ml_top}")

    # =========================
    # RESULTS
    # =========================
    st.markdown("## ⚖️ Results")
    st.write("You:", user_guess)
    st.write("System:", ai_top)
    st.write("ML Model:", ml_top)
    st.write("Actual:", true)

    # =========================
    # FEEDBACK
    # =========================
    st.markdown("## 🧠 Reasoning Feedback")

    bias = max(bias_counter, key=bias_counter.get)

    if bias == "motive":
        st.warning("You focused on motive but ignored feasibility constraints.")
    elif bias == "access":
        st.success("You focused on capability, which aligns with system reasoning.")
    else:
        st.warning("You relied on behavioral patterns, which may be misleading.")

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
