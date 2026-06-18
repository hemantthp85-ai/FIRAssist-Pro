from fastapi import APIRouter
import json

from backend.app.agents.investigation_agent import (
    generate_question
)

from backend.app.agents.field_manager import (
    get_next_missing_field
)

from backend.app.utils.performance import (
    cached_call,
    timed_agent
)

router = APIRouter()


BASE_REQUIRED_FIELDS = [
    "victim_name",
    "victim_phone",
    "victim_father_name",
    "victim_age",
    "victim_gender",
    "victim_address",
    "incident_date",
    "incident_time",
    "location"
]

VEHICLE_THEFT_FIELDS = [
    "vehicle_number",
    "vehicle_model",
    "vehicle_color",
    "property_value"
]

CYBER_FRAUD_FIELDS = [
    "bank_name",
    "transaction_id",
    "amount_lost"
]

PROPERTY_THEFT_FIELDS = [
    "property_type",
    "property_value"
]


def get_case_offence_text(case_data: dict) -> str:

    possible_offences = case_data.get(
        "possible_offences",
        []
    )

    if isinstance(possible_offences, list):

        offence_text = " ".join(
            str(offence) for offence in possible_offences
        )

    else:

        offence_text = str(possible_offences)

    return " ".join([
        offence_text,
        str(case_data.get("crime_type", "")),
        str(case_data.get("property_type", "")),
        str(case_data.get("incident_summary", ""))
    ]).lower()


def get_required_fields(case_data: dict):

    required_fields = list(
        BASE_REQUIRED_FIELDS
    )

    offence_text = get_case_offence_text(
        case_data
    )

    is_vehicle_theft = (
        "vehicle" in offence_text
        or "bike" in offence_text
        or "motorcycle" in offence_text
        or "car" in offence_text
        or bool(str(case_data.get("vehicle_number", "")).strip())
        or bool(str(case_data.get("vehicle_model", "")).strip())
    )

    is_cyber_fraud = (
        "cyber" in offence_text
        or "fraud" in offence_text
        or "upi" in offence_text
        or "bank" in offence_text
        or "transaction" in offence_text
    )

    is_property_theft = (
        "theft" in offence_text
        or "stolen" in offence_text
        or "property" in offence_text
        or bool(str(case_data.get("property_type", "")).strip())
    )

    if is_vehicle_theft:

        required_fields.extend(
            VEHICLE_THEFT_FIELDS
        )

    elif is_cyber_fraud:

        required_fields.extend(
            CYBER_FRAUD_FIELDS
        )

    elif is_property_theft:

        required_fields.extend(
            PROPERTY_THEFT_FIELDS
        )

    return required_fields


@timed_agent("investigation_agent")
def run_investigation_agent(field, case_data):
    return cached_call(
        "investigation_agent",
        {
            "field": field,
            "case_data": case_data
        },
        generate_question,
        field,
        case_data
    )


@timed_agent("field_manager")
def run_field_manager(case_data, required_fields):
    return get_next_missing_field(
        case_data,
        required_fields
    )


@router.post("/next-question")
async def next_question(data: dict):

    field = data.get(
        "field",
        ""
    )

    case_data = data.get(
        "case_data",
        {}
    )

    response = run_investigation_agent(
        field,
        case_data
    )

    try:

        return json.loads(
            response
        )

    except:

        return {
            "field": field,
            "question": response
        }
def validate_field_input(field: str, answer: str) -> tuple[bool, str]:
    import re
    from dateutil.parser import parse as parse_date
    answer_stripped = answer.strip()
    
    # 1. FULL NAME validation
    if field in ["victim_name", "victim_father_name", "accused_name"]:
        # alphabets and spaces, minimum length 2
        if not re.match(r"^[a-zA-Z\s]{2,}$", answer_stripped):
            return False, "Please enter a valid name (alphabets and spaces only, minimum 2 characters)."
            
    # 2. PHONE NUMBER validation
    elif field in ["victim_phone", "accused_phone"]:
        # digits only, exactly 10 digits
        if not re.match(r"^\d{10}$", answer_stripped):
            return False, "Please enter a valid 10-digit mobile number."
            
    # 3. AGE validation
    elif field in ["victim_age", "accused_age"]:
        # integer, range 1-120
        try:
            age = int(answer_stripped)
            if age < 1 or age > 120:
                raise ValueError()
        except ValueError:
            return False, "Please enter a valid age between 1 and 120."
            
    # 4. GENDER validation
    elif field in ["victim_gender", "accused_gender"]:
        # Male, Female, Other
        if answer_stripped.lower() not in ["male", "female", "other"]:
            return False, "Please enter a valid gender (Male, Female, or Other)."
            
    # 5. DATE validation
    elif field in ["incident_date"]:
        # Must parse successfully. Reject tomorrow yesterday, abcd
        if any(w in answer_stripped.lower() for w in ["yesterday", "tomorrow", "today"]) and len(answer_stripped.split()) > 1:
            return False, "Please enter a valid date (e.g., 14 January 2026 or 14/01/2026)."
        try:
            if not any(char.isdigit() for char in answer_stripped) and len(answer_stripped) < 8:
                return False, "Please enter a valid date."
            parsed = parse_date(answer_stripped, fuzzy=False)
        except Exception:
            return False, "Please enter a valid date."
            
    # 6. TIME validation
    elif field in ["incident_time"]:
        # Reject 99:99, random text.
        # Accept 9:30 PM, 21:30.
        t_str = answer_stripped.upper()
        match_12h = re.match(r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s*(AM|PM)$", t_str)
        match_24h = re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", t_str)
        if not (match_12h or match_24h):
            return False, "Please enter a valid time (e.g., 9:30 PM or 21:30)."
            
    # 7. ADDRESS validation
    elif field in ["victim_address", "location"]:
        # Meaningful address text. Minimum length requirement. Reject 123, x, ???
        letters = re.sub(r"[^a-zA-Z]", "", answer_stripped)
        if len(answer_stripped) < 5 or len(letters) < 3:
            return False, "Please enter a valid, meaningful address."
            
    # 8. VEHICLE NUMBER validation
    elif field in ["vehicle_number"]:
        # Validate Indian registration format. Reject 123456, ABCD
        normalized = re.sub(r"[\s-]", "", answer_stripped).upper()
        if not re.match(r"^[A-Z]{2}[0-9]{1,2}[A-Z]{0,3}[0-9]{4}$", normalized):
            return False, "Please enter a valid vehicle registration number (e.g. TN38AB1234)."
            
    # 9. PROPERTY VALUE / AMOUNT LOST validation
    elif field in ["property_value", "amount_lost"]:
        # positive values, reject negative/text values
        try:
            val = float(answer_stripped)
            if val < 0:
                raise ValueError()
        except ValueError:
            return False, "Please enter a valid positive numeric value."
            
    return True, ""

@router.post("/submit-answer")
async def submit_answer(data: dict):

    case_data = data.get(
        "case_data",
        {}
    )

    field = data.get(
        "field",
        ""
    )

    answer = data.get(
        "answer",
        ""
    )

    is_valid, error_msg = validate_field_input(field, answer)
    if not is_valid:
        return {
            "status": "error",
            "message": error_msg,
            "case_data": case_data
        }

    case_data[field] = answer

    return {
        "status": "success",
        "case_data": case_data
    }
@router.post("/next-field")
async def next_field(data: dict):

    case_data = data.get(
        "case_data",
        {}
    )

    required_fields = get_required_fields(
        case_data
    )

    next_field = run_field_manager(
        case_data,
        required_fields
    )

    if next_field is None:

        return {
            "status": "complete"
        }

    return {
        "status": "next",
        "field": next_field
    }
