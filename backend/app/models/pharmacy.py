from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class InventoryItem(BaseModel):
    id: str
    drug_name: str
    generic_name: str
    dosage_form: str # "Tablet", "Injection", "Syrup", "Inhaler", "IV Infusion"
    strength: str
    category: str # "Essential Drug (EDL)", "Antibiotic", "Endocrine", "Cardiovascular", "Emergency", "Narcotic Schedule X"
    batch_no: str
    expiry_date: str # "10/2027"
    stock_quantity: int
    reorder_level: int = 50
    unit_price_inr: float
    is_narcotic: bool = False

class PrescriptionItem(BaseModel):
    drug_name: str
    dosage_form: str
    dosage_instruction: str # "1-0-1 after food"
    duration_days: int
    quantity_prescribed: int
    quantity_dispensed: int = 0
    batch_no: Optional[str] = None
    expiry_date: Optional[str] = None
    unit_price_inr: float = 0.0
    status: str = "DISPENSED" # "PENDING", "DISPENSED"

class PharmacyDispensation(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    encounter_type: str # "OPD" or "IPD"
    prescribed_by: str
    doctor_reg_no: str
    prescribed_at: datetime
    dispensed_at: Optional[datetime] = None
    items: List[PrescriptionItem] = Field(default_factory=list)
    dispensation_status: str = "DISPENSED" # "PENDING", "DISPENSED", "PARTIALLY_DISPENSED"
    pharmacist_name: str = "Shrikanth Joshi, B.Pharm"
    pharmacist_reg_no: str = "KSPC: 48912"
    total_amount_inr: float = 0.0
    is_cashless_scheme: bool = True # Ayushman Bharat Free Drug Initiative
