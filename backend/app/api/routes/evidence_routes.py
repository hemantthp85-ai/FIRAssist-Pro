from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.services.evidence_service import EvidenceService, UPLOAD_DIR
import os
import shutil

router = APIRouter()

@router.get("/evidence/required-documents/{crime_type}")
def get_required_documents(crime_type: str):
    """
    Get list of required documents for a specific crime type.
    """
    try:
        return EvidenceService.get_required_documents(crime_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evidence/upload")
async def upload_evidence(
    case_id: str = Form(...),
    doc_name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a file for a specific case and document name.
    """
    try:
        # Save file locally
        filename = f"{case_id}_{doc_name}_{file.filename}".replace(" ", "_")
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Record metadata
        meta = EvidenceService.save_file_metadata(
            case_id=case_id,
            doc_name=doc_name,
            filename=file.filename,
            file_path=file_path
        )
        return {
            "status": "success",
            "message": f"Successfully uploaded {file.filename}",
            "metadata": meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evidence/case/{case_id}")
def get_case_evidence(case_id: str):
    """
    Get uploaded evidence and notes for a specific case.
    """
    try:
        return EvidenceService.get_case_evidence(case_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evidence/case/{case_id}/notes")
def update_case_notes(case_id: str, data: dict):
    """
    Update notes/remarks for a specific case.
    """
    try:
        notes = data.get("notes", "")
        updated = EvidenceService.update_case_notes(case_id, notes)
        return {
            "status": "success",
            "message": "Notes updated successfully",
            "case_data": updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evidence/case/{case_id}/verify")
def verify_document(case_id: str, data: dict):
    """
    Toggle verification status of an uploaded document.
    """
    try:
        doc_name = data.get("doc_name")
        status = data.get("status", "Verified")  # e.g., 'Verified' or 'Uploaded'
        if not doc_name:
            raise HTTPException(status_code=400, detail="doc_name is required")
            
        result = EvidenceService.verify_document(case_id, doc_name, status)
        if "status" in result and result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
            
        return {
            "status": "success",
            "message": f"Document verification status updated to {status}",
            "document": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
