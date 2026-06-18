from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
import json

@timed_agent("action_recommendation_agent.function")
def recommend_actions(case_data):
    try:
        from backend.app.agents.master_agent import run_master_analysis
        master = run_master_analysis(case_data)
        if isinstance(master, str):
            master = json.loads(master)
        if master and "action_recommendations" in master:
            return json.dumps(master["action_recommendations"])
    except Exception as e:
        print("Fallback in action_recommendation_agent:", e)

    prompt = f"""
You are a senior police operations commander.

Analyze the FIR case.

Recommend:

1. Immediate Actions
2. Investigation Team Assignment
3. Specialized Units Required
4. Evidence Collection Actions
5. Victim Protection Measures
6. Suspect Tracking Actions
7. Escalation Requirements
8. Priority Tasks (next 24 hours)
9. Long-Term Investigation Tasks

Use only available information.

Do not invent facts.

Case Data:

{json.dumps(case_data, indent=2)}

Return JSON only.

Format:

{{
    "immediate_actions": [],
    "investigation_team": [],
    "special_units": [],
    "evidence_actions": [],
    "victim_protection": [],
    "suspect_tracking": [],
    "escalation_required": "",
    "next_24_hours": [],
    "long_term_actions": []
}}
"""
    response = ask_qwen(prompt)
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()
    return response

if __name__ == "__main__":
    sample_case = {
        "victim_name": "Hemantth",
        "incident_summary": "Mobile phone theft",
        "incident_date": "5 June 2026",
        "incident_time": "6:30 PM",
        "location": "Trichy Bus Stand",
        "property_type": "Mobile Phone",
        "property_value": "15000",
        "possible_offences": ["Theft"]
    }
    result = recommend_actions(sample_case)
    print(result)
