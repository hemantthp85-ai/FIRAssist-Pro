from fastapi import APIRouter
import uuid
import json

from app.agents.extraction_agent import (
    extract_complaint_details
)

from app.orchestrator.case_orchestrator import (
    run_case_orchestration_async
)

from app.agents.fir_writer_agent import (
    generate_fir_narrative
)

from app.agents.fir_generator import (
    generate_fir as build_fir
)

from app.agents.legal_agent import (
    recommend_sections
)

from app.utils.performance import (
    cached_call,
    timed_agent
)

from app.db.database import SessionLocal
from app.db.services import CaseService
from app.db.repositories import ComplaintRepository


router = APIRouter()


@timed_agent("extraction_agent")
def run_extraction_agent(complaint):
    return cached_call(
        "extraction_agent",
        complaint,
        extract_complaint_details,
        complaint
    )


@timed_agent("validation_agent")
def run_validation_agent(case_data):
    from app.agents.validation_agent import (
        validate_case_data
    )

    return validate_case_data(
        case_data
    )


@router.post("/generate-fir")
async def generate_fir_dashboard(data: dict):

    complaint = data.get(
        "complaint",
        ""
    )

    extracted = run_extraction_agent(
        complaint
    )

    try:
        extracted_json = json.loads(
            extracted
        )
        extracted_json = run_validation_agent(
            extracted_json
        )
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "raw_response": extracted
        }

    # Generate unique complaint ID and inject it
    complaint_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
    extracted_json["id"] = complaint_id

    dashboard = await run_case_orchestration_async(
        extracted_json
    )

    # Save initial dossier to PostgreSQL
    db = SessionLocal()
    try:
        CaseService.save_full_case_dossier(db, complaint_id, extracted_json, dashboard)
    except Exception as db_err:
        print("Database save error:", db_err)
    finally:
        db.close()

    return {
        "status": "success",
        "complaint_id": complaint_id,
        "dashboard": dashboard
    }


@router.post("/generate-final-fir")
async def generate_final_fir(data: dict):

    case_data = data.get(
        "case_data",
        {}
    )

    fir = build_fir(
        case_data
    )

    # Generate narrative
    narrative = ""
    try:
        narrative = generate_fir_narrative(fir)
    except Exception as e:
        narrative = f"Error generating narrative: {str(e)}"

    try:
        if case_data.get(
            "legal_analysis"
        ):
            legal = case_data.get(
                "legal_analysis"
            )
        elif not case_data.get(
            "possible_offences"
        ):
            legal = {
                "recommended_sections": [],
                "legal_summary":
                "No offence information available."
            }
        else:
            legal = recommend_sections(
                case_data
            )

        if isinstance(legal, str):
            legal = json.loads(
                legal
            )
    except Exception:
        legal = {
            "recommended_sections": []
        }

    # Persist the final FIR narrative and change status to 'FIR Filed'
    complaint_id = case_data.get("id")
    if complaint_id:
        db = SessionLocal()
        try:
            # Update entire dossier details (case_data may have edits)
            dossier_data = {
                "fir": fir,
                "fir_narrative": narrative,
                "legal_analysis": legal,
                "timeline_analysis": case_data.get("timeline") or {},
                "evidence_analysis": case_data.get("evidence") or {},
                "risk_assessment": case_data.get("risk_assessment") or {},
                "investigation_report": case_data.get("investigation") or {},
                "action_recommendations": case_data.get("recommended_actions") or {}
            }
            CaseService.save_full_case_dossier(db, complaint_id, case_data, dossier_data)
            
            # Formally finalize status
            ComplaintRepository.update(db, complaint_id, {
                "status": "FIR Filed",
                "fir_number": fir.get("FIR_Number")
            })
        except Exception as db_err:
            print("Database save error in final FIR:", db_err)
        finally:
            db.close()

    return {
        "status": "success",
        "fir": fir,
        "narrative": narrative,
        "legal_analysis": legal
    }
