import streamlit as st
import time
import random
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
# 🧠 PROFILE
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

st.write(f"Adaptive Difficulty: {difficulty}")

# =========================
# CASE + RANDOMIZATION
# =========================
case = random.choice(cases)

st.markdown("## 📁 Case")
st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

# =========================
# DYNAMIC CLUES
# =========================
clues = case["clues"][:]

if "extra_clues" in case:
    clues += random.sample(case["extra_clues"], k=min(1,len(case["extra_clues"])))

if difficulty == "Hard":
    clues = clues[:-1]

st.markdown("## 🔍 Evidence")
for c in clues:
    st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS
# =========================
st.markdown("## 🧑 Suspects")
for s in case["suspects"]:
    profile = generate_profile(s["traits"])
    st.markdown(f"<div class='panel'><b>{s['name']}</b><br>{'<br>'.join('• '+p for p in profile)}</div>", unsafe_allow_html=True)

# =========================
# QUESTIONS
# =========================
bias_counter = {}
for i,q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias]=bias_counter.get(bias,0)+1

user_guess = st.selectbox("Your suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("Run Investigation"):

    ai_scores={}
    for s in case["suspects"]:
        score=0
        for clue in clues:
            if clue["type"]=="constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score-=100
                else:
                    score+=10
        ai_scores[s["name"]]=score

    ai_top=max(ai_scores,key=ai_scores.get)

    weights=train_model(clues)
    ml_results=predict(case,weights)
    ml_top=max(ml_results,key=ml_results.get)

    st.markdown("## 🧠 ML Output")
    for n,p in ml_results.items():
        percent=int(p*100)
        st.write(f"{n}: {percent}%")
        st.progress(percent)

    true=case["true_suspect"]

    st.markdown("## ⚖️ Results")
    st.write("You:",user_guess)
    st.write("System:",ai_top)
    st.write("Model:",ml_top)
    st.write("Actual:",true)

    score=50 if user_guess==true else -20
    st.session_state.score_history.append(score)

    st.markdown(f"Score: {score}")
