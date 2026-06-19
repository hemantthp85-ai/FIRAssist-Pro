from urllib import response

from app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
from backend.app.agents.date_time_agent import (
    extract_date_and_time,
    parse_incident_timeline
)
import re

def clean_json_str(s):
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1:
        s = s[start:end+1]
    s = re.sub(r',\s*}', '}', s)
    s = re.sub(r',\s*\]', ']', s)
    return s



@timed_agent("extraction_agent.function")
def extract_complaint_details(complaint: str):

    # First, extract dates and times using the specialized date_time_agent
    date_time_result = extract_date_and_time(complaint)
    
    incident_timeline = parse_incident_timeline(complaint)

    prompt = f"""
You are an Expert Police FIR Information Extraction Agent.

Your job is to extract structured FIR information from citizen complaints.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Never explain.
3. Never add markdown.
4. Never invent facts.
5. If information is missing return "".
6. Use the extracted dates and times provided below.
7. If multiple incidents exist:
   - Use the MOST RECENT incident date as incident_date.
   - Mention earlier incidents inside incident_summary.
8. Extract victim and accused separately.
9. Extract location separately.
10. Identify offence categories accurately.
11. Extract victim father's name if mentioned.
12. Extract victim age if mentioned.
13. Extract victim gender if mentioned.
13. incident_summary is MANDATORY.
14. Create a concise summary of the complaint in 1-2 sentences.
15. incident_summary can NEVER be empty if a complaint is provided.
DATE & TIME INFORMATION:

Most Recent Incident Date:
{date_time_result['date']}

Time:
{date_time_result['time']}

All Dates Found:
{', '.join(date_time_result['all_dates'])}

PRIMARY INCIDENT DATE:
{incident_timeline['primary_incident']['date']}

OFFENCE MAPPING:

Stealing -> Theft
Bike Theft -> Theft
Vehicle Theft -> Theft
Mobile Theft -> Theft
Stalking -> Stalking
Harassment -> Harassment
Sexual Harassment -> Sexual Harassment
Attempted Abuse -> Attempt to Commit Offence
Kidnap -> Kidnapping
Abduction -> Kidnapping
UPI Fraud -> Cyber Fraud
Online Scam -> Cyber Fraud

OUTPUT JSON FORMAT:

{{
    "incident_summary": "",

    "victim_name": "",
"victim_father_name": "",
"victim_age": "",
"victim_gender": "",
"victim_phone": "",
"victim_address": "",

    "accused_name": "",
    "accused_phone": "",
    "accused_address": "",

    "incident_date": "{date_time_result['date']}",
    "incident_time": "{date_time_result['time']}",

    "location": "",

    "property_type": "",
    "property_value": "",

    "vehicle_number": "",
    "vehicle_model": "",
    "vehicle_color": "",

    "bank_name": "",
    "transaction_id": "",
    "amount_lost": "",

    "witnesses": "",
    "cctv_available": "",

    "possible_offences": []
}}

EXAMPLE

Complaint:
"The accused stalked me on 12 January 2026 and attempted abuse on 14 January 2026 at 9:30 PM near Othakalmandapam."

Output:

{{
    "incident_summary":"Stalking on 12 January 2026 followed by attempted abuse on 14 January 2026 near Othakalmandapam",

    "victim_name":"",
"victim_father_name":"",
"victim_age":"",
"victim_gender":"",
"victim_phone":"",
"victim_address":"",

    "accused_name":"",
    "accused_phone":"",
    "accused_address":"",

    "incident_date":"14 January 2026",
    "incident_time":"9:30 PM",

    "location":"Othakalmandapam",

    "property_type":"",
    "property_value":"",

    "vehicle_number":"",
    "vehicle_model":"",
    "vehicle_color":"",

    "bank_name":"",
    "transaction_id":"",
    "amount_lost":"",

    "witnesses":"",
    "cctv_available":"",

    "possible_offences":[
        "Stalking",
        "Attempt to Commit Offence"
    ]
}}

FINAL RULES:

Return EXACTLY ONE JSON OBJECT.

DO NOT return:

{{}}

{{}}

DO NOT return multiple JSON objects.

DO NOT return explanations.

DO NOT return notes.

DO NOT return markdown.

DO NOT return code blocks.

The field "possible_offences" MUST be inside the same JSON object.

Return ONLY the JSON object.

Complaint:

{complaint}
"""

    response = ask_qwen(prompt)

    print("\n===== QWEN RESPONSE =====")
    print(response)
    print("========================\n")

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()
    # Fix Qwen returning two JSON objects

    if "}\n\n{" in response:

        parts = response.split("}\n\n{")

        first_json = parts[0] + "}"
        second_json = "{" + parts[1]

        try:

            import json
            first_json = clean_json_str(first_json)
            second_json = clean_json_str(second_json)
            print("FIRST JSON:")
            print(first_json)

            print("SECOND JSON:")
            print(second_json)

            data1 = json.loads(first_json)
            data2 = json.loads(second_json)

            data1["possible_offences"] = data2.get(
                "possible_offences",
                []
            )

            response = json.dumps(
                data1,
                indent=4
            )

        except Exception as e:

            print(
                "JSON Merge Error:",
                e
            )
    try:
        import json
        json.loads(response)
    except Exception as e:
        print("\n========= INVALID JSON =========")
        print(response)
        print("ERROR:", e)
        print("================================")
    

    return response


if __name__ == "__main__":

    complaint = """
    On 5 June 2026 at around 6:30 PM,
    my mobile phone worth ₹15,000 was stolen
    at Trichy Central Bus Stand.
    """

    result = extract_complaint_details(
        complaint
    )

    print(result)
