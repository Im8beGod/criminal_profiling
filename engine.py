def calculate_user_model(case, user_answers, questions):
    trait_scores = {}

    for q_index, selected_option in user_answers.items():
        weights = questions[q_index]["options"][selected_option]

        for trait, weight in weights.items():
            trait_scores[trait] = trait_scores.get(trait, 0) + weight

    suspect_scores = {}

    for suspect in case["suspects"]:
        name = suspect["name"]
        suspect_scores[name] = 0

        for trait in suspect["traits"]:
            if trait in trait_scores:
                suspect_scores[name] += trait_scores[trait]

    total = sum(suspect_scores.values())
    probs = {}

    for s, score in suspect_scores.items():
        probs[s] = round((score / total) * 100, 2) if total > 0 else 0

    return sorted(probs.items(), key=lambda x: x[1], reverse=True)


def calculate_ai_model(case):
    trait_scores = {}

    for clue in case.get("clues", []):
        for trait, weight in clue["traits"].items():
            trait_scores[trait] = trait_scores.get(trait, 0) + weight

    suspect_scores = {}

    for suspect in case["suspects"]:
        name = suspect["name"]
        suspect_scores[name] = 0

        for trait in suspect["traits"]:
            if trait in trait_scores:
                suspect_scores[name] += trait_scores[trait]

    total = sum(suspect_scores.values())
    probs = {}

    for s, score in suspect_scores.items():
        probs[s] = round((score / total) * 100, 2) if total > 0 else 0

    return sorted(probs.items(), key=lambda x: x[1], reverse=True)
