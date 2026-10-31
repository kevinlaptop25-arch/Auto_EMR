import React from 'react';
import {
  FileText,
  Download,
  AlertTriangle,
  CheckCircle,
  Clock,
  Stethoscope,
  UserCheck,
  PlusCircle,
  Activity,
  Layers,
  ArrowRight,
  ClipboardList,
  Calendar,
  Sparkles
} from 'lucide-react';

export default function DoctorStation({ bundle, onDownloadPdf, onAdmitToIpd }) {
  if (!bundle || !bundle.patient) {
    return (
      <div className="p-16 text-center text-slate-400 bg-white rounded-2xl border border-slate-200">
        <Stethoscope className="w-10 h-10 text-slate-300 mx-auto mb-2" />
        <p className="text-sm font-medium text-slate-600">Please select a patient from the registry to inspect clinical case sheets.</p>
      </div>
    );
  }

  const { patient, opd_slip, hp_exam, progress_notes = [], discharge_summary, status_at_timestamp } = bundle;
  const isIpd = Boolean(patient.ip_no);

  // Check if patient has multi-ICD progression
  const hasMultiIcd = progress_notes.some(n => n.round_label?.includes('Comorbidity') || n.round_label?.includes('Liaison'));

  return (
    <div className="space-y-6">
      {/* Station Subheader with Document Index */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-600">
            <ClipboardList className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                isIpd ? 'text-blue-700 bg-blue-50 border-blue-200' : 'text-emerald-700 bg-emerald-50 border-emerald-200'
              }`}>
                {isIpd ? 'INPATIENT DOSSIER' : 'OUTPATIENT DOSSIER'}
              </span>
              <span className="text-xs font-mono text-slate-500">
                {isIpd ? 'FORMS: F/EPH/OPD/01 · MRD/39 · MRD/40 · DISCHARGE/01' : 'FORM: F/EPH/OPD/01'}
              </span>
            </div>
            <h3 className="text-sm font-bold text-slate-900 mt-0.5">
              Clinical Case Sheet & Medical Record Department (MRD) Records
            </h3>
          </div>
        </div>

        {hasMultiIcd && (
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-900 text-xs font-bold shadow-2xs">
            <Layers className="w-4 h-4 text-amber-700 shrink-0" />
            <span>Multi-ICD Progression Active</span>
          </div>
        )}
      </div>

      {/* 1. Outpatient Consultation Slip (FORM F/EPH/OPD/01) */}
      {opd_slip && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-blue-800 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-md">
                FORM F/EPH/OPD/01
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Central OPD Consultation Slip (Mandatory 7-Headings)
                </h4>
                <p className="text-[11px] text-slate-500">
                  Standard NABH/NMC Outpatient format with structured clinical findings.
                </p>
              </div>
            </div>
            <span className="text-xs text-slate-500 font-mono bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
              Consultation: {new Date(opd_slip.consultation_timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>

          {/* 7 Standard Hospital Headings */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 text-xs">
            {/* Heading 1: Actual Problem */}
            <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/90">
              <span className="font-bold text-slate-800 uppercase text-[10px] tracking-wider block mb-1.5 text-slate-600">
                1. Actual Problem / Chief Complaints:
              </span>
              <ul className="space-y-1">
                {opd_slip.actual_problem.map((prob, i) => (
                  <li key={i} className="text-slate-800 flex items-start space-x-1.5 font-medium">
                    <span className="text-red-500 font-bold">•</span>
                    <span>{prob}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Heading 2: History of Present Illness */}
            <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/90">
              <span className="font-bold text-slate-800 uppercase text-[10px] tracking-wider block mb-1.5 text-slate-600">
                2. History of Present Illness (HPI):
              </span>
              <p className="text-slate-700 leading-relaxed font-normal">
                {opd_slip.history_presenting_illness}
              </p>
            </div>

            {/* Heading 3: Past History */}
            <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/90">
              <span className="font-bold text-slate-800 uppercase text-[10px] tracking-wider block mb-1.5 text-slate-600">
                3. Past Medical & Surgical History:
              </span>
              <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-700">
                <div className="bg-white p-1.5 rounded border border-slate-200/60">Diabetes: <b>{opd_slip.past_history.diabetes_mellitus}</b></div>
                <div className="bg-white p-1.5 rounded border border-slate-200/60">Hypertension: <b>{opd_slip.past_history.hypertension}</b></div>
                <div className="bg-white p-1.5 rounded border border-slate-200/60">Asthma/COPD: <b>{opd_slip.past_history.asthma}</b></div>
                <div className="bg-white p-1.5 rounded border border-slate-200/60">Surgical: <b>{opd_slip.past_history.surgical_history}</b></div>
              </div>
            </div>

            {/* Heading 4: Recent Medication & Allergies */}
            <div className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/90">
              <span className="font-bold text-slate-800 uppercase text-[10px] tracking-wider block mb-1.5 text-slate-600">
                4. Recent Medication & Allergies:
              </span>
              <p className="text-slate-800 text-[11px]">
                Prior Drugs: <b>{opd_slip.recent_medication.join(', ')}</b>
              </p>
              <p className="text-emerald-700 text-[11px] mt-2 font-semibold flex items-center space-x-1">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                <span>Allergies: {opd_slip.allergies}</span>
              </p>
            </div>
          </div>

          {/* Heading 5: Clinical Findings & Admission Vitals */}
          <div>
            <span className="font-bold text-slate-600 uppercase text-[10px] tracking-wider block mb-1.5">
              5. Clinical Findings & Outpatient Vitals:
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-6 gap-2 text-xs">
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">BP</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.bp}</span>
                <span className="text-[10px] text-slate-500"> mmHg</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">Pulse</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.pr}</span>
                <span className="text-[10px] text-slate-500"> bpm</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">Resp Rate</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.rr}</span>
                <span className="text-[10px] text-slate-500"> cpm</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">Temperature</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.temp}</span>
                <span className="text-[10px] text-slate-500"> °F</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">SpO2</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.spo2}%</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <span className="text-slate-400 block text-[10px] font-semibold">GRBS</span>
                <span className="font-bold text-slate-900 text-sm">{opd_slip.clinical_findings.vitals.grbs}</span>
                <span className="text-[10px] text-slate-500"> mg/dL</span>
              </div>
            </div>
          </div>

          {/* Heading 6 & 7: Diagnosis & Treatment */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 text-xs">
            <div className="p-3.5 rounded-xl bg-red-50/70 border border-red-200 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-red-600 uppercase tracking-wider block">
                  6. Provisional Diagnosis (Strict ICD-10)
                </span>
                <span className="text-sm font-bold text-red-950 mt-0.5 block">
                  {opd_slip.provisional_diagnosis}
                </span>
              </div>
              <span className="px-3 py-1 rounded-lg bg-red-600 text-white font-mono font-bold text-xs shadow-sm">
                ICD: {opd_slip.icd10_code}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-bold text-slate-600 uppercase text-[10px] tracking-wider block mb-1">
                7. Initial Orders / Treatment Advised:
              </span>
              <ul className="space-y-0.5 text-[11px] text-slate-800">
                {opd_slip.treatment_advised.map((rx, idx) => (
                  <li key={idx} className="font-medium">• {rx}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Heading 8: Conclusion Remarks & Proceeding Action */}
          <div className={`p-4 rounded-xl border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 ${
            isIpd ? 'bg-blue-50/80 border-blue-200 text-blue-950' : 'bg-amber-50/80 border-amber-200 text-amber-950'
          }`}>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider block text-slate-600">
                8. Conclusion Remarks & Clinical Proceeding
              </span>
              <p className="text-xs font-semibold mt-0.5">
                {opd_slip.conclusion_remarks}
              </p>
            </div>
            <div className="flex items-center space-x-2 shrink-0">
              <span className="px-3 py-1 rounded-lg bg-white text-slate-800 font-mono font-bold text-xs border border-slate-300 shadow-2xs">
                Action: {isIpd ? 'ADMITTED_TO_IPD' : opd_slip.proceeding_action}
              </span>
              {!isIpd && onAdmitToIpd && (
                <button
                  onClick={onAdmitToIpd}
                  className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg transition shadow-sm flex items-center space-x-1"
                >
                  <span>Execute Admission</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* 2. History and Physical Examination Form F/EPH/MRD/39 (For Inpatients) */}
      {isIpd && hp_exam && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-blue-800 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-md">
                FORM F/EPH/MRD/39
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Initial Clinical Evaluation & Admission Findings
                </h4>
                <p className="text-[11px] text-slate-500">
                  Comprehensive history, systemic examination, and initial care plan upon ward admission.
                </p>
              </div>
            </div>
            <span className="text-xs text-slate-500 font-mono bg-slate-50 px-2.5 py-1 rounded border border-slate-200">
              Admitted: {new Date(hp_exam.admission_timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>

          {/* Chief Complaints */}
          <div>
            <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Chief Complaints at Admission
            </h5>
            <ul className="space-y-1">
              {hp_exam.chief_complaints.map((cc, i) => (
                <li key={i} className="text-xs text-slate-800 flex items-start space-x-2 font-medium">
                  <span className="text-red-500 font-bold">•</span>
                  <span>{cc}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* HPI */}
          <div>
            <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              History of Presenting Illness (HPI)
            </h5>
            <p className="text-xs text-slate-700 bg-slate-50 p-3.5 rounded-xl border border-slate-200 leading-relaxed font-normal">
              {hp_exam.history_presenting_illness}
            </p>
          </div>

          {/* Systemic Examination */}
          <div>
            <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Systemic Clinical Examination
            </h5>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block text-[11px] uppercase text-slate-500">Cardiovascular System (CVS):</span>
                <span className="text-slate-800 font-medium">{hp_exam.systemic_exam.cardiovascular}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block text-[11px] uppercase text-slate-500">Respiratory System (RS):</span>
                <span className="text-slate-800 font-medium">{hp_exam.systemic_exam.respiratory}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block text-[11px] uppercase text-slate-500">Abdomen / Per-Abdomen (P/A):</span>
                <span className="text-slate-800 font-medium">{hp_exam.systemic_exam.abdomen}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800 block text-[11px] uppercase text-slate-500">Central Nervous System (CNS):</span>
                <span className="text-slate-800 font-medium">{hp_exam.systemic_exam.cns}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 3. Doctor's Progress Notes Form F/MRD/EPH/40 (Multi-Day Inpatient Progression) */}
      {isIpd && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-blue-800 bg-blue-50 border border-blue-200 px-2.5 py-1 rounded-md">
                FORM F/MRD/EPH/40
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Doctor's Daily Progress Notes & Multi-Day Clinical Progression
                </h4>
                <p className="text-[11px] text-slate-500">
                  Chronological ward rounds displayed strictly up to active simulated audit clock.
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono bg-slate-100 px-3 py-1 rounded-lg border border-slate-200 text-slate-800 font-bold">
                {progress_notes.length} Rounds Unlocked
              </span>
            </div>
          </div>

          {progress_notes.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200">
              No clinical progress notes recorded yet prior to the current timestamp.
            </div>
          ) : (
            <div className="space-y-4">
              {progress_notes.map((note) => {
                const isComorbidityNote = note.round_label?.includes('Comorbidity') || note.round_label?.includes('Liaison');
                return (
                  <div
                    key={note.id}
                    className={`p-4 rounded-xl border transition ${
                      isComorbidityNote
                        ? 'bg-amber-50/70 border-amber-300 shadow-2xs'
                        : 'border-slate-200 bg-slate-50/40 hover:bg-white'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-2.5 border-b border-slate-200/80 gap-2 text-xs">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className={`font-bold px-2.5 py-0.5 rounded-md ${
                          isComorbidityNote
                            ? 'text-amber-950 bg-amber-200 border border-amber-300'
                            : 'text-blue-900 bg-blue-100 border border-blue-200'
                        }`}>
                          {note.round_label}
                        </span>
                        <span className="font-mono text-slate-500 flex items-center space-x-1 text-[11px]">
                          <Clock className="w-3 h-3" />
                          <span>{new Date(note.timestamp).toLocaleString()}</span>
                        </span>
                      </div>
                      <div className="flex items-center space-x-1 text-slate-600 font-mono text-[11px]">
                        <UserCheck className="w-3.5 h-3.5 text-emerald-600" />
                        <span>{note.attending_doctor} ({note.doctor_reg_no})</span>
                      </div>
                    </div>

                    <div className="mt-3 text-xs text-slate-800 space-y-2.5">
                      <p className={`p-3 rounded-xl border leading-relaxed ${
                        isComorbidityNote
                          ? 'bg-white border-amber-200 font-medium text-slate-900'
                          : 'bg-white border-slate-100 text-slate-800'
                      }`}>
                        "{note.clinical_narrative}"
                      </p>

                      <div className="grid grid-cols-3 sm:grid-cols-6 gap-2 text-[11px] bg-slate-100/80 p-2.5 rounded-xl border border-slate-200/60 font-medium">
                        <div><span className="text-slate-400 font-normal">BP:</span> <b>{note.vitals.BP}</b></div>
                        <div><span className="text-slate-400 font-normal">PR:</span> <b>{note.vitals.PR}</b></div>
                        <div><span className="text-slate-400 font-normal">RR:</span> <b>{note.vitals.RR}</b></div>
                        <div><span className="text-slate-400 font-normal">SpO2:</span> <b>{note.vitals.SpO2}</b></div>
                        <div><span className="text-slate-400 font-normal">Temp:</span> <b>{note.vitals.Temp}</b></div>
                        <div><span className="text-slate-400 font-normal">GRBS:</span> <b>{note.vitals.GRBS}</b></div>
                      </div>

                      <div>
                        <span className="font-bold text-slate-600 text-[11px] uppercase tracking-wider block mt-1">Prescriptions Ordered / Titrated:</span>
                        <ul className="pl-2 space-y-1 text-[11px] text-slate-800 mt-1">
                          {note.prescriptions_ordered.map((rx, idx) => (
                            <li key={idx} className={`flex items-start space-x-1.5 ${rx.includes('Added') ? 'text-amber-900 font-bold' : ''}`}>
                              <span className="text-blue-500 font-bold">•</span>
                              <span>{rx}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* 4. Discharge Summary Form EPH/DISCHARGE/01 */}
      {isIpd && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-md">
                FORM EPH/DISCHARGE/01
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Inpatient Discharge Summary & ICD Reconciliation
                </h4>
                <p className="text-[11px] text-slate-500">
                  Auditor validation: Must not be unlocked during active mid-day hospitalization.
                </p>
              </div>
            </div>

            {discharge_summary && (
              <button
                onClick={() => onDownloadPdf('discharge')}
                className="flex items-center space-x-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs px-3.5 py-2 rounded-lg font-bold shadow-sm transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Official Discharge PDF</span>
              </button>
            )}
          </div>

          {discharge_summary ? (
            <div className="space-y-4 text-xs">
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                <div>
                  <span className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider block">Reconciled Final Diagnosis</span>
                  <span className="font-bold text-emerald-950 text-base mt-0.5 block">
                    {discharge_summary.final_diagnosis}
                  </span>
                  <span className="text-emerald-800 font-medium text-xs mt-0.5 block">
                    Condition at Discharge: <b>{discharge_summary.condition_at_discharge}</b>
                  </span>
                </div>
                <div className="flex items-center space-x-2 shrink-0">
                  <span className="font-mono bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold shadow-xs">
                    Primary ICD: {discharge_summary.icd10_code}
                  </span>
                </div>
              </div>

              {discharge_summary.secondary_diagnoses && discharge_summary.secondary_diagnoses.length > 0 && discharge_summary.secondary_diagnoses[0] !== 'None' && (
                <div className="p-4 bg-amber-50/80 border border-amber-200 rounded-xl">
                  <span className="font-bold text-amber-900 text-xs block mb-2 uppercase tracking-wider">
                    Bound Secondary Comorbidities & Resolved Inpatient Diagnoses:
                  </span>
                  <ul className="space-y-1.5">
                    {discharge_summary.secondary_diagnoses.map((sec, idx) => (
                      <li key={idx} className="text-amber-950 text-xs flex items-center space-x-2 font-semibold bg-white/70 p-2 rounded-lg border border-amber-200/60">
                        <span className="text-amber-600 font-bold">✓</span>
                        <span>{sec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div>
                <h5 className="font-bold text-slate-700 uppercase tracking-wide mb-1 text-[11px]">Clinical Course During Hospital Stay:</h5>
                <p className="text-slate-700 bg-slate-50 p-3.5 rounded-xl border border-slate-200 leading-relaxed font-normal">
                  {discharge_summary.clinical_summary_course}
                </p>
              </div>

              <div>
                <h5 className="font-bold text-slate-700 uppercase tracking-wide mb-1 text-[11px]">Reconciled Discharge Medications:</h5>
                <ul className="space-y-1.5 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                  {discharge_summary.medications_prescribed.map((med, i) => (
                    <li key={i} className="font-semibold text-slate-800 flex items-center space-x-2 text-xs">
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                      <span>{med}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center text-slate-600 pt-3 border-t border-slate-100 gap-2">
                <span>Follow up Advice: <b className="text-slate-900">{discharge_summary.follow_up_date}</b></span>
                <span>Attending Consultant: <b className="text-slate-900">{discharge_summary.attending_consultant}</b> ({discharge_summary.consultant_reg})</span>
              </div>
            </div>
          ) : (
            <div className="p-6 bg-amber-50/90 border border-amber-200 rounded-xl flex items-start space-x-3 text-amber-900 text-xs">
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <h5 className="font-bold text-amber-950 text-sm">
                  Patient Actively Hospitalized (Status: {status_at_timestamp || 'IPD_ACTIVE'})
                </h5>
                <p className="mt-1 leading-relaxed text-amber-900 font-normal">
                  In compliance with the <b>NMC 2025 Daily Hospital Audit Standard</b>, premature discharge summaries cannot be dumped at mid-day. 
                  At the active simulated clock (01:00 PM), the patient is still receiving inpatient care. 
                  Advance the top audit scrubber to <b>Day 4 (Discharged)</b> to inspect the completed discharge summary and reconciled medications.
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}