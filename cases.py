cases = [

{
    "case_name": "Insider Data Breach",
    "description": "Confidential product data was leaked internally just before launch.",

    "true_suspect": "Arjun (Ex-Employee)",
    "bias": "Motive Bias",

    "clues": [
        {"text": "Data accessed using valid credentials", "traits": {"admin_access": 3}},
        {"text": "Access occurred after office hours", "traits": {"long_hours": 2}},
        {"text": "No malware or hacking traces found", "traits": {"system_knowledge": 2}},
        {"text": "Recent employee dissatisfaction reported", "traits": {"revenge": 3}}
    ],

    "suspects": [
        {
            "name": "Rohan (IT Admin)",
            "description": [
                "Has full system access",
                "Works late frequently",
                "Highly technical"
            ],
            "traits": ["admin_access", "technical", "long_hours"]
        },
        {
            "name": "Priya (HR Manager)",
            "description": [
                "Highly social",
                "Trusted employee",
                "Non-technical"
            ],
            "traits": ["social"]
        },
        {
            "name": "Arjun (Ex-Employee)",
            "description": [
                "Recently left company",
                "Unhappy about promotion",
                "Knows internal systems"
            ],
            "traits": ["revenge", "system_knowledge"]
        },
        {
            "name": "Neha (Intern)",
            "description": [
                "Curious learner",
                "Limited access"
            ],
            "traits": ["curious"]
        }
    ]
},

{
    "case_name": "Corporate Phishing Attack",
    "description": "Employees received fake login emails that stole credentials.",

    "true_suspect": "Priya (HR Manager)",
    "bias": "Technical Bias",

    "clues": [
        {"text": "Attack relied on trust and communication", "traits": {"social": 3}},
        {"text": "No malware or technical exploit used", "traits": {"low_technical": 2}},
        {"text": "Emails appeared highly convincing", "traits": {"social": 2}}
    ],

    "suspects": [
        {
            "name": "Rohan (IT Admin)",
            "description": ["Highly technical", "Low social interaction"],
            "traits": ["technical"]
        },
        {
            "name": "Priya (HR Manager)",
            "description": ["Highly social", "Communicates with all employees"],
            "traits": ["social"]
        },
        {
            "name": "Arjun (Ex-Employee)",
            "description": ["Knows systems", "Emotionally dissatisfied"],
            "traits": ["revenge"]
        },
        {
            "name": "Neha (Intern)",
            "description": ["Learning phase", "Limited influence"],
            "traits": ["curious"]
        }
    ]
}

]
