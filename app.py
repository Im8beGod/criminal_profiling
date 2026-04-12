import streamlit as st
import time
import random
import numpy as np

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# =========================
# 🎮 UI STYLE (ENHANCED)
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

.highlight-eval {border:2px solid yellow;}
.highlight-pass {border:2px solid #00ffcc;}
.highlight-fail {border:2px solid red;}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎬 TYPEWRITER EFFECT
# =========================
def typewriter(text, speed=0.01):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(speed)

# =========================
# 🎬 MISSION BRIEFING
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("🕵️ Forensic Investigation System")

    typewriter("Initializing secure system...\n")
    typewriter("Loading investigation modules...\n")

    st.markdown("""
    ### 🔒 CLASSIFIED BRIEFING
    Analyze. Eliminate. Conclude.
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
# CLUES
# =========================
clues = case["clues"][:]
if "extra_clues" in case:
    clues += random.sample(case["extra_clues"], k=min(1,len(case["extra_clues"])))

# =========================
# DASHBOARD
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 CASE")
    st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

    st.markdown("### 🕒 TIMELINE")
    for t in case.get("timeline", []):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🔍 TECHNICAL")
    for t in case.get("technical", []):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

    st.markdown("### 🧩 OBSERVATIONS")
    for o in case.get("observations", []):
        st.markdown(f"<div class='panel'>• {o}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS + QUESTIONS
# =========================
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🧑 SUSPECTS")
    for s in case["suspects"]:
        st.markdown(f"<div class='panel'><b>{s['name']}</b><br>{'<br>'.join(s.get('traits',[]))}</div>", unsafe_allow_html=True)

with col4:
    st.markdown("### 🧠 YOUR ANALYSIS")

    bias_counter = {}
    progress = st.progress(0)

    for i,q in enumerate(questions):
        ans = st.radio(q["question"], list(q["options"].keys()), key=i)
        bias = q["options"][ans]
        bias_counter[bias] = bias_counter.get(bias,0)+1
        progress.progress((i+1)/len(questions))

    user_guess = st.selectbox("Select suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN
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

    st.markdown("## ⚖️ RESULTS")
    st.write(f"🧠 You: {user_guess}")
    st.write(f"🤖 System: {ai_top}")
    st.write(f"🕵️ Actual: {true}")

    st.markdown("## 📊 ANALYTICS")

    total = sum(bias_counter.values())
    for k,v in bias_counter.items():
        st.write(f"{k}: {int((v/total)*100)}%")
        st.progress(int((v/total)*100))
