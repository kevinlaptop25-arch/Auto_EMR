import React from 'react';
import {
  User,
  Shield,
  FileText,
  Download,
  PlusCircle,
  Building2,
  Calendar,
  AlertCircle,
  CheckCircle,
  Stethoscope,
  BedDouble,
  Zap
} from 'lucide-react';

export default function PatientBanner({
  bundle,
  onDownloadPdf,
  onAdmitToIpd,
  onQuickGenerateAbha
}) {
  if (!bundle || !bundle.patient) return null;

  const { patient, opd_slip, hp_exam, discharge_summary } = bundle;
  const isIpd = Boolean(patient.ip_no);

  // Initials for avatar
  const initials = patient.name
    .split(' ')
    .map(n => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  return (
    <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm p-4 mb-5 transition">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Left: Patient Avatar & Demographics */}
        <div className="flex items-start sm:items-center space-x-3.5">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-base text-white shrink-0 shadow-sm ${
            isIpd
              ? 'bg-gradient-to-br from-blue-700 to-blue-500'
              : 'bg-gradient-to-br from-emerald-700 to-emerald-500'
          }`}>
            {initials}
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                {patient.name}
              </h2>
              <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border shadow-2xs ${
                isIpd
                  ? 'bg-blue-50 text-blue-800 border-blue-200'
                  : 'bg-emerald-50 text-emerald-800 border-emerald-200'
              }`}>
                {isIpd ? 'INPATIENT (IPD)' : 'OUTPATIENT (OPD)'}
              </span>

              {patient.abha_verified && patient.abha_id ? (
                <span className="flex items-center space-x-1 text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-mono font-semibold">
                  <Shield className="w-3 h-3 text-emerald-600" />
                  <span>ABHA: {patient.abha_id}</span>
                </span>
              ) : (
                <button
                  type="button"
                  onClick={() => onQuickGenerateAbha && onQuickGenerateAbha(patient.id)}
                  className="flex items-center space-x-1 text-[10px] text-orange-800 bg-orange-50 hover:bg-orange-100 border border-orange-300 px-2 py-0.5 rounded-full font-mono font-bold cursor-pointer transition shadow-2xs"
                  title="Generate ABHA ID for patient (30% - 35% target)"
                >
                  <Zap className="w-3 h-3 text-orange-600 animate-pulse" />
                  <span>+ Link ABHA ID (Unlinked)</span>
                </button>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-y-1 gap-x-2 text-xs text-slate-500 mt-1">
              <span className="font-medium text-slate-700">{patient.age} Y · {patient.gender}</span>
              <span>·</span>
              <span>MRN: <b className="font-mono text-slate-800">{patient.mr_no}</b></span>
              <span>·</span>
              {isIpd ? (
                <span>IP No: <b className="font-mono text-blue-700">{patient.ip_no}</b></span>
              ) : (
                <span>OPD No: <b className="font-mono text-slate-700">{opd_slip?.opd_number || 'OPD-ACTIVE'}</b></span>
              )}
              <span>·</span>
              <span className="text-slate-600 font-medium">{patient.relative_name}</span>
            </div>
          </div>
        </div>

        {/* Center/Right: Clinical Context & Actions */}
        <div className="flex flex-wrap items-center gap-2 lg:self-center border-t lg:border-t-0 pt-3 lg:pt-0 border-slate-100">
          {/* OPD Slip PDF */}
          <button
            onClick={() => onDownloadPdf('opd')}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold border border-slate-200 transition shadow-2xs"
            title="Download East Point OPD Slip (Form F/EPH/OPD/01)"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" />
            <span>OPD Slip PDF</span>
          </button>

          {/* Case Sheet PDF (IPD) */}
          {isIpd && hp_exam && (
            <button
              onClick={() => onDownloadPdf('casesheet')}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-800 text-xs font-semibold border border-blue-200 transition shadow-2xs"
              title="Download Inpatient Case Sheet (Form F/EPH/MRD/39)"
            >
              <Download className="w-3.5 h-3.5 text-blue-600" />
              <span>Case Sheet PDF</span>
            </button>
          )}

          {/* Discharge Summary PDF (IPD) */}
          {isIpd && discharge_summary && (
            <button
              onClick={() => onDownloadPdf('discharge')}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-sm transition"
              title="Download Discharge Summary (Form EPH/DISCHARGE/01)"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Discharge PDF</span>
            </button>
          )}

          {/* Admit to IPD (OPD) */}
          {!isIpd && onAdmitToIpd && (
            <button
              onClick={onAdmitToIpd}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-sm transition"
              title="Convert OPD encounter to IPD Ward Admission as advised by Consultant"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>Admit to Inpatient Ward</span>
            </button>
          )}
        </div>
      </div>

      {/* Clinical Meta Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-3 mt-3 border-t border-slate-100 text-xs">
        <div className="p-2 rounded-lg bg-slate-50/70 border border-slate-100">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Department & Unit</span>
          <span className="font-semibold text-slate-800 truncate block mt-0.5">{patient.department}</span>
          <span className="text-[11px] text-slate-500 font-mono">{patient.unit}</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-50/70 border border-slate-100">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Ward & Bed Allocation</span>
          <span className="font-semibold text-slate-800 truncate block mt-0.5 flex items-center space-x-1">
            <BedDouble className="w-3 h-3 text-slate-400 shrink-0" />
            <span className="truncate">{isIpd ? patient.ward_bed : `${patient.department} Consultation Desk`}</span>
          </span>
          <span className="text-[11px] text-slate-500">Admitted: {new Date(patient.admission_time).toLocaleDateString()}</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-50/70 border border-slate-100">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Attending Consultant</span>
          <span className="font-semibold text-slate-800 truncate block mt-0.5">{patient.attending_doctor}</span>
          <span className="text-[11px] font-mono text-slate-500">{patient.doctor_reg_no}</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-50/70 border border-slate-100">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Insurance & Allergies</span>
          <span className="font-semibold text-emerald-700 truncate block mt-0.5">{patient.payer_type}</span>
          <span className="text-[11px] font-semibold text-slate-600">Allergies: NKDA</span>
        </div>
      </div>
    </div>
  );
}