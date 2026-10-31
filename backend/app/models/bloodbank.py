from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BloodInventoryUnit(BaseModel):
    unit_id: str
    blood_group: str # "A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"
    component: str # "Packed Red Blood Cells (PRBC)", "Fresh Frozen Plasma (FFP)", "Platelet Concentrate (RDP)", "Single Donor Platelets (SDP)", "Cryoprecipitate"
    volume_ml: int
    collection_date: str
    expiry_date: str
    storage_temp: str # "2°C - 6°C", "-30°C Deep Freezer", "20°C - 24°C Agitator"
    
    # 5-Panel Mandatory Transfusion-Transmissible Infection (TTI) Screening
    tti_hiv: str = "NON-REACTIVE"
    tti_hbsag: str = "NON-REACTIVE"
    tti_hcv: str = "NON-REACTIVE"
    tti_vdrl: str = "NON-REACTIVE"
    tti_mp: str = "NEGATIVE"
    
    status: str = "AVAILABLE" # "AVAILABLE", "CROSSMATCHED_RESERVED", "TRANSFUSED"

class BloodRequisition(BaseModel):
    requisition_no: str
    patient_id: str
    patient_name: str
    mr_no: str
    ip_no: Optional[str] = None
    department: str
    ward_bed: str
    patient_blood_group: str
    clinical_indication: str
    component_requested: str
    units_requested: int = 1
    requested_at: datetime
    crossmatch_status: str = "MAJOR_COMPATIBLE" # "SAMPLE_RECEIVED", "TESTING_COOMBS", "MAJOR_COMPATIBLE", "ISSUED"
    assigned_unit_id: Optional[str] = None
    transfusion_reaction_reported: bool = False
    licensed_medical_officer: str = "Dr. Manjula Swamy, MD (Path & Immuno)"
    medical_officer_reg: str = "KMC: 52190"
