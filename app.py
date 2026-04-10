import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="AI Criminal Profiling", layout="wide")

# 🎨 FBI STYLE
st.markdown("""
<style>
.stApp {background-color:#05070d;color:white;font-family:monospace;}
.card {background:#0d1117;padding:10px;border-radius:10px;margin:5px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Human vs AI Criminal Profiling")

st.info("Analyze the case yourself. Then compare with AI.")

# 📁 SELECT CASE
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

# 📁 CASE
st.header("📁 Case")
st.write(case["description"])

# 🔍 CLUES
st.header("🔍 Evidence")
for c in case["clues"]:
    st.markdown(f"<div class='card'>• {c['text']}</div>", unsafe_allow_html=True)

# 🧑 SUSPECTS
st.header("🧑 Suspects")
for s in case["suspects"]:
    st.markdown(f"<div class='card'>{s['name']}</div>", unsafe_allow_html=True)

# 🧠 USER INPUT
st.header("🧠 Your Analysis")

user_guess = st.selectbox("Your suspect", [s["name"] for s in case["suspects"]])

user_answers = {}
for i, q in enumerate(questions):
    user_answers[i] = st.radio(q["question"], list(q["options"].keys()), key=i)

# 🚨 RUN
if st.button("Run Investigation"):

    with st.spinner("Analyzing..."):
        time.sleep(2)

    # 🧠 HUMAN MODEL
    human_scores = {}

    for i, ans in user_answers.items():
        for t, w in questions[i]["options"][ans].items():
            human_scores[t] = human_scores.get(t, 0) + w

    human_result = {}

    for s in case["suspects"]:
        score = 0
        for t in s["traits"]:
            score += human_scores.get(t, 0)
        human_result[s["name"]] = score

    human_top = max(human_result, key=human_result.get)

    # 🤖 AI MODEL
    ai_scores = {}

    for clue in case["clues"]:
        for t, w in clue["traits"].items():
            ai_scores[t] = ai_scores.get(t, 0) + w

    ai_result = {}

    for s in case["suspects"]:
        score = 0
        for t in s["traits"]:
            score += ai_scores.get(t, 0)
        ai_result[s["name"]] = score

    ai_top = max(ai_result, key=ai_result.get)

    true = case["true_suspect"]

    # ⚖️ SPLIT VIEW
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Result")
        st.write(human_top)

    with col2:
        st.subheader("🤖 AI Result")
        st.write(ai_top)

    # 🕵️ TRUTH
    st.header("🕵️ Truth")
    st.write(true)

    # 📊 INSIGHT
    st.header("📊 Insight")

    if human_top != true:
        st.error("Your reasoning was incorrect")
        st.warning(f"Bias detected: {case['bias']}")
    else:
        st.success("You were correct")

    if ai_top == true:
        st.success("AI solved it using evidence")

    st.info("AI uses structured evidence. Humans rely on intuition.")
