from app.utils.performance import timed_agent


def get_missing_fields(case_data, required_fields):

    missing = []

    for field in required_fields:

        value = case_data.get(field)

        if value is None:
            missing.append(field)

        elif str(value).strip() == "":
            missing.append(field)

    return missing


@timed_agent("field_manager.function")
def get_next_missing_field(
    case_data,
    required_fields
):

    missing = get_missing_fields(
        case_data,
        required_fields
    )

    if len(missing) == 0:

        return None

    return missing[0]
