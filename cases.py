import random

cases = [

{
    "case_name": "Secure Server Breach",
    "complexity": "medium",
    "description": "Sensitive files were accessed at 2:13 AM. No external intrusion detected. System requires admin-level access.",

    "true_suspect": "Rohan (IT Admin)",

    "clues": [
        {"text": "Requires admin-level access", "type": "constraint", "rules": ["admin_access"]},
        {"text": "Internal network used", "type": "constraint", "rules": ["internal_access"]},
        {"text": "No credential sharing", "type": "constraint", "rules": ["direct_access"]}
    ],

    "extra_clues": [
        {"text": "Activity occurred late at night", "type": "behavior"},
        {"text": "System logs show repeated access", "type": "behavior"}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["admin_access", "internal_access", "direct_access", "works_late", "technical"]},
        {"name": "Priya (HR Manager)", "traits": ["internal_access", "social"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge"]},
        {"name": "Neha (Intern)", "traits": ["low_access"]}
    ]
},

{
    "case_name": "Phishing Attack",
    "complexity": "easy",
    "description": "Employees received convincing fake login emails exploiting trust. No malware used.",

    "true_suspect": "Priya (HR Manager)",

    "clues": [
        {"text": "Relies on human trust", "type": "constraint", "rules": ["social"]},
        {"text": "Low technical complexity", "type": "constraint", "rules": ["low_technical"]}
    ],

    "extra_clues": [
        {"text": "Emails appeared internal", "type": "constraint", "rules": ["internal_access"]}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical"]},
        {"name": "Priya (HR Manager)", "traits": ["social", "low_technical", "internal_access"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["technical", "revenge"]},
        {"name": "Neha (Intern)", "traits": ["low_technical"]}
    ]
}

]
