import streamlit as st
import time

from cases import cases
from questions import questions
from engine import calculate_user_model, calculate_ai_model

st.set_page_config(page_title="AI Criminal Profiler", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>
.stApp {background-color:#05070d;color:white;}
.card {background:#0d1117;padding:15px;border-radius:10px;margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Human vs AI Criminal Profiling")

# 🧠 INTRO
st.info("Analyze the case yourself. Then compare your reasoning with AI.")

# 📁 CASE SELECT
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
    st.markdown(f"<div class='card'><b>{s['name']}</b><br>" +
                "<br>".join("• "+d for d in s["description"]) +
                "</div>", unsafe_allow_html=True)

# 🧠 USER
st.header("🧠 Your Analysis")

user_guess = st.selectbox("Your suspect", [s["name"] for s in case["suspects"]])

user_answers = {}
for i,q in enumerate(questions):
    user_answers[i] = st.radio(q["question"], list(q["options"].keys()), key=i)

# 🚨 RUN
if st.button("Run Investigation"):

    with st.spinner("Processing..."):
        time.sleep(2)

    user_res = calculate_user_model(case, user_answers, questions)
    ai_res = calculate_ai_model(case)

    user_top, _ = user_res[0]
    ai_top, _ = ai_res[0]
    true = case["true_suspect"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Result")
        st.write(user_top)

    with col2:
        st.subheader("🤖 AI Result")
        st.write(ai_top)

    st.header("🕵️ Truth")
    st.write(true)

    st.header("📊 Insight")

    if user_top != true:
        st.error("Your reasoning was flawed.")
        st.warning(f"Bias detected: {case['bias_type']}")
    else:
        st.success("You got it right!")

    if ai_top == true:
        st.success("AI correctly solved the case using evidence.")

st.caption("Educational simulation")
