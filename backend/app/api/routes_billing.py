from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.batch_generator import batch_engine

router = APIRouter(prefix="/billing", tags=["Billing & Cashier Desk"])

@router.get("/invoices")
def get_invoices(
    encounter_type: Optional[str] = Query(None, description="OPD or IPD"),
    payment_status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200)
):
    inv_list = list(batch_engine.billing_invoices.values())
    if encounter_type:
        inv_list = [i for i in inv_list if i.encounter_type.upper() == encounter_type.upper()]
    if payment_status:
        inv_list = [i for i in inv_list if i.payment_status.upper() == payment_status.upper()]
        
    return {
        "total_invoices": len(batch_engine.billing_invoices),
        "returned": len(inv_list[:limit]),
        "data": inv_list[:limit]
    }

@router.get("/patient/{patient_id}")
def get_patient_invoice(patient_id: str):
    if patient_id not in batch_engine.billing_invoices:
        if patient_id in batch_engine.patients_db:
            pt = batch_engine.patients_db[patient_id]
            bundle = batch_engine.patient_bundles.get(patient_id, {})
            batch_engine._create_billing_invoice(pt, bundle, is_ipd=bool(pt.ip_no))
            return batch_engine.billing_invoices[patient_id]
        raise HTTPException(status_code=404, detail="Billing record not found for patient")
    return batch_engine.billing_invoices[patient_id]

@router.post("/settle/{invoice_no}")
def settle_invoice_payment(invoice_no: str, payment_mode: str = Query("UPI")):
    matching = [i for i in batch_engine.billing_invoices.values() if i.invoice_no == invoice_no]
    if not matching:
        raise HTTPException(status_code=404, detail="Invoice not found")
    inv = matching[0]
    inv.paid_amount_inr = inv.net_payable_inr
    inv.balance_due_inr = 0.0
    inv.payment_status = "PAID"
    inv.payment_mode = payment_mode
    return {
        "status": "SUCCESS",
        "invoice_no": inv.invoice_no,
        "receipt_no": inv.receipt_no,
        "paid_amount_inr": inv.paid_amount_inr,
        "payment_status": inv.payment_status,
        "payment_mode": inv.payment_mode
    }

@router.get("/stats")
def get_billing_financial_summary():
    invoices = list(batch_engine.billing_invoices.values())
    total_gross = sum(i.gross_total_inr for i in invoices)
    total_concessions = sum(i.scheme_discount_inr for i in invoices)
    total_net = sum(i.net_payable_inr for i in invoices)
    total_collected = sum(i.paid_amount_inr for i in invoices)
    pmjay_count = sum(1 for i in invoices if i.payer_scheme.startswith("Ayushman"))
    cashless_count = sum(1 for i in invoices if i.payer_scheme.startswith("AB-ARK"))
    cash_count = len(invoices) - pmjay_count - cashless_count

    return {
        "total_invoices_generated": len(invoices),
        "gross_billing_inr": round(total_gross, 2),
        "government_scheme_subsidy_inr": round(total_concessions, 2),
        "net_revenue_inr": round(total_net, 2),
        "actual_collections_inr": round(total_collected, 2),
        "scheme_breakdown": {
            "ayushman_bharat_pmjay": pmjay_count,
            "ab_ark_cashless_insurance": cashless_count,
            "direct_cash_upi": cash_count
        }
    }
