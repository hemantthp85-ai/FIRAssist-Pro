import json
import logging
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import (
    Complaint,
    FIR,
    LegalAnalysis,
    EvidenceAnalysis,
    CaseTimeline,
    RiskAssessment,
    InvestigationReport,
    ActionRecommendation
)
from app.db.repositories import ComplaintRepository, OfficerRepository, FIRRepository

logger = logging.getLogger("fir_copilot.db.services")


class CaseService:
    @staticmethod
    def save_full_case_dossier(db: Session, complaint_id: str, case_data: dict, dossier: dict) -> Complaint:
        try:
            # 1. Ensure officer exists
            officer = OfficerRepository.get_or_create_default(db)

            # 2. Extract Complaint attributes from case_data
            complaint_updates = {
                "id": complaint_id,
                "complainant_name": case_data.get("victim_name") or case_data.get("complainant_name") or "Unknown",
                "mobile_number": case_data.get("victim_phone") or case_data.get("complainant_phone") or "Unknown",
                "address": case_data.get("victim_address"),
                "incident_date": case_data.get("incident_date"),
                "incident_time": case_data.get("incident_time"),
                "location": case_data.get("location"),
                "suspect_details": case_data.get("accused_name") or case_data.get("suspect_details"),
                "witness_details": case_data.get("witnesses") or case_data.get("witness_details"),
                "crime_type": case_data.get("crime_type") or case_data.get("possible_offences", ["Other"])[0],
                "property_details": case_data.get("property_type") or case_data.get("property_details"),
                "status": "Pending Review",
                "officer_id": officer.id,
                "officer_name": officer.name,
                "transcript": case_data.get("incident_summary"),
                "completion_percentage": 85
            }

            # If complaint already exists, update it, otherwise create it
            complaint = ComplaintRepository.get_by_id(db, complaint_id)
            if not complaint:
                complaint = Complaint(**complaint_updates)
                db.add(complaint)
            else:
                for k, v in complaint_updates.items():
                    setattr(complaint, k, v)

            db.commit()

            # 3. Save FIR
            fir_num = dossier.get("fir", {}).get("FIR_Number") or f"FIR/TN-CHN-001/2026/{complaint_id.split('-')[-1]}"
            complaint.fir_number = fir_num
            
            # Save or Update FIR record
            fir = db.query(FIR).filter(FIR.complaint_id == complaint_id).first()
            if not fir:
                fir = FIR(
                    complaint_id=complaint_id,
                    fir_number=fir_num,
                    narrative=dossier.get("fir_narrative") or "Narrative pending review.",
                    raw_fir_data=dossier.get("fir") or {}
                )
                db.add(fir)
            else:
                fir.fir_number = fir_num
                fir.narrative = dossier.get("fir_narrative") or fir.narrative
                fir.raw_fir_data = dossier.get("fir") or fir.raw_fir_data

            # 4. Save Legal Analysis
            legal = db.query(LegalAnalysis).filter(LegalAnalysis.complaint_id == complaint_id).first()
            legal_data = dossier.get("legal_analysis") or {}
            recommended = legal_data.get("recommended_sections") if isinstance(legal_data, dict) else []
            summary = legal_data.get("legal_summary") if isinstance(legal_data, dict) else "No summary available."
            if not legal:
                legal = LegalAnalysis(
                    complaint_id=complaint_id,
                    recommended_sections=recommended or [],
                    legal_summary=summary or ""
                )
                db.add(legal)
            else:
                legal.recommended_sections = recommended or legal.recommended_sections
                legal.legal_summary = summary or legal.legal_summary

            # 5. Save Evidence Analysis
            evidence = db.query(EvidenceAnalysis).filter(EvidenceAnalysis.complaint_id == complaint_id).first()
            evidence_data = dossier.get("evidence_analysis") or dossier.get("evidence") or {}
            if not evidence:
                evidence = EvidenceAnalysis(
                    complaint_id=complaint_id,
                    evidence_data=evidence_data
                )
                db.add(evidence)
            else:
                evidence.evidence_data = evidence_data

            # 6. Save Timeline
            timeline = db.query(CaseTimeline).filter(CaseTimeline.complaint_id == complaint_id).first()
            timeline_data = dossier.get("timeline_analysis") or dossier.get("timeline") or {}
            if not timeline:
                timeline = CaseTimeline(
                    complaint_id=complaint_id,
                    timeline_data=timeline_data
                )
                db.add(timeline)
            else:
                timeline.timeline_data = timeline_data

            # 7. Save Risk Assessment
            risk = db.query(RiskAssessment).filter(RiskAssessment.complaint_id == complaint_id).first()
            risk_data = dossier.get("risk_assessment") or {}
            if not risk:
                risk = RiskAssessment(
                    complaint_id=complaint_id,
                    assessment_data=risk_data
                )
                db.add(risk)
            else:
                risk.assessment_data = risk_data

            # 8. Save Investigation Report
            report = db.query(InvestigationReport).filter(InvestigationReport.complaint_id == complaint_id).first()
            report_data = dossier.get("investigation_report") or dossier.get("investigation") or {}
            if not report:
                report = InvestigationReport(
                    complaint_id=complaint_id,
                    report_data=report_data
                )
                db.add(report)
            else:
                report.report_data = report_data

            # 9. Save Action Recommendations
            action = db.query(ActionRecommendation).filter(ActionRecommendation.complaint_id == complaint_id).first()
            action_data = dossier.get("action_recommendations") or dossier.get("recommended_actions") or {}
            if not action:
                action = ActionRecommendation(
                    complaint_id=complaint_id,
                    recommendations_data=action_data
                )
                db.add(action)
            else:
                action.recommendations_data = action_data

            db.commit()
            db.refresh(complaint)
            logger.info("Successfully persisted case dossier for ID: %s", complaint_id)
            return complaint

        except Exception as e:
            db.rollback()
            logger.error("Error saving case dossier: %s", e)
            raise e

    @staticmethod
    def get_full_case_dossier(db: Session, complaint_id: str) -> dict:
        complaint = ComplaintRepository.get_by_id(db, complaint_id)
        if not complaint:
            return {}

        fir = db.query(FIR).filter(FIR.complaint_id == complaint_id).first()
        legal = db.query(LegalAnalysis).filter(LegalAnalysis.complaint_id == complaint_id).first()
        evidence = db.query(EvidenceAnalysis).filter(EvidenceAnalysis.complaint_id == complaint_id).first()
        timeline = db.query(CaseTimeline).filter(CaseTimeline.complaint_id == complaint_id).first()
        risk = db.query(RiskAssessment).filter(RiskAssessment.complaint_id == complaint_id).first()
        report = db.query(InvestigationReport).filter(InvestigationReport.complaint_id == complaint_id).first()
        action = db.query(ActionRecommendation).filter(ActionRecommendation.complaint_id == complaint_id).first()

        # Build dashboard object
        dashboard = {
            "case_overview": {
                "incident": fir.raw_fir_data.get("Incident", {}) if fir else {
                    "Summary": complaint.transcript or "",
                    "Date": complaint.incident_date or "",
                    "Time": complaint.incident_time or "",
                    "Location": complaint.location or ""
                },
                "complainant": fir.raw_fir_data.get("Complainant", {}) if fir else {
                    "Name": complaint.complainant_name,
                    "Phone": complaint.mobile_number,
                    "Address": complaint.address or ""
                },
                "accused": fir.raw_fir_data.get("Accused", {}) if fir else {
                    "Name": complaint.suspect_details or ""
                },
                "property": fir.raw_fir_data.get("Property", {}) if fir else {},
                "cyber": fir.raw_fir_data.get("Cyber", {}) if fir else {},
                "possible_offences": fir.raw_fir_data.get("Possible_Offences", []) if fir else [complaint.crime_type]
            },
            "legal_analysis": {
                "recommended_sections": legal.recommended_sections if legal else [],
                "legal_summary": legal.legal_summary if legal else ""
            },
            "risk_assessment": risk.assessment_data if risk else {},
            "timeline": timeline.timeline_data if timeline else {},
            "evidence": evidence.evidence_data if evidence else {},
            "investigation": report.report_data if report else {},
            "recommended_actions": action.recommendations_data if action else {}
        }

        return {
            "status": "success",
            "complaint": {
                "id": complaint.id,
                "firNumber": complaint.fir_number or "Draft",
                "complainantName": complaint.complainant_name,
                "mobileNumber": complaint.mobile_number,
                "address": complaint.address,
                "incidentDate": complaint.incident_date,
                "incidentTime": complaint.incident_time,
                "location": complaint.location,
                "crimeType": complaint.crime_type,
                "status": complaint.status,
                "createdAt": complaint.created_at.isoformat(),
                "completionPercentage": complaint.completion_percentage
            },
            "dashboard": dashboard,
            "fir": {
                "FIR_Number": fir.fir_number if fir else "Draft",
                "Incident": dashboard["case_overview"]["incident"],
                "Complainant": dashboard["case_overview"]["complainant"],
                "Accused": dashboard["case_overview"]["accused"],
                "Property": dashboard["case_overview"]["property"],
                "Cyber": dashboard["case_overview"]["cyber"],
                "Possible_Offences": dashboard["case_overview"]["possible_offences"]
            } if fir else None,
            "narrative": fir.narrative if fir else "",
            "legal_analysis": dashboard["legal_analysis"]
        }
