import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# 🎮 UI
st.markdown("""
<style>
.stApp {background:#04060c;color:#e6f1ff;font-family:monospace;}
.panel {background:#0b1220;padding:12px;border-radius:8px;margin:6px;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Investigation Console")

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
# CASE
# =========================
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

st.markdown("## 📁 Case")
st.write(case["description"])

# =========================
# EVIDENCE (DIFFICULTY)
# =========================
st.markdown("## 🔍 Evidence")

clues = case["clues"]

if difficulty == "Medium":
    clues = clues[:-1]

elif difficulty == "Hard":
    clues = clues[:-2]

for c in clues:
    st.markdown(f"<div class='panel'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS
# =========================
st.markdown("## 🧑 Suspects")

for s in case["suspects"]:
    st.markdown(f"<div class='panel'>{s['name']}</div>", unsafe_allow_html=True)

# =========================
# QUESTIONS
# =========================
st.markdown("## 🧠 Your Reasoning")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

user_guess = st.selectbox("Select Suspect", [s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("🚨 RUN INVESTIGATION"):

    ai_scores = {}

    for s in case["suspects"]:
        score = 0

        for clue in clues:
            if clue["type"] == "constraint":
                if not all(r in s["traits"] for r in clue["rules"]):
                    score -= 100
                else:
                    score += 10

        ai_scores[s["name"]] = score

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # RESULTS
    # =========================
    st.markdown("## ⚖️ Results")

    st.write("🧠 You:", user_guess)
    st.write("🤖 System:", ai_top)
    st.write("🕵️ Actual:", true)

    # =========================
    # SCORE SYSTEM
    # =========================
    score = 0

    if user_guess == true:
        score += 50
    else:
        score -= 20

    # Difficulty multiplier
    if difficulty == "Medium":
        score *= 1.5
    elif difficulty == "Hard":
        score *= 2

    st.markdown(f"## 🎮 Score: {int(score)}")

    # =========================
    # SAVE TO LEADERBOARD
    # =========================
    name = st.text_input("Enter your name for leaderboard:")

    if st.button("Submit Score"):
        st.session_state.leaderboard.append((name, int(score)))

    # =========================
    # LEADERBOARD
    # =========================
    st.markdown("## 🏆 Leaderboard")

    sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)

    for i, (n, s) in enumerate(sorted_board[:5]):
        st.write(f"{i+1}. {n} — {s}")
