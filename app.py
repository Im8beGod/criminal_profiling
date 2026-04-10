import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="AI Profiling", layout="centered")

# 🎨 STYLE
st.markdown("""
<style>
.stApp {background:#05070d;color:white;font-family:monospace;}
.card {background:#0d1117;padding:12px;border-radius:10px;margin:6px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Criminal Profiling Simulator")

# 🧠 STATE
if "step" not in st.session_state:
    st.session_state.step = 0

# =========================
# STEP 0 → INTRO
# =========================
if st.session_state.step == 0:

    st.markdown("""
    ### 🧠 Your Mission

    Analyze the case, study the suspects, and identify the culprit.

    Then compare your reasoning with AI.
    """)

    if st.button("Start"):
        st.session_state.step = 1


# =========================
# STEP 1 → CASE + SUSPECTS
# =========================
elif st.session_state.step == 1:

    case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])
    st.session_state.case = case

    st.header("📁 Case")
    st.write(case["description"])

    st.header("🔍 Evidence")
    for c in case["clues"]:
        st.markdown(f"<div class='card'>• {c['text']}</div>", unsafe_allow_html=True)

    st.header("🧑 Suspects")

    for s in case["suspects"]:
        st.markdown(f"<div class='card'><b>{s['name']}</b></div>", unsafe_allow_html=True)

    if st.button("Continue"):
        st.session_state.step = 2


# =========================
# STEP 2 → USER GUESS
# =========================
elif st.session_state.step == 2:

    case = st.session_state.case

    st.header("🧠 Your Guess")

    suspects = [s["name"] for s in case["suspects"]]

    guess = st.selectbox("Who do you think is the culprit?", suspects)

    if st.button("Lock Answer"):
        st.session_state.user_guess = guess
        st.session_state.step = 3


# =========================
# STEP 3 → QUESTIONS
# =========================
elif st.session_state.step == 3:

    st.header("🧪 Reasoning Analysis")

    user_answers = {}

    for i, q in enumerate(questions):
        user_answers[i] = st.radio(q["question"], list(q["options"].keys()), key=i)

    if st.button("Analyze"):
        st.session_state.answers = user_answers
        st.session_state.step = 4


# =========================
# STEP 4 → RESULT
# =========================
elif st.session_state.step == 4:

    case = st.session_state.case
    answers = st.session_state.answers

    with st.spinner("Analyzing..."):
        time.sleep(2)

    # 🧠 HUMAN MODEL
    human_scores = {}
    for i, ans in answers.items():
        for t, w in questions[i]["options"][ans].items():
            human_scores[t] = human_scores.get(t, 0) + w

    human_result = {}
    for s in case["suspects"]:
        score = sum(human_scores.get(t, 0) for t in s["traits"])
        human_result[s["name"]] = score

    human_top = max(human_result, key=human_result.get)

    # 🤖 AI MODEL
    ai_scores = {}
    for clue in case["clues"]:
        for t, w in clue["traits"].items():
            ai_scores[t] = ai_scores.get(t, 0) + w

    ai_result = {}
    for s in case["suspects"]:
        score = sum(ai_scores.get(t, 0) for t in s["traits"])
        ai_result[s["name"]] = score

    ai_top = max(ai_result, key=ai_result.get)

    true = case["true_suspect"]

    # ⚖️ RESULT
    st.header("⚖️ Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 You")
        st.write(st.session_state.user_guess)

    with col2:
        st.subheader("🤖 AI")
        st.write(ai_top)

    # 🕵️ TRUTH
    st.header("🕵️ Truth")
    st.write(true)

    # 📊 INSIGHT
    st.header("📊 Insight")

    if st.session_state.user_guess != true:
        st.error("Your reasoning was biased")
        st.warning(f"Bias: {case['bias']}")
    else:
        st.success("Correct!")

    if ai_top == true:
        st.success("AI used evidence correctly")

    st.info("Humans rely on intuition. AI relies on structured evidence.")

    if st.button("Restart"):
        st.session_state.step = 0
