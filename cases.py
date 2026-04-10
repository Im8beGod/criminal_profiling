cases = [

{
    "case_name": "Secure Server Breach",
    "complexity": "medium",
    "description": "Sensitive files were accessed from a secure server at 2:13 AM. No external intrusion detected.",

    "true_suspect": "Rohan (IT Admin)",

    "clues": [
        {"text": "Requires admin access", "type": "constraint", "rules": ["admin_access"]},
        {"text": "Internal network used", "type": "constraint", "rules": ["internal_access"]},
        {"text": "No credential sharing", "type": "constraint", "rules": ["direct_access"]}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["admin_access", "internal_access", "direct_access", "works_late"]},
        {"name": "Priya (HR Manager)", "traits": ["internal_access", "social"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge"]},
        {"name": "Neha (Intern)", "traits": ["low_access"]}
    ]
},

{
    "case_name": "Phishing Attack",
    "complexity": "easy",
    "description": "Employees received fake login emails exploiting trust. No malware involved.",

    "true_suspect": "Priya (HR Manager)",

    "clues": [
        {"text": "Relies on trust", "type": "constraint", "rules": ["social"]},
        {"text": "Low technical requirement", "type": "constraint", "rules": ["low_technical"]}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical"]},
        {"name": "Priya (HR Manager)", "traits": ["social", "low_technical"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["technical", "revenge"]},
        {"name": "Neha (Intern)", "traits": ["low_technical"]}
    ]
}

]
