from app.models.qwen_loader import ask_qwen
from app.utils.performance import timed_agent
import json

@timed_agent("timeline_agent.function")
def generate_case_timeline(case_data):
    try:
        from app.agents.master_agent import run_master_analysis
        master = run_master_analysis(case_data)
        if isinstance(master, str):
            master = json.loads(master)
        if master and "timeline_analysis" in master:
            return json.dumps(master["timeline_analysis"])
    except Exception as e:
        print("Fallback in case_timeline_agent:", e)

    prompt = f"""
You are a senior police investigation officer.

Analyze the FIR case.

Build a chronological timeline of events.

Tasks:

1. Extract all known events.
2. Arrange events in chronological order.
3. Identify missing timeline gaps.
4. Identify suspicious gaps.
5. Suggest timeline verification steps.

Use only information available.

Do not invent facts.

Case Data:

{json.dumps(case_data, indent=2)}

Return JSON only.

Format:

{{
    "timeline":[
        {{
            "time":"",
            "event":""
        }}
    ],
    "missing_time_gaps":[],
    "suspicious_gaps":[],
    "verification_steps":[]
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
    result = generate_case_timeline(sample_case)
    print(result)
