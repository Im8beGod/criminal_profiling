import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="AI Profiling", layout="wide")

# 🎨 UI
st.markdown("""
<style>
.stApp {background:#05070d;color:white;font-family:monospace;}
.card {background:#0d1117;padding:12px;border-radius:10px;margin:8px;}
.section {color:#4ea1ff;margin-top:20px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Human vs AI Criminal Profiling")

st.info("Compare your reasoning with an evidence-based AI system.")

case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

# 📁 CASE
st.markdown("## 📁 Case")
st.write(case["description"])

# 🔍 EVIDENCE
st.markdown("## 🔍 Evidence")
for c in case["clues"]:
    st.markdown(f"<div class='card'>• {c['text']}</div>", unsafe_allow_html=True)

# 🧑 SUSPECTS
st.markdown("## 🧑 Suspects")
for s in case["suspects"]:
    st.markdown(f"<div class='card'>{s['name']}</div>", unsafe_allow_html=True)

# 🧠 QUESTIONS
st.markdown("## 🧠 Your Reasoning")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

# 🧠 FINAL GUESS
user_guess = st.selectbox("Your final suspect:", [s["name"] for s in case["suspects"]])

# 🚨 RUN
if st.button("Run Investigation"):

    with st.spinner("Analyzing..."):
        time.sleep(2)

    # 🔴 HUMAN RESULT = USER GUESS
    human_top = user_guess

    # 🔵 AI MODEL (CONSTRAINT LOGIC)
    ai_scores = {}
    explanations = {}

    for s in case["suspects"]:
        score = 0
        reasons = []

        for clue in case["clues"]:

            if clue["type"] == "constraint":
                required = clue["rules"]

                if not all(r in s["traits"] for r in required):
                    score -= 100
                    reasons.append(f"❌ Failed: {clue['text']}")
                else:
                    score += 10
                    reasons.append(f"✅ Satisfies: {clue['text']}")

        ai_scores[s["name"]] = score
        explanations[s["name"]] = reasons

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # ⚖️ RESULTS
    st.markdown("## ⚖️ Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 You")
        st.write(human_top)

    with col2:
        st.subheader("🤖 AI")
        st.write(ai_top)

    # 🕵️ TRUTH
    st.markdown("## 🕵️ Actual Culprit")
    st.write(true)

    # 📊 INSIGHT
    st.markdown("## 📊 Insight")

    if human_top != true:
        st.error("Your reasoning was incorrect.")
        top_bias = max(bias_counter, key=bias_counter.get)
        st.warning(f"Bias Detected: {top_bias}")
    else:
        st.success("You got it right!")

    if ai_top == true:
        st.success("AI correctly solved using evidence.")

    # 🧠 EXPLANATION ENGINE
    st.markdown("## 🧠 AI Reasoning")

    for reason in explanations[ai_top]:
        st.write(reason)

    st.info("""
    AI eliminates suspects that violate constraints.
    Humans often focus on motive and ignore feasibility.
    """)
