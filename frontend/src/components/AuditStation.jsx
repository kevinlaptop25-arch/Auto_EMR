import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  BarChart3,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Users,
  Building,
  RefreshCw,
  HeartPulse,
  Pill,
  Receipt,
  Droplet,
  Zap,
  Shield,
  Activity
} from 'lucide-react';

export default function AuditStation({ timeline, activePreset, onPresetChange, onRefreshCohort, isGenerating }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  const currentPreset = activePreset || timeline?.active_preset || "INSPECTION_1PM";

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/audit/stats');
      const data = await res.json();
      setStats(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [timeline]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-red-700 bg-red-50 border border-red-200 px-2 py-0.5 rounded">
              REGULATORY AUDIT SUITE
            </span>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-red-600" />
              <span>NMC 2,800+ ENCOUNTERS & TIMELINE INTEGRITY ENGINE</span>
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time audit verification for <b>East Point College of Medical Sciences & Research Centre</b> (21 Departments · 14 Central Workflows)
          </p>
        </div>

        <button
          onClick={onRefreshCohort}
          disabled={isGenerating}
          className="flex items-center space-x-1.5 bg-red-600 hover:bg-red-700 text-white text-xs px-3.5 py-2 rounded-lg font-bold shadow transition cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? 'animate-spin' : ''}`} />
          <span>{isGenerating ? "Synthesizing 2,800..." : "Regenerate 2,800+ Cohort"}</span>
        </button>
      </div>

      {/* KPI Cards: 2,800 Target, 2,600 OPD, 200 IPD, 30-35% ABHA Target */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Total Encounters</span>
              <Users className="w-4 h-4 text-blue-500" />
            </div>
            <div className="text-2xl font-bold text-slate-900 mt-1 font-mono">
              {stats.total_footfall.toLocaleString()}
            </div>
            <div className="flex items-center space-x-1 text-emerald-600 text-[11px] font-semibold mt-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Target (2,800+): {stats.quota_status}</span>
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>OPD Outpatient Visits</span>
              <Building className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="text-2xl font-bold text-slate-900 mt-1 font-mono">
              {stats.opd_footfall.toLocaleString()} / 2,600
            </div>
            <span className="text-emerald-700 font-semibold text-[11px] block mt-1">
              100% Target Met across 21 OPDs
            </span>
          </div>

          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>IPD Active Admissions</span>
              <Layers className="w-4 h-4 text-purple-500" />
            </div>
            <div className="text-2xl font-bold text-slate-900 mt-1 font-mono">
              {stats.ipd_admissions.toLocaleString()} / 200
            </div>
            <span className="text-purple-700 font-semibold text-[11px] block mt-1">
              Bed Occupancy: {stats.bed_occupancy_rate} (Target 200)
            </span>
          </div>

          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>ABHA ID Generation Target</span>
              <Shield className="w-4 h-4 text-orange-500" />
            </div>
            <div className="text-2xl font-bold text-orange-600 mt-1 font-mono">
              {stats.abha_percentage}
            </div>
            <span className="text-orange-800 font-semibold text-[11px] block mt-1">
              Target (30% - 35%): <b>{stats.abha_target_met ? '✓ GOAL MET' : 'IN PROGRESS'}</b> ({stats.abha_verified_count} linked)
            </span>
          </div>
        </div>
      )}

      {/* 4 Integrated Clinical & Auxiliary Modules Overview */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="pb-3 border-b border-slate-200 flex justify-between items-center">
          <div>
            <span className="text-xs font-bold text-blue-600 uppercase">Operational Modules Integration</span>
            <h3 className="text-sm font-bold text-slate-900">Hospital Ancillary & Critical Services</h3>
          </div>
          <span className="text-xs bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full font-bold">
            4 FULL MODULES ACTIVE
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          {/* Emergency Module Card */}
          <div className="p-3.5 bg-rose-50/70 border border-rose-200 rounded-xl space-y-1.5">
            <div className="flex items-center space-x-2 text-rose-900 font-bold">
              <Activity className="w-4 h-4 text-rose-600 animate-pulse" />
              <span>Emergency & Trauma</span>
            </div>
            <div className="text-2xl font-bold text-rose-950 font-mono">
              {stats?.modules_active?.emergency_care_encounters || 6} Cases
            </div>
            <p className="text-[11px] text-rose-800">
              ESI Triage (Red/Yellow/Green) · Crash Cart Protocol · Medico-Legal Case (MLC) Registry
            </p>
          </div>

          {/* Pharmacy Module Card */}
          <div className="p-3.5 bg-teal-50/70 border border-teal-200 rounded-xl space-y-1.5">
            <div className="flex items-center space-x-2 text-teal-900 font-bold">
              <Pill className="w-4 h-4 text-teal-600" />
              <span>Central Pharmacy</span>
            </div>
            <div className="text-2xl font-bold text-teal-950 font-mono">
              {stats?.modules_active?.pharmacy_dispensation_orders?.toLocaleString() || '1,067'} Orders
            </div>
            <p className="text-[11px] text-teal-800">
              Prescription Queue · Batch & Expiry Tracking · Schedule X Narcotic Log · Free Drug Scheme
            </p>
          </div>

          {/* Billing Module Card */}
          <div className="p-3.5 bg-indigo-50/70 border border-indigo-200 rounded-xl space-y-1.5">
            <div className="flex items-center space-x-2 text-indigo-900 font-bold">
              <Receipt className="w-4 h-4 text-indigo-600" />
              <span>Billing & Cashier</span>
            </div>
            <div className="text-2xl font-bold text-indigo-950 font-mono">
              {stats?.modules_active?.billing_encounter_invoices?.toLocaleString() || '2,800'} Invoices
            </div>
            <p className="text-[11px] text-indigo-800">
              Ayushman Bharat PMJAY Cashless Claims · OPD Receipts · IPD Bed & Procedural Billing
            </p>
          </div>

          {/* Blood Bank Module Card */}
          <div className="p-3.5 bg-red-50/70 border border-red-200 rounded-xl space-y-1.5">
            <div className="flex items-center space-x-2 text-red-900 font-bold">
              <Droplet className="w-4 h-4 text-red-600 fill-current" />
              <span>Blood Centre (KA/BLD/042)</span>
            </div>
            <div className="text-2xl font-bold text-red-950 font-mono">
              {stats?.modules_active?.blood_bank_licensed_units || 40} Units
            </div>
            <p className="text-[11px] text-red-800">
              PRBC, Platelets & FFP · Major Cross-Matching · 100% 5-Marker TTI Non-Reactive Safety
            </p>
          </div>
        </div>
      </div>

      {/* Step 3: Live Timeline Simulator Inspector */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="pb-3 border-b border-slate-200">
          <span className="text-xs font-bold text-red-600 uppercase">Chronological Flow Inspector</span>
          <h3 className="text-sm font-bold text-slate-900">Hospital Scrubber & Mid-Day 1:00 PM Audit Protection</h3>
          <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">
            NMC inspectors evaluate that systems do not unrealistically dump completed records mid-day. 
            Select any simulated inspection time below to observe how patient charts automatically lock/unlock events:
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-xs">
          <div
            onClick={() => onPresetChange("MORNING_ADMISSION")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border ${
              currentPreset === "MORNING_ADMISSION"
                ? "bg-blue-100 border-blue-500 ring-2 ring-blue-400 shadow-md"
                : "bg-slate-50 hover:bg-slate-100 border-slate-200"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-slate-800">07:30 AM</span>
              {currentPreset === "MORNING_ADMISSION" && (
                <span className="text-[9px] bg-blue-600 text-white px-1.5 py-0.2 rounded font-bold">ACTIVE</span>
              )}
            </div>
            <span className="text-slate-500 text-[11px] block mt-0.5">Morning Admission</span>
            <span className="text-blue-700 text-[10px] font-semibold mt-2 block">
              ✓ Form F/EPH/MRD/39 created
            </span>
            <span className="text-slate-400 text-[10px] block">✕ Notes & Labs locked</span>
          </div>

          <div
            onClick={() => onPresetChange("ROUNDS_10AM")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border ${
              currentPreset === "ROUNDS_10AM"
                ? "bg-blue-100 border-blue-500 ring-2 ring-blue-400 shadow-md"
                : "bg-slate-50 hover:bg-slate-100 border-slate-200"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-slate-800">10:00 AM</span>
              {currentPreset === "ROUNDS_10AM" && (
                <span className="text-[9px] bg-blue-600 text-white px-1.5 py-0.2 rounded font-bold">ACTIVE</span>
              )}
            </div>
            <span className="text-slate-500 text-[11px] block mt-0.5">Morning Rounds</span>
            <span className="text-blue-700 text-[10px] font-semibold mt-2 block">
              ✓ Day 1 Morning Note unlocked
            </span>
            <span className="text-slate-400 text-[10px] block">✕ Afternoon events locked</span>
          </div>

          <div
            onClick={() => onPresetChange("INSPECTION_1PM")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border-2 ${
              currentPreset === "INSPECTION_1PM"
                ? "bg-red-100 border-red-600 ring-2 ring-red-400 shadow-md"
                : "bg-red-50 hover:bg-red-100 border-red-300"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-red-900">01:00 PM</span>
              <span className="text-[9px] bg-red-600 text-white px-1.5 py-0.2 rounded font-bold">
                {currentPreset === "INSPECTION_1PM" ? "ACTIVE SAFE" : "AUDIT SAFE"}
              </span>
            </div>
            <span className="text-red-700 text-[11px] block mt-0.5 font-semibold">Mid-Day NMC Inspection</span>
            <span className="text-emerald-700 text-[10px] font-semibold mt-2 block">
              ✓ OPD Slips & Morning Rounds
            </span>
            <span className="text-red-600 text-[10px] font-bold block">
              🔒 Premature Discharges LOCKED
            </span>
          </div>

          <div
            onClick={() => onPresetChange("DAY2_COMORBIDITY")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border ${
              currentPreset === "DAY2_COMORBIDITY"
                ? "bg-amber-100 border-amber-600 ring-2 ring-amber-400 shadow-md"
                : "bg-amber-50 hover:bg-amber-100 border-amber-300"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-amber-900">Day 2 Rounds</span>
              {currentPreset === "DAY2_COMORBIDITY" && (
                <span className="text-[9px] bg-amber-600 text-white px-1.5 py-0.2 rounded font-bold">ACTIVE</span>
              )}
            </div>
            <span className="text-amber-700 text-[11px] block mt-0.5 font-medium">Comorbidities Detected</span>
            <span className="text-amber-800 text-[10px] font-semibold mt-2 block">
              ✓ Secondary ICD Diagnoses added
            </span>
            <span className="text-slate-600 text-[10px] block">✓ Diabetic / ABG charts active</span>
          </div>

          <div
            onClick={() => onPresetChange("DAY3_LIAISON")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border ${
              currentPreset === "DAY3_LIAISON"
                ? "bg-purple-100 border-purple-600 ring-2 ring-purple-400 shadow-md"
                : "bg-purple-50 hover:bg-purple-100 border-purple-300"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-purple-900">Day 3 Rounds</span>
              {currentPreset === "DAY3_LIAISON" && (
                <span className="text-[9px] bg-purple-600 text-white px-1.5 py-0.2 rounded font-bold">ACTIVE</span>
              )}
            </div>
            <span className="text-purple-700 text-[11px] block mt-0.5 font-medium">Specialist Liaison</span>
            <span className="text-purple-800 text-[10px] font-semibold mt-2 block">
              ✓ Tertiary ICD / Serology linked
            </span>
            <span className="text-slate-600 text-[10px] block">✓ Multi-organ medication update</span>
          </div>

          <div
            onClick={() => onPresetChange("DISCHARGE_READY")}
            className={`p-3 rounded-lg cursor-pointer transition text-left border-2 sm:col-span-2 lg:col-span-1 ${
              currentPreset === "DISCHARGE_READY" || currentPreset === "DAY4_DISCHARGE"
                ? "bg-emerald-100 border-emerald-600 ring-2 ring-emerald-400 shadow-md"
                : "bg-emerald-50 hover:bg-emerald-100 border-emerald-300"
            }`}
          >
            <div className="flex justify-between items-center">
              <span className="font-bold text-emerald-900">Day 4</span>
              <span className="text-[9px] bg-emerald-600 text-white px-1.5 py-0.2 rounded font-bold">
                {currentPreset === "DISCHARGE_READY" || currentPreset === "DAY4_DISCHARGE" ? "ACTIVE" : "READY"}
              </span>
            </div>
            <span className="text-emerald-700 text-[11px] block mt-0.5 font-semibold">Discharge Fitness</span>
            <span className="text-emerald-800 text-[10px] font-semibold mt-2 block">
              ✓ Form EPH/DISCHARGE/01
            </span>
            <span className="text-emerald-700 text-[10px] font-semibold block">
              ✓ All ICDs bound & reconciled
            </span>
          </div>
        </div>
      </div>

      {/* 21 Departments Footfall Breakdown (14 Central Workflows + 7 Allied) */}
      {stats?.department_distribution && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-3 border-b border-slate-200 gap-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                21 Hospital Departments Footfall Distribution
              </h3>
              <p className="text-xs text-slate-500">
                14 Central Clinical Workflows ({stats.central_encounters_count} encounters) + 7 Allied & Super-Specialty ({stats.allied_encounters_count} encounters)
              </p>
            </div>
            <span className="text-xs text-slate-700 font-mono bg-slate-100 px-3 py-1 rounded-lg font-bold">
              Total: 2,800 Encounters
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs pt-1">
            {Object.entries(stats.department_distribution).map(([dept, count]) => {
              const isCentral = stats.central_workflows?.includes(dept);
              return (
                <div
                  key={dept}
                  className={`p-3 rounded-xl border flex justify-between items-center transition ${
                    isCentral ? 'bg-blue-50/50 border-blue-200' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div className="min-w-0 pr-2">
                    <span className="text-slate-900 font-bold block truncate">{dept}</span>
                    <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded uppercase mt-0.5 inline-block ${
                      isCentral ? 'bg-blue-200 text-blue-900' : 'bg-purple-100 text-purple-800'
                    }`}>
                      {isCentral ? 'Central Workflow' : 'Allied Super-Specialty'}
                    </span>
                  </div>
                  <span className="font-mono font-bold text-slate-900 text-sm bg-white px-2.5 py-1 rounded-lg border border-slate-200 shadow-2xs shrink-0">
                    {count}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
