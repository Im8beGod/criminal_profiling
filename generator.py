import random

def generate_case():

    suspects = [
        {
            "name": "Rohan (IT Admin)",
            "traits": ["admin_access","internal_access","direct_access","technical"],
            "details": ["Has root access","Handles server maintenance","Works late"]
        },
        {
            "name": "Priya (HR)",
            "traits": ["social","internal_access","low_technical"],
            "details": ["Communicates with all employees","Trusted role"]
        },
        {
            "name": "Arjun (Ex-Employee)",
            "traits": ["revenge","technical"],
            "details": ["Recently fired","Knows system partially"]
        },
        {
            "name": "Neha (Intern)",
            "traits": ["low_access","low_technical"],
            "details": ["Limited permissions","New employee"]
        }
    ]

    scenario = random.choice([
        "Sensitive data accessed at unusual hours",
        "Multiple accounts compromised internally",
        "Financial data manipulation detected",
        "Unauthorized system changes logged"
    ])

    timeline = [
        "Login detected",
        "Privilege escalation",
        "Action executed",
        "Logs altered"
    ]

    technical_sets = [
        ["Admin access required","Internal network only"],
        ["No technical exploit","Human interaction involved"],
        ["Script-based automation","Requires technical skill"]
    ]

    technical = random.choice(technical_sets)

    observations = [
        "One suspect had motive",
        "Only internal actors possible",
        "Permissions were required"
    ]

    # decide culprit logically
    if "Admin access required" in technical:
        true = suspects[0]
        clues = [
            {"text":"Admin access needed","type":"constraint","rules":["admin_access"]},
            {"text":"Internal access","type":"constraint","rules":["internal_access"]}
        ]
    elif "Human interaction involved" in technical:
        true = suspects[1]
        clues = [
            {"text":"Social interaction","type":"constraint","rules":["social"]},
            {"text":"Low technical","type":"constraint","rules":["low_technical"]}
        ]
    else:
        true = suspects[0]
        clues = [
            {"text":"Technical skill required","type":"constraint","rules":["technical"]}
        ]

    return {
        "case_name": "Dynamic Generated Case",
        "description": scenario,
        "timeline": timeline,
        "technical": technical,
        "observations": observations,
        "true_suspect": true["name"],
        "clues": clues,
        "suspects": suspects
    }
