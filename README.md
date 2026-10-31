# East Point Hospital - Automated Electronic Medical Record (EMR) System
### Proof of Concept (POC) for NMC 2025 Audit Compliance & ABDM Gateways

Engineered for **Dr. M N Faruk, East Point Hospital & Research Centre**, Bangalore.

---

## 🌟 Executive Summary & Implementation Status

This POC delivers a turnkey, mathematically and medically sound automated EMR system built directly from the physical hospital case sheets procured from East Point Hospital:

1. **Phase 1: Structural Extraction & Departmental Schema**
   - Modeled after the 5 actual inpatient hard copies:
     - `Devendra medicine.pdf` (OBG - Term Pregnancy / Emergency LSCS)
     - `Narasimhapa Medicine.pdf` (General Medicine - Type 2 DM Hyperglycemia)
     - `Shanthamma Medicine.pdf` (Respiratory Medicine - COPD Exacerbation)
     - `Venkateshappa medicine.pdf` (General Medicine / Pulmonology)
     - `Subbamma Medicine.pdf` (General Medicine / Orthopedics - Lumbar Spondylosis)
   - Extracted authentic East Point Hospital Form IDs:
     - **Admission Record** (`AB_ARK Insurance/Cashless`, Kannada & English consent)
     - **Form F/EPH/MRD/39**: Inpatient History & Physical Examination
     - **Form F/MRD/EPH/40**: Doctor's Progress Notes & Multi-Day Clinical Notes
     - **Form F/EPH/MRD/58**: Medication Administration Sheet (Nurse Shift Grid)
     - **Form F/EPH/MRD/54**: Diabetic Chart (GRBS & Subcutaneous Actrapid Insulin)
     - **Form F/MRD/EPH/07**: Graphic TPR Chart (Temperature, Pulse, Respiration)
     - **Form EPH/LAB/02**: Diagnostic Clinical Laboratory Reports
     - **Form EPH/DISCHARGE/01**: Official Discharge Summary

2. **Phase 2: Logic Mapping & Clinical Integrity Engine**
   - Strict ICD-10 clinical bindings:
     - **Malaria (B51.9)**: Fever with rigors $\rightarrow$ Thrombocytopenia (low platelets) $\rightarrow$ Antimalarial IV Artesunate / Primaquine Rx.
     - **Type 2 DM (E11.65)**: High GRBS (412 mg/dL) & HbA1c (12.8%) $\rightarrow$ Actrapid sliding scale insulin $\rightarrow$ Diabetic Chart monitoring.
     - **COPD Exacerbation (J44.1)**: Dyspnea mMRC-3, wheezing $\rightarrow$ Hyperinflated Chest X-Ray $\rightarrow$ Duolin/Budecort nebulization + Augmentin.
     - **Bacterial Pneumonia (J18.9)**: High fever $\rightarrow$ Leukocytosis (16,400 WBC) $\rightarrow$ Lobar consolidation $\rightarrow$ Ceftriaxone IV.
     - **Dengue (A97.1)**: Retro-orbital pain $\rightarrow$ Severe thrombocytopenia (44,000/µL) + NS1 positive $\rightarrow$ IV fluids (Strictly NO NSAIDs).
     - **Term Pregnancy (O82.0)**: Active labour with previous LSCS $\rightarrow$ Pre-op coagulation screen $\rightarrow$ Emergency LSCS delivery.
     - **Lumbar Spondylosis (M51.2)**: SLRT positive $\rightarrow$ MRI LS Spine disc protrusion $\rightarrow$ Zerodol-MR + Pregabalin.
   - Zero-contradiction sanitizer prevents medical anomalies or gender/age mismatches.

3. **Phase 3: "Auto EMR" Batch Engine & Live Timeline Logic**
   - **1,800 Records Daily Quota Engine**: Synthesizes 1,500 OPD footfall + 300 IPD active admissions across 18 medical college departments.
   - **Live Chronological Hospital Flow Simulator**:
     - At **07:30 AM**: Only admission case sheets exist.
     - At **10:00 AM**: Day 1 morning consultant rounds unlocked.
     - At **01:00 PM (NMC Mid-Day Audit)**: Morning rounds and lab tests visible; discharge summaries strictly suppressed.
     - At **07:00 PM**: Evening progress notes unlocked.
     - At **09:30 PM**: Discharge summaries, take-home prescriptions, and follow-ups unlocked.

4. **Phase 4: Digitized Audit Trail & PACS Integration**
   - **Automated PDF Generator (ReportLab)**: Generates printable, high-fidelity PDFs for Case Sheets, Lab Reports, and Discharge Summaries.
   - **PACS / DICOM Viewer Module**: Digital radiological viewer with Window Level / Window Width (WW/WL), Zoom, Pan, Invert, and patient metadata overlay.

5. **Phase 5: ABDM API Workflows Simulation**
   - **M1 (Identity)**: Aadhaar/Mobile OTP flow issuing verifiable ABHA IDs (`91-XXXX-XXXX-XXXX`, `@abdm`, QR code).
   - **M2 (Information Provider - HIP)**: HL7 FHIR R4 JSON document generator (`DiagnosticReportRecord` bundle with Composition, Patient, Practitioner, Organization, Observation).
   - **M3 (Information User - HIU)**: Interactive Physician Consent Pop-Up simulator fetching external hospital records.

---

## 🚀 Quick Start Guide

### 1. Launch EMR Server (One Command)
```bash
./start_emr.sh
```
Or manually:
```bash
source .venv/bin/activate
export PYTHONPATH=backend
uvicorn app.main:app --host 127.0.0.1 --port 8050 --reload
```

### 2. Access the Applications
- **EMR Web Dashboard**: [http://localhost:8050](http://localhost:8050)
- **Interactive OpenAPI / Swagger Docs**: [http://localhost:8050/docs](http://localhost:8050/docs)

### 3. Frontend Development Mode (Optional)
If you wish to modify the React frontend with Vite Hot Reloading:
```bash
cd frontend
npm run dev
# Vite runs on http://localhost:3000 and proxies /api to http://localhost:8050
```

---

## 🩺 Demo Walkthrough for Hospital Administrators & NMC Auditors

1. **Verify NMC 1,800 Quota**:
   - Open [http://localhost:8050](http://localhost:8050)
   - Click the **"NMC Audit (1,800 Quota)"** station tab.
   - Notice the green compliance badge: **1,800 / 1,800 Quota (100% Compliant)**.
   - Review the department breakdown across the 18 NMC clinical departments.

2. **Test Live Timeline Logic**:
   - Look at the **Simulated Audit Clock** in the top navbar.
   - Click the red **"01:00 PM (Audit)"** button.
   - Switch to the **Doctor Station** and scroll to the bottom:
     - Notice the warning box: *"Patient Actively In Hospital (Status: IPD_ACTIVE). In compliance with 2025 NMC audit guidelines, discharge summaries cannot be dumped mid-day before discharge order is signed."*
   - Click **"09:30 PM"** in the navbar:
     - Immediately notice the discharge summary unlocks with take-home prescriptions, and the **"Download Discharge PDF"** button appears!

3. **Inspect Clinical Case Sheets & PDFs**:
   - Select any patient from the left directory (e.g. `Devendra`, `Narasimhapa`, `Shanthamma`, `Venkateshappa`, `Subbamma`).
   - Click **"Download Case Sheet PDF"** to preview the authentic `F/EPH/MRD/39` document.

4. **Review Nursing Station**:
   - Switch to **Nurse Station**: view the **Medication Sheet (`F/EPH/MRD/58`)**, **Graphic TPR Chart (`F/MRD/EPH/07`)**, and **Diabetic Chart (`F/EPH/MRD/54`)**.

5. **Interact with PACS Radiology**:
   - Switch to **PACS Radiology**: adjust **Brightness (WL)**, **Contrast (WW)**, **Zoom**, and **Invert** on the digital scan.

6. **Simulate ABDM Milestones (M1, M2, M3)**:
   - Switch to **ABDM Gateways**:
     - **M1**: Click "Generate ABDM Mock OTP" $\rightarrow$ enter `123456` $\rightarrow$ generate the ABHA ID card.
     - **M2**: Inspect and copy the valid HL7 FHIR R4 JSON bundle.
     - **M3**: Click "Initiate ABDM Consent Request" $\rightarrow$ click "Approve Consent" $\rightarrow$ view historical records fetched from external hospital networks.
