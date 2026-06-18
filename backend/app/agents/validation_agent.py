import re
from backend.app.utils.performance import timed_agent
from backend.app.agents.date_time_agent import (
    extract_date_and_time,
    extract_time
)


def clean_text(value):

    if value is None:
        return ""

    return str(value).strip()


def validate_phone(phone):

    phone = clean_text(phone)

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        return digits

    return ""


def validate_amount(amount):

    amount = clean_text(amount)

    digits = re.sub(r"[^\d]", "", amount)

    return digits


def validate_date(date_value):
    """
    Validate and parse date using advanced date extraction.
    Returns properly formatted date or empty string.
    """
    
    date_value = clean_text(date_value)
    
    if not date_value:
        return ""
    
    # Use the date_time_agent to extract proper date
    result = extract_date_and_time(date_value)
    
    return result.get("date", "")


def validate_time(time_value):
    """
    Validate and parse time using advanced time extraction.
    Returns properly formatted time (HH:MM AM/PM) or empty string.
    """
    
    time_value = clean_text(time_value)
    
    if not time_value:
        return ""
    
    # Use the date_time_agent to extract proper time
    extracted_time = extract_time(time_value)
    
    if extracted_time:
        return extracted_time
    
    # If no time found, return empty (was checking length before, but extraction is better)
    return ""


def validate_location(location):

    location = clean_text(location)

    if len(location) < 3:
        return ""

    return location


@timed_agent("validation_agent.function")
def validate_case_data(case_data):

    case_data["victim_phone"] = validate_phone(
        case_data.get("victim_phone", "")
    )

    case_data["accused_phone"] = validate_phone(
        case_data.get("accused_phone", "")
    )

    case_data["property_value"] = validate_amount(
        case_data.get("property_value", "")
    )

    case_data["amount_lost"] = validate_amount(
        case_data.get("amount_lost", "")
    )

    case_data["incident_date"] = validate_date(
        case_data.get("incident_date", "")
    )

    case_data["incident_time"] = validate_time(
        case_data.get("incident_time", "")
    )

    case_data["location"] = validate_location(
        case_data.get("location", "")
    )

    return case_data


if __name__ == "__main__":

    sample = {

        "victim_phone": "Phone: 8610595920",

        "incident_date":
        "stalked on 12 jan and abused on 14 jan",

        "incident_time":
        "at 9:30 PM",

        "property_value":
        "₹15,000"

    }

    result = validate_case_data(
        sample
    )

    print(result)
