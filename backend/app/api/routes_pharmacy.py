from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.batch_generator import batch_engine

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy & Dispensation"])

@router.get("/inventory")
def get_pharmacy_inventory(category: Optional[str] = Query(None)):
    items = batch_engine.pharmacy_inventory
    if category:
        items = [i for i in items if category.lower() in i.category.lower()]
    return {
        "total_sku_count": len(items),
        "low_stock_count": sum(1 for i in items if i.stock_quantity <= i.reorder_level),
        "narcotic_count": sum(1 for i in items if i.is_narcotic),
        "data": items
    }

@router.get("/dispensations")
def get_dispensations(
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200)
):
    disp_list = list(batch_engine.pharmacy_dispensations.values())
    if status:
        disp_list = [d for d in disp_list if d.dispensation_status.lower() == status.lower()]
    return {
        "total_dispensations": len(batch_engine.pharmacy_dispensations),
        "returned": len(disp_list[:limit]),
        "data": disp_list[:limit]
    }

@router.get("/patient/{patient_id}")
def get_patient_pharmacy(patient_id: str):
    if patient_id not in batch_engine.pharmacy_dispensations:
        # If no dispensation generated yet, generate one on the fly from patient's orders
        if patient_id in batch_engine.patients_db:
            pt = batch_engine.patients_db[patient_id]
            bundle = batch_engine.patient_bundles.get(patient_id, {})
            batch_engine._create_pharmacy_dispensation(pt, bundle, is_ipd=bool(pt.ip_no))
            return batch_engine.pharmacy_dispensations[patient_id]
        raise HTTPException(status_code=404, detail="Patient pharmacy order not found")
    return batch_engine.pharmacy_dispensations[patient_id]

@router.post("/dispense/{disp_id}")
def execute_dispensation(disp_id: str):
    matching = [d for d in batch_engine.pharmacy_dispensations.values() if d.id == disp_id]
    if not matching:
        raise HTTPException(status_code=404, detail="Dispensation order not found")
    disp = matching[0]
    disp.dispensation_status = "DISPENSED"
    disp.dispensed_at = datetime.now()
    
    # Deduct stock for each dispensed item
    for item in disp.items:
        item.status = "DISPENSED"
        for inv in batch_engine.pharmacy_inventory:
            if inv.drug_name == item.drug_name:
                inv.stock_quantity = max(0, inv.stock_quantity - item.quantity_prescribed)
                break
                
    return {
        "status": "SUCCESS",
        "dispensation_id": disp.id,
        "dispensed_at": disp.dispensed_at.isoformat(),
        "pharmacist": disp.pharmacist_name,
        "items_dispensed": len(disp.items)
    }

@router.get("/narcotics")
def get_narcotic_schedule_x_register():
    narcotics = [i for i in batch_engine.pharmacy_inventory if i.is_narcotic]
    return {
        "register_title": "Schedule X Controlled Substance Register - Form F/EPH/PHARM/NAR-01",
        "audit_standard": "Drugs and Cosmetics Rules 1945 & NDPS Act",
        "authorized_pharmacist": "Shrikanth Joshi, B.Pharm (KSPC: 48912)",
        "double_witness_verified": True,
        "controlled_items": narcotics
    }
