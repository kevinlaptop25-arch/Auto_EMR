from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.batch_generator import batch_engine
from app.models.emergency import EmergencyEncounter

router = APIRouter(prefix="/emergency", tags=["Emergency Care & Triage"])

@router.get("/encounters")
def get_emergency_encounters(
    triage_filter: Optional[str] = Query(None, description="RED, YELLOW, or GREEN"),
    mlc_only: bool = Query(False)
):
    encounters = list(batch_engine.emergency_encounters.values())
    
    if triage_filter:
        encounters = [e for e in encounters if e.triage_level.upper() == triage_filter.upper()]
        
    if mlc_only:
        encounters = [e for e in encounters if e.is_mlc]
        
    # Sort with RED first, then arrival time
    priority_map = {"RED": 1, "YELLOW": 2, "GREEN": 3}
    encounters.sort(key=lambda x: (priority_map.get(x.triage_level, 4), x.arrival_time))
    
    return {
        "total_active_er": len(encounters),
        "red_priority_count": sum(1 for e in encounters if e.triage_level == "RED"),
        "yellow_priority_count": sum(1 for e in encounters if e.triage_level == "YELLOW"),
        "green_priority_count": sum(1 for e in encounters if e.triage_level == "GREEN"),
        "mlc_count": sum(1 for e in encounters if e.is_mlc),
        "data": encounters
    }

@router.get("/patient/{patient_id}")
def get_patient_emergency_record(patient_id: str):
    if patient_id not in batch_engine.emergency_encounters:
        raise HTTPException(status_code=404, detail="No Emergency encounter found for this patient")
    return batch_engine.emergency_encounters[patient_id]

@router.post("/triage")
def register_emergency_arrival(payload: Dict[str, Any] = Body(...)):
    patient_id = payload.get("patient_id")
    if not patient_id or patient_id not in batch_engine.patients_db:
        raise HTTPException(status_code=400, detail="Invalid patient_id")
        
    pt = batch_engine.patients_db[patient_id]
    er_id = f"ER-2026-{1000 + len(batch_engine.emergency_encounters) + 1}"
    
    triage_level = payload.get("triage_level", "YELLOW")
    enc = EmergencyEncounter(
        id=er_id,
        patient_id=pt.id,
        patient_name=pt.name,
        age=pt.age,
        gender=pt.gender,
        arrival_time=datetime.now(),
        brought_by=payload.get("brought_by", "108 Emergency Ambulance"),
        triage_level=triage_level,
        triage_score=payload.get("triage_score", "ESI-2"),
        chief_complaint=payload.get("chief_complaint", "Acute clinical distress"),
        vitals=payload.get("vitals", {"BP": "120/80", "PR": "92 bpm", "RR": "20 cpm", "SpO2": "97%"}),
        gcs_score=payload.get("gcs_score", "15/15"),
        is_mlc=payload.get("is_mlc", False),
        mlc_no=f"MLC-2026-{len(batch_engine.emergency_encounters) + 100}" if payload.get("is_mlc") else None,
        police_station="Avalahalli Police Station, Bangalore East" if payload.get("is_mlc") else None,
        injury_nature=payload.get("injury_nature"),
        alcohol_influence=payload.get("alcohol_influence", False),
        attending_er_physician="Dr. K. N. Rajesh",
        physician_reg_no="KMC: 64920",
        emergency_interventions=payload.get("emergency_interventions", ["Vitals monitoring", "IV access secured"]),
        crash_cart_activated=(triage_level == "RED"),
        disposition=payload.get("disposition", "ADMITTED_WARD"),
        disposition_ward=payload.get("disposition_ward", f"{pt.department.upper()} WARD"),
        er_status="STABILIZED" if triage_level != "RED" else "ACTIVE_RESUSCITATION"
    )
    batch_engine.emergency_encounters[pt.id] = enc
    return {"status": "SUCCESS", "encounter": enc}

@router.post("/{er_id}/admit-icu")
def fast_track_icu_admission(er_id: str):
    matching = [e for e in batch_engine.emergency_encounters.values() if e.id == er_id]
    if not matching:
        raise HTTPException(status_code=404, detail="ER encounter not found")
    enc = matching[0]
    enc.disposition = "ADMITTED_ICU"
    enc.disposition_ward = "MULTIDISCIPLINARY ICU Bed 03"
    enc.er_status = "DISPOSED"
    return {"status": "SUCCESS", "disposition": enc.disposition, "ward": enc.disposition_ward}
