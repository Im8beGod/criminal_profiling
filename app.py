import streamlit as st
import time

from cases import cases
from questions import questions
from engine import calculate_results, generate_explanation

st.set_page_config(page_title="AI Investigation Engine", layout="centered")

# 🔥 FBI STYLE
st.markdown("""
<style>
.stApp {
    background-color: #05070d;
    color: #e8f0ff;
    font-family: 'Courier New', monospace;
}
.card {
    background: #0d1117;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #1f2a44;
    margin-bottom: 10px;
}
.section {
    color: #4ea1ff;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ AI Investigation Engine")

# ✅ SAFE LOAD
if not cases:
    st.error("No case data found")
    st.stop()

case = cases[0]

# 📁 CASE
st.markdown("## 📁 Case File")
st.write(case.get("description", ""))

# 🔍 CLUES (SAFE)
st.markdown("## 🔍 Evidence")
for clue in case.get("clues", []):
    st.markdown(f"<div class='card'>• {clue.get('text','')}</div>", unsafe_allow_html=True)

# 🧑 SUSPECTS
st.markdown("## 🧑 Suspects")
for s in case.get("suspects", []):
    st.markdown(f"<div class='card'><b>{s['name']}</b><br>" +
                "<br>".join("• "+d for d in s.get("description", [])) +
                "</div>", unsafe_allow_html=True)

# 🧠 USER GUESS
user_guess = st.selectbox(
    "Who do you think is the culprit?",
    [s["name"] for s in case.get("suspects", [])]
)

# ❓ QUESTIONS
user_answers = {}

for i, q in enumerate(questions):
    st.markdown(f"**{q['question']}**")
    user_answers[i] = st.radio("", list(q["options"].keys()), key=i)

# 🔍 ANALYSIS
if st.button("🚨 Run Analysis"):

    with st.spinner("Analyzing..."):
        time.sleep(2)

    results, trait_scores = calculate_results(case, user_answers, questions)

    if not results:
        st.error("Analysis failed")
        st.stop()

    top_suspect, prob = results[0]

    st.success(f"AI Prediction: {top_suspect} ({prob}%)")

    st.markdown("## 📊 Breakdown")
    for s, p in results:
        st.write(f"{s}: {p}%")

    st.markdown("## ⚖️ Comparison")
    st.write(f"Your Guess: {user_guess}")
    st.write(f"AI Guess: {top_suspect}")

    st.markdown("## 🕵️ Truth")
    true = case.get("true_suspect", "Unknown")
    st.write(f"Actual Culprit: {true}")

    if top_suspect == true:
        st.success("AI correct")
    else:
        st.error("AI influenced by reasoning")

    st.markdown("## 📌 Explanation")
    st.info(generate_explanation(trait_scores))

st.caption("⚠️ Educational simulation only")
