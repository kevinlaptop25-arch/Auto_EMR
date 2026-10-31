import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

from app.core.batch_generator import batch_engine
from app.core.timeline_simulator import timeline_manager

router = APIRouter(prefix="/pacs", tags=["PACS Radiology"])

SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "pacs_samples"))

@router.get("/study/{patient_id}")
def get_radiology_study(patient_id: str):
    if patient_id not in batch_engine.patient_bundles:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    filtered = timeline_manager.filter_bundle(batch_engine.patient_bundles[patient_id])
    study = filtered.get("radiology_study")
    if not study:
        return {"has_study": False, "study": None}
    return {"has_study": True, "study": study}

@router.get("/images/{image_name}")
def get_radiology_image(image_name: str):
    # Map profile images to generated textures
    if "copd" in image_name.lower() or "chest" in image_name.lower() or "pneumonia" in image_name.lower():
        file_path = os.path.join(SAMPLE_DIR, "chest_xray.png")
    else:
        file_path = os.path.join(SAMPLE_DIR, "spine_mri.png")
        
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
        
    return FileResponse(file_path, media_type="image/png")
