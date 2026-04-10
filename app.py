import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# 🎮 GAME UI
st.markdown("""
<style>
.stApp {background:#04060c;color:#e6f1ff;font-family:monospace;}
.panel {background:#0b1220;padding:12px;border-radius:8px;margin:8px;border:1px solid #1f2a44;}
.title {color:#00ffcc;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Investigation Console")
st.markdown("**Mission: Analyze the case and identify the suspect.**")

# =========================
# 🎯 DIFFICULTY
# =========================
difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

# =========================
# 🏆 LEADERBOARD INIT
# =========================
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# =========================
# ⏱️ TIMER
# =========================
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

elapsed = int(time.time() - st.session_state.start_time)
st.write(f"⏱️ Time: {elapsed}s")

# =========================
# 📁 CASE
# =========================
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

st.markdown("## 📁 Case File")
st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

# =========================
# 🔍 EVIDENCE
# =========================
st.markdown("## 🔍 Evidence Log")

clues = case["clues"]

if difficulty == "Medium":
    clues = clues[:-1]
elif difficulty == "Hard":
    clues = clues[:-2]

for c in clues:
    st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# 🧑 SUSPECTS (FIXED)
# =========================
st.markdown("## 🧑 Suspect Profiles")

st.warning("Carefully analyze each suspect. Motive alone is not enough—capability matters.")

for s in case["suspects"]:
    st.markdown(f"""
    <div class='panel'>
    <b>{s['name']}</b><br>
    {"<br>".join("• " + p for p in s["profile"])}
    </div>
    """, unsafe_allow_html=True)

# =========================
# 🧠 USER THINKING
# =========================
st.markdown("## 🧠 Your Analysis")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

# =========================
# 🎯 FINAL DECISION
# =========================
st.markdown("## 🎯 Final Decision")

user_guess = st.selectbox(
    "Select the suspect you believe is responsible:",
    [s["name"] for s in case["suspects"]]
)

# =========================
# 🚨 RUN ANALYSIS
# =========================
if st.button("🚨 Run Investigation"):

    st.markdown("## 🧠 System Analysis")

    ai_scores = {}

    for s in case["suspects"]:
        score = 0

        st.markdown(f"### Evaluating: {s['name']}")

        for clue in clues:
            time.sleep(0.4)

            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                    st.error(f"❌ Eliminated: {clue['text']}")
                else:
                    score += 10
                    st.success(f"✔ Valid: {clue['text']}")

        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # 📊 DASHBOARD
    # =========================
    st.markdown("## 📊 Evaluation Dashboard")

    max_score = max(ai_scores.values())

    for s, score in ai_scores.items():
        normalized = int(((score + 100) / (max_score + 100)) * 100)
        st.write(s)
        st.progress(max(0, normalized))

    # =========================
    # ⚖️ RESULTS
    # =========================
    st.markdown("## ⚖️ Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Conclusion")
        st.write(user_guess)

    with col2:
        st.subheader("🤖 System Conclusion")
        st.write(ai_top)

    # =========================
    # 🕵️ TRUTH
    # =========================
    st.markdown("## 🕵️ Case Resolution")
    st.write(true)

    # =========================
    # 🎮 SCORE
    # =========================
    score = 0

    if user_guess == true:
        score += 50
        st.success("✔ Correct deduction")
    else:
        score -= 20
        st.error("❌ Incorrect reasoning")

    # Difficulty multiplier
    if difficulty == "Medium":
        score = int(score * 1.5)
    elif difficulty == "Hard":
        score = int(score * 2)

    st.markdown(f"### 🎮 Score: {score}")

    # =========================
    # 🏆 LEADERBOARD
    # =========================
    name = st.text_input("Enter your name:")

    if st.button("Submit Score"):
        st.session_state.leaderboard.append((name, score))

    st.markdown("## 🏆 Leaderboard")

    sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)

    for i, (n, s) in enumerate(sorted_board[:5]):
        st.write(f"{i+1}. {n} — {s}")

    # =========================
    # 📊 INSIGHT
    # =========================
    st.markdown("## 📊 Insight")

    if user_guess != true:
        top_bias = max(bias_counter, key=bias_counter.get)
        st.warning(f"Detected Bias: {top_bias}")

    st.info("""
    The system eliminates suspects that violate constraints.
    Human reasoning often focuses on motive rather than feasibility.
    """)
