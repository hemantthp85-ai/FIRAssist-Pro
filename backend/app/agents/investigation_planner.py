from app.models.qwen_loader import ask_qwen
from app.utils.performance import timed_agent
import json


@timed_agent("investigation_planner.function")
def build_investigation_plan(case_data):

    prompt = f"""
You are a senior police investigation officer.

Current FIR Information:

{json.dumps(case_data, indent=2)}

Your task:

Determine ALL important information required
to properly investigate this case.

Rules:

1. Return only field names.
2. Do not return values.
3. Include victim details.
4. Include accused details if applicable.
5. Include incident details.
6. Include evidence details.
7. Include property details if applicable.
8. Return JSON only.
9. If accused is unknown do not request accused details.
10. If theft case, ask property details.
11. If kidnapping case, ask victim details.
12. If cyber fraud, ask bank details.
13. Return only required fields.

Format:

{{
    "required_fields": [
        "victim_name",
        "victim_phone",
        "incident_date"
    ]
}}
"""

    return ask_qwen(prompt)
