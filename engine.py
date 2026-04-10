def calculate_results(case, user_answers, questions):
    
    # Step 1: Trait scoring
    trait_scores = {}

    for q_index, selected_option in user_answers.items():
        option_weights = questions[q_index]["options"][selected_option]

        for trait, weight in option_weights.items():
            trait_scores[trait] = trait_scores.get(trait, 0) + weight

    # Step 2: Suspect scoring
    suspect_scores = {}

    for suspect in case["suspects"]:
        name = suspect["name"]
        suspect_scores[name] = 0

        for trait in suspect["traits"]:
            if trait in trait_scores:
                suspect_scores[name] += trait_scores[trait]

    # Step 3: Convert to probability
    total_score = sum(suspect_scores.values())

    probabilities = {}
    if total_score == 0:
        for suspect in suspect_scores:
            probabilities[suspect] = 0
    else:
        for suspect, score in suspect_scores.items():
            probabilities[suspect] = round((score / total_score) * 100, 2)

    # Step 4: Sort
    sorted_results = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    return sorted_results, trait_scores


def generate_explanation(trait_scores):
    top_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    explanation = "The AI prioritized: " + ", ".join([t for t, _ in top_traits])
    return explanation
