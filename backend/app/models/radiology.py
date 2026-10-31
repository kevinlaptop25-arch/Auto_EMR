from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class DicomInstance(BaseModel):
    sop_instance_uid: str
    instance_number: int
    image_url: str
    modality: str
    window_center: int = 40
    window_width: int = 400
    rows: int = 512
    columns: int = 512
    slice_thickness: Optional[float] = None
    slice_location: Optional[float] = None

class RadiologyStudy(BaseModel):
    id: str
    patient_id: str
    accession_no: str
    study_datetime: datetime
    modality: str  # "CR", "DX", "CT", "MR", "US"
    body_part: str
    study_description: str
    ordering_doctor: str
    findings: str
    impression: str
    instances: List[DicomInstance]
    radiologist_name: str = "Dr. Suresh Babu (MD Radiodiagnosis)"
    radiologist_reg: str = "KMC: 98124"
    status: str = "VERIFIED"
