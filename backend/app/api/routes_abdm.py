import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.models.abdm import (
    M1OtpRequest, M1OtpVerify, AbhaProfile,
    M3ConsentRequest, M3ExternalRecord
)
from app.core.batch_generator import batch_engine
from app.core.fhir_exporter import FhirExporter

router = APIRouter(prefix="/abdm", tags=["ABDM Milestones M1, M2, M3"])

# In-memory ABDM state
M1_SESSIONS: Dict[str, Dict[str, Any]] = {}
M3_CONSENTS: Dict[str, M3ConsentRequest] = {}

@router.post("/m1/generate-otp")
def generate_m1_otp(payload: M1OtpRequest):
    txn_id = str(uuid.uuid4())
    masked = payload.identifier[-4:]
    M1_SESSIONS[txn_id] = {
        "identifier": payload.identifier,
        "auth_method": payload.auth_method,
        "otp": "123456",
        "created_at": datetime.now()
    }
    return {
        "txn_id": txn_id,
        "message": f"OTP successfully sent to registered mobile linked to ******{masked}",
        "demo_hint": "Demo OTP is: 123456"
    }

@router.post("/m1/verify-otp", response_model=AbhaProfile)
def verify_m1_otp(payload: M1OtpVerify):
    if payload.txn_id not in M1_SESSIONS:
        raise HTTPException(status_code=400, detail="Invalid or expired transaction ID")
        
    session = M1_SESSIONS[payload.txn_id]
    if payload.otp != session["otp"]:
        raise HTTPException(status_code=400, detail="Invalid OTP entered")
        
    abha_no = f"91-{str(uuid.uuid4().int)[:4]}-{str(uuid.uuid4().int)[4:8]}-{str(uuid.uuid4().int)[8:12]}"
    abha_addr = payload.desired_abha_address or f"patient.{abha_no[-4:]}@abdm"
    if not abha_addr.endswith("@abdm"):
        abha_addr += "@abdm"
        
    profile = AbhaProfile(
        abha_number=abha_no,
        abha_address=abha_addr,
        name="Ramesh Gowda",
        gender="Male",
        year_of_birth=1978,
        mobile=session["identifier"] if len(session["identifier"]) == 10 else "9876543210",
        verification_status="VERIFIED",
        kyc_level="KYC_VERIFIED",
        qr_code_data=f"ABHA:{abha_no}|NAME:Ramesh Gowda|DOB:1978|GENDER:M"
    )
    return profile

@router.post("/m1/link-patient/{patient_id}")
def link_abha_to_patient(patient_id: str, abha_number: str, abha_address: str):
    if patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    patient = batch_engine.patients_db[patient_id]
    patient.abha_id = abha_number
    patient.abha_address = abha_address
    patient.abha_verified = True
    return {"status": "SUCCESS", "message": f"ABHA ID {abha_number} successfully linked to MR No: {patient.mr_no}"}

@router.post("/m1/quick-generate/{patient_id}")
def quick_generate_abha_for_patient(patient_id: str):
    result = batch_engine.link_abha_patient(patient_id)
    if result.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result

@router.get("/m2/fhir-export/{patient_id}")
def get_m2_fhir_payload(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient clinical records not found")
        
    bundle = batch_engine.patient_bundles[patient_id]
    patient = bundle["patient"]
    labs = bundle.get("lab_reports", [])
    
    if not labs:
        raise HTTPException(status_code=400, detail="No diagnostic reports available to format into FHIR")
        
    # Format first lab into FHIR R4 Bundle
    fhir_bundle = FhirExporter.generate_diagnostic_report_bundle(patient, labs[0])
    return {
        "hip_id": "IN2910000123",
        "hip_name": "East Point Hospital & Research Centre",
        "care_context": {
            "patientReference": patient.id,
            "careContextReference": f"IPD-{patient.ip_no or patient.mr_no}",
            "display": f"Inpatient Encounter - {patient.department}"
        },
        "fhir_bundle": fhir_bundle
    }

@router.post("/m3/request-consent")
def request_m3_consent(
    patient_id: str,
    doctor_name: str = "Dr. B. R. Ramachandra",
    doctor_reg: str = "KMC: 45210"
):
    if patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    patient = batch_engine.patients_db[patient_id]
    consent_id = f"CONSENT-{str(uuid.uuid4())[:8].upper()}"
    
    req = M3ConsentRequest(
        consent_id=consent_id,
        patient_abha_id=patient.abha_id or "91-1234-5678-9012",
        requester_doctor=doctor_name,
        requester_doctor_reg=doctor_reg,
        date_range_from=datetime.now() - timedelta(days=365),
        date_range_to=datetime.now(),
        status="REQUESTED"
    )
    M3_CONSENTS[consent_id] = req
    return req

@router.post("/m3/approve-consent/{consent_id}")
def approve_m3_consent(consent_id: str):
    if consent_id not in M3_CONSENTS:
        raise HTTPException(status_code=404, detail="Consent request not found")
        
    M3_CONSENTS[consent_id].status = "GRANTED"
    return {"status": "GRANTED", "message": "Consent granted by patient via ABDM Health Locker"}

@router.get("/m3/fetch-external-records/{consent_id}")
def fetch_m3_external_records(consent_id: str) -> List[Dict[str, Any]]:
    if consent_id not in M3_CONSENTS:
        raise HTTPException(status_code=404, detail="Consent request not found")
        
    consent = M3_CONSENTS[consent_id]
    if consent.status != "GRANTED":
        raise HTTPException(status_code=403, detail="Consent has not been granted by patient yet")
        
    # Simulated historical health records from external networks (Narayana Health, Manipal Hospital)
    return [
        {
            "source_hospital": "Manipal Hospital, Whitefield",
            "date": "14/02/2025",
            "record_type": "DischargeSummary",
            "diagnosis": "Viral Bronchitis (ICD-10: J20.9)",
            "physician": "Dr. Rajesh K (KMC: 88219)",
            "summary": "Treated with Azithromycin and bronchodilator nebulization. Improved and discharged stable.",
            "documents": ["Discharge_Summary_Manipal.pdf"]
        },
        {
            "source_hospital": "Narayana Health City, Bommasandra",
            "date": "19/08/2024",
            "record_type": "DiagnosticReport",
            "diagnosis": "2D Echocardiography & Cardiac Screening",
            "physician": "Dr. K. Srinivas (KMC: 55120)",
            "summary": "Normal LV systolic function, LVEF 62%, No regional wall motion abnormalities, Grade-1 diastolic dysfunction.",
            "documents": ["Echo_Report_NH.pdf"]
        }
    ]
