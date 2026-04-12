import streamlit as st
import time
import random
import numpy as np

from cases import cases
from questions import questions
from generator import generate_case

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
}
.highlight-eval {border:2px solid yellow; box-shadow:0 0 10px yellow;}
.highlight-pass {border:2px solid #00ffcc; box-shadow:0 0 10px #00ffcc;}
.highlight-fail {border:2px solid red; box-shadow:0 0 10px red;}
.panel:hover {
    transform: scale(1.02);
    transition: 0.2s;
}
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
    typewriter("Loading intelligence modules...\n")

    st.markdown("""
    ### 🔒 CLASSIFIED BRIEFING
    Analyze evidence. Eliminate impossibilities. Identify the culprit.

    ⚠️ Constraints > Motive
    """)

    if st.button("🚀 START INVESTIGATION"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================
# 🎯 MODE + CASE LOCK
# =========================
mode = st.radio("Mode", ["Static Cases", "Dynamic Case"])

if "current_case" not in st.session_state:
    st.session_state.current_case = random.choice(cases)

if st.button("🔄 New Case"):
    st.session_state.current_case = random.choice(cases)
    st.rerun()

case = generate_case() if mode == "Dynamic Case" else st.session_state.current_case

st.title("🕵️ Investigation Console")
st.caption(f"Case ID: {hash(case['case_name']) % 10000}")

# =========================
# 🎯 DIFFICULTY
# =========================
if "score_history" not in st.session_state:
    st.session_state.score_history = []

avg = sum(st.session_state.score_history)/len(st.session_state.score_history) if st.session_state.score_history else 0
difficulty = "Hard" if avg > 30 else "Medium" if avg > 0 else "Easy"
st.write(f"🎯 Difficulty Level: {difficulty}")

# =========================
# 🔍 CLUES
# =========================
clues = case["clues"][:]

# =========================
# 🖥️ SIDE-BY-SIDE INFO (FIXED)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 CASE BRIEF")
    st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

    st.markdown("### 🕒 TIMELINE")
    for t in case.get("timeline", []):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🖥️ TECHNICAL EVIDENCE")
    for t in case.get("technical", []):
        st.markdown(f"<div class='panel'>• {t}</div>", unsafe_allow_html=True)

    st.markdown("### 🧩 OBSERVATIONS")
    for o in case.get("observations", []):
        st.markdown(f"<div class='panel'>• {o}</div>", unsafe_allow_html=True)

# =========================
# 🧑 SUSPECTS + ANALYSIS SIDE-BY-SIDE
# =========================
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🧑 SUSPECT DOSSIERS")

    for i, s in enumerate(case["suspects"]):

        with st.expander(f"🔍 {s['name']}", expanded=False):

            st.markdown("<div class='panel'>", unsafe_allow_html=True)

            st.markdown("**🧬 Traits**")
            for t in s["traits"]:
                st.markdown(f"- {t.replace('_',' ').title()}")

            if "details" in s:
                st.markdown("**📄 Background**")
                for d in s["details"]:
                    st.markdown(f"- {d}")

            st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("### 🧠 YOUR ANALYSIS")

    bias_counter = {}
    progress = st.progress(0)

    for i, q in enumerate(questions):
        ans = st.radio(q["question"], list(q["options"].keys()), key=i)
        bias = q["options"][ans]
        bias_counter[bias] = bias_counter.get(bias, 0) + 1
        progress.progress((i+1)/len(questions))

    user_guess = st.selectbox("Select suspect:", [s["name"] for s in case["suspects"]])

# =========================
# 🟢 ML + LOGIC (UNCHANGED)
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
# 🚨 RUN INVESTIGATION
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    typewriter("System analyzing suspects...\n", 0.02)

    ai_scores = {}

    for s in case["suspects"]:
        score = 0
        container = st.empty()

        container.markdown(f"<div class='panel highlight-eval'><b>{s['name']}</b><br>Evaluating...</div>", unsafe_allow_html=True)
        time.sleep(0.3)

        for clue in clues:
            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                    status = "highlight-fail"
                else:
                    score += 10
                    status = "highlight-pass"

        container.markdown(f"<div class='panel {status}'><b>{s['name']}</b></div>", unsafe_allow_html=True)

        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    weights = train_model(clues)
    ml_results = predict(case, weights)
    ml_top = max(ml_results, key=ml_results.get)

    # RESULTS
    st.markdown("## ⚖️ RESULTS")

    c1, c2, c3 = st.columns(3)
    c1.write(f"🧠 You: {user_guess}")
    c2.write(f"🤖 System: {ai_top}")
    c3.write(f"📊 Model: {ml_top}")

    st.write(f"🕵️ Actual: {true}")

    # ANALYTICS
    # =========================
# 📊 ADVANCED ANALYTICS
# =========================
st.markdown("## 📊 ADVANCED ANALYTICS")

# -------------------------
# 🔍 Probability Distribution
# -------------------------
st.markdown("### 🔍 Probability Distribution")

for n, p in ml_results.items():
    percent = int(p * 100)
    st.write(f"{n}: {percent}%")
    st.progress(percent)

# -------------------------
# 🧠 Cognitive Bias Profile (FIXED)
# -------------------------
st.markdown("""
### 🧠 Cognitive Bias Profile

This reflects **how you approached the investigation**:

- 🔴 **Motive-driven** → Focus on emotions, revenge, intent  
- 🔵 **Access-driven** → Focus on capability and system constraints  
- 🟡 **Behavior-driven** → Focus on patterns and actions  

⚠️ Real-world investigations prioritize **access & constraints over motive**
""")

total = sum(bias_counter.values()) if bias_counter else 1

for k, v in bias_counter.items():
    percent = int((v / total) * 100)

    if k == "motive":
        label = "🔴 Motive Focus"
    elif k == "access":
        label = "🔵 Access Focus"
    else:
        label = "🟡 Behavior Focus"

    st.write(f"{label}: {percent}%")
    st.progress(percent)

# -------------------------
# 🎯 Decision Analysis
# -------------------------
st.markdown("## 🎯 DECISION ANALYSIS")

if user_guess == true:
    st.success("Correct identification")
else:
    st.error("Incorrect reasoning")
