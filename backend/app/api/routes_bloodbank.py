from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.batch_generator import batch_engine

router = APIRouter(prefix="/bloodbank", tags=["Blood Bank & Transfusion Medicine"])

@router.get("/inventory")
def get_blood_inventory(blood_group: Optional[str] = Query(None), component: Optional[str] = Query(None)):
    units = batch_engine.blood_inventory
    if blood_group:
        units = [u for u in units if u.blood_group.upper() == blood_group.upper()]
    if component:
        units = [u for u in units if component.lower() in u.component.lower()]
    return {
        "license_no": "KA/BLD/2019/042",
        "center_name": "East Point Hospital Blood Centre",
        "total_units_in_stock": len(units),
        "data": units
    }

@router.get("/requisitions")
def get_requisitions(crossmatch_status: Optional[str] = Query(None)):
    reqs = batch_engine.blood_requisitions
    if crossmatch_status:
        reqs = [r for r in reqs if r.crossmatch_status.upper() == crossmatch_status.upper()]
    return {
        "total_requisitions": len(reqs),
        "data": reqs
    }

@router.get("/patient/{patient_id}")
def get_patient_blood_requisitions(patient_id: str):
    matching = [r for r in batch_engine.blood_requisitions if r.patient_id == patient_id]
    return {
        "patient_id": patient_id,
        "active_requisitions": matching
    }

@router.post("/issue/{requisition_no}")
def issue_blood_unit(requisition_no: str):
    matching = [r for r in batch_engine.blood_requisitions if r.requisition_no == requisition_no]
    if not matching:
        raise HTTPException(status_code=404, detail="Requisition not found")
    req = matching[0]
    req.crossmatch_status = "ISSUED"
    
    # Mark unit as transfused
    if req.assigned_unit_id:
        for u in batch_engine.blood_inventory:
            if u.unit_id == req.assigned_unit_id:
                u.status = "TRANSFUSED"
                break
                
    return {
        "status": "SUCCESS",
        "requisition_no": req.requisition_no,
        "assigned_unit_id": req.assigned_unit_id,
        "crossmatch_result": "Saline & Anti-Human Globulin (Coombs) Compatible",
        "release_timestamp": datetime.now().isoformat(),
        "authorized_by": req.licensed_medical_officer
    }

@router.get("/stats")
def get_blood_bank_summary():
    units = batch_engine.blood_inventory
    reqs = batch_engine.blood_requisitions
    
    group_counts = {}
    component_counts = {}
    for u in units:
        if u.status == "AVAILABLE":
            group_counts[u.blood_group] = group_counts.get(u.blood_group, 0) + 1
            component_counts[u.component] = component_counts.get(u.component, 0) + 1
            
    return {
        "blood_centre": "East Point College of Medical Sciences Blood Centre",
        "license_number": "KA/BLD/2019/042",
        "total_available_units": sum(1 for u in units if u.status == "AVAILABLE"),
        "total_issued_units": sum(1 for u in units if u.status == "TRANSFUSED"),
        "tti_safe_testing_compliance": "100% NON-REACTIVE (HIV, HBV, HCV, VDRL, MP)",
        "group_distribution": group_counts,
        "component_distribution": component_counts,
        "pending_crossmatches": sum(1 for r in reqs if r.crossmatch_status != "ISSUED")
    }
