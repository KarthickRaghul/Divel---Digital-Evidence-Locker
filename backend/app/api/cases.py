from fastapi import APIRouter

router = APIRouter()

from app.services.database import db

@router.get("/")
def get_cases():
    return db.list_cases()

@router.get("/{case_id}")
def get_case(case_id: str):
    return db.get_case(case_id)

from app.models.case import CaseCreate
import uuid
from datetime import datetime

@router.post("/")
def create_case(case_in: CaseCreate):
    case_data = case_in.dict()
    case_data["id"] = str(uuid.uuid4()) # This works as the PK for forensichain-cases
    case_data["caseNumber"] = f"CR-{uuid.uuid4().hex[:6].upper()}" # Generate simple case number
    case_data["status"] = "Under Investigation" # Default status
    case_data["createdAt"] = str(datetime.now())
    case_data["updatedAt"] = str(datetime.now())
    case_data["evidence"] = [] # Init empty evidence list
    
    return db.create_case(case_data)
