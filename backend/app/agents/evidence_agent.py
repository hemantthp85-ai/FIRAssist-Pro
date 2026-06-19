from app.models.qwen_loader import ask_qwen
from app.utils.performance import timed_agent
import json

@timed_agent("evidence_agent.function")
def analyze_evidence_requirements(case_data):
    try:
        from app.agents.master_agent import run_master_analysis
        master = run_master_analysis(case_data)
        if isinstance(master, str):
            master = json.loads(master)
        if master and "evidence_analysis" in master:
            return json.dumps(master["evidence_analysis"])
    except Exception as e:
        print("Fallback in evidence_agent:", e)

    prompt = f"""
You are a senior forensic investigation officer.

Analyze the FIR case.

Identify:

1. Available Evidence
2. Missing Evidence
3. Physical Evidence Required
4. Digital Evidence Required
5. Documentary Evidence Required
6. Witness Evidence Required
7. High Priority Evidence
8. Evidence Collection Recommendations

Use only information available.

Do not invent facts.

Case Data:

{json.dumps(case_data, indent=2)}

Return JSON only.

Format:

{{
    "available_evidence": [],
    "missing_evidence": [],
    "physical_evidence": [],
    "digital_evidence": [],
    "documentary_evidence": [],
    "witness_evidence": [],
    "high_priority_evidence": [],
    "collection_recommendations": []
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
    result = analyze_evidence_requirements(sample_case)
    print(result)
