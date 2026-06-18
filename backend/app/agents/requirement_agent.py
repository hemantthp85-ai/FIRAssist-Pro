from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
import json


@timed_agent("requirement_agent.function")
def get_required_information(
    complaint,
    extracted_data
):

    offences = extracted_data.get(
        "possible_offences",
        []
    )

    offence_text = " ".join(offences).lower()

    # ==================================
    # VEHICLE / PROPERTY THEFT
    # ==================================

    if "theft" in offence_text:

        return json.dumps({
            "required_information": [

                "complainant_name",
                "complainant_phone",
                "complainant_address",

                "victim_name",
                "victim_phone",

                "incident_date",
                "incident_time",

                "vehicle_number",
                "vehicle_model",
                "vehicle_color",

                "property_value",

                "witnesses",
                "cctv_available"
            ]
        })

    # ==================================
    # MISSING PERSON
    # ==================================

    elif (
        "missing" in offence_text
        or
        "kidnapping" in offence_text
    ):

        return json.dumps({
            "required_information": [

                "complainant_name",
                "complainant_phone",

                "missing_person_name",
                "missing_person_age",
                "missing_person_gender",
                "missing_person_phone",

                "last_seen_location",
                "last_seen_time",

                "relationship_to_complainant",

                "recent_photograph",

                "witnesses"
            ]
        })

    # ==================================
    # CYBER CRIME
    # ==================================

    elif (
        "cyber" in offence_text
        or
        "fraud" in offence_text
        or
        "online" in offence_text
    ):

        return json.dumps({
            "required_information": [

                "complainant_name",
                "complainant_phone",

                "bank_name",

                "account_number",

                "transaction_id",

                "transaction_amount",

                "transaction_date",

                "transaction_time"
            ]
        })

    # ==================================
    # FALLBACK
    # ==================================

    return json.dumps({
        "required_information": [

            "complainant_name",
            "complainant_phone",

            "incident_date",
            "incident_time",

            "location",

            "witnesses"
        ]
    })


if __name__ == "__main__":

    sample_data = {
        "possible_offences": [
            "Theft"
        ]
    }

    print(
        get_required_information(
            "",
            sample_data
        )
    )
