import json
from backend.app.utils.performance import timed_agent


@timed_agent("dashboard_generation.function")
def generate_dashboard(dossier):

    dashboard = {

        "case_overview": {

            "incident":
            dossier.get(
                "fir",
                {}
            ).get(
                "Incident",
                {}
            ),

            "complainant":
            dossier.get(
                "fir",
                {}
            ).get(
                "Complainant",
                {}
            ),

            "accused":
            dossier.get(
                "fir",
                {}
            ).get(
                "Accused",
                {}
            ),

            "property":
            dossier.get(
                "fir",
                {}
            ).get(
                "Property",
                {}
            ),

            "cyber":
            dossier.get(
                "fir",
                {}
            ).get(
                "Cyber",
                {}
            ),

            "possible_offences":
            dossier.get(
                "fir",
                {}
            ).get(
                "Possible_Offences",
                []
            )
        },

        "legal_analysis":
        dossier.get(
            "legal_analysis",
            {}
        ),

        "risk_assessment":
        dossier.get(
            "risk_assessment",
            {}
        ),

        "timeline":
        dossier.get(
            "timeline_analysis",
            {}
        ),

        "evidence":
        dossier.get(
            "evidence_analysis",
            {}
        ),

        "investigation":
        dossier.get(
            "investigation_report",
            {}
        ),

        "recommended_actions":
        dossier.get(
            "action_recommendations",
            {}
        )
    }

    return dashboard


if __name__ == "__main__":

    sample = {

        "fir": {

            "Incident": {

                "Summary":
                "Mobile Phone Theft",

                "Location":
                "Trichy Bus Stand"
            }
        },

        "legal_analysis": {

            "recommended_sections": [
                {
                    "section": "303"
                }
            ]
        },

        "risk_assessment": {

            "threat_level":
            "LOW"
        }
    }

    result = generate_dashboard(
        sample
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
