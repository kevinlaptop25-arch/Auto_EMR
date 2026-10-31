import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from app.models.patient import Patient
from app.models.emergency import EmergencyEncounter
from app.models.pharmacy import InventoryItem, PrescriptionItem, PharmacyDispensation
from app.models.billing import HospitalInvoice, BillItem
from app.models.bloodbank import BloodInventoryUnit, BloodRequisition
from app.core.clinical_engine import (
    EAST_POINT_DOCTORS, DEPARTMENTS, CENTRAL_WORKFLOWS, ALLIED_SUPER_SPECIALTY,
    CLINICAL_PROFILES, ClinicalEngine
)

FIRST_NAMES_MALE = [
    "Venkateshappa", "Narasimhappa", "Devendra", "Manjunatha", "Ramesh", "Suresh",
    "Gopal", "Shivanna", "Anand", "Pradeep", "Raghavendra", "Chandrashekar",
    "Basavaraj", "Mallikarjun", "Naveen", "Kiran", "Santhosh", "Vijay", "Murthy",
    "Praveen", "Ashok", "Siddaraju", "Lokesh", "Girish", "Mahadev"
]

FIRST_NAMES_FEMALE = [
    "Subbamma", "Shanthamma", "Lakshmidevamma", "Radhika", "Parvathamma", "Manjula",
    "Saraswathi", "Geetha", "Bhagyamma", "Kavitha", "Pushpalatha", "Sowmya",
    "Anusuya", "Gangamma", "Renukamma", "Chikkathayamma", "Roopa", "Meenakshi",
    "Divya", "Poornima", "Kavya", "Deepa", "Suma", "Sunitha"
]

SURNAMES_LOCAL = [
    "Gowda", "Reddy", "Rao", "Kumar", "Murthy", "Babu", "Hegde", "Shetty",
    "Acharya", "Nayak", "Patil", "Deshmukh", "Naidu", "Sharma", "Bhat", "Kulkarni"
]

LOCAL_AREAS = [
    "Bidarahalli, Virgo Nagar Post", "Avalahalli, Old Madras Road", "K.R. Puram, Bangalore East",
    "Hoskote Rural, Bangalore", "Chikkaballapur Town", "Peresandra, Chikkaballapur",
    "Jullpalya Village", "Kolar Gold Fields", "Devanahalli, Near Airport", "Whitefield Main Road",
    "Bhattarahalli, Old Madras Road", "Seegehalli, Kadugodi Post"
]

STANDARD_FORMULARY = [
    {"name": "Tab Paracetamol 650mg", "gen": "Paracetamol", "form": "Tablet", "str": "650mg", "cat": "Essential Drug (EDL)", "price": 2.50, "narc": False},
    {"name": "Inj Artesunate 120mg", "gen": "Artesunate", "form": "Injection", "str": "120mg", "cat": "Emergency", "price": 185.00, "narc": False},
    {"name": "Tab Primaquine 15mg", "gen": "Primaquine Phosphate", "form": "Tablet", "str": "15mg", "cat": "Essential Drug (EDL)", "price": 8.00, "narc": False},
    {"name": "Inj Human Actrapid 100 IU/ml", "gen": "Regular Insulin", "form": "Injection", "str": "100 IU/ml", "cat": "Endocrine", "price": 165.00, "narc": False},
    {"name": "Tab Metformin 500mg SR", "gen": "Metformin HCl", "form": "Tablet", "str": "500mg", "cat": "Endocrine", "price": 3.20, "narc": False},
    {"name": "Tab Amlodipine 5mg", "gen": "Amlodipine Besylate", "form": "Tablet", "str": "5mg", "cat": "Cardiovascular", "price": 2.80, "narc": False},
    {"name": "Tab Telmisartan 40mg", "gen": "Telmisartan", "form": "Tablet", "str": "40mg", "cat": "Cardiovascular", "price": 6.50, "narc": False},
    {"name": "Budecort 0.5mg Respules", "gen": "Budesonide", "form": "Inhaler", "str": "0.5mg/2ml", "cat": "Respiratory", "price": 22.00, "narc": False},
    {"name": "Duolin Respules", "gen": "Levosalbutamol + Ipratropium", "form": "Inhaler", "str": "1.25mg/500mcg", "cat": "Respiratory", "price": 18.50, "narc": False},
    {"name": "Tab Pantoprazole 40mg", "gen": "Pantoprazole Sodium", "form": "Tablet", "str": "40mg", "cat": "Essential Drug (EDL)", "price": 4.50, "narc": False},
    {"name": "Tab Amoxicillin-Clav 625mg", "gen": "Amoxicillin + Clavulanic Acid", "form": "Tablet", "str": "625mg", "cat": "Antibiotic", "price": 24.00, "narc": False},
    {"name": "Inj Ceftriaxone 1g", "gen": "Ceftriaxone Sodium", "form": "Injection", "str": "1g", "cat": "Antibiotic", "price": 55.00, "narc": False},
    {"name": "Tab Ursodeoxycholic Acid 300mg", "gen": "UDCA", "form": "Tablet", "str": "300mg", "cat": "Gastroenterology", "price": 32.00, "narc": False},
    {"name": "Inj Tramadol 50mg/ml", "gen": "Tramadol HCl", "form": "Injection", "str": "50mg/ml", "cat": "Narcotic Schedule X", "price": 28.00, "narc": True},
    {"name": "Inj Fentanyl 50mcg/ml", "gen": "Fentanyl Citrate", "form": "Injection", "str": "50mcg/ml", "cat": "Narcotic Schedule X", "price": 65.00, "narc": True},
    {"name": "IV Normal Saline 0.9% 500ml", "gen": "Sodium Chloride 0.9%", "form": "IV Infusion", "str": "500ml", "cat": "Essential Drug (EDL)", "price": 42.00, "narc": False},
    {"name": "IV Ringer Lactate 500ml", "gen": "Compound Sodium Lactate", "form": "IV Infusion", "str": "500ml", "cat": "Essential Drug (EDL)", "price": 46.00, "narc": False},
    {"name": "Inj Adrenaline 1:1000", "gen": "Epinephrine", "form": "Injection", "str": "1mg/ml", "cat": "Emergency", "price": 12.00, "narc": False},
    {"name": "Inj Atropine Sulphate 0.6mg", "gen": "Atropine", "form": "Injection", "str": "0.6mg/ml", "cat": "Emergency", "price": 11.50, "narc": False},
    {"name": "Tab Ciprofloxacin 500mg", "gen": "Ciprofloxacin", "form": "Tablet", "str": "500mg", "cat": "Antibiotic", "price": 5.20, "narc": False}
]

BLOOD_GROUPS = ["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"]
BLOOD_COMPONENTS = [
    ("Packed Red Blood Cells (PRBC)", 300, "2°C - 6°C", 35),
    ("Platelet Concentrate (RDP)", 50, "20°C - 24°C Agitator", 5),
    ("Fresh Frozen Plasma (FFP)", 220, "-30°C Deep Freezer", 365),
    ("Cryoprecipitate", 20, "-30°C Deep Freezer", 365),
    ("Single Donor Platelets (SDP)", 250, "20°C - 24°C Agitator", 5)
]

class BatchGenerator:
    """
    Synthesizes over 2,800 daily encounters (2,600 OPD + 200 IPD), covering 21 departments
    with 14 central workflows, integrated modules for Pharmacy, Billing, Blood Bank, Emergency,
    and a realistic ABHA generation target of 30% to 35%.
    """
    def __init__(self):
        self.patients_db: Dict[str, Patient] = {}
        self.patient_bundles: Dict[str, Dict[str, Any]] = {}
        self.opd_slips: Dict[str, Any] = {}
        
        # New Integrated Modules Data Stores
        self.emergency_encounters: Dict[str, EmergencyEncounter] = {}
        self.pharmacy_inventory: List[InventoryItem] = []
        self.pharmacy_dispensations: Dict[str, PharmacyDispensation] = {}
        self.billing_invoices: Dict[str, HospitalInvoice] = {}
        self.blood_inventory: List[BloodInventoryUnit] = []
        self.blood_requisitions: List[BloodRequisition] = []

    def generate_patient(
        self,
        index: int,
        is_ipd: bool,
        target_date: datetime,
        forced_profile: str = None,
        forced_name: str = None,
        forced_gender: str = None,
        forced_age: int = None
    ) -> Patient:
        if forced_gender:
            is_female = (forced_gender == "Female")
        else:
            is_female = (index % 2 == 0)

        if forced_name:
            first_name = forced_name
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
            
        surname = random.choice(SURNAMES_LOCAL)
        full_name = f"{first_name} {surname}"

        rel_prefix = "W/O" if is_female else "S/O"
        rel_name = f"{rel_prefix} {random.choice(FIRST_NAMES_MALE)} {surname}"

        mr_num = f"202610{index:06d}"
        ip_num = f"263{index:04d}" if is_ipd else None

        # Registration time spread through the working morning (07:30 to 13:00)
        minute_offset = (index * 7) % 330
        reg_time = target_date.replace(hour=7, minute=30) + timedelta(minutes=minute_offset)

        # Discharge time for IPD: Day 4 discharge for flagship cases, 2-4 days for others
        discharge_time = None
        if is_ipd:
            if index <= 6:
                # Flagship 4-day progression cohort discharges on Day 4 at 16:00
                discharge_time = reg_time.replace(hour=16, minute=0) + timedelta(days=3)
            else:
                discharge_time = reg_time + timedelta(days=random.choice([2, 3, 4]), hours=random.randint(2, 6))

        # Assign Department (21 Departments with 14 Central Workflows prioritized)
        profile_key = forced_profile
        if not profile_key:
            if is_ipd:
                profile_key = random.choice(list(CLINICAL_PROFILES.keys()))
                dept = CLINICAL_PROFILES[profile_key]["department"]
            else:
                # 82% weight on the 14 Central Workflows, 18% on the 7 Allied Super-Specialties
                if (index % 100) < 82:
                    dept = random.choice(CENTRAL_WORKFLOWS)
                else:
                    dept = random.choice(ALLIED_SUPER_SPECIALTY)
        else:
            dept = CLINICAL_PROFILES[profile_key]["department"]

        # Ensure obstetric cases only go to females
        if profile_key == "TERM_PREGNANCY_LSCS" or dept == "Obstetrics & Gynaecology":
            is_female = True
            dept = "Obstetrics & Gynaecology"
            if not forced_name:
                first_name = random.choice(FIRST_NAMES_FEMALE)
                full_name = f"{first_name} {surname}"
            age = forced_age or random.randint(21, 34)
        else:
            age = forced_age or random.randint(20, 75)

        # Select doctor from East Point Hospital register
        dept_doctors = [d for d in EAST_POINT_DOCTORS if d["dept"].lower() == dept.lower()]
        if not dept_doctors:
            dept_doctors = EAST_POINT_DOCTORS
        doc = random.choice(dept_doctors)

        # ABHA ID Target: 30% to 35% verified (Deterministic ratio ~32.5%)
        # (index * 37) % 100 < 33 produces an exact 33.0% verification rate
        is_abha_linked = ((index * 37) % 100) < 33
        if is_abha_linked:
            abha_no = f"91-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            abha_addr = f"{first_name.lower()}{random.randint(10, 99)}@abdm"
            abha_verified = True
        else:
            abha_no = None
            abha_addr = None
            abha_verified = False

        patient = Patient(
            id=f"PAT-{mr_num}",
            mr_no=mr_num,
            ip_no=ip_num,
            name=full_name,
            relative_name=rel_name,
            marital_status="Married" if age > 24 else "Single",
            age=age,
            gender="Female" if is_female else "Male",
            religion="Hindu" if index % 7 != 0 else "Muslim",
            address=random.choice(LOCAL_AREAS),
            city="Bangalore",
            phone=f"9{random.randint(100000000, 999999999)}",
            payer_type="Ayushman Bharat PMJAY" if index % 2 == 0 else ("AB-ARK Insurance/Cashless" if index % 3 == 0 else "Self-Pay / Cash"),
            department=dept,
            unit=f"Unit-{random.choice(['I', 'II', 'III', 'IV'])}",
            ward_bed=f"{dept.upper()} WARD Bed {random.randint(1, 30):02d}",
            admission_time=reg_time,
            discharge_time=discharge_time,
            status="IPD_ACTIVE" if is_ipd else "OPD",
            attending_doctor=doc["name"],
            doctor_reg_no=doc["reg"],
            abha_id=abha_no,
            abha_address=abha_addr,
            abha_verified=abha_verified
        )

        return patient

    def generate_batch(self, count: int = 2800, simulated_time: datetime = None) -> Dict[str, Any]:
        """
        Executes batch synthesis handling over 2,800 daily encounters:
        - 2,600 Outpatient (OPD) visits
        - 200 Inpatient (IPD) admissions
        - 21 departments (14 central workflows prioritized)
        - 30% to 35% ABHA generation target
        - Full data integration for Pharmacy, Billing, Blood Bank, and Emergency care
        """
        random.seed(42)
        if not simulated_time:
            simulated_time = datetime.now()

        today = simulated_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Enforce target: 200 IPD + 2600 OPD (or proportionate if custom count provided)
        if count >= 2800:
            ipd_count = 200
            opd_count = count - ipd_count
        else:
            ipd_count = min(200, max(20, int(count * 0.08)))
            opd_count = count - ipd_count

        self.patients_db.clear()
        self.patient_bundles.clear()
        self.opd_slips.clear()
        self.emergency_encounters.clear()
        self.pharmacy_dispensations.clear()
        self.billing_invoices.clear()
        self.blood_requisitions.clear()

        # Seed with 6 flagship clinical cases matching physical hospital PDFs & multi-ICD progression
        featured_profiles = [
            ("MALARIA_PV", "Devendra", "Male", 38, "General Medicine"),
            ("TYPE2_DM_HYPERGLYCEMIA", "Narasimhapa", "Male", 54, "General Medicine"),
            ("COPD_ACUTE_EXACERBATION", "Venkateshappa", "Male", 68, "Respiratory Medicine"),
            ("DENGUE_FEVER", "Shanthamma", "Female", 44, "General Medicine"),
            ("LUMBAR_SPONDYLOSIS", "Subbamma", "Female", 52, "Orthopedics"),
            ("TERM_PREGNANCY_LSCS", "Radhika", "Female", 26, "Obstetrics & Gynaecology"),
        ]

        # 1. Generate IPD Patients (200 Inpatients with full multi-day clinical bundles)
        for i in range(1, ipd_count + 1):
            if i <= len(featured_profiles):
                p_key, sample_name, p_gender, p_age, p_dept = featured_profiles[i - 1]
                p = self.generate_patient(
                    i,
                    is_ipd=True,
                    target_date=today,
                    forced_profile=p_key,
                    forced_name=sample_name,
                    forced_gender=p_gender,
                    forced_age=p_age
                )
            else:
                p_key = random.choice(list(CLINICAL_PROFILES.keys()))
                p = self.generate_patient(i, is_ipd=True, target_date=today, forced_profile=p_key)

            self.patients_db[p.id] = p
            # Create full multi-day clinical bundle
            bundle = ClinicalEngine.generate_full_clinical_bundle(p, p_key, simulated_time)
            self.patient_bundles[p.id] = bundle
            self.opd_slips[p.id] = bundle.get("opd_slip")

            # Generate Pharmacy Dispensation for IPD patient
            self._create_pharmacy_dispensation(p, bundle, is_ipd=True)
            # Generate Billing Invoice for IPD patient
            self._create_billing_invoice(p, bundle, is_ipd=True)

        # 2. Generate OPD Patients (2,600 Outpatient encounters across 21 departments)
        for i in range(ipd_count + 1, count + 1):
            p = self.generate_patient(i, is_ipd=False, target_date=today)
            self.patients_db[p.id] = p
            opd_slip = ClinicalEngine.generate_opd_slip(p)
            self.opd_slips[p.id] = opd_slip

            # Generate Pharmacy & Billing for sample of OPD encounters
            if i % 3 == 0:
                self._create_pharmacy_dispensation(p, {"opd_slip": opd_slip}, is_ipd=False)
            self._create_billing_invoice(p, {"opd_slip": opd_slip}, is_ipd=False)

        # 3. Seed Integrated Pharmacy Formulary
        self._init_pharmacy_inventory()

        # 4. Seed Integrated Blood Bank (Inventory & Cross-Matched Requisitions)
        self._init_blood_bank()

        # 5. Seed Emergency Care & Triage Registry
        self._init_emergency_care(today)

        # Compute Departmental Footfall Summary
        dept_counts = {}
        central_counts = 0
        allied_counts = 0
        for p in self.patients_db.values():
            dept_counts[p.department] = dept_counts.get(p.department, 0) + 1
            if p.department in CENTRAL_WORKFLOWS:
                central_counts += 1
            else:
                allied_counts += 1

        total_pts = len(self.patients_db)
        abha_count = sum(1 for p in self.patients_db.values() if p.abha_verified)
        abha_percent = round((abha_count / float(total_pts)) * 100, 1) if total_pts > 0 else 0.0

        return {
            "total_generated": total_pts,
            "opd_footfall": count - ipd_count,
            "ipd_admissions": ipd_count,
            "quota_status": "COMPLIANT" if total_pts >= 2800 else "PARTIAL",
            "abha_verified_count": abha_count,
            "abha_compliance_pct": f"{abha_percent}%",
            "abha_target_met": (30.0 <= abha_percent <= 36.0),
            "central_workflows_encounters": central_counts,
            "allied_workflows_encounters": allied_counts,
            "department_breakdown": dept_counts,
            "pharmacy_orders": len(self.pharmacy_dispensations),
            "billing_invoices": len(self.billing_invoices),
            "blood_bank_units": len(self.blood_inventory),
            "emergency_encounters": len(self.emergency_encounters),
            "timestamp": simulated_time.isoformat()
        }

    def _init_pharmacy_inventory(self):
        """Initializes the central hospital drug formulary stock."""
        self.pharmacy_inventory.clear()
        for idx, drug in enumerate(STANDARD_FORMULARY):
            item = InventoryItem(
                id=f"MED-{1000 + idx}",
                drug_name=drug["name"],
                generic_name=drug["gen"],
                dosage_form=drug["form"],
                strength=drug["str"],
                category=drug["cat"],
                batch_no=f"EPH-{drug['name'][:3].upper()}-{random.randint(100, 999)}",
                expiry_date=f"{random.randint(1, 12):02d}/{random.randint(2027, 2029)}",
                stock_quantity=random.randint(150, 2400),
                reorder_level=50,
                unit_price_inr=drug["price"],
                is_narcotic=drug["narc"]
            )
            self.pharmacy_inventory.append(item)

    def _create_pharmacy_dispensation(self, patient: Patient, bundle: Dict[str, Any], is_ipd: bool):
        """Creates an itemized pharmacy dispensation order for a patient."""
        disp_id = f"DISP-{patient.id[4:]}"
        items = []
        sample_drugs = random.sample(STANDARD_FORMULARY, random.randint(2, 4))
        total_amt = 0.0

        for d in sample_drugs:
            qty = random.randint(5, 14) if d["form"] == "Tablet" else random.randint(2, 6)
            amt = round(qty * d["price"], 2)
            total_amt += amt
            items.append(PrescriptionItem(
                drug_name=d["name"],
                dosage_form=d["form"],
                dosage_instruction="1-0-1 after food" if d["form"] == "Tablet" else "Stat then Q8H IV",
                duration_days=random.choice([3, 5, 7]),
                quantity_prescribed=qty,
                quantity_dispensed=qty,
                batch_no=f"EPH-{d['name'][:3].upper()}-{random.randint(100, 999)}",
                expiry_date=f"{random.randint(1, 12):02d}/2028",
                unit_price_inr=d["price"],
                status="DISPENSED"
            ))

        disp = PharmacyDispensation(
            id=disp_id,
            patient_id=patient.id,
            patient_name=patient.name,
            encounter_type="IPD" if is_ipd else "OPD",
            prescribed_by=patient.attending_doctor,
            doctor_reg_no=patient.doctor_reg_no,
            prescribed_at=patient.admission_time,
            dispensed_at=patient.admission_time + timedelta(minutes=40),
            items=items,
            dispensation_status="DISPENSED",
            pharmacist_name="Shrikanth Joshi, B.Pharm",
            pharmacist_reg_no="KSPC: 48912",
            total_amount_inr=round(total_amt, 2),
            is_cashless_scheme=(patient.payer_type.startswith("Ayushman") or patient.payer_type.startswith("AB-ARK"))
        )
        self.pharmacy_dispensations[patient.id] = disp

    def _create_billing_invoice(self, patient: Patient, bundle: Dict[str, Any], is_ipd: bool):
        """Generates itemized invoice and payment status."""
        inv_no = f"INV-2026-{patient.mr_no[-5:]}"
        items = []
        is_pmjay = patient.payer_type.startswith("Ayushman")
        is_cashless = is_pmjay or patient.payer_type.startswith("AB-ARK")

        if is_ipd:
            days = 4
            items.append(BillItem(category="Bed Charges", description=f"{patient.department} Inpatient Bed (4 Days)", quantity=days, unit_rate_inr=400.0, total_amount_inr=days * 400.0))
            items.append(BillItem(category="Nursing Care", description="Inpatient 24x7 Vital Signs & Nursing Care", quantity=days, unit_rate_inr=250.0, total_amount_inr=days * 250.0))
            items.append(BillItem(category="Consultation", description=f"Attending Doctor Rounds ({patient.attending_doctor})", quantity=days, unit_rate_inr=300.0, total_amount_inr=days * 300.0))
            items.append(BillItem(category="Lab Investigations", description="NABL Hematology, Biochemistry & Microbiology Profile", quantity=1, unit_rate_inr=850.0, total_amount_inr=850.0))
            items.append(BillItem(category="Radiology", description="Digital Radiography PACS Chest / Spine View", quantity=1, unit_rate_inr=450.0, total_amount_inr=450.0))
            items.append(BillItem(category="Pharmacy", description="Inpatient Consumables & Medication Dispensation", quantity=1, unit_rate_inr=620.0, total_amount_inr=620.0))
            gross = sum(i.total_amount_inr for i in items)
        else:
            items.append(BillItem(category="Registration", description="East Point Central OPD Registration Slip", quantity=1, unit_rate_inr=20.0, total_amount_inr=20.0))
            items.append(BillItem(category="Consultation", description=f"{patient.department} Specialist OPD Consultation", quantity=1, unit_rate_inr=100.0, total_amount_inr=100.0))
            gross = 120.0

        concession = gross if is_pmjay else (gross * 0.85 if is_cashless else 0.0)
        net = gross - concession
        paid = 0.0 if is_pmjay else net

        inv = HospitalInvoice(
            invoice_no=inv_no,
            receipt_no=f"REC-2026-{random.randint(10000, 99999)}",
            patient_id=patient.id,
            patient_name=patient.name,
            mr_no=patient.mr_no,
            ip_no=patient.ip_no,
            encounter_type="IPD" if is_ipd else "OPD",
            bill_timestamp=patient.admission_time,
            payer_scheme=patient.payer_type,
            claim_preauth_id=f"PMJAY-TMS-KA-2026-{random.randint(10000, 99999)}" if is_pmjay else None,
            line_items=items,
            gross_total_inr=round(gross, 2),
            scheme_discount_inr=round(concession, 2),
            net_payable_inr=round(net, 2),
            paid_amount_inr=round(paid, 2),
            balance_due_inr=0.0,
            payment_status="CLAIM_APPROVED" if is_pmjay else ("PAID" if paid > 0 else "SETTLED"),
            payment_mode="Government PMJAY Cashless" if is_pmjay else ("Insurance AB-ARK" if is_cashless else "UPI / Cash"),
            cashier_desk="Main Cash Counter #2, EPH Bangalore",
            cashier_name="Anil Kulkarni"
        )
        self.billing_invoices[patient.id] = inv

    def _init_blood_bank(self):
        """Initializes licensed blood bank inventory and active patient requisitions."""
        self.blood_inventory.clear()
        self.blood_requisitions.clear()

        # Generate 72 licensed units across all ABO & Rh groups
        for grp in BLOOD_GROUPS:
            for comp_name, vol, temp, shelf_days in BLOOD_COMPONENTS:
                exp = (datetime.now() + timedelta(days=random.randint(2, min(shelf_days, 30)))).strftime("%d-%b-%Y")
                unit = BloodInventoryUnit(
                    unit_id=f"BB-2026-{grp.replace('+', 'POS').replace('-', 'NEG')}-{random.randint(100, 999)}",
                    blood_group=grp,
                    component=comp_name,
                    volume_ml=vol,
                    collection_date=(datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%d-%b-%Y"),
                    expiry_date=exp,
                    storage_temp=temp,
                    tti_hiv="NON-REACTIVE",
                    tti_hbsag="NON-REACTIVE",
                    tti_hcv="NON-REACTIVE",
                    tti_vdrl="NON-REACTIVE",
                    tti_mp="NEGATIVE",
                    status="AVAILABLE"
                )
                self.blood_inventory.append(unit)

        # Create active cross-matched requisitions for key inpatients
        flagship_ipds = [p for p in self.patients_db.values() if p.ip_no is not None][:4]
        for idx, pt in enumerate(flagship_ipds):
            comp_req = "Platelet Concentrate (RDP)" if idx == 0 else "Packed Red Blood Cells (PRBC)"
            assigned_unit = next((u.unit_id for u in self.blood_inventory if u.component == comp_req and u.status == "AVAILABLE"), "BB-2026-OPOS-102")
            req = BloodRequisition(
                requisition_no=f"REQ-BB-2026-{1001 + idx}",
                patient_id=pt.id,
                patient_name=pt.name,
                mr_no=pt.mr_no,
                ip_no=pt.ip_no,
                department=pt.department,
                ward_bed=pt.ward_bed,
                patient_blood_group="O+" if idx % 2 == 0 else "B+",
                clinical_indication="Severe Thrombocytopenia (52,000/uL)" if idx == 0 else "Pre-operative Haemoglobin Optimization (< 8.5 g/dL)",
                component_requested=comp_req,
                units_requested=2 if idx == 0 else 1,
                requested_at=pt.admission_time + timedelta(hours=1),
                crossmatch_status="MAJOR_COMPATIBLE",
                assigned_unit_id=assigned_unit,
                transfusion_reaction_reported=False,
                licensed_medical_officer="Dr. Manjula Swamy, MD (Path & Immuno)",
                medical_officer_reg="KMC: 52190"
            )
            self.blood_requisitions.append(req)

    def _init_emergency_care(self, target_date: datetime):
        """Initializes the 24x7 Emergency Care & Triage Department registry."""
        self.emergency_encounters.clear()
        
        er_scenarios = [
            {
                "triage": "RED", "score": "ESI-1 (Immediate)",
                "complaint": "Acute crushing retrosternal chest pain radiating to left arm, diaphoresis, BP 84/50 mmHg, ECG: STEMI Anterior Wall",
                "vitals": {"BP": "84/50", "PR": "128 bpm", "RR": "28 cpm", "SpO2": "88% @ RA", "Temp": "98.2°F"},
                "gcs": "14/15 (E4 V4 M6)", "orders": ["Crash cart activated", "Defibrillator on standby", "Stat Aspirin 300mg + Clopidogrel 300mg", "IV Heparin 5000U", "High-flow O2 via non-rebreather"],
                "disposition": "ADMITTED_ICU", "ward": "CARDIAC ICU Bed 02", "is_mlc": False
            },
            {
                "triage": "RED", "score": "ESI-1 (Immediate)",
                "complaint": "Road Traffic Accident (RTA), rider hit by truck on Old Madras Road, severe blunt chest and abdominal trauma, hypotension",
                "vitals": {"BP": "80/40", "PR": "136 bpm", "RR": "32 cpm", "SpO2": "86% @ RA", "Temp": "97.8°F"},
                "gcs": "10/15 (E2 V3 M5)", "orders": ["Large-bore 16G IV lines x 2", "Rapid crystalloid push RL 1000ml", "FAST Ultrasound positive for hemoperitoneum", "Stat O-Negative PRBC x 2 units requisitioned", "Spine board immobilization"],
                "disposition": "TRANSFER_OT", "ward": "EMERGENCY OT #1", "is_mlc": True
            },
            {
                "triage": "YELLOW", "score": "ESI-2 (Urgent)",
                "complaint": "Acute severe right lower quadrant abdominal pain with rebound tenderness, vomiting x 3 episodes, guarding",
                "vitals": {"BP": "118/76", "PR": "104 bpm", "RR": "20 cpm", "SpO2": "98% @ RA", "Temp": "101.4°F"},
                "gcs": "15/15 (E4 V5 M6)", "orders": ["NPO strict", "IV Ondansetron 4mg stat", "IV Paracetamol 1g infusion", "Emergency Ultrasound Abdomen (Acute Appendicitis suspected)", "Routine pre-op labs sent"],
                "disposition": "ADMITTED_WARD", "ward": "GENERAL SURGERY Bed 12", "is_mlc": False
            },
            {
                "triage": "YELLOW", "score": "ESI-2 (Urgent)",
                "complaint": "Known COPD patient with sudden worsening dyspnea, pursed-lip breathing, audible expiratory wheeze, SpO2 84%",
                "vitals": {"BP": "144/88", "PR": "112 bpm", "RR": "26 cpm", "SpO2": "84% @ RA", "Temp": "99.0°F"},
                "gcs": "15/15 (E4 V5 M6)", "orders": ["Controlled O2 therapy via Venturi mask 28%", "Stat Budecort 1mg + Duolin 2.5ml nebulization Q20M x 3", "Inj Hydrocortisone 100mg IV stat", "Stat ABG sent"],
                "disposition": "ADMITTED_WARD", "ward": "RESPIRATORY MEDICINE Bed 06", "is_mlc": False
            },
            {
                "triage": "GREEN", "score": "ESI-3 (Non-Urgent)",
                "complaint": "Accidental sharp knife laceration over left index finger at workplace, bleeding controlled with pressure dressing",
                "vitals": {"BP": "122/80", "PR": "78 bpm", "RR": "16 cpm", "SpO2": "99% @ RA", "Temp": "98.4°F"},
                "gcs": "15/15 (E4 V5 M6)", "orders": ["Wound irrigation with normal saline & betadine", "Local infiltration 2% Lignocaine", "Primary suture with 3-0 Ethilon (3 sutures)", "Inj Tetanus Toxoid 0.5ml IM stat", "Oral Amoxiclav 625mg x 5 days"],
                "disposition": "DISCHARGED_STABLE", "ward": "Outpatient ER Discharge", "is_mlc": True
            },
            {
                "triage": "GREEN", "score": "ESI-3 (Non-Urgent)",
                "complaint": "High fever with chills and severe body ache x 2 days, ambulatory, oriented, tolerating oral fluids",
                "vitals": {"BP": "114/72", "PR": "88 bpm", "RR": "18 cpm", "SpO2": "98% @ RA", "Temp": "102.2°F"},
                "gcs": "15/15 (E4 V5 M6)", "orders": ["Oral Paracetamol 650mg stat", "CBC + Peripheral Smear for Malarial Parasite sent", "Dengue NS1 Antigen rapid test", "Advised oral rehydration fluids"],
                "disposition": "DISCHARGED_STABLE", "ward": "OPD Fever Clinic Referral", "is_mlc": False
            }
        ]

        pts = list(self.patients_db.values())[:len(er_scenarios)]
        for idx, (pt, sc) in enumerate(zip(pts, er_scenarios)):
            er_id = f"ER-2026-{1001 + idx}"
            enc = EmergencyEncounter(
                id=er_id,
                patient_id=pt.id,
                patient_name=pt.name,
                age=pt.age,
                gender=pt.gender,
                arrival_time=target_date.replace(hour=8, minute=15) + timedelta(minutes=idx * 35),
                brought_by="108 Emergency Ambulance" if sc["triage"] == "RED" else "Relatives",
                triage_level=sc["triage"],
                triage_score=sc["score"],
                chief_complaint=sc["complaint"],
                vitals=sc["vitals"],
                gcs_score=sc["gcs"],
                is_mlc=sc["is_mlc"],
                mlc_no=f"MLC-2026-{random.randint(1000, 9999)}" if sc["is_mlc"] else None,
                police_station="Avalahalli Police Station, Bangalore East" if sc["is_mlc"] else None,
                injury_nature="RTA with Blunt Poly-trauma" if (sc["is_mlc"] and sc["triage"] == "RED") else ("Sharp cut injury" if sc["is_mlc"] else None),
                alcohol_influence=(sc["is_mlc"] and idx == 1),
                attending_er_physician="Dr. K. N. Rajesh",
                physician_reg_no="KMC: 64920",
                emergency_interventions=sc["orders"],
                crash_cart_activated=(sc["triage"] == "RED"),
                disposition=sc["disposition"],
                disposition_ward=sc["ward"],
                er_status="STABILIZED" if sc["disposition"] != "ADMITTED_ICU" else "ACTIVE_RESUSCITATION"
            )
            self.emergency_encounters[pt.id] = enc

    def link_abha_patient(self, patient_id: str) -> Dict[str, Any]:
        """Instant 1-click ABHA generation for unlinked patients."""
        if patient_id not in self.patients_db:
            return {"status": "ERROR", "message": "Patient not found"}
        
        p = self.patients_db[patient_id]
        if p.abha_verified and p.abha_id:
            return {"status": "ALREADY_LINKED", "abha_id": p.abha_id, "abha_address": p.abha_address}
        
        first_name = p.name.split()[0].lower()
        new_abha_id = f"91-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        new_abha_addr = f"{first_name}{random.randint(10, 99)}@abdm"
        
        p.abha_id = new_abha_id
        p.abha_address = new_abha_addr
        p.abha_verified = True
        
        if patient_id in self.patient_bundles:
            self.patient_bundles[patient_id]["patient"].abha_id = new_abha_id
            self.patient_bundles[patient_id]["patient"].abha_address = new_abha_addr
            self.patient_bundles[patient_id]["patient"].abha_verified = True
            
        return {
            "status": "SUCCESS",
            "patient_id": patient_id,
            "abha_id": new_abha_id,
            "abha_address": new_abha_addr,
            "verified": True
        }

    def admit_opd_patient(self, patient_id: str, simulated_time: datetime = None) -> Dict[str, Any]:
        """
        Converts an OPD patient to an active Inpatient (IPD) admission.
        """
        if patient_id not in self.patients_db:
            return None
        p = self.patients_db[patient_id]
        if p.ip_no and p.id in self.patient_bundles:
            return self.patient_bundles[patient_id]

        random.seed(42)
        if not simulated_time:
            simulated_time = datetime.now()

        p.ip_no = f"263{random.randint(5000, 9999)}"
        p.status = "IPD_ACTIVE"
        p.ward_bed = f"{p.department.upper()} WARD Bed {random.randint(1, 30):02d}"
        p.admission_time = simulated_time
        p.discharge_time = simulated_time + timedelta(days=random.choice([2, 3, 4]))

        matching = [k for k, prof in CLINICAL_PROFILES.items() if prof["department"].lower() == p.department.lower()]
        p_key = matching[0] if matching else "MALARIA_PV"

        bundle = ClinicalEngine.generate_full_clinical_bundle(p, p_key, simulated_time)
        self.patient_bundles[p.id] = bundle
        
        # Also generate pharmacy and billing for the newly admitted patient
        self._create_pharmacy_dispensation(p, bundle, is_ipd=True)
        self._create_billing_invoice(p, bundle, is_ipd=True)
        return bundle

    def list_patients(
        self,
        filter_type: str = "ALL",  # "ALL", "IPD", "OPD"
        department: str = None,
        search_query: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Patient]:
        all_pts = list(self.patients_db.values())

        if filter_type == "IPD":
            all_pts = [p for p in all_pts if p.ip_no is not None]
        elif filter_type == "OPD":
            all_pts = [p for p in all_pts if p.ip_no is None]

        if department:
            all_pts = [p for p in all_pts if p.department.lower() == department.lower()]

        if search_query:
            q = search_query.lower()
            all_pts = [
                p for p in all_pts
                if q in p.name.lower() or q in p.mr_no.lower() or (p.ip_no and q in p.ip_no.lower())
            ]

        return all_pts[offset: offset + limit]

batch_engine = BatchGenerator()
# Initialize default cohort with 2,800 records (2,600 OPD + 200 IPD)
batch_engine.generate_batch(count=2800)
