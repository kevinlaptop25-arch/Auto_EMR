import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.models.patient import Patient
from app.models.clinical import HistoryAndPhysical, DischargeSummary, OpdSlip
from app.models.lab import LabReport

class PdfGeneratorService:
    @staticmethod
    def _create_hospital_header(title: str, form_code: str = "F/EPH/MRD/39"):
        styles = getSampleStyleSheet()
        elements = []

        header_data = [
            [
                Paragraph("<b>EAST POINT HOSPITAL</b> &nbsp;<font size=7 color='#990000'><b>[POC]</b></font><br/><font size=7>Powered by Node4 Tech · Jnana Prabha Campus, Bidarahalli<br/>Bangalore - 560049</font>", styles["Normal"]),
                Paragraph(f"<font size=8><b>{form_code}</b><br/><b>AB_ARK Insurance/Cashless</b><br/>NABH / NMC Accredited</font>", ParagraphStyle('HRight', alignment=2))
            ]
        ]
        t = Table(header_data, colWidths=[330, 200])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ]))
        elements.append(t)
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#990000"), spaceAfter=6, spaceBefore=4))
        
        doc_title = Paragraph(f"<font size=12><b><font color='#990000'>{title.upper()}</font></b></font>", ParagraphStyle('DocTitle', alignment=1, spaceAfter=8))
        elements.append(doc_title)
        return elements

    @staticmethod
    def generate_case_sheet_pdf(patient: Patient, hp: HistoryAndPhysical) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=25)
        styles = getSampleStyleSheet()
        elements = []

        # Hospital Header
        elements.extend(PdfGeneratorService._create_hospital_header("INPATIENT CASE SHEET (ADMISSION & CLINICAL EVALUATION)", "F/EPH/MRD/39"))

        # Patient Info Grid
        pat_data = [
            [f"Patient Name: {patient.name}", f"MR No: {patient.mr_no}", f"IP No: {patient.ip_no or 'N/A'}"],
            [f"Age / Gender: {patient.age} Y / {patient.gender}", f"Marital Status: {patient.marital_status}", f"Relative: {patient.relative_name}"],
            [f"Department: {patient.department}", f"Ward / Bed: {patient.ward_bed}", f"Date of Adm: {patient.admission_time.strftime('%d-%b-%Y %I:%M %p')}"],
            [f"Consultant: {patient.attending_doctor}", f"Reg No: {patient.doctor_reg_no}", f"Payer: {patient.payer_type}"]
        ]
        pat_table = Table(pat_data, colWidths=[200, 160, 170])
        pat_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(pat_table)
        elements.append(Spacer(1, 10))

        # Chief Complaints
        elements.append(Paragraph("<b>1. CHIEF COMPLAINTS:</b>", styles["Heading4"]))
        for cc in hp.chief_complaints:
            elements.append(Paragraph(f"• {cc}", styles["Normal"]))
        elements.append(Spacer(1, 8))

        # HPI
        elements.append(Paragraph("<b>2. HISTORY OF PRESENT ILLNESS:</b>", styles["Heading4"]))
        elements.append(Paragraph(hp.history_presenting_illness, styles["Normal"]))
        elements.append(Spacer(1, 8))

        # General Examination
        elements.append(Paragraph("<b>3. GENERAL EXAMINATION & VITALS:</b>", styles["Heading4"]))
        vitals_text = f"BP: <b>{hp.general_exam.get('bp_mmhg', '120/80')} mmHg</b> | PR: <b>{hp.general_exam.get('pulse_bpm', '78')} bpm</b> | Temp: <b>{hp.general_exam.get('temperature_f', '98.4')}°F</b> | RR: <b>{hp.general_exam.get('respiration_cpm', '18')} cpm</b> | SpO2: <b>{hp.general_exam.get('spo2_percent', '98')}% @ Room Air</b>"
        elements.append(Paragraph(vitals_text, styles["Normal"]))
        elements.append(Paragraph(f"General: Pallor: {hp.general_exam.get('pallor', 'Absent')} | Icterus: {hp.general_exam.get('icterus', 'Absent')} | Edema: {hp.general_exam.get('edema', 'Absent')}", styles["Normal"]))
        elements.append(Spacer(1, 8))

        # Systemic Examination
        elements.append(Paragraph("<b>4. SYSTEMIC EXAMINATION:</b>", styles["Heading4"]))
        sys_data = [
            [f"CVS: {hp.systemic_exam.get('cardiovascular', 'S1 S2 heard')}", f"RS: {hp.systemic_exam.get('respiratory', 'NVBS heard, clear')}"],
            [f"Abdomen: {hp.systemic_exam.get('abdomen', 'Soft, non-tender')}", f"CNS: {hp.systemic_exam.get('cns', 'Conscious, oriented')}"]
        ]
        sys_table = Table(sys_data, colWidths=[265, 265])
        sys_table.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(sys_table)
        elements.append(Spacer(1, 10))

        # Diagnosis
        elements.append(Paragraph(f"<b>PROVISIONAL DIAGNOSIS:</b> <font color='#990000'><b>{hp.provisional_diagnosis}</b></font> (ICD-10: <b>{hp.icd10_code}</b>)", styles["Heading4"]))
        elements.append(Spacer(1, 6))

        # Initial Orders
        elements.append(Paragraph("<b>INITIAL TREATMENT ORDERS (ADMISSION DAY):</b>", styles["Heading4"]))
        for rx in hp.care_plan_treatment:
            elements.append(Paragraph(f"• {rx}", styles["Normal"]))

        elements.append(Spacer(1, 25))
        sig_data = [
            [Paragraph(f"Duty Medical Officer / Resident:<br/><b>{hp.consultant_name}</b><br/>{hp.consultant_reg}", styles["Normal"]),
             Paragraph("Medical Records Department (MRD)<br/>East Point Hospital<br/>Bangalore - 560049", styles["Normal"])]
        ]
        elements.append(Table(sig_data, colWidths=[260, 270]))

        doc.build(elements)
        return buffer.getvalue()

    @staticmethod
    def generate_opd_slip_pdf(patient: Patient, opd: OpdSlip) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=25)
        styles = getSampleStyleSheet()
        elements = []

        # Hospital Header Form F/EPH/OPD/01
        elements.extend(PdfGeneratorService._create_hospital_header("OUTPATIENT CONSULTATION RECORD (OPD SLIP)", "FORM F/EPH/OPD/01"))

        # Patient Demographics Matrix
        pat_data = [
            [f"Patient Name: {patient.name}", f"MR No: {patient.mr_no}", f"OPD Reg No: {opd.opd_number}"],
            [f"Age / Gender: {patient.age} Y / {patient.gender}", f"Payer / Scheme: {patient.payer_type}", f"Contact: {patient.phone}"],
            [f"Department / Unit: {opd.department} ({opd.unit})", f"Consultant: {opd.attending_doctor}", f"KMC Reg: {opd.doctor_reg_no}"],
            [f"Address: {patient.address}", f"Consultation Date: {opd.consultation_timestamp.strftime('%d-%b-%Y %I:%M %p')}", f"ABHA ID: {patient.abha_id or 'Verified'}"]
        ]
        pat_table = Table(pat_data, colWidths=[190, 170, 170])
        pat_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(pat_table)
        elements.append(Spacer(1, 8))

        # 1. ACTUAL PROBLEM / CHIEF COMPLAINTS
        elements.append(Paragraph("<b>1. ACTUAL PROBLEM / CHIEF COMPLAINTS:</b>", styles["Heading4"]))
        for prob in opd.actual_problem:
            elements.append(Paragraph(f"• {prob}", styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 2. HISTORY OF PRESENT ILLNESS
        elements.append(Paragraph("<b>2. HISTORY OF PRESENT ILLNESS (HPI):</b>", styles["Heading4"]))
        elements.append(Paragraph(opd.history_presenting_illness, styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 3. PAST MEDICAL & SURGICAL HISTORY
        elements.append(Paragraph("<b>3. PAST MEDICAL & SURGICAL HISTORY:</b>", styles["Heading4"]))
        past_str = f"Diabetes: {opd.past_history.get('diabetes_mellitus', 'No')} | HTN: {opd.past_history.get('hypertension', 'No')} | Asthma: {opd.past_history.get('asthma', 'No')} | TB: {opd.past_history.get('tuberculosis', 'No')} | Surgical History: {opd.past_history.get('surgical_history', 'None')}"
        elements.append(Paragraph(past_str, styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 4. RECENT MEDICATION & ALLERGIES
        elements.append(Paragraph("<b>4. RECENT MEDICATION & ALLERGIES:</b>", styles["Heading4"]))
        med_str = f"Prior Medications: {', '.join(opd.recent_medication)} | Drug Allergies: <b>{opd.allergies}</b>"
        elements.append(Paragraph(med_str, styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 5. CLINICAL FINDINGS (VITALS & PHYSICAL EXAMINATION)
        elements.append(Paragraph("<b>5. CLINICAL FINDINGS & VITALS:</b>", styles["Heading4"]))
        vitals_dict = opd.clinical_findings.get("vitals", {})
        vitals_text = f"BP: <b>{vitals_dict.get('bp', '120/80')} mmHg</b> | Pulse: <b>{vitals_dict.get('pr', '78')} bpm</b> | Temp: <b>{vitals_dict.get('temp', '98.4')}°F</b> | RR: <b>{vitals_dict.get('rr', '18')} cpm</b> | SpO2: <b>{vitals_dict.get('spo2', '98')}%</b> | GRBS: <b>{vitals_dict.get('grbs', '104')} mg/dL</b>"
        elements.append(Paragraph(vitals_text, styles["Normal"]))
        if "exam" in opd.clinical_findings:
            elements.append(Paragraph(f"Physical Examination: {opd.clinical_findings['exam']}", styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 6. PROVISIONAL DIAGNOSIS
        elements.append(Paragraph("<b>6. PROVISIONAL DIAGNOSIS (ICD-10 BINDING):</b>", styles["Heading4"]))
        elements.append(Paragraph(f"<font color='#990000'><b>{opd.provisional_diagnosis}</b></font> &nbsp;&nbsp; [ICD-10: <b>{opd.icd10_code}</b>]", styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 7. TREATMENT ADVISED / PRESCRIPTIONS
        elements.append(Paragraph("<b>7. TREATMENT ADVISED & ORDERS:</b>", styles["Heading4"]))
        for rx in opd.treatment_advised:
            elements.append(Paragraph(f"• <b>{rx}</b>", styles["Normal"]))
        if opd.investigations_ordered:
            elements.append(Paragraph(f"Investigations Ordered: <i>{', '.join(opd.investigations_ordered)}</i>", styles["Normal"]))
        elements.append(Spacer(1, 6))

        # 8. FINAL CONCLUSION REMARKS & FURTHER PROCEEDING
        elements.append(Paragraph("<b>8. FINAL CONCLUSION REMARKS & FURTHER PROCEEDING:</b>", styles["Heading4"]))
        disposition_box = [
            [Paragraph(f"<b>Clinical Disposition:</b> <font color='#0369a1'><b>{opd.conclusion_remarks}</b></font><br/>"
                       f"Action: <b>{opd.proceeding_action}</b> &nbsp;|&nbsp; Follow up / Next Review: <b>{opd.next_review_date or 'As advised'}</b>", styles["Normal"])]
        ]
        disp_table = Table(disposition_box, colWidths=[530])
        disp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0284c7")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(disp_table)

        elements.append(Spacer(1, 15))
        sig_data = [
            [Paragraph(f"Consulting Doctor:<br/><b>{opd.attending_doctor}</b><br/>{opd.doctor_reg_no}<br/>East Point Hospital OPD", styles["Normal"]),
             Paragraph("Registration Desk Officer<br/>Central OPD Counter<br/>East Point College of Medical Sciences", styles["Normal"])]
        ]
        elements.append(Table(sig_data, colWidths=[260, 270]))

        doc.build(elements)
        return buffer.getvalue()

    @staticmethod
    def generate_lab_report_pdf(patient: Patient, lab: LabReport) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=25)
        styles = getSampleStyleSheet()
        elements = []

        elements.extend(PdfGeneratorService._create_hospital_header("DEPARTMENT OF CLINICAL LABORATORY SCIENCES", "EPH/LAB/02"))

        # Demographic Table
        lab_hdr = [
            [f"Patient Name: {patient.name}", f"Sample ID: {lab.sample_id}", f"Department: {lab.department}"],
            [f"Age/Sex: {patient.age} Y / {patient.gender}", f"MR No: {patient.mr_no}", f"Collected: {lab.collected_at.strftime('%d-%b-%Y %H:%M')}"],
            [f"Referred By: {patient.attending_doctor}", f"Sample: {lab.sample_type}", f"Reported: {lab.reported_at.strftime('%d-%b-%Y %H:%M')}"]
        ]
        t = Table(lab_hdr, colWidths=[190, 170, 170])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # Test Title
        elements.append(Paragraph(f"<b><font size=11 color='#0f172a'>{lab.test_category.upper()}</font></b>", styles["Normal"]))
        elements.append(Spacer(1, 6))

        # Results Table
        table_rows = [["TEST PARAMETER", "OBSERVED VALUE", "UNITS", "REFERENCE RANGE", "FLAG"]]
        for item in lab.items:
            flag_str = item.flag if item.flag != "NORMAL" else "-"
            table_rows.append([item.name, item.result_value, item.unit, item.reference_range, flag_str])

        res_table = Table(table_rows, colWidths=[180, 110, 80, 110, 50])
        res_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(res_table)
        elements.append(Spacer(1, 10))

        if lab.clinical_impression:
            elements.append(Paragraph(f"<b>Interpretation / Clinical Impression:</b> {lab.clinical_impression}", styles["Normal"]))
            elements.append(Spacer(1, 10))

        elements.append(Spacer(1, 20))
        sig_data = [
            [Paragraph(f"Verified By:<br/><b>{lab.pathologist_name}</b><br/>{lab.pathologist_reg}", styles["Normal"]),
             Paragraph("End of Report<br/>Laboratory Director<br/>East Point Hospital Diagnostic Services", styles["Normal"])]
        ]
        elements.append(Table(sig_data, colWidths=[260, 270]))

        doc.build(elements)
        return buffer.getvalue()

    @staticmethod
    def generate_discharge_summary_pdf(patient: Patient, summary: DischargeSummary) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=25, bottomMargin=25)
        styles = getSampleStyleSheet()
        elements = []

        elements.extend(PdfGeneratorService._create_hospital_header("INPATIENT DISCHARGE SUMMARY", "EPH/DISCHARGE/01"))

        pat_data = [
            [f"Patient Name: {patient.name}", f"MR No: {patient.mr_no}", f"IP No: {patient.ip_no or 'N/A'}"],
            [f"Age / Gender: {patient.age} Y / {patient.gender}", f"Date of Adm: {patient.admission_time.strftime('%d-%b-%Y')}", f"Date of Disch: {summary.discharge_timestamp.strftime('%d-%b-%Y')}"],
            [f"Department: {patient.department}", f"Consultant: {summary.attending_consultant}", f"Reg No: {summary.consultant_reg}"]
        ]
        t = Table(pat_data, colWidths=[200, 165, 165])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10))

        elements.append(Paragraph(f"<b>FINAL DIAGNOSIS:</b> <font color='#b91c1c'><b>{summary.final_diagnosis} (ICD-10: {summary.icd10_code})</b></font>", styles["Heading4"]))
        if summary.secondary_diagnoses:
            elements.append(Paragraph(f"<b>Secondary Diagnoses:</b> {', '.join(summary.secondary_diagnoses)}", styles["Normal"]))
        elements.append(Spacer(1, 6))

        if summary.procedures_done:
            elements.append(Paragraph(f"<b>Procedures Performed:</b> {', '.join(summary.procedures_done)}", styles["Normal"]))
            elements.append(Spacer(1, 6))

        elements.append(Paragraph("<b>CLINICAL COURSE IN HOSPITAL:</b>", styles["Heading4"]))
        elements.append(Paragraph(summary.clinical_summary_course, styles["Normal"]))
        elements.append(Spacer(1, 8))

        elements.append(Paragraph("<b>DISCHARGE MEDICATIONS:</b>", styles["Heading4"]))
        for med in summary.medications_prescribed:
            elements.append(Paragraph(f"• <b>{med}</b>", styles["Normal"]))
        elements.append(Spacer(1, 8))

        elements.append(Paragraph(f"<b>DIET & LIFESTYLE ADVICE:</b> {summary.diet_lifestyle_advice}", styles["Normal"]))
        elements.append(Paragraph(f"<b>NEXT REVIEW / FOLLOW UP:</b> <font color='#0369a1'><b>{summary.follow_up_date} in {patient.department} OPD</b></font>", styles["Normal"]))

        elements.append(Spacer(1, 25))
        sig_data = [
            [Paragraph(f"Consultant Signature:<br/><b>{summary.attending_consultant}</b><br/>{summary.consultant_reg}", styles["Normal"]),
             Paragraph("Medical Superintendent<br/>East Point Hospital & Research Centre<br/>Bangalore - 560049", styles["Normal"])]
        ]
        elements.append(Table(sig_data, colWidths=[260, 270]))

        doc.build(elements)
        return buffer.getvalue()
