def calculate_results(case, user_answers, questions):

    trait_scores = {}

    # ✅ Add clue weights (SAFE)
    for clue in case.get("clues", []):
        for trait, weight in clue.get("traits", {}).items():
            trait_scores[trait] = trait_scores.get(trait, 0) + weight

    # ✅ Add user answers
    for q_index, selected_option in user_answers.items():
        option_weights = questions[q_index]["options"][selected_option]

        for trait, weight in option_weights.items():
            trait_scores[trait] = trait_scores.get(trait, 0) + weight

    # ✅ Score suspects
    suspect_scores = {}

    for suspect in case.get("suspects", []):
        name = suspect["name"]
        suspect_scores[name] = 0

        for trait in suspect.get("traits", []):
            if trait in trait_scores:
                suspect_scores[name] += trait_scores[trait]

    # ✅ Convert to %
    total = sum(suspect_scores.values())

    probabilities = {}
    for s, score in suspect_scores.items():
        probabilities[s] = round((score / total) * 100, 2) if total > 0 else 0

    sorted_results = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    return sorted_results, trait_scores


def generate_explanation(trait_scores):
    top = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return "AI prioritized: " + ", ".join([t for t, _ in top])
