import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="AI Criminal Profiling", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>
.stApp {background:#05070d;color:white;font-family:monospace;}
.card {background:#0d1117;padding:12px;border-radius:10px;margin:6px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Human vs AI Criminal Profiling")

st.info("Analyze the case carefully. Then compare your reasoning with AI.")

# 📁 SELECT CASE
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

# =========================
# 📁 CASE
# =========================
st.header("📁 Case")
st.write(case["description"])

# =========================
# 🔍 EVIDENCE
# =========================
st.header("🔍 Evidence")

for c in case["clues"]:
    st.markdown(f"<div class='card'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# 🧑 SUSPECTS (FULL INFO)
# =========================
st.header("🧑 Suspects")

for s in case["suspects"]:
    st.markdown(f"""
    <div class='card'>
    <b>{s['name']}</b><br>
    {"<br>".join("• " + d for d in s.get("description", []))}
    </div>
    """, unsafe_allow_html=True)

# =========================
# 🧪 QUESTIONS (THINKING)
# =========================
st.header("🧪 Your Analysis")

user_answers = {}

for i, q in enumerate(questions):
    user_answers[i] = st.radio(q["question"], list(q["options"].keys()), key=i)

# =========================
# 🧠 FINAL DECISION
# =========================
st.header("🧠 Final Decision")

user_guess = st.selectbox(
    "Who do you think is the culprit?",
    [s["name"] for s in case["suspects"]]
)

# =========================
# 🚨 ANALYZE
# =========================
if st.button("🚨 Run Investigation"):

    with st.spinner("Analyzing..."):
        time.sleep(2)

    # 🧠 HUMAN MODEL
    human_scores = {}

    for i, ans in user_answers.items():
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

    # =========================
    # ⚖️ RESULTS
    # =========================
    st.header("⚖️ Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Conclusion")
        st.write(user_guess)

    with col2:
        st.subheader("🤖 AI Conclusion")
        st.write(ai_top)

    # =========================
    # 🕵️ TRUTH
    # =========================
    st.header("🕵️ Actual Culprit")
    st.write(true)

    # =========================
    # 📊 INSIGHT
    # =========================
    st.header("📊 Insight")

    if user_guess != true:
        st.error("Your reasoning was influenced by bias.")
        st.warning(f"Detected Bias: {case['bias']}")
    else:
        st.success("You correctly identified the suspect!")

    if ai_top == true:
        st.success("AI correctly solved the case using evidence.")

    st.info("Humans rely on intuition. AI relies on structured evidence.")
