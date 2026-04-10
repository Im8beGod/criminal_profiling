cases = [
    {
        "case_name": "The Insider Leak",
        "description": "A confidential product design was leaked to a competitor just days before launch. No signs of external hacking were found.",

        "true_suspect": "Arjun (Ex-Employee)",

        "clues": [
            {"text": "No malware detected in system logs", "traits": {"admin_access": 2, "system_knowledge": 2}},
            {"text": "Data accessed using valid credentials", "traits": {"admin_access": 3}},
            {"text": "Leak occurred after office hours", "traits": {"long_hours": 2, "logical": 1}},
            {"text": "Recent employee dissatisfaction reported", "traits": {"revenge": 3, "emotional": 2}}
        ],

        "suspects": [
            {
                "name": "Rohan (IT Administrator)",
                "description": [
                    "Has full system access",
                    "Works late nights",
                    "Highly logical",
                    "Introverted"
                ],
                "traits": ["admin_access", "technical", "logical", "long_hours"]
            },
            {
                "name": "Priya (HR Manager)",
                "description": [
                    "Highly social",
                    "Trusted role",
                    "Low technical knowledge"
                ],
                "traits": ["social", "people_skills", "trusted_role"]
            },
            {
                "name": "Arjun (Ex-Employee)",
                "description": [
                    "Recently left company",
                    "Strong system knowledge",
                    "Emotionally dissatisfied"
                ],
                "traits": ["revenge", "system_knowledge", "emotional"]
            },
            {
                "name": "Neha (Intern)",
                "description": [
                    "Curious learner",
                    "Explores systems",
                    "Limited access"
                ],
                "traits": ["curious", "explorer", "low_access"]
            }
        ]
    }
]
