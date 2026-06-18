from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
import json


@timed_agent("question_agent.function")
def generate_questions(complaint, extracted_data):

    required_fields = extracted_data.get("missing_fields", [])

    questions = []

    for field in required_fields:

        prompt = f"""
You are a Tamil Nadu Police FIR Investigation Officer.

Complaint:
{complaint}

Generate ONE natural question for this field:

{field}

Return ONLY the question text.
"""

        question = ask_qwen(prompt).strip()

        questions.append({
            "field": field,
            "question": question
        })

    return json.dumps(
        {
            "questions": questions
        },
        indent=4
    )


if __name__ == "__main__":

    complaint = "My bike was stolen near Coimbatore Bus Stand."

    extracted_data = {
        "missing_fields": [
            "victim_name",
            "victim_phone",
            "victim_address",
            "accused_name",
            "incident_date",
            "incident_time",
            "witnesses",
            "cctv_available"
        ]
    }

    print(
        generate_questions(
            complaint,
            extracted_data
        )
    )
