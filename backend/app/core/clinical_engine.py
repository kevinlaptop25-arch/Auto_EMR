import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from app.models.patient import Patient
from app.models.clinical import (
    HistoryAndPhysical, ProgressNote, MedicationAdministration,
    DiabeticChartEntry, TPRReading, GraphicTPRChart, DischargeSummary,
    OpdSlip
)
from app.models.lab import LabReport, LabTestItem
from app.models.radiology import RadiologyStudy, DicomInstance

# Standard East Point Hospital Doctor Register (Faculty & Consultants)
EAST_POINT_DOCTORS = [
    {"name": "Dr. B. R. Ramachandra", "reg": "KMC: 45210", "dept": "General Medicine", "designation": "Professor & HOD"},
    {"name": "Dr. Nihal Sahgal", "reg": "KMC: 174958", "dept": "General Medicine", "designation": "Associate Professor"},
    {"name": "Dr. Chinmay M", "reg": "KMC: 168404", "dept": "General Medicine", "designation": "Assistant Professor"},
    {"name": "Dr. Prathap Tulasiram R", "reg": "KMC: 131239", "dept": "General Medicine", "designation": "Senior Resident"},
    {"name": "Dr. Shanthi Priya T. Reddy", "reg": "KMC: 135306", "dept": "Obstetrics & Gynaecology", "designation": "Professor & Consultant"},
    {"name": "Dr. Yashshree Shah", "reg": "KMC: 199591", "dept": "Obstetrics & Gynaecology", "designation": "Senior Resident"},
    {"name": "Dr. Gayatri Devi H.J.", "reg": "KMC: 18769", "dept": "Respiratory Medicine", "designation": "Professor & HOD"},
    {"name": "Dr. Mahapara Mushtaq", "reg": "KMC: 161375", "dept": "Respiratory Medicine", "designation": "Senior Resident"},
    {"name": "Dr. Abhijit M.G.", "reg": "KMC: 57139", "dept": "General Surgery", "designation": "Professor & Surgeon"},
    {"name": "Dr. Omkar V", "reg": "KMC: 154210", "dept": "Orthopedics", "designation": "Associate Professor"},
    {"name": "Dr. Tarun Kumar", "reg": "KMC: 148920", "dept": "Orthopedics", "designation": "Assistant Professor"},
    {"name": "Dr. R.M. Laxmi Priya", "reg": "KMC: 128941", "dept": "Ophthalmology", "designation": "Consultant"},
    {"name": "Dr. C. K. Narayana Swamy", "reg": "KMC: 39812", "dept": "Pediatrics", "designation": "Professor & HOD"},
    {"name": "Dr. Harish Kumar M", "reg": "KMC: 112048", "dept": "ENT (Otorhinolaryngology)", "designation": "Associate Professor"},
    {"name": "Dr. Archana Bhat", "reg": "KMC: 98412", "dept": "Dermatology, Venereology & Leprosy", "designation": "Associate Professor"},
    {"name": "Dr. Srinivas Prasad", "reg": "KMC: 76391", "dept": "Psychiatry", "designation": "Consultant"},
    {"name": "Dr. K. N. Rajesh", "reg": "KMC: 64920", "dept": "Emergency Medicine", "designation": "Head of Emergency & Trauma"},
    {"name": "Dr. V. Ravikumar", "reg": "KMC: 58210", "dept": "Anaesthesiology & Critical Care", "designation": "Chief Anaesthesiologist"},
    {"name": "Dr. Jayashree K", "reg": "KMC: 73940", "dept": "Radiodiagnosis", "designation": "Chief Radiologist"},
    {"name": "Dr. Manjula Swamy", "reg": "KMC: 52190", "dept": "Pathology & Transfusion Medicine", "designation": "Blood Centre In-Charge"},
    {"name": "Dr. Anand Murthy", "reg": "KMC: 61840", "dept": "Cardiology", "designation": "Consultant Cardiologist"},
    {"name": "Dr. Venugopal S", "reg": "KMC: 88192", "dept": "Neurology", "designation": "Consultant Neurologist"},
    {"name": "Dr. S. K. Rao", "reg": "KMC: 115403", "dept": "Neurology", "designation": "Consultant Neurosurgeon"},
    {"name": "Dr. R. Prabhakar", "reg": "KMC: 71203", "dept": "Nephrology", "designation": "Consultant Nephrologist"},
    {"name": "Dr. Sudheer Reddy", "reg": "KMC: 93412", "dept": "Gastroenterology", "designation": "Consultant Gastroenterologist"},
    {"name": "Dr. Vinayaka B", "reg": "KMC: 104521", "dept": "Urology", "designation": "Consultant Urologist"},
    {"name": "Dr. Deepthi Rao", "reg": "KMC: 119830", "dept": "Plastic Surgery", "designation": "Consultant Plastic Surgeon"},
    {"name": "Dr. Sandeep Hegde", "reg": "KMC: 84310", "dept": "Dentistry & Maxillofacial", "designation": "Maxillofacial Surgeon"}
]

# 14 Central Clinical Workflows (Core NMC Undergraduate & Post-Graduate Training Departments)
CENTRAL_WORKFLOWS = [
    "General Medicine",
    "General Surgery",
    "Obstetrics & Gynaecology",
    "Pediatrics",
    "Orthopedics",
    "Respiratory Medicine",
    "Emergency Medicine",
    "Dermatology, Venereology & Leprosy",
    "Psychiatry",
    "Ophthalmology",
    "ENT (Otorhinolaryngology)",
    "Anaesthesiology & Critical Care",
    "Radiodiagnosis",
    "Pathology & Transfusion Medicine"
]

# 7 Allied & Super-Specialty Workflows
ALLIED_SUPER_SPECIALTY = [
    "Cardiology",
    "Neurology",
    "Nephrology",
    "Gastroenterology",
    "Urology",
    "Plastic Surgery",
    "Dentistry & Maxillofacial"
]

# All 21 Standardized Hospital Departments
DEPARTMENTS = CENTRAL_WORKFLOWS + ALLIED_SUPER_SPECIALTY

# Strict Clinical Condition Blueprints
CLINICAL_PROFILES = {
    "MALARIA_PV": {
        "disease_name": "Plasmodium Vivax Malaria",
        "icd10": "B51.9",
        "department": "General Medicine",
        "multi_icd_progression": True,
        "chief_complaints": [
            "c/o High grade fever with chills and rigors x 4 days",
            "c/o Severe generalized headache and bodyache x 3 days",
            "c/o Nausea and 3 episodes of non-bilious vomiting x 2 days"
        ],
        "hpi": "Patient was apparently well 4 days ago when they developed intermittent high-grade fever associated with chills and rigors, peaking during afternoon/evening hours. Followed by drenching sweats. Associated with severe myalgia and anorexia. No history of cough, dysuria, or altered sensorium.",
        "vitals_admission": {"bp": "110/70", "pr": "116", "rr": "20", "temp": "103.2", "spo2": "98", "grbs": "104"},
        "exam_admission": {
            "pallor": "Present (+)", "icterus": "Mild (+)", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, tachycardic, no murmurs",
            "rs": "NVBS bilaterally, chest clear",
            "abdomen": "Mild splenomegaly (palpable 2cm below left costal margin), soft, non-tender",
            "cns": "Conscious, oriented, no meningeal signs"
        },
        "pathology": {
            "category": "Complete Blood Count & Smear",
            "items": [
                {"name": "Hemoglobin", "result_value": "9.4", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "LOW"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "4100", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "52000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "CRITICAL"},
                {"name": "Hematocrit (PCV)", "result_value": "29.2", "unit": "%", "reference_range": "40.0 - 50.0", "flag": "LOW"},
                {"name": "ESR (Westergren)", "result_value": "48", "unit": "mm/1st hr", "reference_range": "0 - 15", "flag": "HIGH"},
                {"name": "Peripheral Smear Examination", "result_value": "Schizonts & ring trophozoites of Plasmodium vivax seen. Thrombocytopenia confirmed.", "unit": "-", "reference_range": "No hemoparasites", "flag": "POSITIVE"}
            ]
        },
        "microbiology": {
            "category": "Malaria Rapid Diagnostic Card Test (RDT) & Viral Serology",
            "items": [
                {"name": "Malaria Pan-LDH / Pv-LDH", "result_value": "POSITIVE for Plasmodium vivax", "unit": "-", "reference_range": "Negative", "flag": "POSITIVE"},
                {"name": "Malaria Pf-HRP2", "result_value": "NEGATIVE for Plasmodium falciparum", "unit": "-", "reference_range": "Negative", "flag": "NEGATIVE"},
                {"name": "HBsAg (Surface Antigen Rapid)", "result_value": "REACTIVE (Positive)", "unit": "-", "reference_range": "Non-Reactive", "flag": "POSITIVE"},
                {"name": "Dengue NS1 Antigen", "result_value": "Negative", "unit": "-", "reference_range": "Negative", "flag": "NORMAL"},
                {"name": "Widal Slide Agglutination", "result_value": "TO < 1:80, TH < 1:80 (Negative)", "unit": "-", "reference_range": "Titre < 1:80", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Metabolic, Liver & Renal Profile",
            "items": [
                {"name": "Random Blood Glucose (GRBS)", "result_value": "326", "unit": "mg/dL", "reference_range": "70 - 140", "flag": "CRITICAL"},
                {"name": "HbA1c (Glycated Hemoglobin)", "result_value": "11.2", "unit": "%", "reference_range": "< 5.7", "flag": "HIGH"},
                {"name": "Total Bilirubin", "result_value": "3.2", "unit": "mg/dL", "reference_range": "0.2 - 1.2", "flag": "HIGH"},
                {"name": "Direct Bilirubin", "result_value": "1.2", "unit": "mg/dL", "reference_range": "0.0 - 0.3", "flag": "HIGH"},
                {"name": "Indirect Bilirubin", "result_value": "2.0", "unit": "mg/dL", "reference_range": "0.1 - 0.8", "flag": "HIGH"},
                {"name": "SGOT (AST)", "result_value": "148", "unit": "U/L", "reference_range": "10 - 40", "flag": "HIGH"},
                {"name": "SGPT (ALT)", "result_value": "152", "unit": "U/L", "reference_range": "10 - 45", "flag": "HIGH"},
                {"name": "Blood Urea", "result_value": "28", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.9", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"}
            ]
        },
        "medications_inpatient": [
            "Inj Artesunate 120mg IV at 0, 12, 24 hrs then OD",
            "Tab Primaquine 15mg 1-0-0 x 14 days (G6PD verified normal)",
            "Inj Human Actrapid (Regular Insulin) Subcutaneous sliding scale pre-meals (Added Day 2 for E11.65)",
            "Tab Ursodeoxycholic acid 300mg 1-0-1 post-food (Added Day 3 for B16.9)",
            "Inj Paracetamol 1g IV in 100ml NS infusion SOS for Temp > 100°F",
            "IV Fluids: 0.9% Normal Saline 75 ml/hr"
        ],
        "medications_discharge": [
            "Tab Primaquine 15mg 1-0-0 post-breakfast x 14 days",
            "Tab Metformin 500mg 1-0-1 post-meals (for E11.65)",
            "Tab Ursodeoxycholic acid 300mg 1-0-1 x 1 month (for B16.9)",
            "Tab Pan 40mg 1-0-0 (B/F) x 14 days",
            "Review in General Medicine OPD with repeat LFT & FBS in 10 days"
        ],
        "radiology_required": False
    },
    "TYPE2_DM_HYPERGLYCEMIA": {
        "disease_name": "Type 2 Diabetes Mellitus with Severe Uncontrolled Hyperglycemia",
        "icd10": "E11.65",
        "department": "General Medicine",
        "chief_complaints": [
            "c/o Easy fatigability and generalized weakness x 2 weeks",
            "c/o Polyuria, polydipsia and nocturia x 3 weeks",
            "c/o Burning sensation and numbness in bilateral feet x 1 month"
        ],
        "hpi": "Known case of Type 2 Diabetes Mellitus since 4 years on irregular oral hypoglycemic agents. Patient presented with worsening weakness, tingling and numbness in both lower limbs. No chest pain, palpitations, or shortness of breath. No history of diabetic ketoacidosis.",
        "vitals_admission": {"bp": "140/90", "pr": "84", "rr": "18", "temp": "98.4", "spo2": "98", "grbs": "412"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Mild bilateral pedal edema (+)", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal rhythm",
            "rs": "Bilateral air entry equal, NVBS heard",
            "abdomen": "Soft, non-tender, no organomegaly",
            "cns": "Conscious, oriented. Decreased pinprick sensation in glove & stocking distribution (diabetic sensory neuropathy). Ankle reflex diminished bilaterally."
        },
        "pathology": {
            "category": "Complete Blood Count & Urine Examination",
            "items": [
                {"name": "Hemoglobin", "result_value": "12.8", "unit": "g/dL", "reference_range": "12.0 - 15.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "8600", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "240000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Urine Glucose", "result_value": "3+ (Heavy)", "unit": "-", "reference_range": "Nil", "flag": "HIGH"},
                {"name": "Urine Ketone Bodies", "result_value": "Negative", "unit": "-", "reference_range": "Negative", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Glycemic & Renal Profile",
            "items": [
                {"name": "Random Blood Sugar (GRBS Stat)", "result_value": "412", "unit": "mg/dL", "reference_range": "70 - 140", "flag": "CRITICAL"},
                {"name": "Fasting Blood Sugar (FBS)", "result_value": "238", "unit": "mg/dL", "reference_range": "70 - 100", "flag": "HIGH"},
                {"name": "HbA1c (Glycosylated Hemoglobin)", "result_value": "12.8", "unit": "%", "reference_range": "< 5.7", "flag": "CRITICAL"},
                {"name": "Blood Urea", "result_value": "34", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "1.1", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"},
                {"name": "Serum Sodium (Na+)", "result_value": "134", "unit": "mEq/L", "reference_range": "135 - 145", "flag": "LOW"},
                {"name": "Serum Potassium (K+)", "result_value": "4.2", "unit": "mEq/L", "reference_range": "3.5 - 5.0", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Urine Culture & Sensitivity",
            "items": [
                {"name": "Urine Wet Mount", "result_value": "Pus cells 2-4 /hpf, Epithelial cells 3-5 /hpf", "unit": "-", "reference_range": "0-5 pus cells", "flag": "NORMAL"},
                {"name": "Urine Culture", "result_value": "No significant bacterial growth after 48 hrs incubation", "unit": "-", "reference_range": "Sterile", "flag": "NORMAL"}
            ]
        },
        "medications_inpatient": [
            "Inj Human Actrapid (Regular Insulin) S/C sliding scale Q6H (12-12-10 U S/C)",
            "Tab Metformin 500mg 1-0-1 (Post meals)",
            "Inj Optineuron 1 ampoule in 100ml NS IV OD",
            "Tab Pregabalin 75mg 0-0-1 (HS)",
            "Tab Pantoprazole 40mg 1-0-0 (B/F)",
            "IV Normal Saline 0.9% 75 ml/hr",
            "Diabetic Chart monitoring Q4H GRBS"
        ],
        "medications_discharge": [
            "Inj Human Mixtard 30/70 (18 units before breakfast, 12 units before dinner) S/C",
            "Tab Metformin 500mg 1-0-1",
            "Tab Pregabalin 75mg 0-0-1 (HS) x 1 month",
            "Tab Telmisartan 40mg 1-0-0"
        ],
        "radiology_required": False
    },
    "COPD_ACUTE_EXACERBATION": {
        "disease_name": "Chronic Obstructive Pulmonary Disease with Acute Exacerbation",
        "icd10": "J44.1",
        "department": "Respiratory Medicine",
        "chief_complaints": [
            "c/o Shortness of breath mMRC Grade-3 x 5 days",
            "c/o Cough with copious mucopurulent expectoration x 1 week",
            "c/o Wheezing and chest tightness x 3 days"
        ],
        "hpi": "65-year-old patient with a 25-pack-year smoking history, known COPD on regular bronchodilator inhalers, presents with acute worsening of breathlessness, increased sputum purulence, and sleep disturbance over the last 5 days following upper respiratory tract infection.",
        "vitals_admission": {"bp": "130/80", "pr": "96", "rr": "26", "temp": "99.1", "spo2": "89", "grbs": "112"},
        "exam_admission": {
            "pallor": "Mild (+)", "icterus": "Absent", "edema": "Absent", "cyanosis": "Mild peripheral (+)", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal heart sounds",
            "rs": "Bilateral reduced air entry, prolonged expiration with widespread expiratory polyphonic wheezes and occasional coarse basal crepitations",
            "abdomen": "Soft, non-tender",
            "cns": "Conscious, oriented, anxious"
        },
        "pathology": {
            "category": "Complete Blood Count & ESR",
            "items": [
                {"name": "Hemoglobin", "result_value": "15.4", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "12800", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "HIGH"},
                {"name": "Neutrophils", "result_value": "82", "unit": "%", "reference_range": "40 - 75", "flag": "HIGH"},
                {"name": "Lymphocytes", "result_value": "14", "unit": "%", "reference_range": "20 - 45", "flag": "LOW"},
                {"name": "Platelet Count", "result_value": "265000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "ESR", "result_value": "28", "unit": "mm/1st hr", "reference_range": "0 - 15", "flag": "HIGH"}
            ]
        },
        "microbiology": {
            "category": "Sputum AFB & Truenat MTB PCR",
            "items": [
                {"name": "Sputum AFB (ZN Stain)", "result_value": "Negative for Acid Fast Bacilli", "unit": "-", "reference_range": "Negative", "flag": "NORMAL"},
                {"name": "Sputum Truenat MTB Real-Time PCR", "result_value": "MTB NOT DETECTED (Valid test, internal control passed)", "unit": "-", "reference_range": "Not Detected", "flag": "NORMAL"},
                {"name": "Sputum Gram Stain", "result_value": "Gram-negative bacilli and pus cells > 25/LPF", "unit": "-", "reference_range": "Normal flora", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Routine Biochemistry & ABG Screen",
            "items": [
                {"name": "Blood Urea", "result_value": "26", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.85", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"},
                {"name": "Serum Sodium", "result_value": "138", "unit": "mEq/L", "reference_range": "135 - 145", "flag": "NORMAL"},
                {"name": "Serum Potassium", "result_value": "4.1", "unit": "mEq/L", "reference_range": "3.5 - 5.0", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "CHEST_XRAY",
        "radiology_details": {
            "modality": "CR",
            "body_part": "CHEST",
            "study_description": "Chest X-Ray PA View",
            "findings": "Hyperinflated bilateral lung fields with flattening of bilateral diaphragmatic domes. Increased retrosternal clear space. Narrow tubular cardiac silhouette. Prominent pulmonary vascular markings in lower zones without gross consolidation.",
            "impression": "Findings consistent with Chronic Obstructive Pulmonary Disease (COPD) with emphysematous changes."
        },
        "medications_inpatient": [
            "O2 inhalation via nasal prongs at 1-2 L/min target SpO2 88-92%",
            "Nebulization Duolin (Levosalbutamol + Ipratropium) 1-1-1",
            "Nebulization Budecort 0.5mg 1-0-1",
            "Inj Hydrocortisone 100mg IV BD x 3 days",
            "Tab Augmentin (Amox-Clav) 625mg 1-0-1 x 5 days",
            "Tab Pulmoclear (Acebrophylline + Acetylcysteine) 1-0-1",
            "Tab Pantoprazole 40mg 1-0-0 (B/F)"
        ],
        "medications_discharge": [
            "Inhaler Foracort 200 (Formoterol + Budesonide) 2 puffs BD with spacer",
            "Tab Augmentin 625mg 1-0-1 x 3 more days",
            "Tab Pulmoclear 1-0-1 x 10 days",
            "Tab Pantoprazole 40mg 1-0-0 x 7 days",
            "Smoking cessation counseling provided"
        ]
    },
    "BACTERIAL_PNEUMONIA": {
        "disease_name": "Community-Acquired Bacterial Lobar Pneumonia",
        "icd10": "J18.9",
        "department": "General Medicine",
        "chief_complaints": [
            "c/o High grade fever with chills x 3 days",
            "c/o Productive cough with yellowish-green rust sputum x 3 days",
            "c/o Right sided pleuritic chest pain aggravated by deep inspiration x 2 days"
        ],
        "hpi": "Patient presented with acute onset fever reaching 102.6°F associated with chills, right sided chest discomfort on coughing, and prominent productive cough. No hemoptysis, no past history of tuberculosis.",
        "vitals_admission": {"bp": "118/74", "pr": "104", "rr": "26", "temp": "102.4", "spo2": "93", "grbs": "118"},
        "exam_admission": {
            "pallor": "Mild (+)", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, tachycardic",
            "rs": "Dull percussion note over right infra-axillary and infrascapular areas. Bronchial breath sounds and coarse inspiratory crepitations over right lower zone. Whispering pectoriloquy present.",
            "abdomen": "Soft, non-tender",
            "cns": "Conscious, oriented"
        },
        "pathology": {
            "category": "Complete Blood Count & Inflammatory Markers",
            "items": [
                {"name": "Hemoglobin", "result_value": "11.8", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "LOW"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "16400", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "HIGH"},
                {"name": "Neutrophils", "result_value": "86", "unit": "%", "reference_range": "40 - 75", "flag": "HIGH"},
                {"name": "Lymphocytes", "result_value": "10", "unit": "%", "reference_range": "20 - 45", "flag": "LOW"},
                {"name": "Platelet Count", "result_value": "290000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "ESR", "result_value": "62", "unit": "mm/1st hr", "reference_range": "0 - 15", "flag": "HIGH"}
            ]
        },
        "microbiology": {
            "category": "Sputum Gram Stain & Truenat MTB",
            "items": [
                {"name": "Sputum Gram Stain", "result_value": "Gram-positive lancet-shaped diplococci in pairs and short chains, > 25 neutrophils/HPF", "unit": "-", "reference_range": "Normal respiratory flora", "flag": "POSITIVE"},
                {"name": "Sputum Truenat MTB", "result_value": "MTB NOT DETECTED", "unit": "-", "reference_range": "Not Detected", "flag": "NORMAL"},
                {"name": "Blood Culture (Aerobic)", "result_value": "Streptococcus pneumoniae isolated, sensitive to Ceftriaxone, Amoxicillin-Clavulanate, Levofloxacin", "unit": "-", "reference_range": "Sterile", "flag": "POSITIVE"}
            ]
        },
        "biochemistry": {
            "category": "Renal Function & CRP",
            "items": [
                {"name": "C-Reactive Protein (CRP Quantitative)", "result_value": "68.4", "unit": "mg/L", "reference_range": "< 6.0", "flag": "CRITICAL"},
                {"name": "Blood Urea", "result_value": "32", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.95", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "CHEST_XRAY",
        "radiology_details": {
            "modality": "CR",
            "body_part": "CHEST",
            "study_description": "Chest X-Ray PA View",
            "findings": "Homogeneous dense radio-opacity with prominent air bronchograms observed in the Right Lower Lobe. Right costophrenic angle is clear. Trachea is central. Cardiac silhouette is within normal limits.",
            "impression": "Right Lower Lobe Lobar Pneumonia / Consolidation."
        },
        "medications_inpatient": [
            "Inj Ceftriaxone 1g IV BD in 100ml NS",
            "Tab Azithromycin (Azee) 500mg 1-0-0 x 5 days",
            "Inj Paracetamol 1g IV infusion SOS",
            "Nebulization Duolin TDS",
            "Tab Pantoprazole 40mg 1-0-0",
            "IV Normal Saline 75 ml/hr"
        ],
        "medications_discharge": [
            "Tab Cefuroxime Axetil 500mg 1-0-1 x 5 days",
            "Tab Paracetamol 650mg 1-0-1 SOS",
            "Tab Pantoprazole 40mg 1-0-0 x 5 days",
            "Review in Chest OPD after 7 days with repeat CXR"
        ]
    },
    "DENGUE_FEVER": {
        "disease_name": "Dengue Fever with Thrombocytopenia",
        "icd10": "A97.1",
        "department": "General Medicine",
        "chief_complaints": [
            "c/o Acute sudden onset high fever with severe chills x 4 days",
            "c/o Severe retro-orbital pain and breakbone arthralgia x 3 days",
            "c/o Flushing and petechial spots on both forearms x 1 day"
        ],
        "hpi": "Young adult presented with classic constitutional symptoms of dengue including high fever, intense headache behind the eyes, marked generalized muscular pain, and loss of appetite. No history of spontaneous bleeding, melena, or hematuria.",
        "vitals_admission": {"bp": "110/72", "pr": "108", "rr": "20", "temp": "103.0", "spo2": "98", "grbs": "98"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal sounds",
            "rs": "Bilateral clear, no crepitations",
            "abdomen": "Mild tenderness in right hypochondrium, liver just palpable, soft",
            "cns": "Conscious, alert, irritable",
            "skin": "Erythematous macular rash with scattered petechiae over lower extremities and forearms. Tourniquet test positive."
        },
        "pathology": {
            "category": "Complete Blood Count (Serial Monitoring)",
            "items": [
                {"name": "Hemoglobin", "result_value": "14.8", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Hematocrit (PCV)", "result_value": "46.5", "unit": "%", "reference_range": "40.0 - 50.0", "flag": "HIGH"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "2900", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "LOW"},
                {"name": "Platelet Count", "result_value": "44000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "CRITICAL"},
                {"name": "Peripheral Smear", "result_value": "Marked Thrombocytopenia, Atypical reactive lymphocytes seen.", "unit": "-", "reference_range": "Normal morphology", "flag": "HIGH"}
            ]
        },
        "microbiology": {
            "category": "Dengue Serology Duo Panel",
            "items": [
                {"name": "Dengue NS1 Antigen", "result_value": "POSITIVE", "unit": "-", "reference_range": "Negative", "flag": "POSITIVE"},
                {"name": "Dengue IgM Antibody", "result_value": "POSITIVE (Weakly Reactive)", "unit": "-", "reference_range": "Negative", "flag": "POSITIVE"},
                {"name": "Dengue IgG Antibody", "result_value": "Negative", "unit": "-", "reference_range": "Negative", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Hepatic Transaminases",
            "items": [
                {"name": "SGOT (AST)", "result_value": "138", "unit": "U/L", "reference_range": "10 - 40", "flag": "HIGH"},
                {"name": "SGPT (ALT)", "result_value": "92", "unit": "U/L", "reference_range": "10 - 45", "flag": "HIGH"},
                {"name": "Serum Albumin", "result_value": "3.8", "unit": "g/dL", "reference_range": "3.5 - 5.0", "flag": "NORMAL"}
            ]
        },
        "medications_inpatient": [
            "Strict IV Fluid Regimen: Ringer Lactate 100 ml/hr titrated to maintain hematocrit < 42%",
            "Tab Paracetamol 650mg 1-0-1 SOS for Temp > 100°F (Strictly NO NSAIDs / Aspirin)",
            "Inj Pantoprazole 40mg IV OD",
            "Oral rehydration fluids (ORS, coconut water, fresh juices) ad libitum",
            "Serial Platelet Count & Hematocrit monitoring Q8H",
            "Strict bed rest with mosquito net"
        ],
        "medications_discharge": [
            "Tab Paracetamol 650mg SOS",
            "Tab Pantoprazole 40mg 1-0-0 x 5 days",
            "Nutritious high-protein diet and adequate oral hydration (2.5 - 3 L/day)"
        ],
        "radiology_required": False
    },
    "TERM_PREGNANCY_LSCS": {
        "disease_name": "G2P1L1 at 38+4 Weeks POG with Previous LSCS in Active Labour",
        "icd10": "O82.0",
        "department": "Obstetrics & Gynaecology",
        "chief_complaints": [
            "c/o Pain in abdomen since early morning (labour pains)",
            "c/o Leaking per vaginum x 2 hours",
            "History of 9 months of amenorrhea"
        ],
        "hpi": "24-year-old G2P1L1 at 38 weeks + 4 days of gestational age with history of previous Lower Segment Cesarean Section 2.5 years ago. Patient presented in active labor with regular uterine contractions and spontaneous rupture of membranes. Fetal heart sounds 142 bpm, regular.",
        "vitals_admission": {"bp": "124/80", "pr": "92", "rr": "18", "temp": "98.4", "spo2": "99", "grbs": "94"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Mild physiological ankle edema (+)", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard",
            "rs": "Clear",
            "abdomen": "P/A: Uterus term size, longitudinal lie, cephalic presentation, contractions 3 in 10 mins each lasting 35-40 secs. Previous Pfannenstiel scar healed by primary intention, non-tender. FHR 140 bpm regular.",
            "cns": "Conscious, cooperative",
            "local_exam": "P/V: Cervix 4-5 cm dilated, 70% effaced, vertex at -1 station, membranes absent, clear liquor drain."
        },
        "pathology": {
            "category": "Pre-Operative Hematology & Coagulation",
            "items": [
                {"name": "Hemoglobin", "result_value": "11.6", "unit": "g/dL", "reference_range": "11.0 - 15.0", "flag": "NORMAL"},
                {"name": "Blood Group & Rh Type", "result_value": "B Rh Positive", "unit": "-", "reference_range": "-", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "245000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Bleeding Time (BT)", "result_value": "2 min 15 sec", "unit": "min/sec", "reference_range": "2 - 7 min", "flag": "NORMAL"},
                {"name": "Clotting Time (CT)", "result_value": "5 min 30 sec", "unit": "min/sec", "reference_range": "4 - 9 min", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.8", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.02", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Antenatal Viral Serology Panel",
            "items": [
                {"name": "HIV 1 & 2 ELISA", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg (Surface Antigen)", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HCV Antibody", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "VDRL / RPR", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Electrolytes & Renal Screen",
            "items": [
                {"name": "Serum Creatinine", "result_value": "0.62", "unit": "mg/dL", "reference_range": "0.5 - 1.1", "flag": "NORMAL"},
                {"name": "Blood Urea", "result_value": "18", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Random Blood Glucose", "result_value": "92", "unit": "mg/dL", "reference_range": "70 - 140", "flag": "NORMAL"}
            ]
        },
        "medications_inpatient": [
            "Inj Cefotaxime (Mahacef) 1g IV BD",
            "Inj Metronidazole (Metrogyl) 100ml IV TDS",
            "Inj Pantoprazole 40mg IV OD",
            "Inj Tramadol 50mg IV in 100ml NS SOS for postoperative analgesia",
            "IV Fluids: 5% Dextrose Normal Saline + Ringer Lactate",
            "Post-op care: Catheter removal Day 1, suture removal / dressing Day 7"
        ],
        "medications_discharge": [
            "Tab Cefixime (Taxim-O) 200mg 1-0-1 x 5 days",
            "Tab Metrogyl 400mg 1-1-1 x 5 days",
            "Tab Diclomol 1-0-1 x 5 days",
            "Tab Pan 40mg 1-0-0 (B/F)",
            "Syrup Autrin (Iron) 10ml OD & Tab Shelcal 500mg 1-0-1 x 3 months",
            "Exclusive breastfeeding advised"
        ],
        "radiology_required": False
    },
    "LUMBAR_SPONDYLOSIS": {
        "disease_name": "Lumbar Spondylosis with L4-L5 Radiculopathy",
        "icd10": "M51.2",
        "department": "Orthopedics",
        "chief_complaints": [
            "c/o Low back pain radiating to right lower limb x 3 months",
            "c/o Difficulty bending forward and prolonged standing x 1 month",
            "c/o Tingling sensation along right L5 dermatome x 2 weeks"
        ],
        "hpi": "52-year-old manual worker presents with chronic dull aching lower back pain radiating down the posterolateral aspect of the right thigh and leg to the great toe. Aggravated by sneezing, bending, and heavy lifting. Relieved partially by supine posture.",
        "vitals_admission": {"bp": "128/82", "pr": "76", "rr": "16", "temp": "98.4", "spo2": "99", "grbs": "106"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard",
            "rs": "Clear",
            "abdomen": "Soft",
            "cns": "Conscious, oriented",
            "local_exam": "Paraspinal muscle spasm over lumbar region. Tenderness over L4-L5 interspinous space. Straight Leg Raising Test (SLRT) positive on right side at 45 degrees, negative on left (80 degrees). Lasegue sign positive right side. Right EHL weakness Grade 4/5."
        },
        "pathology": {
            "category": "Routine Hematology & Inflammatory Panel",
            "items": [
                {"name": "Hemoglobin", "result_value": "13.4", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count", "result_value": "7200", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "ESR", "result_value": "14", "unit": "mm/1st hr", "reference_range": "0 - 15", "flag": "NORMAL"},
                {"name": "Rheumatoid Factor (RA Factor Quantitative)", "result_value": "8.2", "unit": "IU/mL", "reference_range": "< 14.0", "flag": "NORMAL"},
                {"name": "Serum Uric Acid", "result_value": "5.4", "unit": "mg/dL", "reference_range": "3.5 - 7.2", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Serum Calcium & Vitamin D3",
            "items": [
                {"name": "Serum Calcium", "result_value": "9.1", "unit": "mg/dL", "reference_range": "8.8 - 10.2", "flag": "NORMAL"},
                {"name": "Serum Phosphorus", "result_value": "3.4", "unit": "mg/dL", "reference_range": "2.5 - 4.5", "flag": "NORMAL"},
                {"name": "Serum Alkaline Phosphatase (ALP)", "result_value": "82", "unit": "U/L", "reference_range": "40 - 130", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "General Pre-Operative Screening",
            "items": [
                {"name": "HIV 1&2 Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "L_S_SPINE_MRI",
        "radiology_details": {
            "modality": "MR",
            "body_part": "L-S SPINE",
            "study_description": "MRI Lumbar Spine with Screening",
            "findings": "Straightening of lumbar lordosis due to muscle spasm. Reduced disc height and disc desiccation with T2 hypointensity at L4-L5 level. Right paracentral disc protrusion at L4-L5 encroaching right lateral recess and compromising traversing right L5 nerve root. Facet joint arthrosis present.",
            "impression": "L4-L5 Right Paracentral Disc Protrusion with Right L5 Nerve Root Compression."
        },
        "medications_inpatient": [
            "Tab Zerodol-MR (Aceclofenac 100mg + Tizanidine 2mg) 1-0-1 x 5 days",
            "Tab Pregabalin 75mg + Methylcobalamin 750mcg (Pregaba-M) 0-0-1 (HS) x 1 month",
            "Tab Pantoprazole 40mg 1-0-0 (B/F)",
            "Tab Shelcal-XT (Calcium + Vit D3) 0-1-0 x 1 month",
            "Nanofast gel local application TDS",
            "Lumbosacral belt support during ambulation and physiotherapy guidance"
        ],
        "medications_discharge": [
            "Tab Zerodol-MR 1-0-1 x 5 days post-food",
            "Tab Pregaba-M 0-0-1 (HS) x 30 days",
            "Tab Shelcal-XT 0-1-0 x 30 days",
            "Physiotherapy: Core strengthening & pelvic bridging exercises",
            "Review in Orthopedics OPD after 2 weeks"
        ]
    },
    "GADEMMA_AUB": {
        "disease_name": "Abnormal Uterine Bleeding (AUB-L / Endometrial Hyperplasia)",
        "icd10": "N92.0",
        "department": "Obstetrics & Gynaecology",
        "chief_complaints": [
            "c/o Heavy menstrual bleeding with passage of large clots x 9 months",
            "c/o Lower abdominal dragging and crampy pain during periods x 6 months",
            "c/o Generalized weakness, fatigue, and exertional palpitation x 2 months"
        ],
        "hpi": "45-year-old P2L2 female presented with complaints of excessive and irregular menstrual bleeding for 9 months, soaking 5-6 pads daily with large clots. Associated with lower abdominal dragging pain and easy fatigability. No history of post-coital bleeding or foul-smelling discharge. Pelvic examination reveals bulky uterus; endometrial evaluation planned.",
        "vitals_admission": {"bp": "110/70", "pr": "88", "rr": "18", "temp": "98.4", "spo2": "99", "grbs": "98"},
        "exam_admission": {
            "pallor": "Present (++)", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, hemic ejection systolic murmur grade 2/6 over pulmonary area",
            "rs": "Normal vesicular breath sounds bilaterally, chest clear",
            "abdomen": "Soft, mild tenderness over suprapubic region, no organomegaly",
            "cns": "Conscious, oriented",
            "local_exam": "Per Speculum (P/S): Cervix healthy, external os closed, blood clots seen in posterior fornix. Per Vaginum (P/V): Uterus anteverted, bulky (~8-10 weeks gravid size), firm, mobile, non-tender. Bilateral fornices free."
        },
        "pathology": {
            "category": "Complete Blood Count & Coagulation Profile",
            "items": [
                {"name": "Hemoglobin", "result_value": "8.4", "unit": "g/dL", "reference_range": "11.0 - 15.0", "flag": "LOW"},
                {"name": "Packed Cell Volume (PCV)", "result_value": "27.2", "unit": "%", "reference_range": "36.0 - 46.0", "flag": "LOW"},
                {"name": "Mean Corpuscular Volume (MCV)", "result_value": "72.4", "unit": "fL", "reference_range": "80.0 - 100.0", "flag": "LOW"},
                {"name": "Mean Corpuscular Hb (MCH)", "result_value": "23.1", "unit": "pg", "reference_range": "27.0 - 32.0", "flag": "LOW"},
                {"name": "Platelet Count", "result_value": "285000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "7800", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.4", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.01", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Renal Function & Serum Ferritin",
            "items": [
                {"name": "Serum Ferritin", "result_value": "11.2", "unit": "ng/mL", "reference_range": "15.0 - 150.0", "flag": "LOW"},
                {"name": "Blood Urea", "result_value": "21", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.72", "unit": "mg/dL", "reference_range": "0.5 - 1.1", "flag": "NORMAL"},
                {"name": "Random Blood Sugar", "result_value": "98", "unit": "mg/dL", "reference_range": "70 - 140", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Pap Smear & Pre-Operative Serology",
            "items": [
                {"name": "Cervical Pap Smear Cytology", "result_value": "Negative for Intraepithelial Lesion or Malignancy (NILM); Inflammatory changes", "unit": "-", "reference_range": "NILM", "flag": "NORMAL"},
                {"name": "HIV 1&2 Rapid Screen", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Screen", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "PELVIC_USG",
        "radiology_details": {
            "modality": "US",
            "body_part": "PELVIS",
            "study_description": "Ultrasound Pelvis (Transabdominal & Transvaginal)",
            "findings": "Uterus is anteverted, bulky, measuring 9.4 x 5.6 x 5.0 cm with normal myometrial echotexture. No focal fibroid lesion seen. Endometrium is uniformly thickened measuring 14.8 mm, showing heterogeneous texture with cystic spaces suspicious for hyperplasia. Bilateral ovaries appear normal in size and stroma. No free fluid in pouch of Douglas.",
            "impression": "Bulky uterus with thickened endometrium (14.8 mm). Suggestive of Endometrial Hyperplasia. Histopathological evaluation via Dilatation and Curettage (D&C) recommended."
        },
        "medications_inpatient": [
            "Inj Tranexamic Acid 500mg IV TDS x 48 hours",
            "Inj Iron Sucrose 200mg in 100ml NS IV infusion alternate days x 2 doses",
            "Tab Meprate (Medroxyprogesterone acetate) 10mg 1-0-1",
            "Tab Pantoprazole 40mg 1-0-0 (B/F)",
            "IV Normal Saline 0.9% 75 ml/hr",
            "Pre-op preparation for D&C (NPO, consent, anaesthetic review)"
        ],
        "medications_discharge": [
            "Tab Medroxyprogesterone acetate 10mg 1-0-1 x 21 days (from Day 5 of cycle)",
            "Tab Orofer-XT (Ferrous Ascorbate + Folic Acid) 1-0-0 post lunch x 2 months",
            "Tab Tranexamic Acid 500mg TDS SOS during heavy flow",
            "Tab Pantoprazole 40mg 1-0-0 x 14 days",
            "Review with Histopathology (HPE) report in 7 days"
        ]
    },
    "MARY_STELLA_ANC": {
        "disease_name": "Antenatal Care G2P1L1 at 36 Weeks POG with Gestational Hypothyroidism",
        "icd10": "Z34.80",
        "department": "Obstetrics & Gynaecology",
        "chief_complaints": [
            "Routine planned Antenatal Checkup at 36 weeks gestational age",
            "c/o Mild bilateral pedal edema x 2 weeks",
            "Known case of Primary Hypothyroidism on Tab Thyroxine 50mcg OD"
        ],
        "hpi": "33-year-old G2P1L1 at 36 weeks POG presented for planned antenatal review. Prior FTND 4 years ago with healthy male child. Known case of primary hypothyroidism detected in early second trimester, maintained on Tab Thyroxine 50mcg OD. Patient reports active fetal movements (> 10 kicks/day). No complaints of headache, visual blurring, epigastric pain, or per-vaginal leaking/bleeding.",
        "vitals_admission": {"bp": "118/76", "pr": "82", "rr": "18", "temp": "98.4", "spo2": "99", "grbs": "92"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Mild bilateral pitting ankle edema (+)", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal",
            "rs": "Bilateral vesicular breath sounds, clear",
            "abdomen": "P/A: Uterus corresponds to 36 weeks size, relaxed. Longitudinal lie, cephalic presentation. Head high, not engaged. Fetal Heart Sounds (FHS) 144 bpm, regular in right lower quadrant. No scar tenderness.",
            "cns": "Conscious, cooperative, deep tendon reflexes normal (+2 bilaterally)"
        },
        "pathology": {
            "category": "Third Trimester Antenatal Hematology",
            "items": [
                {"name": "Hemoglobin", "result_value": "11.2", "unit": "g/dL", "reference_range": "11.0 - 15.0", "flag": "NORMAL"},
                {"name": "Blood Group & Rh Type", "result_value": "O Rh Positive", "unit": "-", "reference_range": "-", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "225000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Urine Routine - Protein / Albumin", "result_value": "Nil", "unit": "-", "reference_range": "Nil", "flag": "NORMAL"},
                {"name": "Urine Routine - Sugar", "result_value": "Nil", "unit": "-", "reference_range": "Nil", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Thyroid Profile & Glycemic Screen",
            "items": [
                {"name": "Serum TSH (3rd Generation)", "result_value": "2.84", "unit": "µIU/mL", "reference_range": "0.3 - 3.0 (Trimester 3)", "flag": "NORMAL"},
                {"name": "Free T4 (FT4)", "result_value": "1.18", "unit": "ng/dL", "reference_range": "0.8 - 1.8", "flag": "NORMAL"},
                {"name": "Fasting Plasma Glucose", "result_value": "86", "unit": "mg/dL", "reference_range": "70 - 95", "flag": "NORMAL"},
                {"name": "Serum Uric Acid", "result_value": "4.2", "unit": "mg/dL", "reference_range": "2.5 - 6.0", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "High Vaginal Swab & Antenatal Serology",
            "items": [
                {"name": "High Vaginal Swab (HVS) Culture", "result_value": "No pathogenic bacterial or candida growth", "unit": "-", "reference_range": "Normal flora", "flag": "NORMAL"},
                {"name": "HIV 1&2 ELISA", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "OBSTETRIC_USG",
        "radiology_details": {
            "modality": "US",
            "body_part": "OBSTETRICS",
            "study_description": "Obstetric Ultrasound with Color Doppler (36 Weeks Growth Scan)",
            "findings": "Single live intrauterine fetus in cephalic presentation. BPD: 89.2 mm, FL: 70.4 mm, AC: 316.0 mm. Estimated Fetal Weight (EFW): 2680 ± 150 grams (~50th percentile). Amniotic Fluid Index (AFI): 13.6 cm (Adequate liquor). Placenta: Anterior, Grade II maturity, clear of internal os. Umbilical Artery Doppler: S/D ratio 2.3, RI 0.56, good end-diastolic flow.",
            "impression": "Single live intrauterine gestation corresponding to 36 weeks with normal biophysical profile, adequate liquor volume, and reassuring umbilical artery Doppler indices."
        },
        "medications_inpatient": [
            "Tab Thyroxine Sodium 50mcg 1-0-0 (stat early morning empty stomach)",
            "Tab Shelcal 500mg (Calcium + Vit D3) 1-0-1 (Post meals)",
            "Tab Autrin (Ferrous Fumarate + Folic Acid) 1-0-0 (Post lunch)",
            "Daily Fetal Movement Count (DFMC) charting",
            "Non-Stress Test (NST) monitoring daily"
        ],
        "medications_discharge": [
            "Tab Thyroxine Sodium 50mcg 1-0-0 empty stomach daily",
            "Tab Shelcal 500mg 1-0-1 x 1 month",
            "Tab Autrin 1-0-0 x 1 month",
            "Maintain Daily Fetal Movement Count (DFMC > 10 kicks / 12 hours)",
            "Report immediately if leaking, bleeding per vaginum, or decreased fetal kicks",
            "Review in OBG Antenatal Clinic at 37 weeks"
        ]
    },
    "BHARATH_TBI": {
        "disease_name": "Acute Traumatic Brain Injury (Concussion & Cortical Hemorrhagic Contusion)",
        "icd10": "S06.0X0A",
        "department": "Neurology",
        "chief_complaints": [
            "c/o Head trauma following Road Traffic Accident (Two-wheeler skid) x 3 hours",
            "c/o Transient loss of consciousness for ~5 minutes at the accident spot",
            "c/o Multiple episodes of projectile vomiting and severe bifrontal headache",
            "c/o Scalp laceration over right parietal region"
        ],
        "hpi": "17-year-old male pillion rider (not wearing helmet) sustained acute head trauma following a two-wheeler collision with skid 3 hours prior to presentation. History of loss of consciousness lasting approximately 5 minutes, followed by drowsiness, 3 episodes of non-bilious projectile vomiting, and severe diffuse headache. No history of seizures, ear/nose bleeding, or limb weakness. Brought to emergency for acute neuro-trauma management.",
        "vitals_admission": {"bp": "124/76", "pr": "68", "rr": "16", "temp": "98.6", "spo2": "98", "grbs": "110"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, regular rate and rhythm",
            "rs": "Bilateral vesicular breath sounds, chest clear",
            "abdomen": "Soft, non-tender, bowel sounds present",
            "cns": "Conscious but drowsy. Glasgow Coma Scale (GCS): E4 V4 M6 = 14/15. Pupils: Equal (3mm) and briskly reacting to light bilaterally. Cranial nerves I-XII grossly intact. Motor power: 5/5 in all 4 limbs, tone normal. Deep tendon reflexes: 2+ bilaterally. Plantars: Bilateral flexor. No signs of meningeal irritation.",
            "local_exam": "3 x 0.5 cm contused lacerated wound over right parietal scalp, hemostasis achieved, no visible skull depression or bone fragments."
        },
        "pathology": {
            "category": "Emergency Trauma Hematology & Coagulation Panel",
            "items": [
                {"name": "Hemoglobin", "result_value": "14.2", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "10400", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "210000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.2", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.02", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"},
                {"name": "Blood Group & Rh Type", "result_value": "A Rh Positive", "unit": "-", "reference_range": "-", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Serum Electrolytes & Renal Function",
            "items": [
                {"name": "Serum Sodium", "result_value": "140", "unit": "mEq/L", "reference_range": "135 - 145", "flag": "NORMAL"},
                {"name": "Serum Potassium", "result_value": "4.2", "unit": "mEq/L", "reference_range": "3.5 - 5.0", "flag": "NORMAL"},
                {"name": "Blood Urea", "result_value": "24", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.82", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Pre-Admission Infection Screen",
            "items": [
                {"name": "HIV 1&2 Rapid Test", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Test", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "NCCT_BRAIN",
        "radiology_details": {
            "modality": "CT",
            "body_part": "HEAD",
            "study_description": "Non-Contrast Computed Tomography (NCCT) Brain Axial 5mm",
            "findings": "Small 8 x 6 mm hyperdense hemorrhagic contusion seen in the right high parietal cortex with surrounding minimal rim of perifocal edema. No acute epidural or subdural hematoma seen. Lateral ventricles and 3rd ventricle are normal in caliber. Basal cisterns are clear. No midline shift. Calvarium is intact without depressed fracture.",
            "impression": "Small right parietal cortical hemorrhagic contusion and cerebral concussion. No mass effect or midline shift. Managed conservatively with strict neurological observation."
        },
        "medications_inpatient": [
            "Inj Mannitol 20% 100ml IV TDS x 48 hours (anti-edema therapy)",
            "Inj Levetiracetam 500mg IV BD (post-traumatic seizure prophylaxis)",
            "Inj Citicoline 500mg IV BD in 100ml NS",
            "Inj Ondansetron 4mg IV TDS (antiemetic)",
            "Inj Pantoprazole 40mg IV OD",
            "Inj Tramadol 50mg IV in 100ml NS SOS for severe headache",
            "Inj Tetanus Toxoid 0.5ml IM stat (wound care)",
            "Strict Neuro-Chart monitoring (GCS, pupil size, reaction Q1H)"
        ],
        "medications_discharge": [
            "Tab Levetiracetam 500mg 1-0-1 x 14 days",
            "Tab Citicoline 500mg 1-0-1 x 1 month",
            "Tab Paracetamol 650mg TDS SOS for headache",
            "Tab Pantoprazole 40mg 1-0-0 x 7 days",
            "Strictly avoid strenuous sports / riding two-wheeler for 4 weeks",
            "Review in Neurology OPD in 7 days or immediately if vomiting/drowsiness recurs"
        ]
    },
    "NAGARAJA_SDH": {
        "disease_name": "Chronic Subdural Hematoma (Right Fronto-Parietal)",
        "icd10": "I62.00",
        "department": "Neurology",
        "chief_complaints": [
            "c/o Progressive dull aching headache x 3 weeks",
            "c/o Progressive weakness in left upper and lower limbs x 5 days",
            "c/o Episodes of mental slowing, disorientation, and unsteady gait x 1 week"
        ],
        "hpi": "55-year-old male with history of trivial accidental slip and fall 3 weeks ago without initial LOC. Developed gradually progressive holocranial headache refractory to over-the-counter analgesics. Over the last 5 days, family noticed progressive weakness in left arm and leg (slipping of footwear, clumsiness in buttoning shirt), slowed cognition, and dragging gait. Brought for emergency neuro-evaluation.",
        "vitals_admission": {"bp": "148/90", "pr": "64", "rr": "16", "temp": "98.4", "spo2": "98", "grbs": "132"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, bradycardic rhythm",
            "rs": "Bilateral vesicular breath sounds, clear",
            "abdomen": "Soft, non-tender",
            "cns": "Conscious, mild cognitive slowing. GCS: E4 V4 M6 = 14/15. Left upper motor neuron facial paresis. Motor Power: Left Upper Limb 4-/5, Left Lower Limb 4/5, Right limbs 5/5. Tone: Spasticity in left limbs. Reflexes: Left biceps, knee, ankle hyperreflexic (3+), right 2+. Plantar reflex: Left extensor (positive Babinski), right flexor. Sensory examination intact."
        },
        "pathology": {
            "category": "Pre-Operative Neuro-Surgical Hematology & Coagulation",
            "items": [
                {"name": "Hemoglobin", "result_value": "13.8", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "8600", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "235000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.8", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.04", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"},
                {"name": "Activated Partial Thromboplastin Time (aPTT)", "result_value": "28.4", "unit": "seconds", "reference_range": "25 - 35", "flag": "NORMAL"},
                {"name": "Blood Group & Rh Type", "result_value": "O Rh Positive", "unit": "-", "reference_range": "-", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Renal Panel & Pre-Op Electrolytes",
            "items": [
                {"name": "Serum Sodium", "result_value": "136", "unit": "mEq/L", "reference_range": "135 - 145", "flag": "NORMAL"},
                {"name": "Serum Potassium", "result_value": "4.1", "unit": "mEq/L", "reference_range": "3.5 - 5.0", "flag": "NORMAL"},
                {"name": "Blood Urea", "result_value": "28", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.91", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Pre-Operative Viral Screen",
            "items": [
                {"name": "HIV 1&2 ELISA", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Test", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "Anti-HCV", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "NCCT_BRAIN",
        "radiology_details": {
            "modality": "CT",
            "body_part": "HEAD",
            "study_description": "NCCT Brain Axial with Multiplanar Reconstructions",
            "findings": "Large crescent-shaped hypodense to isodense extra-axial fluid collection along the right fronto-parieto-temporal convexity measuring 18.2 mm in maximum thickness. Significant mass effect with compression of right lateral ventricle, effacement of cortical sulci, and 7.2 mm midline shift to the left. No acute fresh hyperdense hemorrhage.",
            "impression": "Large Right Fronto-Parieto-Temporal Chronic Subdural Hematoma (CSDH) with significant mass effect and 7.2 mm midline shift. Indication for urgent surgical burr-hole craniostomy and subdural evacuation."
        },
        "medications_inpatient": [
            "Emergency Burr-Hole Craniostomy & Subdural Evacuation with drain under sedation",
            "Inj Ceftriaxone 1g IV BD x 3 days",
            "Inj Levetiracetam 500mg IV BD (antiepileptic cover)",
            "Inj Pantoprazole 40mg IV OD",
            "Inj Paracetamol 1g IV TDS SOS",
            "IV Normal Saline 0.9% 75 ml/hr (keep patient well hydrated in flat position)",
            "Closed subdural gravity drainage bag monitoring (measure output Q8H)"
        ],
        "medications_discharge": [
            "Tab Levetiracetam 500mg 1-0-1 x 1 month",
            "Tab Cefpodoxime Proxetil 200mg 1-0-1 x 5 days",
            "Tab Pantoprazole 40mg 1-0-0 x 14 days",
            "Tab Paracetamol 650mg TDS SOS",
            "Keep surgical wound clean and dry; suture removal on Day 8 in OPD",
            "Review in Neurosurgery / Neurology OPD in 7 days with repeat scan if symptoms recur"
        ]
    },
    "ANIL_KUMAR_FRACTURE": {
        "disease_name": "Closed Fracture Patella Right Knee (Transverse Displaced)",
        "icd10": "S82.001A",
        "department": "Orthopedics",
        "chief_complaints": [
            "c/o Severe pain, tense swelling, and deformity of right knee x 5 hours",
            "c/o Absolute inability to bear weight on right lower limb",
            "c/o Complete inability to actively extend the right knee or perform straight leg raise"
        ],
        "hpi": "31-year-old male sustained direct blunt trauma to the anterior aspect of right knee against the car bumper in a two-wheeler collision 5 hours ago. Complains of excruciating pain, rapid tense swelling of the knee joint, and inability to stand or extend the knee. No neurovascular deficits in foot. Brought to casualty for orthopedic management.",
        "vitals_admission": {"bp": "126/82", "pr": "86", "rr": "18", "temp": "98.4", "spo2": "99", "grbs": "102"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal",
            "rs": "Vesicular breath sounds, clear",
            "abdomen": "Soft, non-tender",
            "cns": "Conscious, oriented",
            "local_exam": "Right Knee: Tense hemarthrosis with gross swelling and anterior ecchymosis. A distinct, palpable transverse defect / gap (approx 2cm) felt over mid-patella with extreme bony tenderness and crepitus. Active knee extension completely absent; active Straight Leg Raise (SLR) test impossible (extensor disruption). Distal neurovascular status: Dorsalis pedis and posterior tibial pulses brisk (+2). Sensation over dorsal and plantar foot intact."
        },
        "pathology": {
            "category": "Pre-Operative Orthopedic Hematology & Coagulation",
            "items": [
                {"name": "Hemoglobin", "result_value": "14.6", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "9800", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "270000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.6", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.01", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"},
                {"name": "Blood Group & Rh Type", "result_value": "B Rh Positive", "unit": "-", "reference_range": "-", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Renal & Electrolyte Profile",
            "items": [
                {"name": "Blood Urea", "result_value": "22", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "0.84", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"},
                {"name": "Serum Sodium", "result_value": "139", "unit": "mEq/L", "reference_range": "135 - 145", "flag": "NORMAL"},
                {"name": "Serum Potassium", "result_value": "4.0", "unit": "mEq/L", "reference_range": "3.5 - 5.0", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Pre-Operative Serology Panel",
            "items": [
                {"name": "HIV 1&2 Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "KNEE_XRAY",
        "radiology_details": {
            "modality": "CR",
            "body_part": "RIGHT KNEE",
            "study_description": "Digital Radiography Right Knee AP and Lateral Views",
            "findings": "Complete displaced transverse fracture through the mid-substance of the right patella with 6.8 mm separation / distraction of bony fragments. Marked suprapatellar bursal distension and joint effusion (hemarthrosis). Distal femoral condyles and proximal tibial plateau are intact with preserved alignment. No secondary fracture seen.",
            "impression": "Displaced transverse fracture of right patella with complete disruption of extensor apparatus. Requires Open Reduction and Internal Fixation (ORIF) with Modified Tension Band Wiring (TBW)."
        },
        "medications_inpatient": [
            "ORIF Right Patella with Tension Band Wiring (TBW) under Spinal Anaesthesia",
            "Inj Cefuroxime 1.5g IV BD x 2 days",
            "Inj Diclofenac Sodium 75mg IM BD SOS",
            "Inj Tramadol 50mg in 100ml NS IV infusion SOS for severe breakthrough pain",
            "Inj Pantoprazole 40mg IV OD",
            "Limb elevation in above-knee slab; ice packs application Q4H",
            "Static quadriceps exercises started post-op Day 1"
        ],
        "medications_discharge": [
            "Tab Cefuroxime Axetil 500mg 1-0-1 post food x 5 days",
            "Tab Zerodol-SP (Aceclofenac + Serratiopeptidase + Paracetamol) 1-0-1 x 5 days",
            "Tab Pantoprazole 40mg 1-0-0 (B/F) x 7 days",
            "Tab Shelcal-XT (Calcium + Vit D3) 0-1-0 x 1 month",
            "Immobilization in long knee brace; non-weight bearing crutch walking for 3 weeks",
            "Suture removal on Day 12 in Orthopedics OPD"
        ]
    },
    "MUNI_NARAYANAPPA_ANKLE": {
        "disease_name": "Right Trimalleolar Ankle Fracture-Dislocation (Weber C)",
        "icd10": "S82.851A",
        "department": "Orthopedics",
        "chief_complaints": [
            "c/o Severe pain, gross deformity, and swelling of right ankle x 4 hours",
            "c/o Inability to bear weight on right lower limb following slip and fall",
            "c/o Inability to move right ankle joint"
        ],
        "hpi": "62-year-old male with history of accidental slip and fall down two steps at home 4 hours prior to presentation. Sustained sudden rotational twisting injury to right ankle. Complains of excruciating pain, rapid extensive ankle swelling, and gross visible deformity. No open puncture wound. Evaluated and splinted in emergency casualty before admission.",
        "vitals_admission": {"bp": "138/86", "pr": "84", "rr": "17", "temp": "98.4", "spo2": "98", "grbs": "128"},
        "exam_admission": {
            "pallor": "Absent", "icterus": "Absent", "edema": "Absent", "cyanosis": "Absent", "clubbing": "Absent",
            "cvs": "S1 S2 heard, normal",
            "rs": "Bilateral vesicular breath sounds, clear",
            "abdomen": "Soft, non-tender",
            "cns": "Conscious, oriented",
            "local_exam": "Right Ankle: Gross valgus and posterior deformity with prominent medial malleolar skin tenting. Tense bimalleolar swelling with ecchymosis. Severe tenderness over distal fibula, medial malleolus, and posterior tibial rim. Closed injury (skin intact, no fracture blisters). Distal neurovascular: Dorsalis pedis and posterior tibial pulses palpable (+2), capillary refill < 2 secs, sensation in all toes intact."
        },
        "pathology": {
            "category": "Pre-Operative Ankle Fracture Hematology",
            "items": [
                {"name": "Hemoglobin", "result_value": "13.0", "unit": "g/dL", "reference_range": "13.0 - 17.0", "flag": "NORMAL"},
                {"name": "Total Leucocyte Count (TLC)", "result_value": "8900", "unit": "cells/cumm", "reference_range": "4000 - 11000", "flag": "NORMAL"},
                {"name": "Platelet Count", "result_value": "240000", "unit": "/µL", "reference_range": "150000 - 450000", "flag": "NORMAL"},
                {"name": "Prothrombin Time (PT)", "result_value": "12.8", "unit": "seconds", "reference_range": "11 - 14", "flag": "NORMAL"},
                {"name": "INR", "result_value": "1.02", "unit": "-", "reference_range": "0.8 - 1.2", "flag": "NORMAL"}
            ]
        },
        "biochemistry": {
            "category": "Renal Function & Diabetic Screening",
            "items": [
                {"name": "Blood Urea", "result_value": "32", "unit": "mg/dL", "reference_range": "15 - 45", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "result_value": "1.02", "unit": "mg/dL", "reference_range": "0.6 - 1.2", "flag": "NORMAL"},
                {"name": "HbA1c (Glycated Hemoglobin)", "result_value": "6.8", "unit": "%", "reference_range": "< 5.7 (Good control)", "flag": "HIGH"},
                {"name": "Random Blood Glucose", "result_value": "128", "unit": "mg/dL", "reference_range": "70 - 140", "flag": "NORMAL"}
            ]
        },
        "microbiology": {
            "category": "Routine Pre-Surgical Screen",
            "items": [
                {"name": "HIV 1&2 Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"},
                {"name": "HBsAg Rapid Card", "result_value": "Non-Reactive", "unit": "-", "reference_range": "Non-Reactive", "flag": "NORMAL"}
            ]
        },
        "radiology_required": True,
        "radiology_type": "ANKLE_XRAY",
        "radiology_details": {
            "modality": "CR",
            "body_part": "RIGHT ANKLE",
            "study_description": "Digital Radiography Right Ankle Joint AP, Lateral, and Mortise Views",
            "findings": "Trimalleolar fracture of right ankle: Displaced oblique fracture of distal fibula above syndesmosis (Danis-Weber Type C), displaced transverse fracture of medial malleolus with 4.2 mm gap, and posterior malleolar triangular lip fracture involving 25% of tibial plafond. Lateral talar subluxation with widening of medial clear space.",
            "impression": "Right Trimalleolar Ankle Fracture-Subluxation (Danis-Weber C / Lauge-Hansen SER IV). Unstable mortise requiring Open Reduction and Internal Fixation (ORIF) with plate and screw osteosynthesis."
        },
        "medications_inpatient": [
            "ORIF Right Ankle (Distal fibula 1/3 tubular plate + Medial malleolar 4.0mm cancellous lag screws) under spinal anaesthesia",
            "Inj Ceftriaxone 1g IV BD x 3 days",
            "Inj Tramadol 50mg IV in 100ml NS SOS",
            "Inj Dynapar (Diclofenac 75mg) IM BD",
            "Tab Serratiopeptidase 10mg 1-0-1 (anti-edema)",
            "Inj Pantoprazole 40mg IV OD",
            "Limb elevation on Braun's Bohler frame; below-knee back slab support"
        ],
        "medications_discharge": [
            "Tab Cefixime (Taxim-O) 200mg 1-0-1 x 5 days",
            "Tab Zerodol-P (Aceclofenac + Paracetamol) 1-0-1 x 5 days",
            "Tab Serratiopeptidase 10mg 1-0-1 x 5 days",
            "Tab Pantoprazole 40mg 1-0-0 (B/F) x 7 days",
            "Below-knee synthetic fiber cast; strictly non-weight bearing with walker/crutches x 6 weeks",
            "Orthopedic clinic review and suture inspection in 14 days"
        ]
    }
}

class ClinicalEngine:
    """
    Engine enforcing strict medical logic mapping, realistic vital signs, 
    matching lab abnormalities, accurate pharmacology, and zero clinical contradictions.
    """

    @staticmethod
    def get_supported_conditions() -> List[str]:
        return list(CLINICAL_PROFILES.keys())

    @staticmethod
    def validate_clinical_integrity(patient: Patient, profile_key: str) -> List[str]:
        """
        Sanitizer verifying that no medical contradictions or audit puzzles exist.
        """
        violations = []
        profile = CLINICAL_PROFILES.get(profile_key)
        if not profile:
            violations.append(f"Invalid clinical profile key: {profile_key}")
            return violations

        # Gender validation (e.g. LSCS / Pregnancy / Gynecologic conditions must be Female)
        if profile_key in ["TERM_PREGNANCY_LSCS", "GADEMMA_AUB", "MARY_STELLA_ANC"] and patient.gender != "Female":
            violations.append("Clinical contradiction: Obstetric/Gynecologic condition assigned to non-female patient.")

        # Age validation
        if profile_key == "TERM_PREGNANCY_LSCS" and (patient.age < 18 or patient.age > 45):
            violations.append(f"Clinical anomaly: Pregnancy LSCS with atypical age {patient.age}.")

        if profile_key == "COPD_ACUTE_EXACERBATION" and patient.age < 40:
            violations.append(f"Clinical warning: COPD typically presents in patients > 40 years (age: {patient.age}).")

        # Department alignment
        if patient.department != profile["department"]:
            violations.append(f"Department mismatch: {patient.department} vs profile {profile['department']}.")

        return violations

    @staticmethod
    def generate_opd_slip(patient: Patient, profile_key: str = None) -> OpdSlip:
        if not profile_key:
            matching = [k for k, p in CLINICAL_PROFILES.items() if p["department"] == patient.department]
            profile_key = matching[0] if matching else "MALARIA_PV"
        profile = CLINICAL_PROFILES.get(profile_key, CLINICAL_PROFILES["MALARIA_PV"])
        
        is_ipd = bool(patient.ip_no)
        opd_no = f"OPD-{patient.mr_no[-6:]}"
        consultation_time = patient.admission_time.replace(minute=max(0, patient.admission_time.minute - 25))
        
        past_hx = {
            "diabetes_mellitus": "Yes (on irregular OHA)" if ("DM" in profile_key or profile_key == "MALARIA_PV") else "No",
            "hypertension": "Yes (on Tab Telmisartan 40mg)" if patient.age > 50 else "No",
            "tuberculosis": "No",
            "asthma": "Yes (Bronchodilators SOS)" if "COPD" in profile_key else "No",
            "ihd": "No",
            "surgical_history": "Appendectomy (2018)" if patient.age > 40 else "None"
        }
        
        recent_meds = ["Tab Paracetamol 650mg SOS"]
        if "DM" in profile_key:
            recent_meds.append("Tab Metformin 500mg BD (Irregular)")
        if "COPD" in profile_key:
            recent_meds.append("Asthalin Inhaler 2 puffs PRN")
        if "LUMBAR" in profile_key:
            recent_meds.append("Tab Aceclofenac 100mg SOS")
            
        treatment_rx = profile["medications_inpatient"][:3]
        
        findings = {
            "vitals": {
                "bp": profile["vitals_admission"]["bp"],
                "pr": profile["vitals_admission"]["pr"],
                "rr": profile["vitals_admission"]["rr"],
                "temp": profile["vitals_admission"]["temp"],
                "spo2": profile["vitals_admission"]["spo2"],
                "grbs": profile["vitals_admission"]["grbs"]
            },
            "exam": f"Pallor: {profile['exam_admission'].get('pallor', 'Absent')}, Icterus: {profile['exam_admission'].get('icterus', 'Absent')}, CVS: {profile['exam_admission'].get('cvs', 'S1 S2 heard')}, RS: {profile['exam_admission'].get('rs', 'Clear')}"
        }
        
        conclusion = "Advise immediate admission to Inpatient Ward for IV therapy and diagnostic workup." if is_ipd else "Outpatient management prescribed. Follow-up after 5 days or if red flags emerge."
        proceeding = "ADMIT_TO_IPD" if is_ipd else "OPD_HOME_CARE"
        
        return OpdSlip(
            patient_id=patient.id,
            form_code="FORM F/EPH/OPD/01",
            opd_number=opd_no,
            consultation_timestamp=consultation_time,
            department=patient.department,
            unit=patient.unit,
            attending_doctor=patient.attending_doctor,
            doctor_reg_no=patient.doctor_reg_no,
            actual_problem=profile["chief_complaints"][:2],
            history_presenting_illness=profile["hpi"][:280] + "...",
            past_history=past_hx,
            recent_medication=recent_meds,
            allergies="No Known Drug Allergies (NKDA)",
            clinical_findings=findings,
            provisional_diagnosis=profile["disease_name"],
            icd10_code=profile["icd10"],
            treatment_advised=treatment_rx,
            investigations_ordered=["Complete Blood Count (CBC)", "Renal & Liver Function Tests", "Peripheral Blood Smear"],
            conclusion_remarks=conclusion,
            proceeding_action=proceeding,
            next_review_date=(consultation_time + timedelta(days=5)).strftime("%d/%m/%Y")
        )

    @staticmethod
    def generate_full_clinical_bundle(
        patient: Patient,
        profile_key: str,
        current_sim_time: datetime
    ) -> Dict[str, Any]:
        """
        Generates linked H&P, Progress Notes, Lab Reports, TPR Chart,
        Medication Chart, Diabetic Chart, and Radiology study chronologically.
        """
        profile = CLINICAL_PROFILES[profile_key]
        admission_time = patient.admission_time

        # 0. Outpatient Consultation Record (OPD Slip F/EPH/OPD/01)
        opd_slip = ClinicalEngine.generate_opd_slip(patient, profile_key)

        # 1. History and Physical Examination (F/EPH/MRD/39) - Recorded at Admission
        hp_exam = HistoryAndPhysical(
            patient_id=patient.id,
            admission_timestamp=admission_time,
            doctor_unit=f"{patient.department} - {patient.unit}",
            chief_complaints=profile["chief_complaints"],
            history_presenting_illness=profile["hpi"],
            general_exam={
                "weight_kg": str(random.randint(52, 78)),
                "height_cm": str(random.randint(155, 175)),
                "temperature_f": profile["vitals_admission"]["temp"],
                "pulse_bpm": profile["vitals_admission"]["pr"],
                "respiration_cpm": profile["vitals_admission"]["rr"],
                "bp_mmhg": profile["vitals_admission"]["bp"],
                "spo2_percent": profile["vitals_admission"]["spo2"],
                **profile["exam_admission"]
            },
            provisional_diagnosis=profile["disease_name"],
            icd10_code=profile["icd10"],
            care_plan_investigations=list(profile.get("pathology", {}).get("items", [{}])[0].keys()) if "pathology" in profile else ["Routine CBC", "RFT", "CXR"],
            care_plan_treatment=profile["medications_inpatient"][:4],
            consultant_name=patient.attending_doctor,
            consultant_reg=patient.doctor_reg_no
        )

        # 2. Chronological Progress Notes (F/MRD/EPH/40)
        progress_notes = []
        note_cursor = admission_time + timedelta(hours=2)
        day_count = 1

        while day_count <= 4:
            # Baseline daily trend calculations
            temp_val = round(float(profile["vitals_admission"]["temp"]) - (day_count * 0.8), 1)
            temp_val = max(temp_val, 98.4)
            pr_val = max(72, int(profile["vitals_admission"]["pr"]) - (day_count * 8))

            # Multi-ICD progression specific round narratives across departments
            if profile_key == "MALARIA_PV":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with high-grade rigors (Temp 103.2°F), severe myalgia, headache. Peripheral smear confirms ring trophozoites of Plasmodium vivax. Critical thrombocytopenia (52,000/µL). Started on IV Artesunate 120mg stat + IV fluids DNS + RL. G6PD screen sent prior to Primaquine."
                    m_vitals = {"BP": "110/70", "PR": "116 bpm", "RR": "20 cpm", "SpO2": "98% @ RA", "Temp": "103.2°F", "GRBS": "104 mg/dL"}
                    m_rx = ["Inj Artesunate 120mg IV stat then at 12, 24 hrs", "IV Fluids 0.9% Normal Saline 75 ml/hr", "Inj Paracetamol 1g IV SOS"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Registrar Review)"
                    e_narrative = "Fever spikes persisting. Second dose IV Artesunate 120mg administered at 12 hours. Splenomegaly palpable 2cm, non-tender. Urine output adequate (1400 ml/24h). Strict Q4H TPR monitoring maintained."
                    e_vitals = {"BP": "112/72", "PR": "108 bpm", "RR": "19 cpm", "SpO2": "98% @ RA", "Temp": "101.8°F", "GRBS": "112 mg/dL"}
                    e_rx = ["Continue IV Artesunate protocol", "Monitor platelet count in morning"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity E11.65 Identified)"
                    m_narrative = "Patient reviewed by Dr. B. R. Ramachandra & Unit team. Rigors subsided, Temp 99.4°F. Routine morning glycemic check revealed severe hyperglycemia (GRBS: 326 mg/dL, stat venous glucose: 314 mg/dL). Patient reports previously unaddressed polydipsia, nocturia, and polyuria. Added Secondary Diagnosis: Type 2 Diabetes Mellitus with severe hyperglycemia (ICD-10: E11.65). Initiated Inj Human Actrapid regular insulin subcutaneous sliding scale. Activated Diabetic Chart (Form F/EPH/MRD/54). HbA1c sent."
                    m_vitals = {"BP": "122/80", "PR": "92 bpm", "RR": "18 cpm", "SpO2": "98% @ RA", "Temp": "99.4°F", "GRBS": "326 mg/dL"}
                    m_rx = ["Inj Artesunate 120mg IV OD (Day 2)", "Tab Primaquine 15mg 1-0-0 (G6PD confirmed normal)", "Inj Human Actrapid Subcutaneous sliding scale pre-meals", "Diabetic renal diet (1800 kcal)"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Post-actrapid GRBS controlled at 218 mg/dL. Patient reports significant relief from headache. Sclera appears mildly icteric. LFT and viral hepatitis serology ordered. Continue insulin sliding scale."
                    e_vitals = {"BP": "120/78", "PR": "86 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.8°F", "GRBS": "218 mg/dL"}
                    e_rx = ["Inj Human Actrapid 8U SC pre-dinner", "Tab Primaquine 15mg OD"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Viral Hepatitis B16.9 Liaison)"
                    m_narrative = "Reviewed by Consultant with Hepatology liaison. Persistent scleral icterus observed. Viral hepatitis serology panel returned: HBsAg REACTIVE (ICD-10: B16.9 - Acute Hepatitis B without delta-agent). Liver enzymes elevated: AST 148 U/L, ALT 152 U/L, Total Bilirubin 3.2 mg/dL. Platelets recovering to 98,000/µL. Added Tab Ursodeoxycholic acid 300mg BD. Barrier precautions and infection-control nursing guidelines enforced."
                    m_vitals = {"BP": "120/78", "PR": "84 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.6°F", "GRBS": "184 mg/dL"}
                    m_rx = ["Tab Primaquine 15mg OD (Day 3)", "Inj Human Actrapid 6U SC pre-meals", "Tab Ursodeoxycholic acid 300mg 1-0-1 post-food", "Tab Pan 40mg 1-0-0"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Repeat platelet count: 118,000/µL (improving). Patient tolerating oral diabetic soft diet well. Actrapid stepped down to low-dose regular insulin. Patient hemodynamically stable."
                    e_vitals = {"BP": "118/76", "PR": "80 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "162 mg/dL"}
                    e_rx = ["Continue Tab Ursodeoxycholic acid 300mg BD", "Tab Primaquine 15mg OD"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Patient afebrile for > 48 hours. Platelets 168,000/µL (normalized). Blood smear negative for malaria parasites. Glycemic control stable on oral hypoglycemics (Tab Metformin 500mg BD). Discharged with complete multi-morbidity advice and hepatology follow-up."
                    m_vitals = {"BP": "120/80", "PR": "76 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "140 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Post-Discharge Handover)"
                    e_narrative = "Discharge summary explained in Kannada and English to patient and attendant. Prescriptions handed over."
                    e_vitals = {"BP": "120/80", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "136 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "COPD_ACUTE_EXACERBATION":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with severe acute exacerbation of COPD (ICD-10: J44.1). Tachypneic (RR 26 cpm), SpO2 89% on room air. Coarse expiratory wheezing and prolonged expiration heard bilaterally. Started on supplemental oxygen via Venturi mask (FiO2 28%), Nebulization Duolin + Budecort Q4H, IV Hydrocortisone 100mg Q8H, and IV Levofloxacin 500mg OD."
                    m_vitals = {"BP": "130/80", "PR": "96 bpm", "RR": "26 cpm", "SpO2": "89% @ RA", "Temp": "99.1°F", "GRBS": "112 mg/dL"}
                    m_rx = ["Nebulization Duolin TDS", "Nebulization Budecort 0.5mg BD", "Inj Hydrocortisone 100mg IV Q8H", "Inj Levofloxacin 500mg IV OD"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Review)"
                    e_narrative = "Dyspnea partially relieved on O2 support. SpO2 93% with Venturi. Sputum tenacious and purulent. Sputum AFB and culture sent. Continue nebulization and steroid therapy."
                    e_vitals = {"BP": "132/82", "PR": "92 bpm", "RR": "24 cpm", "SpO2": "93% @ O2", "Temp": "98.6°F", "GRBS": "118 mg/dL"}
                    e_rx = ["Continue same bronchodilator protocol", "Chest physiotherapy SOS"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity J96.02 Identified)"
                    m_narrative = "Patient evaluated by Pulmonology team. Morning Arterial Blood Gas (ABG) shows severe hypercapnic respiratory acidosis: pH 7.30, PaCO2 58 mmHg, PaO2 59 mmHg, HCO3 28 mEq/L. Added Secondary Diagnosis: Acute Hypercapnic Respiratory Failure - Type II (ICD-10: J96.02). Initiated Non-Invasive Positive Pressure Ventilation (BiPAP: IPAP 12 cmH2O, EPAP 4 cmH2O) via full-face mask. Activated ABG and graphic respiratory monitoring protocol."
                    m_vitals = {"BP": "138/84", "PR": "88 bpm", "RR": "22 cpm", "SpO2": "92% @ BiPAP", "Temp": "98.6°F", "GRBS": "124 mg/dL"}
                    m_rx = ["BiPAP support IPAP 12 / EPAP 4 cmH2O", "Neb Duolin + Budecort alternating Q3H", "Inj Deriphyllin 2ml IV TDS", "Inj Hydrocortisone 100mg IV Q8H"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Repeat ABG on BiPAP: pH 7.35, PaCO2 48 mmHg (hypercapnia significantly improving). SpO2 maintained at 95%. Patient tolerating interface without skin breakdown. Taper BiPAP during meals."
                    e_vitals = {"BP": "130/80", "PR": "82 bpm", "RR": "20 cpm", "SpO2": "95% @ BiPAP", "Temp": "98.4°F", "GRBS": "116 mg/dL"}
                    e_rx = ["Continue intermittent BiPAP nocturnally", "Nebulization Duolin TDS"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity I27.9 Liaison)"
                    m_narrative = "Reviewed with Cardiology liaison. 2D Echocardiography reveals marked right ventricular hypertrophy with mild tricuspid regurgitation and estimated PASP 46 mmHg (ICD-10: I27.9 - Cor Pulmonale & Secondary Pulmonary Hypertension). Bilateral mild pitting pedal edema (+). Added Tab Torsemide 10mg OD. Weaned off daytime BiPAP to low-flow nasal cannula (2 L/min)."
                    m_vitals = {"BP": "124/78", "PR": "78 bpm", "RR": "18 cpm", "SpO2": "95% @ RA", "Temp": "98.4°F", "GRBS": "110 mg/dL"}
                    m_rx = ["Tab Torsemide 10mg 1-0-0 (B/F)", "Inhaler Foracort 200 (Budesonide+Formoterol) 2 puffs BD with spacer", "Tab Deriphyllin Retard 150mg 1-0-1", "Tab Pantoprazole 40mg 1-0-0"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Good diuresis established (urine output 1900 ml). Pedal edema subsided. Lungs clear with minimal basal rhonchi. Stable on room air without desaturation upon bedside ambulation."
                    e_vitals = {"BP": "120/76", "PR": "74 bpm", "RR": "18 cpm", "SpO2": "96% @ RA", "Temp": "98.4°F", "GRBS": "108 mg/dL"}
                    e_rx = ["Continue Tab Torsemide 10mg OD", "Inhaler Foracort 200 BD"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Patient hemodynamically stable. Dyspnea resolved to baseline mMRC-1. SpO2 96% on room air. ABG normal: pH 7.39, PaCO2 41 mmHg. Discharged with inhaler technique instructions, pneumococcal vaccination recommendation, and pulmonary rehabilitation advice."
                    m_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "96% @ RA", "Temp": "98.4°F", "GRBS": "106 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Discharge summary and metered dose inhaler technique demonstrated to patient. Follow-up booked in Chest Clinic."
                    e_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "96% @ RA", "Temp": "98.4°F", "GRBS": "106 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "DENGUE_FEVER":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with classic Dengue Fever with Severe Thrombocytopenia (ICD-10: A97.1). High fever (103°F), retro-orbital pain, petechial rash. Platelet count critically low at 44,000/µL, Hematocrit 46.5%. Dengue NS1 positive. Initiated strict WHO IV fluid replacement protocol with Ringer Lactate 100 ml/hr. Strictly avoid NSAIDs."
                    m_vitals = {"BP": "110/72", "PR": "108 bpm", "RR": "20 cpm", "SpO2": "98% @ RA", "Temp": "103.0°F", "GRBS": "98 mg/dL"}
                    m_rx = ["IV Ringer Lactate 100 ml/hr titrated", "Tab Paracetamol 650mg SOS for Temp > 100°F", "Inj Pantoprazole 40mg IV OD", "Q8H CBC monitoring"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Review)"
                    e_narrative = "Fever settling with paracetamol. Mild abdominal fullness reported. No overt bleeding manifestations, gums and stool normal. Urine output 1200 ml. Platelet count repeat: 42,000/µL."
                    e_vitals = {"BP": "112/70", "PR": "100 bpm", "RR": "20 cpm", "SpO2": "98% @ RA", "Temp": "100.8°F", "GRBS": "102 mg/dL"}
                    e_rx = ["Continue IV Ringer Lactate 75 ml/hr", "Strict bed rest"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity A97.2 Identified)"
                    m_narrative = "Consultant review with Dr. B. R. Ramachandra. Patient developed persistent severe abdominal pain, 3 episodes of non-bilious vomiting, and rising hematocrit (46.5% -> 49.5%), indicating active plasma leakage. Added Secondary Diagnosis: Dengue with Warning Signs & Capillary Leakage (ICD-10: A97.2). Bedside USG shows gall bladder wall edema and minimal free fluid in pelvis. Activated strict Fluid Balance Chart with hourly urine output."
                    m_vitals = {"BP": "106/68", "PR": "104 bpm", "RR": "22 cpm", "SpO2": "98% @ RA", "Temp": "99.2°F", "GRBS": "100 mg/dL"}
                    m_rx = ["IV Ringer Lactate increased to 125 ml/hr x 4 hrs then step down", "Inj Ondansetron 4mg IV TDS", "Inj Pantoprazole 40mg IV BD", "Serial Hct & Platelets Q6H"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Abdominal tenderness reduced. Hematocrit stabilized at 45.0%. Urine output maintained > 1 ml/kg/hr. Platelet count nadir reached: 38,000/µL without bleeding signs. Step down IV fluids."
                    e_vitals = {"BP": "112/74", "PR": "92 bpm", "RR": "19 cpm", "SpO2": "98% @ RA", "Temp": "98.6°F", "GRBS": "104 mg/dL"}
                    e_rx = ["IV Ringer Lactate stepped down to 75 ml/hr", "Oral ORS fluid encouragement"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity K72.0 Liaison)"
                    m_narrative = "Morning biochemistry panel reveals marked acute hepatic transaminitis: SGOT (AST) 168 U/L, SGPT (ALT) 132 U/L, Total Bilirubin 1.8 mg/dL. Added Secondary Diagnosis: Acute Dengue Hepatitis / Hepatic Transaminitis (ICD-10: K72.0). Added Tab Ursodeoxycholic acid 300mg BD for hepatoprotective support. Platelet count shows sharp upward recovery: 82,000/µL. Fluid leak stabilized."
                    m_vitals = {"BP": "116/76", "PR": "84 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "96 mg/dL"}
                    m_rx = ["Tab Ursodeoxycholic acid 300mg 1-0-1 post-food", "Taper IV fluids to 50 ml/hr", "Tab Paracetamol SOS only"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Patient feeling much better, appetite returning. Convalescent maculopapular rash with white islands of normal skin observed ('isles of white in a sea of red'). Repeat platelets: 112,000/µL. Discontinue IV line."
                    e_vitals = {"BP": "118/78", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "98 mg/dL"}
                    e_rx = ["Stop IV fluids, encourage oral fluids", "Tab Ursodeoxycholic acid 300mg BD"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Patient fully recovered. Afebrile for 72 hours. Platelet count normalized to 154,000/µL, Hematocrit stable at 40.5%. Liver enzymes improving. Tolerating normal diet. Fit for discharge."
                    m_vitals = {"BP": "120/80", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "96 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Discharge summary handed over. Instructions on hydration and fever warning signs provided."
                    e_vitals = {"BP": "120/80", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "96 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "TYPE2_DM_HYPERGLYCEMIA":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with severe uncontrolled hyperglycemia (ICD-10: E11.65, GRBS 412 mg/dL, HbA1c 12.8%). Severe polyuria, polydipsia, and bilateral lower extremity tingling. Urine ketones negative (no DKA). Initiated Subcutaneous regular insulin sliding scale (Inj Human Actrapid Q6H), IV Normal Saline hydration, and activated Diabetic Chart (Form F/EPH/MRD/54)."
                    m_vitals = {"BP": "140/90", "PR": "84 bpm", "RR": "18 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "412 mg/dL"}
                    m_rx = ["Inj Human Actrapid Subcutaneous sliding scale (14U stat)", "IV Normal Saline 0.9% 100 ml/hr", "Tab Metformin 500mg 1-0-1", "Diabetic renal diet (1800 kcal)"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Review)"
                    e_narrative = "Evening post-actrapid GRBS: 324 mg/dL. Actrapid 12U administered. Patient comfortable, hydration improved. Continue Q4H capillary glucose monitoring."
                    e_vitals = {"BP": "138/88", "PR": "82 bpm", "RR": "18 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "324 mg/dL"}
                    e_rx = ["Inj Human Actrapid 12U SC pre-dinner", "Tab Metformin 500mg"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity E11.42 Identified)"
                    m_narrative = "Morning rounds by Dr. B. R. Ramachandra. Fasting blood sugar 238 mg/dL. Comprehensive neuro-examination confirms bilateral symmetrical glove-and-stocking sensory deficit, absent ankle reflexes, and impaired 128Hz tuning fork vibration sense. Added Secondary Diagnosis: Diabetic Peripheral Sensorimotor Polyneuropathy (ICD-10: E11.42). Added neuro-regenerative therapy: Tab Pregabalin 75mg + Methylcobalamin 750mcg HS. Foot care education provided."
                    m_vitals = {"BP": "136/86", "PR": "80 bpm", "RR": "17 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "238 mg/dL"}
                    m_rx = ["Inj Human Actrapid 10U SC pre-meals", "Tab Pregabalin 75mg + Methylcobalamin (Pregaba-M) 0-0-1 (HS)", "Tab Metformin 500mg 1-0-1", "Diabetic foot inspection OD"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Post-prandial GRBS down to 218 mg/dL. Neuropathic burning dysesthesia in soles improved. Actrapid 8U given before dinner."
                    e_vitals = {"BP": "134/84", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "218 mg/dL"}
                    e_rx = ["Inj Human Actrapid 8U SC", "Tab Pregabalin 75mg HS"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity E11.22 Liaison)"
                    m_narrative = "Nephrology liaison review. Spot urine albumin-creatinine ratio returns significantly elevated at 195 mg/g (persistent microalbuminuria) with serum creatinine 1.1 mg/dL and Stage-1 hypertension (BP 150/94 mmHg). Added Tertiary Diagnosis: Diabetic Nephropathy with Persistent Microalbuminuria (ICD-10: E11.22). Added renoprotective therapy: Tab Telmisartan 40mg OD. Transitioning glycemic control from sliding scale to premix insulin."
                    m_vitals = {"BP": "150/94", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "168 mg/dL"}
                    m_rx = ["Tab Telmisartan 40mg 1-0-0", "Inj Human Mixtard 30/70 18U SC before breakfast, 12U before dinner", "Tab Metformin 500mg 1-0-1", "Tab Pregaba-M 0-0-1 HS"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Pre-dinner blood glucose 148 mg/dL. BP well controlled on Telmisartan (128/82 mmHg). Patient and attendant trained in self-injection insulin pen technique."
                    e_vitals = {"BP": "128/82", "PR": "76 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "148 mg/dL"}
                    e_rx = ["Inj Human Mixtard 12U SC pre-dinner", "Tab Pregaba-M HS"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Optimal glycemic control achieved: Fasting BS 114 mg/dL, Post-prandial BS 152 mg/dL. Neuropathic pain well controlled. Discharged on stable regimen with comprehensive diabetic diet sheet, kidney care advice, and glucometer log instructions."
                    m_vitals = {"BP": "124/80", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "132 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Prescriptions and insulin administration technique verified. Follow-up booked in Diabetic Clinic."
                    e_vitals = {"BP": "124/80", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "132 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "TERM_PREGNANCY_LSCS":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission & Delivery Rounds)"
                    m_narrative = "Patient admitted in active labor with previous LSCS scar (ICD-10: O82.0). Successful Emergency repeat Lower Segment Cesarean Section performed under subarachnoid block. Delivered live term female baby, weight 3.1 kg, cried immediately, Apgar 9/10. Hemostasis achieved, uterus well contracted, estimated blood loss 450 ml. Shifted to post-op recovery."
                    m_vitals = {"BP": "124/80", "PR": "92 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "94 mg/dL"}
                    m_rx = ["Inj Cefotaxime 1g IV BD", "Inj Metronidazole 100ml IV TDS", "Inj Tramadol 50mg IV in 100ml NS SOS", "IV DNS + RL 100 ml/hr", "Inj Oxytocin 10 IU in 500ml RL"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Post-Op Review)"
                    e_narrative = "Post-op vitals stable. Uterus well retracted to 20 weeks size. Locha rubra moderate, non-offensive. Foley's catheter draining clear urine (900 ml). Analgesia adequate. Infant initiated on early breastfeeding."
                    e_vitals = {"BP": "126/82", "PR": "86 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.6°F", "GRBS": "98 mg/dL"}
                    e_rx = ["Continue IV antibiotics and analgesics", "Perineal care Q8H"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity O13.9 Identified)"
                    m_narrative = "Reviewed by OBG Consultant. Foley's catheter removed. Patient mobilizing. Morning vitals demonstrate persistent elevated blood pressure (154/98 mmHg, repeat 152/96 mmHg) with mild bilateral pedal edema. Urine spot protein 1+ (non-pre-eclamptic). Added Secondary Diagnosis: Gestational / Postpartum Hypertension (ICD-10: O13.9). Initiated Tab Labetalol 100mg BD with serial Q4H BP charting. Surgical wound inspected: clean, dressing intact."
                    m_vitals = {"BP": "154/98", "PR": "84 bpm", "RR": "18 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "92 mg/dL"}
                    m_rx = ["Tab Labetalol 100mg 1-0-1 post-food", "Inj Cefotaxime 1g IV BD", "Tab Paracetamol 650mg TDS", "BP monitoring Q4H", "Clear liquid diet stepped to soft diet"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "BP reduced to 132/84 mmHg on Tab Labetalol. Passed flatus and urine freely. Lochia minimal. Infant active, passing meconium."
                    e_vitals = {"BP": "132/84", "PR": "80 bpm", "RR": "17 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "96 mg/dL"}
                    e_rx = ["Tab Labetalol 100mg BD", "Tab Cefixime 200mg BD"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity O92.2 Liaison)"
                    m_narrative = "Lactation and pediatric liaison rounds. Patient developed bilateral painful breast engorgement with delayed milk letdown and difficulty latching (ICD-10: O92.2 - Lactation Failure & Engorgement). Lactation consultant demonstrated warm fomentation, gentle manual expression, and proper latching posture. Administered Tab Metoclopramide 10mg BD. BP stable on Labetalol (126/80 mmHg)."
                    m_vitals = {"BP": "126/80", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.6°F", "GRBS": "90 mg/dL"}
                    m_rx = ["Tab Labetalol 100mg 1-0-1", "Tab Metoclopramide 10mg 1-0-1 x 3 days", "Tab Calcium + Vit D3 1-0-0", "Tab Iron (Autrin) 0-1-0", "Warm compress to bilateral breasts"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Breast engorgement relieved, infant latching satisfactorily on both sides. Surgical scar dressing dry and clean. Patient ambulating independently."
                    e_vitals = {"BP": "122/78", "PR": "76 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "92 mg/dL"}
                    e_rx = ["Continue Tab Labetalol 100mg BD", "Tab Calcium & Iron supplements"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Mother and baby fit for discharge. Pfannenstiel surgical incision healing by primary intention, no induration or discharge. BP normal (120/78 mmHg). Baby alert, thriving, birth immunization (BCG, OPV, Hep B-0) administered. Suture removal scheduled on Day 7."
                    m_vitals = {"BP": "120/78", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "90 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Discharge summary, newborn immunization card, and postnatal advice booklet handed over. Review in 7 days."
                    e_vitals = {"BP": "120/78", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "90 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "LUMBAR_SPONDYLOSIS":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with severe low back pain, muscle spasm, and restricted spine movements (ICD-10: M47.8). Pain score VAS 8/10. Tenderness over L4-L5 interspinous space. Straight Leg Raise (SLR) positive at 45° on right side. Started on IV analgesics (Inj Aceclofenac), muscle relaxants, and local cryotherapy. Urgent MRI Lumbar Spine ordered."
                    m_vitals = {"BP": "130/84", "PR": "82 bpm", "RR": "18 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "108 mg/dL"}
                    m_rx = ["Inj Aceclofenac 100mg IM BD", "Tab Tizanidine 2mg 1-0-1", "Tab Pantoprazole 40mg 1-0-0", "Strict hard-bed rest", "MRI L-S Spine"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Review)"
                    e_narrative = "Acute spasm reducing. MRI completed. Pain score VAS 6/10. No bowel or bladder incontinence. Deep tendon reflexes intact."
                    e_vitals = {"BP": "128/80", "PR": "80 bpm", "RR": "17 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "104 mg/dL"}
                    e_rx = ["Continue analgesics", "Apply Nanofast gel locally"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity M54.16 Identified)"
                    m_narrative = "Reviewed by Orthopedic Consultant with MRI report: L4-L5 right paracentral disc protrusion compressing the right L5 nerve root. Physical exam demonstrates Right L5 Compressive Radiculopathy (ICD-10: M54.16) with sensory blunting over right lateral leg and mild extensor hallucis longus weakness (Grade 4/5). Added neuropathic pain modulator: Tab Pregabalin 75mg + Methylcobalamin 750mcg HS. Fitted with semi-rigid Lumbosacral belt for mobilization."
                    m_vitals = {"BP": "124/80", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "106 mg/dL"}
                    m_rx = ["Tab Zerodol-MR (Aceclofenac + Tizanidine) 1-0-1", "Tab Pregabalin 75mg + Methylcobalamin (Pregaba-M) 0-0-1 (HS)", "Lumbosacral corset belt fitting", "Physiotherapy gentle isometric back exercises"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Patient ambulated to washroom with LS belt support. Radicular shooting pain significantly alleviated (VAS 4/10). No sensory deterioration."
                    e_vitals = {"BP": "122/78", "PR": "76 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "102 mg/dL"}
                    e_rx = ["Tab Pregaba-M 0-0-1 HS", "Nanofast gel TDS"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity M81.0 Liaison)"
                    m_narrative = "Bone & Mineral density screening review. Dual Energy X-Ray Absorptiometry (DXA) reveals severe Postmenopausal Osteoporosis (ICD-10: M81.0, T-score -2.9 at femoral neck and -3.1 at lumbar spine). Added aggressive anti-osteoporotic therapy: Tab Shelcal-XT (Calcium 500mg + Calcitriol + Vit D3), and scheduled for IV Zoledronic acid 5mg infusion following baseline renal check."
                    m_vitals = {"BP": "120/78", "PR": "74 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "100 mg/dL"}
                    m_rx = ["Tab Shelcal-XT 0-1-0 post-food x 3 months", "Tab Pregaba-M 0-0-1 HS", "Tab Zerodol-MR 1-0-1 post-food", "Physiotherapy: Core strengthening & posture training"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Ambulation comfortable with LS belt. Posture improved. Tolerating oral calcium and pain regimen without epigastric distress."
                    e_vitals = {"BP": "120/76", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "102 mg/dL"}
                    e_rx = ["Continue oral regimen", "LS belt during ambulation"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Patient ready for discharge. Back pain subsided to VAS 2/10. Radicular sensory symptoms resolved. SLR negative up to 75°. Mobilizing independently with lumbosacral support. Discharged with ergonomic lifestyle instructions and osteoporosis home management."
                    m_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "98 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Discharge summary explained. Spinal precautions (no forward bending, no lifting > 5kg) advised."
                    e_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "98 mg/dL"}
                    e_rx = ["Discharged"]

            elif profile_key == "BACTERIAL_PNEUMONIA":
                if day_count == 1:
                    m_label = f"C/S/B {patient.department} (Day 1 Admission Rounds)"
                    m_narrative = "Patient admitted with Community-Acquired Lobar Bacterial Pneumonia of Right Lower Lobe (ICD-10: J18.1). High fever (102.8°F), rust-colored purulent sputum, pleuritic right chest pain. Auscultation reveals bronchial breath sounds and coarse crackles over right base. CXR confirms dense RLL consolidation. CRP markedly elevated (68.4 mg/L). Initiated on IV Ceftriaxone 1g BD + Tab Azithromycin 500mg OD."
                    m_vitals = {"BP": "126/82", "PR": "102 bpm", "RR": "24 cpm", "SpO2": "92% @ RA", "Temp": "102.8°F", "GRBS": "118 mg/dL"}
                    m_rx = ["Inj Ceftriaxone 1g IV BD in 100ml NS", "Tab Azithromycin 500mg 1-0-0", "Nebulization Duolin TDS", "Inj Paracetamol 1g IV SOS", "O2 via nasal prongs at 2 L/min"]

                    e_label = f"C/S/B {patient.department} (Day 1 Evening Review)"
                    e_narrative = "Fever spiking to 101.4°F controlled with paracetamol. SpO2 96% on 2 L/min O2. Sputum Gram stain shows Gram-positive diplococci (Streptococcus pneumoniae). Continue dual IV coverage."
                    e_vitals = {"BP": "124/80", "PR": "96 bpm", "RR": "22 cpm", "SpO2": "96% @ O2", "Temp": "101.4°F", "GRBS": "122 mg/dL"}
                    e_rx = ["Continue IV Ceftriaxone + Azithromycin", "Chest physiotherapy"]
                elif day_count == 2:
                    m_label = f"C/S/B {patient.department} (Day 2 Rounds - Comorbidity J90 Identified)"
                    m_narrative = "Consultant review with Dr. Gayatri Devi. Right basal dullness to percussion noted. Bedside thoracic ultrasound confirms reactive Parapneumonic Pleural Effusion (ICD-10: J90) with 150ml fluid in right costophrenic angle. Diagnostic pleural fluid aspiration performed: clear exudative fluid, WBC 1800, gram stain negative, pH 7.38 (non-purulent, non-loculated). Managed conservatively with targeted antibiotic continuation."
                    m_vitals = {"BP": "122/78", "PR": "90 bpm", "RR": "20 cpm", "SpO2": "95% @ RA", "Temp": "99.6°F", "GRBS": "130 mg/dL"}
                    m_rx = ["Continue Inj Ceftriaxone 1g IV BD", "Tab Azithromycin 500mg OD (Day 2)", "Nebulization Duolin TDS", "Incentive spirometry Q2H"]

                    e_label = f"C/S/B {patient.department} (Day 2 Evening Review)"
                    e_narrative = "Pleuritic chest pain resolving. Sputum expectoration easier with spirometry. SpO2 maintained at 96% on room air."
                    e_vitals = {"BP": "120/76", "PR": "84 bpm", "RR": "19 cpm", "SpO2": "96% @ RA", "Temp": "98.8°F", "GRBS": "128 mg/dL"}
                    e_rx = ["Continue same antibiotic protocol", "Monitor effusion clinically"]
                elif day_count == 3:
                    m_label = f"C/S/B {patient.department} (Day 3 Rounds - Comorbidity R73.09 Liaison)"
                    m_narrative = "Morning metabolic screen reveals persistent Stress-Induced Hyperglycemia (ICD-10: R73.09, GRBS 228 mg/dL, Fasting venous glucose: 212 mg/dL) secondary to severe acute systemic infection and stress response. Initiated short-term Subcutaneous regular insulin sliding scale coverage (Inj Human Actrapid) to facilitate infection clearance and neutrophil function. Activated Diabetic Monitoring Chart."
                    m_vitals = {"BP": "120/76", "PR": "80 bpm", "RR": "18 cpm", "SpO2": "97% @ RA", "Temp": "98.4°F", "GRBS": "228 mg/dL"}
                    m_rx = ["Inj Human Actrapid SC sliding scale (6U stat)", "Inj Ceftriaxone 1g IV BD (Day 3)", "Tab Azithromycin 500mg OD (Day 3)", "Diabetic soft diet (1800 kcal)"]

                    e_label = f"C/S/B {patient.department} (Day 3 Evening Review)"
                    e_narrative = "Post-actrapid GRBS down to 158 mg/dL. Patient afebrile for 24 hours. Crackles over right base markedly decreased. Repeat CRP down to 24.2 mg/L."
                    e_vitals = {"BP": "118/74", "PR": "76 bpm", "RR": "17 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "158 mg/dL"}
                    e_rx = ["Inj Human Actrapid 4U SC pre-dinner", "Continue IV antibiotics"]
                else:
                    m_label = f"C/S/B {patient.department} (Day 4 Discharge Fitness Review)"
                    m_narrative = "Patient afebrile for 48 hours. Lung fields clear, resolution of bronchial breathing. Repeat CXR shows significant clearing of consolidation and resolution of reactive effusion. Glycemia normalized without insulin (GRBS 118 mg/dL). Switched to oral Cefuroxime for step-down completion. Discharged home fit."
                    m_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "98% @ RA", "Temp": "98.4°F", "GRBS": "118 mg/dL"}
                    m_rx = profile["medications_discharge"]

                    e_label = f"C/S/B {patient.department} (Day 4 Discharge Handover)"
                    e_narrative = "Discharge summary handed over. Step-down oral antibiotics course explained. Chest clinic review in 7 days."
                    e_vitals = {"BP": "120/80", "PR": "72 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F", "GRBS": "118 mg/dL"}
                    e_rx = ["Discharged"]

            else:
                m_label = f"C/S/B {patient.department} (Day {day_count} Morning Rounds)"
                m_narrative = f"Patient reviewed. Symptoms {'subsiding' if day_count > 1 else 'present'}. Tolerating soft diet, afebrile."
                m_vitals = {
                    "BP": profile["vitals_admission"]["bp"],
                    "PR": f"{pr_val} bpm",
                    "RR": f"{max(16, int(profile['vitals_admission']['rr']) - day_count)} cpm",
                    "SpO2": f"{min(99, int(profile['vitals_admission']['spo2']) + day_count)}% @ RA",
                    "Temp": f"{temp_val}°F",
                    "GRBS": profile["vitals_admission"]["grbs"]
                }
                m_rx = profile["medications_inpatient"]

                e_label = f"C/S/B {patient.department} (Day {day_count} Evening Rounds)"
                e_narrative = "Case reviewed with on-duty registrar. Hemodynamically stable. Continue prescribed medications."
                e_vitals = {
                    "BP": profile["vitals_admission"]["bp"],
                    "PR": f"{pr_val} bpm",
                    "RR": "18 cpm",
                    "SpO2": "98% @ RA",
                    "Temp": "98.4°F",
                    "GRBS": profile["vitals_admission"]["grbs"]
                }
                e_rx = ["Continue same treatment"]

            # Morning Round (approx 8:30 AM)
            m_time = note_cursor.replace(hour=8, minute=random.randint(15, 45))
            if admission_time <= m_time:
                progress_notes.append(
                    ProgressNote(
                        id=f"NOTE-{patient.id}-D{day_count}-M",
                        patient_id=patient.id,
                        timestamp=m_time,
                        round_label=m_label,
                        clinical_narrative=m_narrative,
                        vitals=m_vitals,
                        systemic_notes={
                            "CVS": "S1 S2 heard",
                            "RS": "Bilateral air entry adequate",
                            "P/A": "Soft, non-tender",
                            "CNS": "Conscious, oriented"
                        },
                        prescriptions_ordered=m_rx,
                        lab_radiology_orders=["Review investigations", "Monitor vitals Q4H"],
                        attending_doctor=patient.attending_doctor,
                        doctor_reg_no=patient.doctor_reg_no
                    )
                )

            # Evening Round (approx 5:30 PM)
            e_time = note_cursor.replace(hour=17, minute=random.randint(15, 45))
            if admission_time <= e_time:
                progress_notes.append(
                    ProgressNote(
                        id=f"NOTE-{patient.id}-D{day_count}-E",
                        patient_id=patient.id,
                        timestamp=e_time,
                        round_label=e_label,
                        clinical_narrative=e_narrative,
                        vitals=e_vitals,
                        systemic_notes={
                            "CVS": "S1 S2 heard",
                            "RS": "NVBS",
                            "P/A": "Soft",
                            "CNS": "Conscious"
                        },
                        prescriptions_ordered=e_rx,
                        lab_radiology_orders=["Monitor urine output and vitals"],
                        attending_doctor=patient.attending_doctor,
                        doctor_reg_no=patient.doctor_reg_no
                    )
                )

            note_cursor += timedelta(days=1)
            day_count += 1

        # 3. Lab Reports (Biochemistry, Microbiology, Pathology)
        lab_reports = []
        lab_time = admission_time + timedelta(hours=3)
        # Pathology CBC
        if "pathology" in profile:
            lab_reports.append(
                LabReport(
                    id=f"LAB-PATH-{patient.id}",
                    patient_id=patient.id,
                    department="Pathology",
                    sample_id=f"EDTA-{random.randint(10000, 99999)}",
                    sample_type="Whole Blood (EDTA)",
                    collected_at=admission_time + timedelta(minutes=45),
                    reported_at=lab_time,
                    test_category=profile["pathology"]["category"],
                    items=[LabTestItem(**item) for item in profile["pathology"]["items"]],
                    clinical_impression=f"Compatible with {profile['disease_name']}"
                )
            )

        # Biochemistry
        if "biochemistry" in profile:
            lab_reports.append(
                LabReport(
                    id=f"LAB-BIO-{patient.id}",
                    patient_id=patient.id,
                    department="Biochemistry",
                    sample_id=f"SERUM-{random.randint(10000, 99999)}",
                    sample_type="Serum",
                    collected_at=admission_time + timedelta(minutes=50),
                    reported_at=lab_time + timedelta(minutes=20),
                    test_category=profile["biochemistry"]["category"],
                    items=[LabTestItem(**item) for item in profile["biochemistry"]["items"]],
                    clinical_impression="Correlate clinically with glycemic and metabolic status."
                )
            )

        # Microbiology
        if "microbiology" in profile:
            lab_reports.append(
                LabReport(
                    id=f"LAB-MIC-{patient.id}",
                    patient_id=patient.id,
                    department="Microbiology",
                    sample_id=f"MIC-{random.randint(10000, 99999)}",
                    sample_type="Serum / Smear",
                    collected_at=admission_time + timedelta(minutes=60),
                    reported_at=lab_time + timedelta(minutes=40),
                    test_category=profile["microbiology"]["category"],
                    items=[LabTestItem(**item) for item in profile["microbiology"]["items"]],
                    clinical_impression="Report verified by Microbiologist."
                )
            )

        # 4. Radiology / PACS Study
        radiology_study = None
        if profile.get("radiology_required"):
            rad_time = admission_time + timedelta(hours=4)
            rad_info = profile["radiology_details"]
            radiology_study = RadiologyStudy(
                id=f"RAD-{patient.id}",
                patient_id=patient.id,
                accession_no=f"ACC-{random.randint(100000, 999999)}",
                study_datetime=rad_time,
                modality=rad_info["modality"],
                body_part=rad_info["body_part"],
                study_description=rad_info["study_description"],
                ordering_doctor=patient.attending_doctor,
                findings=rad_info["findings"],
                impression=rad_info["impression"],
                instances=[
                    DicomInstance(
                        sop_instance_uid=f"1.2.840.10008.5.1.4.1.1.{random.randint(10000, 99999)}",
                        instance_number=1,
                        image_url=f"/api/pacs/images/{profile_key.lower()}_sample.png",
                        modality=rad_info["modality"],
                        window_center=40,
                        window_width=400
                    )
                ]
            )

        # 5. Medication Administration Sheet (F/EPH/MRD/58)
        med_sheets = []
        for drug in profile["medications_inpatient"]:
            med_sheets.append(
                MedicationAdministration(
                    patient_id=patient.id,
                    drug_name=drug.split(" ")[1] if " " in drug else drug,
                    dosage="Standard",
                    route="IV" if "IV" in drug else "Oral",
                    frequency="1-0-1",
                    start_date=admission_time.strftime("%d/%m/%Y")
                )
            )

        # 6. Diabetic Chart (F/EPH/MRD/54) - If Diabetic or Comorbidity E11.65 Detected
        diabetic_entries = []
        if profile_key == "TYPE2_DM_HYPERGLYCEMIA":
            d_times = [
                admission_time + timedelta(hours=1),
                admission_time + timedelta(hours=5),
                admission_time + timedelta(hours=9),
                admission_time + timedelta(hours=14)
            ]
            grbs_seq = [412, 324, 260, 218]
            doses = [14, 12, 10, 8]
            for dt, grbs, dose in zip(d_times, grbs_seq, doses):
                diabetic_entries.append(
                    DiabeticChartEntry(
                        id=f"DM-{patient.id}-{dt.strftime('%H%M')}",
                        patient_id=patient.id,
                        timestamp=dt,
                        blood_sugar_grbs=grbs,
                        insulin_medication="Inj H. Actrapid",
                        dose_units=dose,
                        route="Subcutaneous",
                        nurse_signature="Nurse Shanti (Reg: 4102)"
                    )
                )
        elif profile_key == "MALARIA_PV":
            # Multi-ICD comorbidity regular insulin monitoring starting Day 2
            d_times = [
                admission_time + timedelta(hours=25), # Day 2 08:30 AM
                admission_time + timedelta(hours=30), # Day 2 01:30 PM
                admission_time + timedelta(hours=36), # Day 2 07:30 PM
                admission_time + timedelta(hours=49), # Day 3 08:30 AM
                admission_time + timedelta(hours=55)  # Day 3 02:30 PM
            ]
            grbs_seq = [326, 268, 218, 174, 152]
            doses = [14, 10, 8, 6, 4]
            for dt, grbs, dose in zip(d_times, grbs_seq, doses):
                diabetic_entries.append(
                    DiabeticChartEntry(
                        id=f"DM-{patient.id}-{dt.strftime('%H%M')}",
                        patient_id=patient.id,
                        timestamp=dt,
                        blood_sugar_grbs=grbs,
                        insulin_medication="Inj H. Actrapid (Regular Insulin)",
                        dose_units=dose,
                        route="Subcutaneous",
                        nurse_signature="Nurse Priya (Reg: 4892)"
                    )
                )

        elif profile_key == "BACTERIAL_PNEUMONIA":
            # Stress-induced hyperglycemia sliding scale monitoring starting Day 3
            d_times = [
                admission_time + timedelta(hours=49), # Day 3 08:30 AM
                admission_time + timedelta(hours=55), # Day 3 02:30 PM
                admission_time + timedelta(hours=61), # Day 3 08:30 PM
                admission_time + timedelta(hours=73)  # Day 4 08:30 AM
            ]
            grbs_seq = [228, 178, 142, 118]
            doses = [6, 4, 2, 0]
            for dt, grbs, dose in zip(d_times, grbs_seq, doses):
                diabetic_entries.append(
                    DiabeticChartEntry(
                        id=f"DM-{patient.id}-{dt.strftime('%H%M')}",
                        patient_id=patient.id,
                        timestamp=dt,
                        blood_sugar_grbs=grbs,
                        insulin_medication="Inj H. Actrapid (Regular Insulin)",
                        dose_units=dose,
                        route="Subcutaneous",
                        nurse_signature="Nurse Shanti (Reg: 4102)"
                    )
                )

        # 7. Graphic TPR Chart (F/MRD/EPH/07)
        tpr_readings = []
        slots = ["06:00", "10:00", "14:00", "18:00", "22:00", "02:00"]
        tpr_cursor = admission_time
        day_idx = 1
        while day_idx <= 4:
            for s in slots:
                hour_part = int(s.split(":")[0])
                reading_dt = tpr_cursor.replace(hour=hour_part, minute=0)
                if admission_time <= reading_dt:
                    tpr_readings.append(
                        TPRReading(
                            timestamp=reading_dt,
                            day_no=day_idx,
                            slot_label=s,
                            temp_f=float(profile["vitals_admission"]["temp"]) - (day_idx * 0.4) + random.uniform(-0.3, 0.3),
                            pulse_bpm=int(profile["vitals_admission"]["pr"]) - (day_idx * 5) + random.randint(-4, 4),
                            resp_cpm=max(16, int(profile["vitals_admission"]["rr"]) - day_idx + random.randint(-1, 1))
                        )
                    )
            tpr_cursor += timedelta(days=1)
            day_idx += 1

        tpr_chart = GraphicTPRChart(patient_id=patient.id, readings=tpr_readings)

        # 8. Discharge Summary (EPH/DISCHARGE/01) - Generated for complete stay, filtered by timeline
        discharge_summary = None
        if patient.discharge_time:
            # Determine secondary diagnoses dynamically with multi-ICD progression
            sec_diagnoses = ["None"]
            if profile_key == "MALARIA_PV":
                sec_diagnoses = [
                    "Type 2 Diabetes Mellitus with Severe Hyperglycemia - Newly Detected (ICD-10: E11.65)",
                    "Acute Hepatitis B Viral Infection without delta-agent (ICD-10: B16.9)",
                    "Secondary Severe Thrombocytopenia - Resolved (ICD-10: D69.6)"
                ]
            elif profile_key == "COPD_ACUTE_EXACERBATION":
                sec_diagnoses = [
                    "Acute Hypercapnic Respiratory Failure - Type II (ICD-10: J96.02)",
                    "Cor Pulmonale & Secondary Pulmonary Hypertension (ICD-10: I27.9)",
                    "Chronic Nicotine Dependence (ICD-10: F17.210)"
                ]
            elif profile_key == "DENGUE_FEVER":
                sec_diagnoses = [
                    "Dengue with Warning Signs & Plasma Capillary Leakage (ICD-10: A97.2)",
                    "Acute Dengue Hepatitis / Hepatic Transaminitis (ICD-10: K72.0)",
                    "Severe Thrombocytopenia - Recovered (ICD-10: D69.6)"
                ]
            elif profile_key == "TYPE2_DM_HYPERGLYCEMIA":
                sec_diagnoses = [
                    "Diabetic Peripheral Sensorimotor Polyneuropathy (ICD-10: E11.42)",
                    "Diabetic Nephropathy with Persistent Microalbuminuria (ICD-10: E11.22)",
                    "Essential Hypertension Stage-1 (ICD-10: I10)"
                ]
            elif profile_key == "TERM_PREGNANCY_LSCS":
                sec_diagnoses = [
                    "Previous Cesarean Delivery Scar in Uterus (ICD-10: O34.2)",
                    "Gestational / Postpartum Hypertension (ICD-10: O13.9)",
                    "Postpartum Lactation Failure & Engorgement (ICD-10: O92.2)"
                ]
            elif profile_key == "LUMBAR_SPONDYLOSIS":
                sec_diagnoses = [
                    "Right L5 Compressive Radiculopathy (ICD-10: M54.16)",
                    "Severe Postmenopausal Osteoporosis without pathological fracture (ICD-10: M81.0)"
                ]
            elif profile_key == "BACTERIAL_PNEUMONIA":
                sec_diagnoses = [
                    "Reactive Parapneumonic Pleural Effusion (ICD-10: J90)",
                    "Transient Stress-Induced Hyperglycemia (ICD-10: R73.09)"
                ]
            elif profile_key == "GADEMMA_AUB":
                sec_diagnoses = [
                    "Endometrial Hyperplasia without atypia (ICD-10: N85.0)",
                    "Microcytic Hypochromic Iron Deficiency Anemia (ICD-10: D50.9)"
                ]
            elif profile_key == "MARY_STELLA_ANC":
                sec_diagnoses = [
                    "Gestational Hypothyroidism on replacement therapy (ICD-10: O99.284)",
                    "Physiological Edema of Pregnancy (ICD-10: O12.0)"
                ]
            elif profile_key == "BHARATH_TBI":
                sec_diagnoses = [
                    "Right Parietal Scalp Contused Lacerated Wound - Sutured (ICD-10: S01.01XA)",
                    "Post-Traumatic Cephalea (ICD-10: G44.3)"
                ]
            elif profile_key == "NAGARAJA_SDH":
                sec_diagnoses = [
                    "Transient Secondary Left Hemiparesis - Resolved (ICD-10: G81.92)",
                    "Essential Hypertension Stage-1 (ICD-10: I10)"
                ]
            elif profile_key == "ANIL_KUMAR_FRACTURE":
                sec_diagnoses = [
                    "Right Knee Traumatic Hemarthrosis (ICD-10: M25.061)",
                    "Right Lower Extremity Contusion (ICD-10: S80.01XA)"
                ]
            elif profile_key == "MUNI_NARAYANAPPA_ANKLE":
                sec_diagnoses = [
                    "Dislocation of Right Ankle Joint - Reduced (ICD-10: S93.001A)",
                    "Type 2 Diabetes Mellitus - Controlled (ICD-10: E11.9)"
                ]

            proc_list = ["Conservative inpatient medical management"]
            if profile_key == "TERM_PREGNANCY_LSCS":
                proc_list = ["Emergency LSCS under spinal anaesthesia"]
            elif profile_key == "GADEMMA_AUB":
                proc_list = ["Diagnostic & Therapeutic Dilatation and Curettage (D&C)", "Endometrial Biopsy"]
            elif profile_key == "BHARATH_TBI":
                proc_list = ["Neuro-ICU Protocol & Cerebral Anti-Edema Therapy", "Scalp Laceration Debridement & Primary Closure"]
            elif profile_key == "NAGARAJA_SDH":
                proc_list = ["Emergency Right Fronto-Parietal Burr-Hole Craniostomy & Evacuation of Chronic Subdural Hematoma", "Subdural Closed Suction Drain Placement"]
            elif profile_key == "ANIL_KUMAR_FRACTURE":
                proc_list = ["Open Reduction and Internal Fixation (ORIF) Right Patella with Modified Tension Band Wiring (TBW) under Spinal Anaesthesia"]
            elif profile_key == "MUNI_NARAYANAPPA_ANKLE":
                proc_list = ["Open Reduction and Internal Fixation (ORIF) Right Ankle (Distal Fibula Plate + Medial Malleolus Screw Fixation) under Spinal Anaesthesia"]
            elif profile_key == "MARY_STELLA_ANC":
                proc_list = ["High-Risk Antenatal Fetal Surveillance & Biophysical Profile", "Obstetric Doppler Ultrasound"]

            discharge_summary = DischargeSummary(
                patient_id=patient.id,
                discharge_timestamp=patient.discharge_time,
                final_diagnosis=profile["disease_name"],
                icd10_code=profile["icd10"],
                secondary_diagnoses=sec_diagnoses,
                procedures_done=proc_list,
                clinical_summary_course=f"Patient admitted with {profile['disease_name']}. Evaluated thoroughly with relevant lab and radiological investigations. Treated as per standard hospital protocols. Responded well to medical therapy. Afebrile and hemodynamically stable at the time of discharge.",
                condition_at_discharge="Recovered & Hemodynamically Stable",
                discharge_vitals={
                    "BP": "120/80 mmHg",
                    "PR": "74 bpm",
                    "RR": "16 cpm",
                    "SpO2": "99% on Room Air",
                    "Temp": "98.4°F"
                },
                medications_prescribed=profile["medications_discharge"],
                diet_lifestyle_advice="Normal diabetic/balanced diet, adequate fluid intake, avoid heavy weight lifting.",
                follow_up_date=(patient.discharge_time + timedelta(days=7)).strftime("%d/%m/%Y"),
                attending_consultant=patient.attending_doctor,
                consultant_reg=patient.doctor_reg_no
            )

        return {
            "patient": patient,
            "opd_slip": opd_slip,
            "hp_exam": hp_exam,
            "progress_notes": progress_notes,
            "lab_reports": lab_reports,
            "radiology_study": radiology_study,
            "medication_sheets": med_sheets,
            "diabetic_entries": diabetic_entries,
            "tpr_chart": tpr_chart,
            "discharge_summary": discharge_summary
        }
