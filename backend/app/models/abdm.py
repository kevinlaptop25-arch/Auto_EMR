from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class M1OtpRequest(BaseModel):
    auth_method: str = "AADHAAR_OTP"  # "AADHAAR_OTP" or "MOBILE_OTP"
    identifier: str  # 12-digit Aadhaar or 10-digit Mobile

class M1OtpVerify(BaseModel):
    txn_id: str
    otp: str = "123456"
    desired_abha_address: Optional[str] = None

class AbhaProfile(BaseModel):
    abha_number: str  # e.g., "91-4432-8901-2234"
    abha_address: str  # e.g., "patient@abdm"
    name: str
    gender: str
    year_of_birth: int
    mobile: str
    profile_photo: Optional[str] = None
    verification_status: str = "VERIFIED"
    kyc_level: str = "KYC_VERIFIED"
    qr_code_data: str

class M2CareContext(BaseModel):
    patient_reference: str
    care_context_reference: str  # e.g., "IPD-2635136"
    display: str

class M2FhirBundlePayload(BaseModel):
    hip_id: str = "IN2910000123"  # East Point Hospital ABDM HIP ID
    care_context: M2CareContext
    fhir_bundle: Dict[str, Any]
    generated_at: datetime

class M3ConsentRequest(BaseModel):
    consent_id: str
    patient_abha_id: str
    requester_doctor: str
    requester_doctor_reg: str
    hiu_id: str = "IN2910000123"
    purpose: str = "CAREMGT"  # Care Management
    date_range_from: datetime
    date_range_to: datetime
    hi_types: List[str] = ["DiagnosticReport", "Prescription", "DischargeSummary", "OPConsultation"]
    status: str = "REQUESTED"  # "REQUESTED", "GRANTED", "DENIED", "EXPIRED"

class M3ExternalRecord(BaseModel):
    source_hospital: str
    date: str
    document_type: str
    summary: str
    details: Dict[str, Any]
