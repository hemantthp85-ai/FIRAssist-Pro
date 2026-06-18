import os
import json
import datetime
from typing import List, Dict, Any

EVIDENCE_DATA_PATH = os.path.join("data", "evidence_metadata.json")
UPLOAD_DIR = os.path.join("data", "uploads")

# Ensure required directories exist
os.makedirs(os.path.dirname(EVIDENCE_DATA_PATH), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

COMMON_DOCUMENTS = [
    "Complainant ID Proof",
    "Witness Statements",
    "Spot Inspection Report",
    "Photographs/Videos",
    "Seizure Memo",
    "Case Diary Entries",
    "Investigation Officer Report"
]

CRIME_SPECIFIC_DOCUMENTS = {
    "assault": [
        "Medical Examination Report",
        "Wound Certificate",
        "Hospital Records",
        "Doctor Opinion",
        "Injury Photos",
        "CCTV Footage",
        "Weapon Recovery Report"
    ],
    "physical attack": [
        "Medical Examination Report",
        "Wound Certificate",
        "Hospital Records",
        "Doctor Opinion",
        "Injury Photos",
        "CCTV Footage",
        "Weapon Recovery Report"
    ],
    "murder": [
        "Inquest Report",
        "Post-Mortem Report",
        "Death Certificate",
        "Crime Scene Photos",
        "Forensic Reports",
        "Fingerprint Reports",
        "DNA Analysis"
    ],
    "homicide": [
        "Inquest Report",
        "Post-Mortem Report",
        "Death Certificate",
        "Crime Scene Photos",
        "Forensic Reports",
        "Fingerprint Reports",
        "DNA Analysis"
    ],
    "theft": [
        "Purchase Bills",
        "Ownership Proof",
        "CCTV Footage",
        "Witness Statements",
        "Recovery Memo",
        "Property Identification Documents",
        "Bank Statements"
    ],
    "missing person": [
        "Recent Photograph",
        "Aadhaar Copy",
        "School ID",
        "Passport Copy",
        "Mobile Details",
        "Call Detail Records",
        "Social Media Information",
        "Witness Statements",
        "Missing Person Form"
    ],
    "road accident": [
        "Driving License",
        "RC Book",
        "Insurance Certificate",
        "Vehicle Inspection Report",
        "Accident Sketch",
        "Hospital Records"
    ],
    "accident": [
        "Driving License",
        "RC Book",
        "Insurance Certificate",
        "Vehicle Inspection Report",
        "Accident Sketch",
        "Hospital Records"
    ],
    "cyber crime": [
        "Screenshots",
        "Email Records",
        "Chat Logs",
        "Transaction Statements",
        "Bank Records",
        "IP Address Logs"
    ],
    "kidnapping": [
        "Victim Photograph",
        "Witness Statements",
        "Call Records",
        "CCTV Footage",
        "GPS Data",
        "Ransom Messages"
    ],
    "abduction": [
        "Victim Photograph",
        "Witness Statements",
        "Call Records",
        "CCTV Footage",
        "GPS Data",
        "Ransom Messages"
    ],
    "domestic violence": [
        "Medical Reports",
        "Injury Photos",
        "Previous Complaints",
        "Audio Evidence",
        "Video Evidence",
        "Messages/Chats"
    ],
    "sexual assault": [
        "Medical Examination Report",
        "DNA Samples",
        "Forensic Evidence",
        "Clothing Seizure Memo",
        "Victim Statement"
    ],
    "property damage": [
        "Photographs",
        "Repair Estimates",
        "Ownership Documents",
        "CCTV Footage"
    ],
    "vandalism": [
        "Photographs",
        "Repair Estimates",
        "Ownership Documents",
        "CCTV Footage"
    ]
}

class EvidenceService:
    @staticmethod
    def get_required_documents(crime_type: str) -> Dict[str, Any]:
        """
        Return common and crime-specific documents based on normalized crime type.
        """
        crime_key = str(crime_type).lower().strip()
        
        # Robust normalization matching
        matched_key = None
        if crime_key in CRIME_SPECIFIC_DOCUMENTS:
            matched_key = crime_key
        else:
            # Match longest key that is a substring of crime_key (e.g. "sexual assault" matched for "sexual assault")
            substring_matches = [k for k in CRIME_SPECIFIC_DOCUMENTS.keys() if k in crime_key]
            if substring_matches:
                matched_key = max(substring_matches, key=len)
            else:
                # Fallback: Match shortest key of which crime_key is a substring (e.g. "assault" for "assa")
                superstring_matches = [k for k in CRIME_SPECIFIC_DOCUMENTS.keys() if crime_key in k]
                if superstring_matches:
                    matched_key = min(superstring_matches, key=len)
        
        matched_specific = CRIME_SPECIFIC_DOCUMENTS.get(matched_key, []) if matched_key else []
                
        return {
            "crime_type": crime_type,
            "common_documents": COMMON_DOCUMENTS,
            "crime_specific_documents": matched_specific
        }

    @staticmethod
    def _read_metadata() -> Dict[str, Any]:
        if not os.path.exists(EVIDENCE_DATA_PATH):
            return {}
        try:
            with open(EVIDENCE_DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def _write_metadata(data: Dict[str, Any]):
        with open(EVIDENCE_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def get_case_evidence(cls, case_id: str) -> Dict[str, Any]:
        """
        Get metadata (uploaded files, notes) for a specific case.
        """
        db = cls._read_metadata()
        case_data = db.get(case_id, {
            "uploaded_files": [],
            "notes": ""
        })
        return case_data

    @classmethod
    def save_file_metadata(cls, case_id: str, doc_name: str, filename: str, file_path: str) -> Dict[str, Any]:
        """
        Save file upload metadata to the case record.
        """
        db = cls._read_metadata()
        if case_id not in db:
            db[case_id] = {
                "uploaded_files": [],
                "notes": ""
            }
        
        # Check if already exists, overwrite if yes
        files = db[case_id]["uploaded_files"]
        existing = next((f for f in files if f["doc_name"] == doc_name), None)
        
        timestamp = datetime.datetime.now().isoformat()
        
        file_meta = {
            "doc_name": doc_name,
            "filename": filename,
            "timestamp": timestamp,
            "status": "Uploaded",
            "file_path": file_path
        }
        
        if existing:
            # Update
            existing.update(file_meta)
        else:
            files.append(file_meta)
            
        cls._write_metadata(db)
        return file_meta

    @classmethod
    def update_case_notes(cls, case_id: str, notes: str) -> Dict[str, Any]:
        db = cls._read_metadata()
        if case_id not in db:
            db[case_id] = {
                "uploaded_files": [],
                "notes": ""
            }
        db[case_id]["notes"] = notes
        cls._write_metadata(db)
        return db[case_id]

    @classmethod
    def verify_document(cls, case_id: str, doc_name: str, status: str) -> Dict[str, Any]:
        """
        Verify or toggle status of a document (e.g. 'Verified' or 'Uploaded').
        """
        db = cls._read_metadata()
        if case_id in db:
            files = db[case_id]["uploaded_files"]
            existing = next((f for f in files if f["doc_name"] == doc_name), None)
            if existing:
                existing["status"] = status
                cls._write_metadata(db)
                return existing
        return {"status": "error", "message": "Document not found"}
