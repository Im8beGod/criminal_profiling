import streamlit as st
import time

from cases import cases
from questions import questions

st.set_page_config(page_title="Forensic Profiling System", layout="wide")

# 🎨 CLEAN FORENSIC UI
st.markdown("""
<style>
.stApp {
    background-color: #05070d;
    color: #e6edf3;
    font-family: monospace;
}
.section {
    border-bottom: 1px solid #1f2a44;
    margin-top: 20px;
    margin-bottom: 10px;
}
.card {
    background: #0d1117;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("Forensic Profiling System")

st.caption("Internal Investigation Interface")

# =========================
# CASE SELECTION
# =========================
case = st.selectbox("Select Case File", cases, format_func=lambda x: x["case_name"])

# =========================
# CASE FILE
# =========================
st.markdown("## CASE FILE")
st.write(case["description"])

# =========================
# EVIDENCE
# =========================
st.markdown("## EVIDENCE LOG")

for c in case["clues"]:
    st.markdown(f"<div class='card'>• {c['text']}</div>", unsafe_allow_html=True)

# =========================
# SUSPECTS
# =========================
st.markdown("## SUSPECT DATABASE")

for s in case["suspects"]:
    st.markdown(f"<div class='card'>{s['name']}</div>", unsafe_allow_html=True)

# =========================
# USER ANALYSIS
# =========================
st.markdown("## INVESTIGATOR INPUT")

bias_counter = {}

for i, q in enumerate(questions):
    ans = st.radio(q["question"], list(q["options"].keys()), key=i)
    bias = q["options"][ans]
    bias_counter[bias] = bias_counter.get(bias, 0) + 1

user_guess = st.selectbox("Select Primary Suspect", [s["name"] for s in case["suspects"]])

# =========================
# RUN ANALYSIS
# =========================
if st.button("Execute Analysis"):

    st.markdown("## ANALYSIS LOG")

    with st.spinner("Running forensic checks..."):
        time.sleep(1)

    ai_scores = {}
    explanations = {}

    for s in case["suspects"]:
        score = 0
        reasons = []

        st.markdown(f"### Evaluating: {s['name']}")

        for clue in case["clues"]:
            time.sleep(0.4)

            if clue["type"] == "constraint":
                required = clue["rules"]

                if not all(r in s["traits"] for r in required):
                    score -= 100
                    st.write(f"[REJECTED] {clue['text']}")
                    reasons.append(f"Rejected due to: {clue['text']}")
                else:
                    score += 10
                    st.write(f"[VALID] {clue['text']}")
                    reasons.append(f"Valid condition: {clue['text']}")

        ai_scores[s["name"]] = score
        explanations[s["name"]] = reasons

    ai_top = max(ai_scores, key=ai_scores.get)
    true = case["true_suspect"]

    # =========================
    # SUMMARY
    # =========================
    st.markdown("## ANALYSIS SUMMARY")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### INVESTIGATOR CONCLUSION")
        st.write(user_guess)

    with col2:
        st.markdown("### SYSTEM CONCLUSION")
        st.write(ai_top)

    # =========================
    # FINAL RESULT
    # =========================
    st.markdown("## CASE RESOLUTION")
    st.write(f"Confirmed Individual: {true}")

    # =========================
    # EVALUATION
    # =========================
    st.markdown("## EVALUATION")

    if user_guess != true:
        st.write("Investigator conclusion inconsistent with evidence.")
        top_bias = max(bias_counter, key=bias_counter.get)
        st.write(f"Observed reasoning bias: {top_bias}")
    else:
        st.write("Investigator conclusion aligned with evidence.")

    if ai_top == true:
        st.write("System analysis consistent with all constraints.")

    # =========================
    # FINAL NOTE
    # =========================
    st.markdown("## OBSERVATION")

    st.write("""
    The system evaluates constraints and eliminates invalid candidates.
    Human reasoning often prioritizes subjective factors over feasibility.
    """)
