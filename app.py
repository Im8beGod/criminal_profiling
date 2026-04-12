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
    background: rgba(11,18,32,0.9);
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid rgba(0,255,200,0.2);
    box-shadow: 0 0 15px rgba(0,255,200,0.15);
    transition: 0.3s ease;
}

.panel:hover {
    transform: scale(1.02);
}

.section-title {
    color: #00ffcc;
    font-size: 18px;
    margin-top: 20px;
}

.highlight-eval {border:2px solid yellow; box-shadow:0 0 15px yellow;}
.highlight-pass {border:2px solid #00ffcc; box-shadow:0 0 15px #00ffcc;}
.highlight-fail {border:2px solid red; box-shadow:0 0 15px red;}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎬 TYPEWRITER
# =========================
def typewriter(text, speed=0.01):
    placeholder = st.empty()
    out = ""
    for c in text:
        out += c
        placeholder.markdown(out)
        time.sleep(speed)

# =========================
# 🎬 MISSION BRIEFING
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("🕵️ Forensic Investigation System")

    typewriter("Initializing system...\n")
    typewriter("Loading modules...\n")

    st.markdown("""
    ### 🔒 CLASSIFIED BRIEFING

    - Analyze evidence  
    - Evaluate suspects  
    - Identify culprit  

    ⚠️ Constraints > Motive
    """)

    if st.button("🚀 START INVESTIGATION"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================
# 🎯 CASE LOCK
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
# 🧠 PROFILE
# =========================
def generate_profile(traits):
    return [t.replace("_"," ").title() for t in traits]

# =========================
# 🟢 ML MODEL
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
    return 1/(1+np.exp(-x))

def train_model(clues):
    w = np.array([0.8,0.7,0.9,0.5,0.3,0.2,-0.6])
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
# 🎯 DIFFICULTY
# =========================
if "score_history" not in st.session_state:
    st.session_state.score_history=[]

avg = sum(st.session_state.score_history)/len(st.session_state.score_history) if st.session_state.score_history else 0
difficulty = "Hard" if avg>30 else "Medium" if avg>0 else "Easy"

st.write(f"🎯 Difficulty: {difficulty}")

# =========================
# 🔍 CLUES
# =========================
clues = case["clues"][:]
if "extra_clues" in case:
    clues += random.sample(case["extra_clues"], k=min(1,len(case["extra_clues"])))

# =========================
# 🖥️ DASHBOARD
# =========================
col1,col2 = st.columns(2)

with col1:
    st.markdown("### 📁 INCIDENT")
    st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

    st.markdown("### 🕒 TIMELINE")
    for t in case.get("timeline",[]):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🖥️ TECHNICAL")
    for t in case.get("technical",[]):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

    st.markdown("### 🧩 OBSERVATIONS")
    for o in case.get("observations",[]):
        st.markdown(f"<div class='panel'>• {o}</div>", unsafe_allow_html=True)

col3,col4 = st.columns(2)

with col3:
    st.markdown("### 🧑 SUSPECTS")
    for s in case["suspects"]:
        profile = generate_profile(s["traits"])
        st.markdown(f"<div class='panel'><b>{s['name']}</b><br>{'<br>'.join(profile)}</div>", unsafe_allow_html=True)

with col4:
    st.markdown("### 🧠 ANALYSIS")

    bias_counter={}
    progress = st.progress(0)

    for i,q in enumerate(questions):
        ans = st.radio(q["question"], list(q["options"].keys()), key=i)
        bias = q["options"][ans]
        bias_counter[bias] = bias_counter.get(bias,0)+1
        progress.progress((i+1)/len(questions))

    user_guess = st.selectbox("Select suspect:", [s["name"] for s in case["suspects"]])

# =========================
# 🚨 RUN
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    typewriter("System initializing...\n",0.02)
    typewriter("Analyzing suspects...\n",0.02)

    ai_scores={}

    for s in case["suspects"]:
        score=0
        container=st.empty()

        container.markdown(f"<div class='panel highlight-eval'><b>{s['name']}</b><br>Evaluating...</div>", unsafe_allow_html=True)
        time.sleep(0.3)

        for clue in clues:
            if clue["type"]=="constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score-=100
                    status="highlight-fail"
                else:
                    score+=10
                    status="highlight-pass"

        container.markdown(f"<div class='panel {status}'><b>{s['name']}</b></div>", unsafe_allow_html=True)
        ai_scores[s["name"]] = score

    ai_top=max(ai_scores,key=ai_scores.get)
    true=case["true_suspect"]

    weights=train_model(clues)
    ml_results=predict(case,weights)
    ml_top=max(ml_results,key=ml_results.get)

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
    # 📊 ANALYTICS
    # =========================
    st.markdown("## 📊 ADVANCED ANALYTICS")

    st.markdown("### 🔍 Probabilities")
    for n,p in ml_results.items():
        percent=int(p*100)
        st.write(f"{n}: {percent}%")
        st.progress(percent)

    st.markdown("### 🧠 Bias")
    total=sum(bias_counter.values()) if bias_counter else 1
    for k,v in bias_counter.items():
        percent=int((v/total)*100)
        st.write(f"{k}: {percent}%")
        st.progress(percent)

    st.markdown("### 🎯 Decision Analysis")
    if user_guess == true:
        st.success("Correct identification")
    else:
        st.error("Incorrect reasoning")

    st.info("System prioritizes constraints over emotional reasoning.")

    score = 50 if user_guess == true else -20
    st.session_state.score_history.append(score)

    st.markdown(f"## 🎮 SCORE: {score}")
