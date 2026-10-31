from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Patient(BaseModel):
    id: str
    mr_no: str
    ip_no: Optional[str] = None
    name: str
    relative_name: str
    marital_status: str = "Married"
    age: int
    gender: str  # "Male" or "Female"
    religion: str = "Hindu"
    address: str = "Bidarahalli, Virgo Nagar Post"
    city: str = "Bangalore"
    phone: str = "9876543210"
    occupation: str = "Self-employed"
    medico_legal: bool = False
    payer_type: str = "AB-ARK Insurance/Cashless"
    
    # Departmental Assignment (Across 18+ NMC Departments)
    department: str
    sub_department: Optional[str] = None
    unit: str = "Unit-I"
    ward_bed: str = "General Ward Bed 04"
    
    # Timeline
    admission_time: datetime
    discharge_time: Optional[datetime] = None
    status: str = "IPD_ACTIVE"  # "OPD", "IPD_ACTIVE", "DISCHARGED"
    
    # Clinical In-Charge (East Point Hospital Doctors & KMC Reg Nos)
    attending_doctor: str
    doctor_reg_no: str  # e.g. "KMC: 174958"
    
    # ABDM Milestones
    abha_id: Optional[str] = None       # e.g. "91-7234-8921-9923"
    abha_address: Optional[str] = None  # e.g. "patient@abdm"
    abha_verified: bool = False
