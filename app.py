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

.highlight-pass {border:2px solid #00ffcc; box-shadow:0 0 15px #00ffcc;}
.highlight-fail {border:2px solid red; box-shadow:0 0 15px red;}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎬 MISSION BRIEFING STATE
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

# =========================
# 🎬 MISSION BRIEFING SCREEN
# =========================
if not st.session_state.started:

    st.title("🕵️ Forensic Investigation System")

    st.markdown("""
    ### 🔒 CLASSIFIED BRIEFING

    You are assigned as an **investigator**.

    Your objective:
    - Analyze the case
    - Evaluate suspects
    - Identify the culprit

    ⚠️ Important:
    - Motive can mislead  
    - Behavior can deceive  
    - Only **feasibility and constraints reveal truth**
    """)

    st.markdown("""
    ### 🎯 YOUR TASK
    1. Study evidence  
    2. Analyze suspects  
    3. Answer reasoning questions  
    4. Make your decision  
    """)

    if st.button("🚀 START INVESTIGATION"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================
# MAIN SYSTEM STARTS HERE
# =========================
st.title("🕵️ Investigation Console")
st.caption("Analyze. Eliminate. Conclude.")

# =========================
# PROFILE
# =========================
def generate_profile(traits):
    mapping = {
        "admin_access":"Admin access",
        "internal_access":"Internal access",
        "direct_access":"Direct system access",
        "technical":"Technically skilled",
        "social":"Trusted",
        "revenge":"Possible motive",
        "low_access":"Limited permissions"
    }
    return [mapping.get(t,t) for t in traits]

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

def logistic(x): return 1/(1+np.exp(-x))

def train_model(clues):
    w=np.array([0.8,0.7,0.9,0.5,0.3,0.2,-0.6])
    for c in clues:
        if c["type"]=="constraint":
            for r in c["rules"]:
                if r=="admin_access": w[0]+=0.5
                if r=="internal_access": w[1]+=0.5
                if r=="direct_access": w[2]+=0.5
    return w

def predict(case,w):
    return {s["name"]: logistic(np.dot(w,extract_features(s))) for s in case["suspects"]}

# =========================
# DIFFICULTY
# =========================
if "score_history" not in st.session_state:
    st.session_state.score_history=[]

avg=sum(st.session_state.score_history)/len(st.session_state.score_history) if st.session_state.score_history else 0
difficulty="Hard" if avg>30 else "Medium" if avg>0 else "Easy"

st.write(f"🎯 Difficulty: {difficulty}")

# =========================
# CASE
# =========================
case=random.choice(cases)
clues=case["clues"][:]

if "extra_clues" in case:
    clues+=random.sample(case["extra_clues"],k=min(1,len(case["extra_clues"])))

if difficulty=="Hard" and len(clues)>1:
    clues=clues[:-1]

# =========================
# DASHBOARD
# =========================
col1,col2=st.columns(2)

with col1:
    st.markdown("<div class='section-title'>📁 CASE</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{case['description']}</div>",unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-title'>🔍 EVIDENCE</div>",unsafe_allow_html=True)
    for c in clues:
        st.markdown(f"<div class='panel'>• {c['text']}</div>",unsafe_allow_html=True)

col3,col4=st.columns(2)

with col3:
    st.markdown("<div class='section-title'>🧑 SUSPECTS</div>",unsafe_allow_html=True)
    for s in case["suspects"]:
        profile=generate_profile(s["traits"])
        st.markdown(f"<div class='panel'><b>{s['name']}</b><br>{'<br>'.join('• '+p for p in profile)}</div>",unsafe_allow_html=True)

with col4:
    st.markdown("<div class='section-title'>🧠 ANALYSIS</div>",unsafe_allow_html=True)

    bias_counter={}
    for i,q in enumerate(questions):
        ans=st.radio(q["question"],list(q["options"].keys()),key=i)
        bias=q["options"][ans]
        bias_counter[bias]=bias_counter.get(bias,0)+1

    user_guess=st.selectbox("Select suspect:",[s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    st.markdown("## 🧠 ANALYSIS")

    ai_scores={}
    for s in case["suspects"]:
        score=0
        status="highlight-pass"

        for clue in clues:
            time.sleep(0.2)
            if clue["type"]=="constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score-=100
                    status="highlight-fail"

        st.markdown(f"<div class='panel {status}'><b>{s['name']}</b></div>",unsafe_allow_html=True)
        ai_scores[s["name"]]=score

    ai_top=max(ai_scores,key=ai_scores.get)
    true=case["true_suspect"]

    weights=train_model(clues)
    ml_results=predict(case,weights)
    ml_top=max(ml_results,key=ml_results.get)

    st.markdown("## ⚖️ RESULTS")
    st.write("You:",user_guess)
    st.write("System:",ai_top)
    st.write("Model:",ml_top)
    st.write("Actual:",true)

    score=50 if user_guess==true else -20
    st.session_state.score_history.append(score)

    st.markdown(f"## 🎮 SCORE: {score}")
