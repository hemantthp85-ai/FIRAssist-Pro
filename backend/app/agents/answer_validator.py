import re
from app.utils.performance import timed_agent


@timed_agent("answer_validator.function")
def validate_answer(field_name, answer):

    answer = str(answer).strip()

    # =========================
    # PHONE NUMBER
    # =========================

    if field_name in [
        "victim_phone",
        "accused_phone",
        "complainant_phone"
    ]:

        if re.fullmatch(
            r"[6-9]\d{9}",
            answer
        ):

            return True, answer

        return (
            False,
            "Please enter a valid 10-digit mobile number."
        )

    # =========================
    # AGE
    # =========================

    if field_name in [
        "victim_age",
        "accused_age"
    ]:

        if answer.isdigit():

            age = int(answer)

            if 0 < age < 120:

                return True, answer

        return (
            False,
            "Please enter a valid age."
        )

    # =========================
    # PROPERTY VALUE
    # =========================

    if field_name in [
        "property_value",
        "amount_lost"
    ]:

        clean = answer.replace(",", "")

        if clean.isdigit():

            return True, clean

        return (
            False,
            "Please enter a valid amount."
        )

    # =========================
    # DATE
    # =========================

    if field_name in [
        "incident_date",
        "transaction_date"
    ]:

        if len(answer) >= 4:

            return True, answer

        return (
            False,
            "Please enter a valid date."
        )

    # =========================
    # TIME
    # =========================

    if field_name in [
        "incident_time",
        "transaction_time"
    ]:

        if len(answer) >= 3:

            return True, answer

        return (
            False,
            "Please enter a valid time."
        )

    # =========================
    # LOCATION
    # =========================

    if field_name in [
        "location",
        "incident_location"
    ]:

        if len(answer) >= 3:

            if not any(
                char.isdigit()
                for char in answer
            ):

                return True, answer

        return (
            False,
            "Please enter a valid location."
        )

    # =========================
    # DEFAULT
    # =========================

    if len(answer) == 0:

        return (
            False,
            "Answer cannot be empty."
        )

    return (
        True,
        answer
    )


if __name__ == "__main__":

    tests = [

        (
            "victim_phone",
            "8610595920"
        ),

        (
            "victim_phone",
            "hello"
        ),

        (
            "property_value",
            "15000"
        ),

        (
            "incident_location",
            "5pm"
        )
    ]

    for field, value in tests:

        result = validate_answer(
            field,
            value
        )

        print(
            field,
            value,
            result
        )
