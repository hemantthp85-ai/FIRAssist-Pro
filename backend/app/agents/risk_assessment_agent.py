from app.models.qwen_loader import ask_qwen
from app.utils.performance import timed_agent
import json

@timed_agent("risk_assessment_agent.function")
def assess_case_risk(case_data):
    try:
        from app.agents.master_agent import run_master_analysis
        master = run_master_analysis(case_data)
        if isinstance(master, str):
            master = json.loads(master)
        if master and "risk_assessment" in master:
            return json.dumps(master["risk_assessment"])
    except Exception as e:
        print("Fallback in risk_assessment_agent:", e)

    prompt = f"""
You are a senior police risk assessment officer.

Analyze the FIR case.

Determine:

1. Threat Level
2. Victim Risk
3. Public Safety Risk
4. Repeat Offence Risk
5. Suspect Flight Risk
6. Evidence Loss Risk
7. Investigation Priority
8. Recommended Response Time
9. Recommended Immediate Actions

Threat Levels:

LOW
MEDIUM
HIGH
CRITICAL

Rules:

- Use only available facts.
- Do not invent information.
- If information is missing, state uncertainty.
- Be objective.

Case Data:

{json.dumps(case_data, indent=2)}

Return JSON only.

Format:

{{
    "threat_level":"",
    "victim_risk":"",
    "public_safety_risk":"",
    "repeat_offence_risk":"",
    "suspect_flight_risk":"",
    "evidence_loss_risk":"",
    "investigation_priority":"",
    "recommended_response_time":"",
    "immediate_actions":[]
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
        "incident_summary": "Mobile phone theft near Trichy Bus Stand",
        "incident_date": "5 June 2026",
        "incident_time": "6:30 PM",
        "location": "Trichy Bus Stand",
        "property_type": "Mobile Phone",
        "property_value": "15000",
        "possible_offences": ["Theft"]
    }
    result = assess_case_risk(sample_case)
    print(result)
