import streamlit as st
import time
import random
import numpy as np

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# =========================
# 🎮 UI (UPGRADED)
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #060a1a, #02030a);
    color: #e6f1ff;
    font-family: monospace;
}

.panel {
    background: rgba(11,18,32,0.85);
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid rgba(0,255,200,0.15);
    box-shadow: 0 0 12px rgba(0,255,200,0.08);
}

.section-title {
    color: #00ffcc;
    font-size: 18px;
    margin-top: 20px;
    margin-bottom: 5px;
    letter-spacing: 1px;
}

button[kind="primary"] {
    background: linear-gradient(90deg,#00ffcc,#00aaff);
    color: black;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Investigation Console")
st.caption("Analyze. Eliminate. Conclude.")

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
# 🟢 PRODUCTION ML
# =========================
def extract_features(s):
    return np.array([
        int("admin_access" in s["traits"]),
        int("internal_access" in s["traits"]),
        int("direct_access" in s["traits"]),
        int("technical" in s["traits"]),
        int("social" in s["traits"]),
        int("revenge" in s["traits"]),
        int("low_access" in s["traits"])
    ])

def logistic(x):
    return 1 / (1 + np.exp(-x))

def train_model(clues):
    weights = np.array([0.8,0.7,0.9,0.5,0.3,0.2,-0.6])

    for clue in clues:
        if clue["type"] == "constraint":
            for r in clue["rules"]:
                if r == "admin_access": weights[0]+=0.5
                if r == "internal_access": weights[1]+=0.5
                if r == "direct_access": weights[2]+=0.5

    return weights

def predict(case, weights):
    results = {}
    for s in case["suspects"]:
        x = extract_features(s)
        prob = logistic(np.dot(weights, x))
        results[s["name"]] = prob
    return results

# =========================
# 🎯 ADAPTIVE DIFFICULTY
# =========================
if "score_history" not in st.session_state:
    st.session_state.score_history = []

avg_score = sum(st.session_state.score_history)/len(st.session_state.score_history) if st.session_state.score_history else 0

if avg_score > 30:
    difficulty = "Hard"
elif avg_score > 0:
    difficulty = "Medium"
else:
    difficulty = "Easy"

st.write(f"🎯 Difficulty Level: {difficulty}")

# =========================
# CASE (RANDOMIZED)
# =========================
case = random.choice(cases)

st.markdown("<div class='section-title'>📁 CASE FILE</div>", unsafe_allow_html=True)
st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

# =========================
# DYNAMIC CLUES
# =========================
clues = case["clues"][:]

if "extra_clues" in case:
    clues += random.sample(case["extra_clues"], k=min(1, len(case["extra_clues"])))

if difficulty == "Hard" and len(clues) > 1:
    clues = clues[:-1]

st.markdown("<div class='section-title'>🔍 EVIDENCE LOG</div>", unsafe_allow_html=True)

for c in clues:
    st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS
# =========================
st.markdown("<div class='section-title'>🧑 SUSPECT PROFILES</div>", unsafe_allow_html=True)
st.warning("Capability matters more than motive.")

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
st.markdown("<div class='section-title'>🧠 YOUR ANALYSIS</div>", unsafe_allow_html=True)

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

# =========================
# FINAL DECISION
# =========================
st.markdown("<div class='section-title'>🎯 FINAL DECISION</div>", unsafe_allow_html=True)

user_guess = st.selectbox("Select the suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN INVESTIGATION
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    st.markdown("<div class='section-title'>🧠 SYSTEM ANALYSIS</div>", unsafe_allow_html=True)

    ai_scores = {}

    for s in case["suspects"]:
        score = 0

        st.markdown(f"### Evaluating {s['name']}")

        for clue in clues:
            time.sleep(0.25)

            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                    st.error(f"❌ Failed: {clue['text']}")
                else:
                    score += 10
                    st.success(f"✔ Valid: {clue['text']}")

        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # ML MODEL
    # =========================
    weights = train_model(clues)
    ml_results = predict(case, weights)
    ml_top = max(ml_results, key=ml_results.get)

    st.markdown("<div class='section-title'>🧠 PREDICTIVE MODEL</div>", unsafe_allow_html=True)

    for name, prob in ml_results.items():
        percent = int(prob * 100)
        st.write(f"{name}: {percent}%")
        st.progress(percent)

    # =========================
    # RESULTS
    # =========================
    st.markdown("<div class='section-title'>⚖️ RESULTS</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🧠 You:", user_guess)

    with col2:
        st.write("🤖 System:", ai_top)

    with col3:
        st.write("📊 Model:", ml_top)

    st.markdown("### 🕵️ Actual Culprit")
    st.write(true)

    # =========================
    # FEEDBACK
    # =========================
    st.markdown("<div class='section-title'>🧠 REASONING FEEDBACK</div>", unsafe_allow_html=True)

    bias = max(bias_counter, key=bias_counter.get)

    if bias == "motive":
        st.warning("You focused on motive but ignored feasibility constraints.")
    elif bias == "access":
        st.success("You focused on capability. Strong analytical reasoning.")
    else:
        st.warning("Behavioral reasoning can be misleading without constraints.")

    # =========================
    # SCORE + ADAPTATION
    # =========================
    score = 50 if user_guess == true else -20
    st.session_state.score_history.append(score)

    st.markdown(f"<div class='section-title'>🎮 SCORE: {score}</div>", unsafe_allow_html=True)
