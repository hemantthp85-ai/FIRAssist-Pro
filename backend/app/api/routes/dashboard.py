from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.repositories import ComplaintRepository, AnalyticsRepository
from backend.app.db.services import CaseService
import logging

logger = logging.getLogger("fir_copilot.api.dashboard")
router = APIRouter()


@router.get("/dashboard/stats")
def get_stats(db: Session = Depends(get_db)):
    try:
        stats = AnalyticsRepository.get_dashboard_stats(db)
        return stats
    except Exception as e:
        logger.error("Error getting dashboard stats: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/analytics")
def get_analytics(db: Session = Depends(get_db)):
    try:
        analytics = AnalyticsRepository.get_analytics_details(db)
        return analytics
    except Exception as e:
        logger.error("Error getting analytics: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/complaints")
def list_complaints(
    status: str = Query(None),
    search: str = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    try:
        results, total = ComplaintRepository.list_all(
            db, status=status, search=search, limit=limit, offset=offset
        )
        
        complaints_list = []
        for c in results:
            complaints_list.append({
                "id": c.id,
                "firNumber": c.fir_number or "Draft",
                "complainantName": c.complainant_name,
                "mobileNumber": c.mobile_number,
                "address": c.address,
                "incidentDate": c.incident_date,
                "incidentTime": c.incident_time,
                "location": c.location,
                "crimeType": c.crime_type or "Other",
                "status": c.status,
                "createdAt": c.created_at.isoformat(),
                "completionPercentage": c.completion_percentage
            })
            
        return {
            "status": "success",
            "total": total,
            "complaints": complaints_list
        }
    except Exception as e:
        logger.error("Error listing complaints: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/complaints/{complaint_id}")
def get_complaint_details(complaint_id: str, db: Session = Depends(get_db)):
    try:
        dossier = CaseService.get_full_case_dossier(db, complaint_id)
        if not dossier:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return dossier
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting case details: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
