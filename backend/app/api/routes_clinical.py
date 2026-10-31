from fastapi import APIRouter, HTTPException, Response
from typing import Dict, Any

from app.core.batch_generator import batch_engine
from app.core.timeline_simulator import timeline_manager
from app.core.pdf_service import PdfGeneratorService

router = APIRouter(prefix="/clinical", tags=["Clinical Case Sheets"])

@router.get("/{patient_id}/full")
def get_clinical_bundle(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Clinical records not found for patient")
    
    raw_bundle = batch_engine.patient_bundles[patient_id]
    filtered = timeline_manager.filter_bundle(raw_bundle)
    return filtered

@router.get("/{patient_id}/pdf/casesheet")
def download_casesheet_pdf(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient records not found")
    
    raw_bundle = batch_engine.patient_bundles[patient_id]
    pdf_bytes = PdfGeneratorService.generate_case_sheet_pdf(
        raw_bundle["patient"],
        raw_bundle["hp_exam"]
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=casesheet_{raw_bundle['patient'].mr_no}.pdf"}
    )

@router.get("/{patient_id}/pdf/discharge")
def download_discharge_summary_pdf(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient records not found")
    
    raw_bundle = batch_engine.patient_bundles[patient_id]
    filtered = timeline_manager.filter_bundle(raw_bundle)
    
    summary = filtered.get("discharge_summary")
    if not summary:
        raise HTTPException(
            status_code=400,
            detail=f"Discharge summary is not available at current simulated time ({timeline_manager.get_current_time().strftime('%I:%M %p')}). Patient is currently admitted in hospital."
        )

    pdf_bytes = PdfGeneratorService.generate_discharge_summary_pdf(
        raw_bundle["patient"],
        summary
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=discharge_{raw_bundle['patient'].mr_no}.pdf"}
    )

@router.get("/{patient_id}/pdf/opd-slip")
def download_opd_slip_pdf(patient_id: str):
    if patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    patient = batch_engine.patients_db[patient_id]
    opd_slip = None
    if patient_id in batch_engine.patient_bundles:
        opd_slip = batch_engine.patient_bundles[patient_id].get("opd_slip")
    if not opd_slip:
        opd_slip = batch_engine.opd_slips.get(patient_id)
    if not opd_slip:
        from app.core.clinical_engine import ClinicalEngine
        opd_slip = ClinicalEngine.generate_opd_slip(patient)
        batch_engine.opd_slips[patient_id] = opd_slip

    pdf_bytes = PdfGeneratorService.generate_opd_slip_pdf(patient, opd_slip)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=opd_slip_{patient.mr_no}.pdf"}
    )

@router.post("/{patient_id}/admit-to-ipd")
def admit_patient_to_ipd(patient_id: str):
    if patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    bundle = batch_engine.admit_opd_patient(patient_id, simulated_time=timeline_manager.get_current_time())
    filtered = timeline_manager.filter_bundle(bundle)
    return {
        "status": "ADMITTED",
        "message": f"Patient successfully admitted to {bundle['patient'].department} Ward Bed {bundle['patient'].ward_bed}. IP No assigned: {bundle['patient'].ip_no}",
        "bundle": filtered
    }
