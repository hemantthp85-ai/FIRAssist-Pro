from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import cached_call, timed_agent
import json
import re

def clean_json_str(s):
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1:
        s = s[start:end+1]
    s = re.sub(r',\s*}', '}', s)
    s = re.sub(r',\s*\]', ']', s)
    return s

def _run_master_analysis_uncached(case_data):
    prompt = f"""
You are a senior police commander, risk assessment officer, and forensic expert.
Analyze the following FIR case data and return a JSON containing all analyses:

CASE DATA:
{json.dumps(case_data, indent=2)}

Return valid JSON ONLY in this format:
{{
    "timeline_analysis": {{
        "timeline": [
            {{"time": "...", "event": "..."}}
        ],
        "missing_time_gaps": [],
        "suspicious_gaps": [],
        "verification_steps": []
    }},
    "evidence_analysis": {{
        "available_evidence": [],
        "missing_evidence": [],
        "physical_evidence": [],
        "digital_evidence": [],
        "documentary_evidence": [],
        "witness_evidence": [],
        "high_priority_evidence": [],
        "collection_recommendations": []
    }},
    "risk_assessment": {{
        "threat_level": "...",
        "victim_risk": "...",
        "public_safety_risk": "...",
        "repeat_offence_risk": "...",
        "suspect_flight_risk": "...",
        "evidence_loss_risk": "...",
        "investigation_priority": "...",
        "recommended_response_time": "...",
        "immediate_actions": []
    }},
    "action_recommendations": {{
        "immediate_actions": [],
        "investigation_team": [],
        "special_units": [],
        "evidence_actions": [],
        "victim_protection": [],
        "suspect_tracking": [],
        "escalation_required": "...",
        "next_24_hours": [],
        "long_term_actions": []
    }},
    "investigation_report": {{
        "case_summary": "...",
        "evidence_required": [],
        "witness_actions": [],
        "cctv_actions": [],
        "digital_evidence": [],
        "suspect_identification": [],
        "immediate_actions": [],
        "risk_assessment": "...",
        "recommended_steps": []
    }}
}}
"""
    response = ask_qwen(prompt)
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()
    try:
        return json.loads(clean_json_str(response))
    except Exception as e:
        print("Master agent JSON parse failed:", e)
        # return empty structure with correct keys to avoid crashes
        return {
            "timeline_analysis": {"timeline": [], "missing_time_gaps": [], "suspicious_gaps": [], "verification_steps": []},
            "evidence_analysis": {"available_evidence": [], "missing_evidence": [], "physical_evidence": [], "digital_evidence": [], "documentary_evidence": [], "witness_evidence": [], "high_priority_evidence": [], "collection_recommendations": []},
            "risk_assessment": {"threat_level": "MEDIUM", "victim_risk": "LOW", "public_safety_risk": "LOW", "repeat_offence_risk": "LOW", "suspect_flight_risk": "LOW", "evidence_loss_risk": "LOW", "investigation_priority": "MEDIUM", "recommended_response_time": "24 HOURS", "immediate_actions": []},
            "action_recommendations": {"immediate_actions": [], "investigation_team": [], "special_units": [], "evidence_actions": [], "victim_protection": [], "suspect_tracking": [], "escalation_required": "NO", "next_24_hours": [], "long_term_actions": []},
            "investigation_report": {"case_summary": "Auto-analyzed case details.", "evidence_required": [], "witness_actions": [], "cctv_actions": [], "digital_evidence": [], "suspect_identification": [], "immediate_actions": [], "risk_assessment": "MEDIUM", "recommended_steps": []}
        }

@timed_agent("master_analysis")
def run_master_analysis(case_data):
    return cached_call(
        "master_analysis",
        case_data,
        _run_master_analysis_uncached,
        case_data
    )
