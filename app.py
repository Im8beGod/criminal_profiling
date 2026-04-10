import streamlit as st
import time

from cases import cases
from questions import questions
from engine import calculate_results, generate_explanation

st.set_page_config(page_title="AI Suspect Profiler", layout="centered")

# 🔥 Dark Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f17;
        color: #e6edf3;
    }
    .suspect-card {
        padding: 15px;
        border-radius: 12px;
        background: #161b22;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 🎬 Title
st.title("🕵️ AI Suspect Profiler")
st.markdown("**Can you identify the criminal better than AI?**")

case = cases[0]

# 📁 Case
st.subheader(f"📁 Case: {case['case_name']}")
st.write(case["description"])

st.divider()

# 🧑 Suspects
st.subheader("🧑 Suspects")

for suspect in case["suspects"]:
    st.markdown(f"""
    <div class="suspect-card">
        <b>{suspect['name']}</b><br>
        {"<br>".join("• " + d for d in suspect["description"])}
    </div>
    """, unsafe_allow_html=True)

# 🧠 User Guess
user_guess = st.selectbox(
    "🧠 Who do YOU think is the culprit?",
    [s["name"] for s in case["suspects"]]
)

st.divider()

# ❓ Questions
st.subheader("🧪 AI Interrogation")

user_answers = {}

for i, q in enumerate(questions):
    st.markdown(f"**{q['question']}**")
    answer = st.radio("", list(q["options"].keys()), key=i)
    user_answers[i] = answer

# 🔍 Analyze
if st.button("🔍 Analyze"):

    with st.spinner("Analyzing behavioral patterns..."):
        time.sleep(2)

    results, trait_scores = calculate_results(case, user_answers, questions)

    top_suspect, top_prob = results[0]

    # 🎯 Result
    st.subheader("🧠 AI Prediction")
    st.success(f"{top_suspect} is the most likely suspect ({top_prob}%)")

    # 📊 Breakdown
    st.subheader("📊 Probability Breakdown")
    for suspect, prob in results:
        st.progress(int(prob))
        st.write(f"{suspect}: {prob}%")

    # ⚖️ Comparison
    st.subheader("⚖️ Human vs AI")
    st.write(f"🧑 Your Guess: **{user_guess}**")
    st.write(f"🤖 AI Prediction: **{top_suspect}**")

    # 🧠 Explanation
    st.subheader("📌 Why did AI choose this?")
    explanation = generate_explanation(trait_scores)
    st.info(explanation)

    # ⚠️ Bias
    if user_guess != top_suspect:
        st.warning("Your decision may have been influenced by bias.")
    else:
        st.success("Your reasoning aligns with AI analysis.")

# ⚠️ Disclaimer
st.caption("⚠️ This is a fictional simulation for educational purposes only.")
