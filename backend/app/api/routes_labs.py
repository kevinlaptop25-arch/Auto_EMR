from fastapi import APIRouter, HTTPException, Response
from typing import List, Dict, Any

from app.core.batch_generator import batch_engine
from app.core.timeline_simulator import timeline_manager
from app.core.pdf_service import PdfGeneratorService
from app.core.fhir_exporter import FhirExporter

router = APIRouter(prefix="/labs", tags=["Diagnostics & Labs"])

@router.get("/{patient_id}")
def get_patient_labs(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        return {"reports": []}
    
    filtered = timeline_manager.filter_bundle(batch_engine.patient_bundles[patient_id])
    return {"reports": filtered.get("lab_reports", [])}

@router.get("/{patient_id}/{lab_id}/pdf")
def download_lab_report_pdf(patient_id: str, lab_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    bundle = batch_engine.patient_bundles[patient_id]
    target_report = None
    for r in bundle["lab_reports"]:
        if r.id == lab_id:
            target_report = r
            break
            
    if not target_report:
        raise HTTPException(status_code=404, detail="Lab report not found")
        
    pdf_bytes = PdfGeneratorService.generate_lab_report_pdf(bundle["patient"], target_report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={lab_id}.pdf"}
    )

@router.get("/{patient_id}/{lab_id}/fhir")
def get_lab_fhir_bundle(patient_id: str, lab_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    bundle = batch_engine.patient_bundles[patient_id]
    target_report = None
    for r in bundle["lab_reports"]:
        if r.id == lab_id:
            target_report = r
            break
            
    if not target_report:
        raise HTTPException(status_code=404, detail="Lab report not found")
        
    fhir_bundle = FhirExporter.generate_diagnostic_report_bundle(bundle["patient"], target_report)
    return fhir_bundle
