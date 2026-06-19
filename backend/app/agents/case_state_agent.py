import json
from app.utils.performance import timed_agent


# =====================================
# Crime Templates
# =====================================

CRIME_REQUIREMENTS = {

    "Theft": [

        "victim_name",
        "victim_phone",

        "incident_date",
        "incident_time",

        "property_type",
        "property_value",

        "location",

        "witnesses",
        "cctv_available"
    ],

    "Kidnapping": [

        "victim_name",
        "victim_age",
        "victim_gender",

        "incident_date",
        "incident_time",

        "location",

        "witnesses",
        "cctv_available"
    ],

    "Cyber Fraud": [

        "victim_name",
        "victim_phone",

        "bank_name",

        "transaction_id",

        "amount_lost",

        "transaction_date",

        "transaction_time"
    ]
}


# =====================================
# Build Case State
# =====================================

@timed_agent("case_state_agent.build")
def build_case_state(case_data):

    offences = case_data.get(
        "possible_offences",
        []
    )

    crime_type = ""

    if offences:

        crime_type = offences[0]

    required_fields = CRIME_REQUIREMENTS.get(
        crime_type,
        []
    )

    known_fields = []

    missing_fields = []

    for field in required_fields:

        value = case_data.get(field)

        if value:

            known_fields.append(
                field
            )

        else:

            missing_fields.append(
                field
            )

    return {

        "crime_type":
        crime_type,

        "known_fields":
        known_fields,

        "missing_fields":
        missing_fields
    }


# =====================================
# Next Missing Field
# =====================================

@timed_agent("case_state_agent.next_missing")
def get_next_missing_field(case_state):

    missing = case_state.get(
        "missing_fields",
        []
    )

    if len(missing) == 0:

        return None

    return missing[0]


# =====================================
# Testing
# =====================================

if __name__ == "__main__":

    sample = {

        "possible_offences": [
            "Kidnapping"
        ],

        "victim_name":
        "Paridhi",

        "victim_age":
        "12"
    }

    state = build_case_state(
        sample
    )

    print(
        json.dumps(
            state,
            indent=4
        )
    )

    print(
        "\nNext Missing Field:"
    )

    print(
        get_next_missing_field(
            state
        )
    )
