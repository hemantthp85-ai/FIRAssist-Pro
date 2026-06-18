import json
from backend.app.utils.performance import timed_agent


@timed_agent("fir_generator.function")
def generate_fir(case_data):

    fir_number = case_data.get("fir_number") or case_data.get("firNumber")
    if not fir_number or fir_number in ["AUTO-GENERATED", "new", "Draft"]:
        case_id = case_data.get("id") or "new"
        suffix = case_id.split("-")[-1] if "-" in case_id else case_id
        fir_number = f"FIR/2026/{suffix}"

    fir = {
        "FIR_Number": fir_number,
        "Police_Station": case_data.get("police_station") or case_data.get("station_name") or "Not Available",
        "Station_Code": case_data.get("station_code") or "Not Available",
        "District": case_data.get("district") or (case_data.get("location", "").split(",")[-1].strip() if "," in case_data.get("location", "") else "Not Available"),
        "Officer": {
            "Name": case_data.get("officer_name") or case_data.get("assigned_officer") or "Not Available",
            "Rank": case_data.get("officer_rank") or "Not Available",
            "Badge_No": case_data.get("officer_badge") or "Not Available"
        },

        "Complainant": {

            "Name":
            case_data.get(
                "victim_name",
                ""
            ),

            "Father_Name":
            case_data.get(
                "victim_father_name",
                ""
            ),

            "Age":
            case_data.get(
                "victim_age",
                ""
            ),

            "Gender":
            case_data.get(
                "victim_gender",
                ""
            ),

            "Phone":
            case_data.get(
                "victim_phone",
                ""
            ),

            "Address":
            case_data.get(
                "victim_address",
                ""
            )
        },

        "Accused": {

            "Name":
            case_data.get(
                "accused_name",
                ""
            ),

            "Phone":
            case_data.get(
                "accused_phone",
                ""
            ),

            "Address":
            case_data.get(
                "accused_address",
                ""
            )
        },

        "Incident": {

            "Summary":
            case_data.get(
                "incident_summary",
                ""
            ),

            "Date":
            case_data.get(
                "incident_date",
                ""
            ),

            "Time":
            case_data.get(
                "incident_time",
                ""
            ),

            "Location":
            case_data.get(
                "location",
                ""
            )
        },

        "Property": {

            "Type":
            case_data.get(
                "property_type",
                ""
            ),

            "Registration_Number":
            case_data.get(
                "vehicle_number",
                ""
            ),

            "Vehicle_Model":
            case_data.get(
                "vehicle_model",
                ""
            ),

            "Vehicle_Color":
            case_data.get(
                "vehicle_color",
                ""
            ),

            "Value":
            case_data.get(
                "property_value",
                ""
            )
        },

        "Cyber": {

            "Bank_Name":
            case_data.get(
                "bank_name",
                ""
            ),

            "Transaction_ID":
            case_data.get(
                "transaction_id",
                ""
            ),

            "Amount_Lost":
            case_data.get(
                "amount_lost",
                ""
            )
        },

        "Evidence": {

            "Witnesses":
            case_data.get(
                "witnesses",
                ""
            ),

            "CCTV":
            case_data.get(
                "cctv_available",
                ""
            )
        },

        "Possible_Offences":
        case_data.get(
            "possible_offences",
            []
        ),

        "Legal_Analysis":
        case_data.get(
            "legal_analysis",
            {}
        )
    }

    return fir


if __name__ == "__main__":

    sample = {

        "victim_name":
        "Hemantth",

        "victim_phone":
        "8610595920",

        "incident_summary":
        "Mobile phone theft",

        "incident_date":
        "5 June 2026",

        "incident_time":
        "6:30 PM",

        "location":
        "Trichy Bus Stand",

        "property_type":
        "Mobile Phone",

        "property_value":
        "15000",

        "possible_offences":
        [
            "Theft"
        ]
    }

    result = generate_fir(
        sample
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
