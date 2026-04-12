cases = [

# =========================
# CASE 1
# =========================
{
    "case_name": "Mukti Server Breach",
    "description": "Unauthorized access at 02:13 AM. No external intrusion detected.",
    "timeline": [
        "01:58 AM – Internal login",
        "02:05 AM – Privilege escalation",
        "02:13 AM – Data extraction",
        "02:17 AM – Session terminated"
    ],
    "technical": [
        "Admin privileges required",
        "Internal network only",
        "Command-line tools used"
    ],
    "observations": [
        "Admin scheduled for maintenance",
        "Ex-employee had motive",
        "Intern had limited access"
    ],
    "true_suspect": "Rohan (IT Admin)",
    "clues": [
        {"text": "Admin access needed", "type": "constraint", "rules": ["admin_access"]},
        {"text": "Internal access", "type": "constraint", "rules": ["internal_access"]}
    ],
    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["admin_access","internal_access","direct_access","technical"]},
        {"name": "Priya (HR)", "traits": ["internal_access","social"]},
        {"name": "Arjun (Ex-Employee)", "traits": ["revenge"]},
        {"name": "Neha (Intern)", "traits": ["low_access"]}
    ]
},

# =========================
# CASE 2
# =========================
{
    "case_name": "Phishing Campaign",
    "description": "Employees received fake login emails.",
    "timeline": [
        "Emails sent at 9:00 AM",
        "Multiple employees entered credentials",
        "Accounts compromised"
    ],
    "technical": [
        "No malware used",
        "Social engineering attack",
        "Internal email formatting"
    ],
    "observations": [
        "HR communicates frequently",
        "IT admin rarely sends emails",
    ],
    "true_suspect": "Priya (HR)",
    "clues": [
        {"text": "Relies on trust", "type": "constraint", "rules": ["social"]},
        {"text": "Low technical complexity", "type": "constraint", "rules": ["low_technical"]}
    ],
    "suspects": [
        {"name": "Rohan (IT Admin)", "traits": ["technical"]},
        {"name": "Priya (HR)", "traits": ["social","low_technical","internal_access"]},
        {"name": "Arjun", "traits": ["technical","revenge"]},
        {"name": "Neha", "traits": ["low_technical"]}
    ]
},

# =========================
# CASE 3
# =========================
{
    "case_name": "Financial Fraud Automation",
    "description": "Automated transactions siphoning funds.",
    "timeline": [
        "Transactions started months ago",
        "Consistent pattern detected",
        "Automation confirmed"
    ],
    "technical": [
        "Script-based execution",
        "Requires technical skill",
        "Requires system access"
    ],
    "observations": [
        "Pattern too precise",
        "Non-technical users unlikely"
    ],
    "true_suspect": "Rohan (IT Admin)",
    "clues": [
        {"text": "Requires automation", "type": "constraint", "rules": ["technical"]},
        {"text": "Requires admin access", "type": "constraint", "rules": ["admin_access"]}
    ],
    "suspects": [
        {"name": "Rohan", "traits": ["technical","admin_access"]},
        {"name": "Priya", "traits": ["social"]},
        {"name": "Arjun", "traits": ["revenge"]},
        {"name": "Neha", "traits": ["low_access"]}
    ]
},

# =========================
# CASE 4
# =========================
{
    "case_name": "Internal Data Leak",
    "description": "Sensitive files leaked externally.",
    "timeline": [
        "Leak detected",
        "No external login",
        "Internal transfer suspected"
    ],
    "technical": [
        "Direct file access needed",
        "Internal system only"
    ],
    "observations": [
        "Ex-employee blamed initially",
        "Access required privileges"
    ],
    "true_suspect": "Rohan (IT Admin)",
    "clues": [
        {"text": "Internal access", "type": "constraint", "rules": ["internal_access"]},
        {"text": "Direct access", "type": "constraint", "rules": ["direct_access"]}
    ],
    "suspects": [
        {"name": "Rohan", "traits": ["internal_access","direct_access"]},
        {"name": "Priya", "traits": ["internal_access"]},
        {"name": "Arjun", "traits": ["revenge"]},
        {"name": "Neha", "traits": ["low_access"]}
    ]
},

# =========================
# CASE 5
# =========================
{
    "case_name": "Verbal Information Leak",
    "description": "Sensitive info leaked without system breach.",
    "timeline": [
        "Meeting held",
        "Info leaked externally",
        "No digital trace"
    ],
    "technical": [
        "No system breach",
        "Human interaction"
    ],
    "observations": [
        "Relies on communication",
        "Technical users unlikely"
    ],
    "true_suspect": "Priya (HR)",
    "clues": [
        {"text": "No technical breach", "type": "constraint", "rules": ["low_technical"]},
        {"text": "Social interaction", "type": "constraint", "rules": ["social"]}
    ],
    "suspects": [
        {"name": "Rohan", "traits": ["technical"]},
        {"name": "Priya", "traits": ["social","low_technical"]},
        {"name": "Arjun", "traits": ["revenge"]},
        {"name": "Neha", "traits": ["low_access"]}
    ]
}

]
