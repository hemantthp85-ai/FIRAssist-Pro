from app.models.qwen_loader import ask_qwen
from app.utils.performance import timed_agent

import json


FIELD_QUESTIONS = {
    "victim_name": "What is your full name?",
    "victim_phone": "What is your phone number?",
    "victim_father_name": "What is your father's name?",
    "victim_age": "What is your age?",
    "victim_gender": "What is your gender?",
    "victim_address": "Please provide your complete address.",
    "incident_date": "On what date did the incident occur?",
    "incident_time": "At what time did the incident occur?",
    "location": "Where did the incident take place?",
    "property_type": "What type of property was stolen?",
    "property_value": "What is the approximate value of the stolen property or vehicle?",
    "vehicle_number": "What is the vehicle registration number?",
    "vehicle_model": "What is the vehicle model?",
    "vehicle_color": "What is the color of the vehicle?",
    "bank_name": "Which bank account was involved?",
    "transaction_id": "What is the transaction ID?",
    "amount_lost": "What amount was lost?"
}


@timed_agent("investigation_agent.function")
def generate_question(field_name, case_data):

    if field_name in FIELD_QUESTIONS:

        return json.dumps({
            "field": field_name,
            "question": FIELD_QUESTIONS[field_name]
        })

    prompt = f"""
You are an experienced police investigation officer.

Current Case Data:

{json.dumps(case_data, indent=2)}

You need information for:

Field:
{field_name}

Rules:

1. Ask ONLY ONE question.
2. Ask naturally like a police officer.
3. Question must be relevant to the complaint.
4. Do NOT ask multiple questions.
5. Do NOT explain.
6. Return JSON only.

Format:

{{
    "field":"{field_name}",
    "question":"Your question here"
}}

Return JSON only.
"""

    return ask_qwen(prompt)


if __name__ == "__main__":

    sample_case = {

        "incident_summary":
        "Child kidnapped near school",

        "accused_name":
        "Ravi",

        "location":
        "School",

        "possible_offences":
        [
            "Kidnapping"
        ]
    }

    print(
        generate_question(
            "victim_name",
            sample_case
        )
    )
