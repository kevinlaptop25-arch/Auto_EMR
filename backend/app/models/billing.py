from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BillItem(BaseModel):
    category: str # "Registration", "Consultation", "Bed Charges", "Nursing", "Lab Investigations", "Radiology", "Pharmacy", "Procedure"
    description: str
    quantity: int = 1
    unit_rate_inr: float
    total_amount_inr: float

class HospitalInvoice(BaseModel):
    invoice_no: str
    receipt_no: Optional[str] = None
    patient_id: str
    patient_name: str
    mr_no: str
    ip_no: Optional[str] = None
    encounter_type: str # "OPD" or "IPD"
    bill_timestamp: datetime
    payer_scheme: str # "Ayushman Bharat PMJAY", "AB-ARK Insurance/Cashless", "Self-Pay Cash/UPI"
    claim_preauth_id: Optional[str] = None # e.g. "PMJAY-TMS-KA-2026-8912"
    
    line_items: List[BillItem] = Field(default_factory=list)
    gross_total_inr: float
    scheme_discount_inr: float = 0.0
    net_payable_inr: float
    paid_amount_inr: float
    balance_due_inr: float = 0.0
    payment_status: str = "PAID" # "PAID", "CLAIM_APPROVED", "PENDING", "CREDIT"
    payment_mode: str = "Government Cashless Settlement" # "Cashless Scheme", "UPI", "Credit Card", "Cash"
    cashier_desk: str = "Main Billing Counter #2, EPH Bangalore"
    cashier_name: str = "Anil Kulkarni"
