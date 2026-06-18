from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
import json

@timed_agent("investigation_report_agent.function")
def generate_investigation_report(case_data):
    try:
        from backend.app.agents.master_agent import run_master_analysis
        master = run_master_analysis(case_data)
        if isinstance(master, str):
            master = json.loads(master)
        if master and "investigation_report" in master:
            return json.dumps(master["investigation_report"])
    except Exception as e:
        print("Fallback in investigation_report_agent:", e)

    prompt = f"""
You are a senior police investigation officer.

Analyze the FIR case.

Generate:

1. Case Summary
2. Key Evidence Required
3. Witness Investigation Plan
4. CCTV Investigation Plan
5. Digital Evidence Plan
6. Suspect Identification Plan
7. Immediate Police Actions
8. Risk Assessment
9. Recommended Investigation Steps

Use only information available in the FIR.

Do not invent facts.

Case Data:

{json.dumps(case_data, indent=2)}

Return JSON only.

Format:

{{
    "case_summary": "",
    "evidence_required": [],
    "witness_actions": [],
    "cctv_actions": [],
    "digital_evidence": [],
    "suspect_identification": [],
    "immediate_actions": [],
    "risk_assessment": "",
    "recommended_steps": []
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
    result = generate_investigation_report(sample_case)
    print(result)
