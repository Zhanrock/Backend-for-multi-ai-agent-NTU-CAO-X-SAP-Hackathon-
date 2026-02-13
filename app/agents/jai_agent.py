# app/agents/jai_agent.py
import pandas as pd
import json
from app.utils.helpers import load_json, load_csv

# ---------------- CONFIG ----------------
PERFORMANCE_FILE = "data/mock/mock_performance.csv"
CAREER_PATH_FILE = "data/mock/career_path.json"
NUDGE_FILE = "data/mock/nudge_library.json"


# ---------------- FEATURES ----------------
def get_growth_path(employee_id):
    df = load_csv(PERFORMANCE_FILE)
    data = load_json(CAREER_PATH_FILE)

    row = df[df["employee_id"] == employee_id]

    if row.empty:
        return f"❌ Employee ID {employee_id} not found."
    row = row.iloc[0]
    current_role = row["role"]

    if current_role not in data:
        return f"❌ No career path info for {current_role}"

    next_role = data[current_role]["next_role"]
    skills = data[current_role]["skills_required"]

    return f"""
👤 {row['name']}
Current Role: {current_role}
Next Role: {next_role}
Skills Required: {", ".join(skills)}
"""


def get_weekly_nudge(employee_id):
    df = load_csv(PERFORMANCE_FILE)
    career_data = load_json(CAREER_PATH_FILE)
    nudge_data = load_json(NUDGE_FILE)

    row = df[df["employee_id"] == employee_id]

    if row.empty:
        return f"❌ Employee ID {employee_id} not found."

    row = row.iloc[0]
    current_role = row["role"]
    skills = str(row.get("skills_unlocked", "") or "").strip()
    unlocked = skills.split(";") if skills else []

    if current_role not in career_data:
        return f"❌ No career path info for {current_role}"

    next_role = career_data[current_role]["next_role"]
    required = career_data[current_role]["skills_required"]

    # find first missing skill
    growth_skill = None
    for s in required:
        if s not in unlocked:
            growth_skill = s
            break

    if not growth_skill:
        return f"✅ {row['name']} is fully ready for promotion to {next_role}!"

    tip = nudge_data.get(growth_skill, "Keep practicing this skill!")

    return f"""
🎯 Weekly Nudge for {row['name']}
Growth Opportunity: {growth_skill}
Next Role: {next_role}
Tip: {tip}
"""


def get_skill_tree(employee_id):
    df = load_csv(PERFORMANCE_FILE)
    row = df[df["employee_id"] == employee_id]

    if row.empty:
        return f"❌ Employee ID {employee_id} not found."
    row = row.iloc[0]
    skills = row["skills_unlocked"]
    if pd.isna(skills) or str(skills).strip().lower() in ["", "nan"]:
        return f"❌ No skills unlocked yet."
    else:
        return f"👤 Skill Acquired: {skills}"
