cases = [

{
    "case_name": "Insider Data Breach",
    "description": "Confidential product designs were leaked. No external intrusion detected.",
    "true_suspect": "Arjun (Ex-Employee)",
    "bias_type": "Motive Bias",

    "clues": [
        {"text": "No malware detected", "traits": {"system_knowledge": 2}},
        {"text": "Valid credentials used", "traits": {"admin_access": 3}},
        {"text": "After-hours access", "traits": {"long_hours": 2}},
        {"text": "Employee dissatisfaction reported", "traits": {"revenge": 3}}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "description": ["Full system access", "Works late", "Technical"], "traits": ["admin_access", "technical", "long_hours"]},
        {"name": "Priya (HR Manager)", "description": ["Social", "Trusted", "Non-technical"], "traits": ["social", "trusted_role"]},
        {"name": "Arjun (Ex-Employee)", "description": ["Left recently", "Unhappy", "Knows systems"], "traits": ["revenge", "system_knowledge"]},
        {"name": "Neha (Intern)", "description": ["Curious", "Limited access"], "traits": ["curious", "low_access"]}
    ]
},

{
    "case_name": "Corporate Phishing Attack",
    "description": "Fake login page used to steal employee credentials.",
    "true_suspect": "Priya (HR Manager)",
    "bias_type": "Technical Bias",

    "clues": [
        {"text": "Relied on trust", "traits": {"people_skills": 3}},
        {"text": "No malware used", "traits": {"low_technical": 2}},
        {"text": "Highly convincing emails", "traits": {"social": 2}}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "description": ["Highly technical"], "traits": ["technical"]},
        {"name": "Priya (HR Manager)", "description": ["Highly social", "Trusted"], "traits": ["people_skills", "social"]},
        {"name": "Arjun (Ex-Employee)", "description": ["Knows systems", "Angry"], "traits": ["system_knowledge", "revenge"]},
        {"name": "Neha (Intern)", "description": ["Limited access"], "traits": ["low_access"]}
    ]
},

{
    "case_name": "Internal Financial Fraud",
    "description": "Money siphoned slowly without alerts.",
    "true_suspect": "Rohan (IT Admin)",
    "bias_type": "Emotional Bias",

    "clues": [
        {"text": "Automated transactions", "traits": {"technical": 3}},
        {"text": "Consistent pattern", "traits": {"logical": 2}},
        {"text": "System-level access needed", "traits": {"admin_access": 3}}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "description": ["System access", "Logical"], "traits": ["admin_access", "technical", "logical"]},
        {"name": "Priya (HR Manager)", "description": ["Non-technical"], "traits": ["trusted_role"]},
        {"name": "Arjun (Ex-Employee)", "description": ["Emotional"], "traits": ["revenge"]},
        {"name": "Neha (Intern)", "description": ["Limited access"], "traits": ["low_access"]}
    ]
}

]
