import random

def generate_case():

    suspects = [
        {"name":"Rohan (IT Admin)","traits":["admin_access","internal_access","technical","direct_access"]},
        {"name":"Priya (HR)","traits":["social","internal_access","low_technical"]},
        {"name":"Arjun (Ex-Employee)","traits":["revenge","technical"]},
        {"name":"Neha (Intern)","traits":["low_access","low_technical"]}
    ]

    scenario = random.choice([
        "Sensitive data was accessed at night.",
        "Multiple accounts were compromised.",
        "Internal financial data was leaked.",
        "Unauthorized system changes detected."
    ])

    timeline = [
        "Login detected",
        "Access escalated",
        "Data accessed",
        "Session terminated"
    ]

    technical = random.choice([
        ["Admin access required","Internal network only"],
        ["No technical exploit","Human interaction involved"],
        ["Script-based automation","Requires technical skill"]
    ])

    observations = [
        "One suspect had motive",
        "Only internal users involved",
        "Some users lacked permissions"
    ]

    # pick true suspect based on constraints
    if "Admin access required" in technical:
        true = suspects[0]
    elif "Human interaction involved" in technical:
        true = suspects[1]
    else:
        true = suspects[0]

    clues = []

    if "Admin access required" in technical:
        clues.append({"text":"Admin access needed","type":"constraint","rules":["admin_access"]})

    if "Internal network only" in technical:
        clues.append({"text":"Internal access","type":"constraint","rules":["internal_access"]})

    if "Human interaction involved" in technical:
        clues.append({"text":"Social interaction","type":"constraint","rules":["social"]})

    return {
        "case_name": "Dynamic Case",
        "description": scenario,
        "timeline": timeline,
        "technical": technical,
        "observations": observations,
        "true_suspect": true["name"],
        "clues": clues,
        "suspects": suspects
    }
