cases = [

{
    "case_name": "Insider Data Breach",
    "description": "Confidential product data was leaked internally.",
    "true_suspect": "Arjun (Ex-Employee)",
    "bias": "Motive Bias",

    "clues": [
        {"text": "Valid credentials used", "traits": {"admin_access": 3}},
        {"text": "After-hours access", "traits": {"long_hours": 2}},
        {"text": "No malware detected", "traits": {"system_knowledge": 2}},
        {"text": "Employee dissatisfaction reported", "traits": {"revenge": 3}}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["admin_access", "technical", "long_hours"]},
        {"name": "Priya (HR)", "traits": ["social"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge", "system_knowledge"]},
        {"name": "Neha (Intern)", "traits": ["curious"]}
    ]
},

{
    "case_name": "Phishing Attack",
    "description": "Employees received fake login emails.",
    "true_suspect": "Priya (HR)",
    "bias": "Technical Bias",

    "clues": [
        {"text": "Relied on trust", "traits": {"social": 3}},
        {"text": "No malware", "traits": {"low_technical": 2}}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical"]},
        {"name": "Priya (HR)", "traits": ["social"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge"]},
        {"name": "Neha (Intern)", "traits": ["curious"]}
    ]
}

]
