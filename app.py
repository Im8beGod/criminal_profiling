import streamlit as st
import time

from cases import cases
from questions import questions
from engine import calculate_results, generate_explanation

st.set_page_config(page_title="AI Investigation Engine", layout="centered")

# 🔥 FBI STYLE CSS
st.markdown("""
<style>
    .stApp {
        background-color: #05070d;
        color: #e8f0ff;
        font-family: 'Courier New', monospace;
    }

    h1, h2, h3 {
        text-align: center;
        letter-spacing: 1px;
    }

    .card {
        background: #0d1117;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #1f2a44;
        margin-bottom: 10px;
    }

    .highlight {
        color: #00ffcc;
        font-weight: bold;
    }

    .section-title {
        color: #4ea1ff;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid #1f2a44;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 🎬 HEADER
st.markdown("<h1>🕵️ AI INVESTIGATION ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Behavioral Analysis • Evidence Processing • Suspect Profiling</p>", unsafe_allow_html=True)

case = cases[0]

# 📁 CASE FILE
st.markdown("<div class='section-title'>📁 CASE FILE</div>", unsafe_allow_html=True)
st.markdown(f"<div class='card'><span class='highlight'>{case['case_name']}</span><br>{case['description']}</div>", unsafe_allow_html=True)

# 🔍 EVIDENCE
st.markdown("<div class='section-title'>🔍 EVIDENCE LOG</div>", unsafe_allow_html=True)
for clue in case["clues"]:
    st.markdown(f"<div class='card'>• {clue['text']}</div>", unsafe_allow_html=True)

# 🧑 SUSPECTS
st.markdown("<div class='section-title'>🧑 SUSPECT DATABASE</div>", unsafe_allow_html=True)

for s in case["suspects"]:
    st.markdown(f"""
    <div class='card'>
        <span class='highlight'>{s['name']}</span><br>
        {"<br>".join("• " + d for d in s["description"])}
    </div>
    """, unsafe_allow_html=True)

# 🧠 USER GUESS
st.markdown("<div class='section-title'>🧠 INITIAL HYPOTHESIS</div>", unsafe_allow_html=True)

user_guess = st.selectbox(
    "Select your suspected individual:",
    [s["name"] for s in case["suspects"]]
)

# ❓ INTERROGATION
st.markdown("<div class='section-title'>🧪 INTERROGATION MODULE</div>", unsafe_allow_html=True)

user_answers = {}

for i, q in enumerate(questions):
    st.markdown(f"<div class='card'><b>{q['question']}</b></div>", unsafe_allow_html=True)
    user_answers[i] = st.radio("", list(q["options"].keys()), key=i)

# 🔍 ANALYZE BUTTON
if st.button("🚨 RUN ANALYSIS"):

    with st.spinner("Processing behavioral patterns..."):
        time.sleep(2)

    results, trait_scores = calculate_results(case, user_answers, questions)
    top_suspect, prob = results[0]

    # 🎯 RESULT
    st.markdown("<div class='section-title'>🧠 AI VERDICT</div>", unsafe_allow_html=True)
    st.success(f"{top_suspect} identified with {prob}% probability")

    # 📊 BREAKDOWN
    st.markdown("<div class='section-title'>📊 PROBABILITY MATRIX</div>", unsafe_allow_html=True)
    for s, p in results:
        st.progress(int(p))
        st.write(f"{s}: {p}%")

    # ⚖️ COMPARISON
    st.markdown("<div class='section-title'>⚖️ HUMAN vs AI</div>", unsafe_allow_html=True)
    st.write(f"Your Selection: {user_guess}")
    st.write(f"AI Selection: {top_suspect}")

    # 🕵️ TRUTH
    st.markdown("<div class='section-title'>🕵️ CASE RESOLUTION</div>", unsafe_allow_html=True)
    true = case["true_suspect"]

    st.write(f"Confirmed Culprit: **{true}**")

    if top_suspect == true:
        st.success("AI successfully identified the suspect.")
    else:
        st.error("AI analysis was influenced by reasoning bias.")

    # 🧠 EXPLANATION
    st.markdown("<div class='section-title'>📌 ANALYSIS INSIGHT</div>", unsafe_allow_html=True)
    st.info(generate_explanation(trait_scores))

    # ⚠️ BIAS
    if user_guess != true:
        st.warning("Your reasoning path shows potential bias influence.")
    else:
        st.success("Your reasoning aligns with evidence-based logic.")

# ⚠️ FOOTER
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("⚠️ Simulation only • Not a real investigative system")
