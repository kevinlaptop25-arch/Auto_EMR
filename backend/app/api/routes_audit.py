from fastapi import APIRouter, Query, Body
from typing import Dict, Any, Optional
from datetime import datetime

from app.core.timeline_simulator import timeline_manager
from app.core.batch_generator import batch_engine

router = APIRouter(prefix="/audit", tags=["NMC Audit & Timeline Logic"])

@router.get("/timeline")
def get_timeline_status():
    curr = timeline_manager.get_current_time()
    return {
        "simulated_time": curr.isoformat(),
        "display_time": curr.strftime("%d-%b-%Y %I:%M:%S %p"),
        "hour_minute": curr.strftime("%H:%M"),
        "active_preset": timeline_manager.get_active_preset()
    }

@router.post("/timeline/set-preset")
def set_timeline_preset(preset: str = Query(..., description="MORNING_ADMISSION, ROUNDS_10AM, INSPECTION_1PM, AFTERNOON_4PM, EVENING_ROUNDS_7PM, DAY2_COMORBIDITY, DAY3_LIAISON, DISCHARGE_READY")):
    new_time = timeline_manager.set_demo_preset(preset)
    return {
        "status": "UPDATED",
        "preset": preset,
        "active_preset": preset,
        "new_simulated_time": new_time.isoformat(),
        "display_time": new_time.strftime("%d-%b-%Y %I:%M %p"),
        "audit_note": f"System timeline set to {new_time.strftime('%I:%M %p')}. Any progress notes or discharges after this timestamp will be strictly suppressed."
    }

@router.post("/timeline/set-custom")
def set_custom_time(iso_time_string: str = Body(..., embed=True)):
    dt = datetime.fromisoformat(iso_time_string)
    timeline_manager.set_simulated_time(dt)
    return {
        "status": "UPDATED",
        "new_simulated_time": dt.isoformat(),
        "display_time": dt.strftime("%d-%b-%Y %I:%M %p")
    }

from app.core.clinical_engine import CENTRAL_WORKFLOWS, ALLIED_SUPER_SPECIALTY

@router.post("/generate-batch")
def trigger_batch_generation(count: int = Query(2800, ge=50, le=4000)):
    result = batch_engine.generate_batch(count=count, simulated_time=timeline_manager.get_current_time())
    return result

@router.get("/stats")
def get_audit_summary():
    total_pts = len(batch_engine.patients_db)
    ipd_pts = [p for p in batch_engine.patients_db.values() if p.ip_no is not None]
    opd_pts = [p for p in batch_engine.patients_db.values() if p.ip_no is None]
    
    # Department distribution across 21 departments
    dept_distribution = {}
    central_count = 0
    allied_count = 0
    for p in batch_engine.patients_db.values():
        dept_distribution[p.department] = dept_distribution.get(p.department, 0) + 1
        if p.department in CENTRAL_WORKFLOWS:
            central_count += 1
        else:
            allied_count += 1
        
    curr_time = timeline_manager.get_current_time()
    
    # ABHA Metrics (30% to 35% compliance target)
    abha_count = sum(1 for p in batch_engine.patients_db.values() if p.abha_verified)
    abha_pct = round((abha_count / float(total_pts)) * 100, 1) if total_pts > 0 else 0.0
    
    return {
        "nmc_audit_year": 2026,
        "college_name": "East Point College of Medical Sciences & Research Centre",
        "total_footfall": total_pts,
        "opd_footfall": len(opd_pts),
        "target_opd": 2600,
        "ipd_admissions": len(ipd_pts),
        "target_ipd": 200,
        "bed_occupancy_rate": f"{min(95, round((len(ipd_pts) / 220.0) * 100, 1))}%",
        "quota_requirement": 2800,
        "quota_status": "COMPLIANT" if total_pts >= 2800 else "PARTIAL",
        "department_count": len(dept_distribution),
        "central_workflows": CENTRAL_WORKFLOWS,
        "central_encounters_count": central_count,
        "allied_super_specialty": ALLIED_SUPER_SPECIALTY,
        "allied_encounters_count": allied_count,
        "department_distribution": dept_distribution,
        "abha_verified_count": abha_count,
        "abha_percentage": f"{abha_pct}%",
        "abha_target_met": (30.0 <= abha_pct <= 36.0),
        "modules_active": {
            "emergency_care_encounters": len(batch_engine.emergency_encounters),
            "pharmacy_dispensation_orders": len(batch_engine.pharmacy_dispensations),
            "billing_encounter_invoices": len(batch_engine.billing_invoices),
            "blood_bank_licensed_units": len(batch_engine.blood_inventory),
            "blood_requisitions_active": len(batch_engine.blood_requisitions)
        },
        "simulated_audit_timestamp": curr_time.strftime("%d-%b-%Y %I:%M %p")
    }
