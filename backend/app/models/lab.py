from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class LabTestItem(BaseModel):
    name: str
    result_value: str
    unit: str
    reference_range: str
    flag: Optional[str] = "NORMAL"  # "HIGH", "LOW", "NORMAL", "CRITICAL", "POSITIVE", "NEGATIVE"

class LabReport(BaseModel):
    id: str
    patient_id: str
    department: str  # "Biochemistry", "Microbiology", "Pathology"
    sample_id: str
    sample_type: str  # "Serum", "Whole Blood (EDTA)", "Sputum", "Midstream Urine"
    collected_at: datetime
    reported_at: datetime
    test_category: str  # e.g., "Complete Blood Count", "Liver Function Test", "Truenat TB"
    items: List[LabTestItem]
    clinical_impression: Optional[str] = None
    pathologist_name: str = "Dr. Manjula G (MD Pathologist)"
    pathologist_reg: str = "KMC: 142851"
    status: str = "FINAL_VERIFIED"
