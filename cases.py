cases = [

# =========================
# 🕵️ CASE 1: SERVER BREACH
# =========================
{
    "case_name": "Secure Server Breach",
    "description": "Sensitive files were accessed from a secure internal server at 2:13 AM. System requires admin credentials. No external intrusion detected.",

    "true_suspect": "Rohan (IT Admin)",
    "bias": "Motive Bias",

    "clues": [
        {"text": "Access required admin privileges", "type": "constraint", "rules": ["admin_access"]},
        {"text": "Login from internal network", "type": "constraint", "rules": ["internal_access"]},
        {"text": "No credential sharing detected", "type": "constraint", "rules": ["direct_access"]},
        {"text": "Action performed late at night", "type": "behavior"}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["admin_access", "internal_access", "direct_access"]},
        {"name": "Priya (HR Manager)", "traits": ["internal_access"]},
        {"name": "Arjun (Ex-Employee)", "traits": []},
        {"name": "Neha (Intern)", "traits": []}
    ]
},

# =========================
# 💻 CASE 2: PHISHING
# =========================
{
    "case_name": "Phishing Attack",
    "description": "Employees received convincing fake emails. No malware involved. Attack relied on trust.",

    "true_suspect": "Priya (HR Manager)",
    "bias": "Technical Bias",

    "clues": [
        {"text": "Attack relied on human trust", "type": "constraint", "rules": ["social"]},
        {"text": "No technical exploit used", "type": "constraint", "rules": ["low_technical"]},
        {"text": "Emails appeared internal", "type": "constraint", "rules": ["internal_access"]}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical"]},
        {"name": "Priya (HR Manager)", "traits": ["social", "low_technical", "internal_access"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["technical"]},
        {"name": "Neha (Intern)", "traits": ["low_technical"]}
    ]
},

# =========================
# 🏦 CASE 3: FRAUD
# =========================
{
    "case_name": "Financial Fraud",
    "description": "Money was siphoned in small automated transactions over months.",

    "true_suspect": "Rohan (IT Admin)",
    "bias": "Emotional Bias",

    "clues": [
        {"text": "Transactions automated", "type": "constraint", "rules": ["technical"]},
        {"text": "Pattern consistent over time", "type": "constraint", "rules": ["logical"]},
        {"text": "Required system-level access", "type": "constraint", "rules": ["admin_access"]}
    ],

    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical", "logical", "admin_access"]},
        {"name": "Priya (HR Manager)", "traits": []},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge"]},
        {"name": "Neha (Intern)", "traits": []}
    ]
}

]
