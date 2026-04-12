import streamlit as st
import time
import random
import numpy as np

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# =========================
# 🎮 UI STYLE
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
}

.highlight-eval {border:2px solid yellow;}
.highlight-pass {border:2px solid #00ffcc;}
.highlight-fail {border:2px solid red;}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎬 MISSION BRIEFING
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("🕵️ Forensic Investigation System")

    st.markdown("""
    ### 🔒 CLASSIFIED BRIEFING
    You are assigned as an investigator.

    - Analyze evidence  
    - Evaluate suspects  
    - Identify the culprit  

    ⚠️ Constraints > Motive
    """)

    if st.button("🚀 START INVESTIGATION"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================
# CASE LOCK
# =========================
if "current_case" not in st.session_state:
    st.session_state.current_case = random.choice(cases)

case = st.session_state.current_case

if st.button("🔄 New Case"):
    st.session_state.current_case = random.choice(cases)
    st.rerun()

st.title("🕵️ Investigation Console")
st.caption(f"Case ID: {hash(case['case_name']) % 10000}")

# =========================
# PROFILE
# =========================
def generate_profile(traits):
    return [t.replace("_", " ").title() for t in traits]

# =========================
# ML
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
    w = np.array([0.8,0.7,0.9,0.5,0.3,0.2,-0.6])
    for c in clues:
        if c["type"]=="constraint":
            for r in c["rules"]:
                if r=="admin_access": w[0]+=0.5
                if r=="internal_access": w[1]+=0.5
                if r=="direct_access": w[2]+=0.5
    return w

def predict(case, w):
    return {s["name"]: logistic(np.dot(w, extract_features(s))) for s in case["suspects"]}

# =========================
# DIFFICULTY
# =========================
if "score_history" not in st.session_state:
    st.session_state.score_history=[]

avg = sum(st.session_state.score_history)/len(st.session_state.score_history) if st.session_state.score_history else 0
difficulty = "Hard" if avg>30 else "Medium" if avg>0 else "Easy"

st.write(f"🎯 Difficulty: {difficulty}")

# =========================
# CLUES
# =========================
clues = case["clues"][:]
if "extra_clues" in case:
    clues += random.sample(case["extra_clues"], k=min(1,len(case["extra_clues"])))

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 CASE")
    st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🔍 EVIDENCE")
    for c in clues:
        st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🧑 SUSPECTS")
    for s in case["suspects"]:
        profile = generate_profile(s["traits"])
        st.markdown(f"<div class='panel'><b>{s['name']}</b><br>{'<br>'.join(profile)}</div>", unsafe_allow_html=True)

with col4:
    st.markdown("### 🧠 ANALYSIS")

    bias_counter = {}
    for i,q in enumerate(questions):
        ans = st.radio(q["question"], list(q["options"].keys()), key=i)
        bias = q["options"][ans]
        bias_counter[bias] = bias_counter.get(bias,0)+1

    user_guess = st.selectbox("Select suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    st.markdown("## 🧠 ANALYSIS STARTED")

    ai_scores={}
    for s in case["suspects"]:
        score=0
        for clue in clues:
            if clue["type"]=="constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score-=100
                else:
                    score+=10
        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    weights = train_model(clues)
    ml_results = predict(case, weights)
    ml_top = max(ml_results, key=ml_results.get)

    # =========================
    # RESULTS
    # =========================
    st.markdown("## ⚖️ RESULTS")

    c1,c2,c3 = st.columns(3)
    c1.write(f"🧠 You: {user_guess}")
    c2.write(f"🤖 System: {ai_top}")
    c3.write(f"📊 Model: {ml_top}")

    st.write(f"🕵️ Actual: {true}")

    # =========================
    # 📊 ADVANCED ANALYTICS
    # =========================
    st.markdown("## 📊 ADVANCED ANALYTICS")

    # Probability chart
    st.markdown("### 🔍 Suspect Probability Distribution")
    for n,p in ml_results.items():
        percent = int(p*100)
        st.write(f"{n}: {percent}%")
        st.progress(percent)

    # Bias meter
    st.markdown("### 🧠 Bias Meter")
    total = sum(bias_counter.values()) if bias_counter else 1
    for k,v in bias_counter.items():
        percent = int((v/total)*100)
        st.write(f"{k}: {percent}%")
        st.progress(percent)

    # Reasoning comparison
    st.markdown("### 🎯 Decision Comparison")
    if user_guess == true:
        st.success("You identified the correct suspect.")
    else:
        st.error("Your reasoning diverged from the actual outcome.")

    if ai_top == true:
        st.success("System reasoning is correct.")
    else:
        st.warning("System reasoning mismatch (edge case).")

    if ml_top == true:
        st.success("ML prediction aligns with reality.")

    # Feature influence
    st.markdown("### 🧬 Feature Influence")
    st.info("Model prioritizes access, system constraints, and technical capability over emotional motive.")

    score = 50 if user_guess == true else -20
    st.session_state.score_history.append(score)

    st.markdown(f"## 🎮 SCORE: {score}")
