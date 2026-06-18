from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
import json




@timed_agent("completeness_agent.function")
def check_completeness(case_data):

    mandatory = [
        "incident_summary",
        "possible_offences"
    ]

    count = 0

    for field in mandatory:

        if case_data.get(field):

            count += 1

    if count >= len(mandatory):

        return json.dumps({
            "status": "need_more_information"
        })

    return json.dumps({
        "status": "need_more_information"
    })
