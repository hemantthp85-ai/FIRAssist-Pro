from app.agents.extraction_agent import (
    extract_complaint_details
)

from app.agents.investigation_planner import (
    build_investigation_plan
)

from app.agents.investigation_agent import (
    generate_question
)

from app.agents.field_manager import (
    get_missing_fields
)

from app.agents.answer_validator import (
    validate_answer
)

from app.agents.legal_agent import (
    recommend_sections
)

from app.sessions.session_agent import (
    FIRSession
)

from app.agents.fir_generator import (
    generate_fir
)

from app.agents.fir_writer_agent import (
    generate_fir_narrative
)

from app.agents.investigation_report_agent import (
    generate_investigation_report
)

from app.agents.evidence_agent import (
    analyze_evidence_requirements
)

from app.agents.case_timeline_agent import (
    generate_case_timeline
)

from app.agents.risk_assessment_agent import (
    assess_case_risk
)

from app.agents.action_recommendation_agent import (
    recommend_actions
)

import json


def main():

    complaint = input(
        "Enter Complaint: "
    )

    session = FIRSession()

    # =====================================
    # EXTRACTION
    # =====================================

    extracted = extract_complaint_details(
        complaint
    )

    try:

        extracted_json = json.loads(
            extracted
        )
        from app.agents.validation_agent import (
            validate_case_data
        )

        extracted_json = validate_case_data(
            extracted_json
        )

    except Exception as e:

        print("\nExtraction Error:")
        print(e)

        print("\nRaw Response:\n")
        print(extracted)

        return

    session.update(
        extracted_json
    )

    print(
        "\nExtracted Data:\n"
    )

    print(
        json.dumps(
            session.get_data(),
            indent=4
        )
    )

    # =====================================
    # BUILD INVESTIGATION PLAN ONCE
    # =====================================

    planner_response = build_investigation_plan(
        session.get_data()
    )

    try:

        planner = json.loads(
            planner_response
        )

    except Exception as e:

        print(
            "\nPlanner Parse Error:"
        )

        print(e)

        print(planner_response)

        return

    required_fields = planner.get(
        "required_fields",
        []
    )

    print(
        "\nINVESTIGATION PLAN:\n"
    )

    print(
        json.dumps(
            planner,
            indent=4
        )
    )

    print(
        "\nInvestigation Started\n"
    )

    # =====================================
    # INVESTIGATION LOOP
    # =====================================

    MAX_QUESTIONS = 20

    for _ in range(MAX_QUESTIONS):

        missing_fields = get_missing_fields(
            session.get_data(),
            required_fields
        )

        print(
            "\nMISSING FIELDS:\n"
        )

        print(
            json.dumps(
                missing_fields,
                indent=4
            )
        )

        if len(missing_fields) == 0:

            print(
                "\nInvestigation Complete."
            )

            break

        next_field = missing_fields[0]

        question_response = generate_question(
            next_field,
            session.get_data()
        )

        print(
            "\nDEBUG QUESTION:\n"
        )

        print(
            question_response
        )

        try:

            question_json = json.loads(
                question_response
            )

        except:

            print(
                "\nQuestion Parse Error"
            )

            break

        question = question_json.get(
            "question",
            f"Please provide {next_field}"
        )

        print(
            f"\nAI: {question}"
        )

        # ==========================
        # VALIDATION LOOP
        # ==========================

        while True:

            answer = input(
                "Citizen: "
            )

            is_valid, result = validate_answer(
                next_field,
                answer
            )

            if is_valid:

                session.update({

                    next_field:
                    result

                })

                break

            print(
                f"\nAI: {result}"
            )

    # =====================================
    # FINAL FIR DATA
    # =====================================

    final_data = session.get_data()

    print(
        "\nFINAL FIR DATA\n"
    )

    print(
        json.dumps(
            final_data,
            indent=4
        )
    )

    # =====================================
    # FIR GENERATION
    # =====================================

    fir_document = generate_fir(
        final_data
    )
    fir_narrative = generate_fir_narrative(
        fir_document
    )

    print(
        "\nFIR NARRATIVE\n"
    )

    print(
        fir_narrative
    )

    print(
        "\nGENERATED FIR\n"
    )

    print(
        json.dumps(
            fir_document,
            indent=4
        )
    )

    # =====================================
    # LEGAL ANALYSIS
    # =====================================

    print(
        "\nLEGAL ANALYSIS\n"
    )

    try:

        legal_output = recommend_sections(
            final_data
        )

        print(
            legal_output
        )

    except Exception as e:

        print(
            "\nLegal Agent Error:"
        )

        print(e)
    print(
        "\nINVESTIGATION REPORT\n"
    )

    try:

        report = generate_investigation_report(
            final_data
        )

        print(report)

    except Exception as e:

        print(
            "\nInvestigation Report Error:"
        )

        print(e)
    
    print(
        "\nEVIDENCE ANALYSIS\n"
    )

    try:

        evidence_report = (
            analyze_evidence_requirements(
                final_data
            )
        )

        print(
            evidence_report
        )

    except Exception as e:

        print(
            "\nEvidence Agent Error:"
        )

        print(e)

    print(
        "\nCASE TIMELINE ANALYSIS\n"
    )

    try:

        timeline_report = (
            generate_case_timeline(
                final_data
            )
        )

        print(
            timeline_report
        )

    except Exception as e:

        print(
            "\nTimeline Agent Error:"
        )

        print(e)

    print(
        "\nRISK ASSESSMENT\n"
    )

    try:

        risk_report = assess_case_risk(
            final_data
        )

        print(
            risk_report
        )

    except Exception as e:

        print(
            "\nRisk Assessment Error:"
        )

        print(e)
    print(
        "\nACTION RECOMMENDATIONS\n"
    )

    try:

        action_report = recommend_actions(
            final_data
        )

        print(
            action_report
        )

    except Exception as e:

        print(
            "\nAction Recommendation Error:"
        )

        print(e)
if __name__ == "__main__":

    main()