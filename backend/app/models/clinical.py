from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class OpdSlip(BaseModel):
    patient_id: str
    form_code: str = "FORM F/EPH/OPD/01"
    opd_number: str
    consultation_timestamp: datetime
    department: str
    unit: str = "Unit-I"
    attending_doctor: str
    doctor_reg_no: str
    
    # 6-7 Standard Hospital Headings:
    actual_problem: List[str]            # Heading 1: Actual Problem / Chief Complaints
    history_presenting_illness: str     # Heading 2: History of Presenting Illness
    past_history: Dict[str, str] = {    # Heading 3: Past History
        "diabetes_mellitus": "No",
        "hypertension": "No",
        "tuberculosis": "No",
        "asthma": "No",
        "ihd": "No",
        "surgical_history": "None"
    }
    recent_medication: List[str] = ["None / Paracetamol 500mg SOS"] # Heading 4: Recent Medication
    allergies: str = "No Known Drug Allergies (NKDA)"
    clinical_findings: Dict[str, Any]   # Heading 5: Findings (Vitals & Physical Exam)
    provisional_diagnosis: str          # Heading 6: Diagnosis (ICD-10 bound)
    icd10_code: str
    treatment_advised: List[str]        # Prescriptions & Dosage
    investigations_ordered: List[str] = ["Routine CBC", "RFT"]
    conclusion_remarks: str             # Heading 7: Final Conclusion Remarks & Further Proceeding
    proceeding_action: str = "ADMIT_TO_IPD" # "ADMIT_TO_IPD", "DAY_CARE", "OPD_HOME_CARE", "SCHEDULE_OT"
    next_review_date: Optional[str] = None

class HistoryAndPhysical(BaseModel):
    patient_id: str
    form_code: str = "F/EPH/MRD/39"
    admission_timestamp: datetime
    doctor_unit: str
    source_informant: str = "Self (Reliable)"
    
    chief_complaints: List[str]
    history_presenting_illness: str
    
    past_history: Dict[str, str] = {
        "diabetes_mellitus": "No",
        "hypertension": "No",
        "tuberculosis": "No",
        "asthma": "No",
        "ihd": "No",
        "surgical_history": "None"
    }
    family_history: str = "No significant family history"
    personal_history: Dict[str, str] = {
        "diet": "Mixed",
        "appetite": "Normal",
        "sleep": "Adequate",
        "bowel_bladder": "Regular",
        "habits": "Non-smoker, non-alcoholic"
    }
    drug_allergies: str = "No known drug allergies (NKDA)"
    obstetric_history: Optional[str] = None
    
    general_exam: Dict[str, str] = {
        "weight_kg": "62",
        "height_cm": "165",
        "temperature_f": "98.4",
        "pulse_bpm": "78",
        "respiration_cpm": "18",
        "bp_mmhg": "120/80",
        "spo2_percent": "98",
        "pallor": "Absent",
        "edema": "Absent",
        "icterus": "Absent",
        "cyanosis": "Absent",
        "clubbing": "Absent",
        "lymphadenopathy": "Absent"
    }
    
    systemic_exam: Dict[str, str] = {
        "cardiovascular": "S1 S2 heard, no murmurs",
        "respiratory": "Bilateral normal vesicular breath sounds (NVBS), clear",
        "abdomen": "Soft, non-tender, no organomegaly, bowel sounds present",
        "cns": "Conscious, alert, oriented to time/place/person, no focal neurological deficit"
    }
    
    local_exam: Optional[str] = "No focal abnormality"
    provisional_diagnosis: str
    icd10_code: str
    care_plan_investigations: List[str]
    care_plan_treatment: List[str]
    consultant_name: str
    consultant_reg: str


class ProgressNote(BaseModel):
    id: str
    patient_id: str
    form_code: str = "F/MRD/EPH/40"
    timestamp: datetime
    round_label: str  # e.g. "C/S/B GM-I (Morning Rounds)"
    clinical_narrative: str
    vitals: Dict[str, str]  # BP, PR, RR, SpO2, Temp, GRBS
    systemic_notes: Dict[str, str]
    prescriptions_ordered: List[str]
    lab_radiology_orders: List[str]
    attending_doctor: str
    doctor_reg_no: str
    signed: bool = True


class MedicationAdministration(BaseModel):
    patient_id: str
    form_code: str = "F/EPH/MRD/58"
    drug_name: str
    dosage: str
    route: str  # "Oral", "IV", "SC", "Nebulization"
    frequency: str  # "1-0-1", "1-1-1", "1-0-0", "0-1-0", "SOS"
    start_date: str
    slots: Dict[str, str] = Field(
        default_factory=lambda: {
            "06:00": "SN",
            "10:00": "SN",
            "14:00": "RJ",
            "18:00": "RJ",
            "22:00": "MP"
        }
    )


class DiabeticChartEntry(BaseModel):
    id: str
    patient_id: str
    form_code: str = "F/EPH/MRD/54"
    timestamp: datetime
    blood_sugar_grbs: int  # mg/dL
    sugar_type: str = "GRBS"  # FBS, PPBS, RBS, GRBS
    urine_sugar: str = "Nil"
    urine_ketone: str = "Negative"
    insulin_medication: Optional[str] = None  # "Inj H. Actrapid"
    dose_units: Optional[int] = None
    route: str = "Subcutaneous"
    nurse_signature: str = "Nurse Priya (Reg: 4892)"


class TPRReading(BaseModel):
    timestamp: datetime
    day_no: int
    slot_label: str  # "02:00", "06:00", "10:00", "14:00", "18:00", "22:00"
    temp_f: float
    pulse_bpm: int
    resp_cpm: int
    stool: str = "Passed"
    urine: str = "Voided"
    sputum: str = "-"
    bath: str = "Given"


class GraphicTPRChart(BaseModel):
    patient_id: str
    form_code: str = "F/MRD/EPH/07"
    readings: List[TPRReading]


class DischargeSummary(BaseModel):
    patient_id: str
    form_code: str = "EPH/DISCHARGE/01"
    discharge_timestamp: datetime
    final_diagnosis: str
    icd10_code: str
    secondary_diagnoses: List[str] = []
    procedures_done: List[str] = []
    clinical_summary_course: str
    condition_at_discharge: str = "Recovered / Hemodynamically Stable"
    discharge_vitals: Dict[str, str]
    medications_prescribed: List[str]
    diet_lifestyle_advice: str
    follow_up_date: str
    attending_consultant: str
    consultant_reg: str
