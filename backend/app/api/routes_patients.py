from fastapi import APIRouter, Query, HTTPException, Response
from typing import Optional, List, Dict, Any

from app.core.batch_generator import batch_engine
from app.core.timeline_simulator import timeline_manager
from app.core.clinical_engine import ClinicalEngine

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("")
def get_patients(
    filter_type: str = Query("ALL", description="ALL, IPD, or OPD"),
    department: Optional[str] = Query(None, description="Department name"),
    search: Optional[str] = Query(None, description="Search by name, MR No or IP No"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    patients = batch_engine.list_patients(
        filter_type=filter_type,
        department=department,
        search_query=search,
        limit=limit,
        offset=offset
    )
    total_count = len(batch_engine.patients_db)
    return {
        "total_records": total_count,
        "returned": len(patients),
        "limit": limit,
        "offset": offset,
        "data": patients
    }

@router.get("/{patient_id}")
def get_patient_detail(patient_id: str, preset: Optional[str] = Query(None)):
    if preset:
        timeline_manager.set_demo_preset(preset)
        
    if patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient = batch_engine.patients_db[patient_id]
    bundle = batch_engine.patient_bundles.get(patient_id)
    
    if bundle:
        filtered_bundle = timeline_manager.filter_bundle(bundle)
        return filtered_bundle
    
    # OPD Patient: return patient with their generated OPD slip
    opd_slip = batch_engine.opd_slips.get(patient_id)
    if not opd_slip:
        opd_slip = ClinicalEngine.generate_opd_slip(patient)
        batch_engine.opd_slips[patient_id] = opd_slip

    return {
        "patient": patient,
        "admitted": False,
        "opd_slip": opd_slip,
        "progress_notes": [],
        "lab_reports": [],
        "radiology_study": None,
        "medication_sheets": [],
        "diabetic_entries": [],
        "tpr_chart": {"patient_id": patient.id, "readings": []},
        "discharge_summary": None,
        "status_at_timestamp": "OPD"
    }
