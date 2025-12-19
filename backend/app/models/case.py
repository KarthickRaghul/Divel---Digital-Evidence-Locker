from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class Accused(BaseModel):
    name: str
    fatherName: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    status: str

class CaseCreate(BaseModel):
    district: str
    unit: str
    lawSections: List[str]
    dateOfOffence: str
    dateOfReport: str
    sceneOfCrime: str
    latitude: str
    longitude: str
    contrabandType: Optional[str] = None
    contrabandQuantity: Optional[str] = None
    vehicleDetails: Optional[str] = None
    accused: List[Accused]
    customFields: List[Any] = []
    publicAlertEnabled: bool = False
    publicAlertMessage: Optional[str] = None
    publicAlertMobile: Optional[str] = None
