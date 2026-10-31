from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class EmergencyEncounter(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    age: int
    gender: str
    arrival_time: datetime
    brought_by: str = "108 Emergency Ambulance"
    triage_level: str  # "RED", "YELLOW", "GREEN"
    triage_score: str = "ESI-2" # Emergency Severity Index
    chief_complaint: str
    vitals: Dict[str, str] = Field(default_factory=dict) # BP, PR, RR, SpO2, GCS, Temp
    gcs_score: str = "15/15 (E4 V5 M6)"
    
    # Medico-Legal Case (MLC) Registry
    is_mlc: bool = False
    mlc_no: Optional[str] = None
    police_station: Optional[str] = None
    injury_nature: Optional[str] = None # Blunt trauma, RTA, Fall from height, Poisoning
    alcohol_influence: bool = False
    
    # Emergency Interventions & Disposition
    attending_er_physician: str
    physician_reg_no: str
    emergency_interventions: List[str] = Field(default_factory=list)
    crash_cart_activated: bool = False
    disposition: str = "ADMITTED_WARD" # "ADMITTED_ICU", "TRANSFER_OT", "ADMITTED_WARD", "DISCHARGED_STABLE", "LAMA"
    disposition_ward: Optional[str] = None
    er_status: str = "STABILIZED" # "ACTIVE_RESUSCITATION", "STABILIZED", "DISPOSED"
