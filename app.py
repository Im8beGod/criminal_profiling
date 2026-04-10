import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="Investigation Console", layout="wide")

# 🎮 UI
st.markdown("""
<style>
.stApp {background:#04060c;color:#e6f1ff;font-family:monospace;}
.panel {background:#0b1220;padding:12px;border-radius:8px;margin:8px;border:1px solid #1f2a44;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Investigation Console")

# =========================
# 🧠 AUTO PROFILE GENERATOR
# =========================
def generate_profile(traits):
    mapping = {
        "admin_access": "Has administrative system access",
        "internal_access": "Can access internal network",
        "direct_access": "Can directly access system",
        "technical": "Has strong technical skills",
        "low_technical": "Limited technical ability",
        "social": "Highly social and trusted",
        "revenge": "Has possible motive (conflict history)",
        "low_access": "Limited permissions",
        "works_late": "Often active during late hours"
    }

    return [mapping.get(t, t) for t in traits]

# =========================
# 🎯 DIFFICULTY
# =========================
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# =========================
# 🏆 LEADERBOARD
# =========================
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# =========================
# CASE
# =========================
case = st.selectbox("Select Case", cases, format_func=lambda x: x["case_name"])

st.markdown("## 📁 Case")
st.markdown(f"<div class='panel'>{case['description']}</div>", unsafe_allow_html=True)

# =========================
# EVIDENCE
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
# SUSPECTS (AUTO PROFILE)
# =========================
st.markdown("## 🧑 Suspects")

st.warning("Study each suspect carefully. Capability matters more than motive.")

for s in case["suspects"]:
    profile = generate_profile(s["traits"])

    st.markdown(f"""
    <div class='panel'>
    <b>{s['name']}</b><br>
    {"<br>".join("• " + p for p in profile)}
    </div>
    """, unsafe_allow_html=True)

# =========================
# QUESTIONS
# =========================
st.markdown("## 🧠 Your Reasoning")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

# =========================
# FINAL GUESS
# =========================
user_guess = st.selectbox("Your suspect:", [s["name"] for s in case["suspects"]])

# =========================
# RUN
# =========================
if st.button("🚨 Run Investigation"):

    ai_scores = {}

    st.markdown("## 🧠 System Analysis")

    for s in case["suspects"]:
        score = 0
        st.markdown(f"### Evaluating {s['name']}")

        for clue in clues:
            time.sleep(0.3)

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

    # RESULTS
    st.markdown("## ⚖️ Results")
    st.write("🧠 You:", user_guess)
    st.write("🤖 System:", ai_top)
    st.write("🕵️ Actual:", true)

    # SCORE
    score = 50 if user_guess == true else -20

    if difficulty == "Medium":
        score *= 1.5
    elif difficulty == "Hard":
        score *= 2

    st.markdown(f"## 🎮 Score: {int(score)}")

    # LEADERBOARD
    name = st.text_input("Enter name:")

    if st.button("Submit Score"):
        st.session_state.leaderboard.append((name, int(score)))

    st.markdown("## 🏆 Leaderboard")

    board = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)

    for i, (n, s) in enumerate(board[:5]):
        st.write(f"{i+1}. {n} — {s}")

    # INSIGHT
    st.markdown("## 📊 Insight")

    if user_guess != true:
        bias = max(bias_counter, key=bias_counter.get)
        st.warning(f"Bias Detected: {bias}")

    st.info("System eliminates impossible suspects. Humans focus on intuition.")
