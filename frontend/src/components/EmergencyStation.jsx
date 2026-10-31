import React, { useState, useEffect } from 'react';
import {
  AlertOctagon,
  Siren,
  Clock,
  ShieldAlert,
  HeartPulse,
  Activity,
  BedDouble,
  CheckCircle,
  Stethoscope,
  PhoneCall,
  UserCheck,
  Zap,
  ArrowRight
} from 'lucide-react';

export default function EmergencyStation({ selectedPatient }) {
  const [encounters, setEncounters] = useState([]);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState('ALL'); // 'ALL', 'RED', 'YELLOW', 'GREEN', 'MLC'
  const [loading, setLoading] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);

  const fetchEncounters = async () => {
    setLoading(true);
    try {
      let url = '/api/emergency/encounters';
      if (filter === 'RED' || filter === 'YELLOW' || filter === 'GREEN') {
        url += `?triage_filter=${filter}`;
      } else if (filter === 'MLC') {
        url += `?mlc_only=true`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setEncounters(data.data || []);
      setStats(data);
      if (data.data && data.data.length > 0 && !selectedCase) {
        setSelectedCase(data.data[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEncounters();
  }, [filter]);

  useEffect(() => {
    if (selectedPatient && encounters.length > 0) {
      const match = encounters.find(e => e.patient_id === selectedPatient.id);
      if (match) setSelectedCase(match);
    }
  }, [selectedPatient, encounters]);

  const handleAdmitIcu = async (erId) => {
    try {
      await fetch(`/api/emergency/${erId}/admit-icu`, { method: 'POST' });
      await fetchEncounters();
      if (selectedCase && selectedCase.id === erId) {
        setSelectedCase(prev => ({
          ...prev,
          disposition: 'ADMITTED_ICU',
          disposition_ward: 'MULTIDISCIPLINARY ICU Bed 03',
          er_status: 'DISPOSED'
        }));
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-5 animate-in fade-in duration-150">
      {/* Station Header */}
      <div className="bg-white rounded-xl border border-slate-200/90 p-4 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-600 to-rose-700 flex items-center justify-center text-white shadow-md shadow-rose-900/30">
            <Siren className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Casualty & Emergency Department (24x7)
              </h2>
              <span className="text-[10px] bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded-full border border-red-200">
                LEVEL-1 TRAUMA CENTRE
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Emergency Severity Index (ESI) Triage · Crash Cart Protocol · Medico-Legal Case (MLC) Registry
            </p>
          </div>
        </div>

        {/* Triage Filter Pills */}
        <div className="flex items-center space-x-1.5 overflow-x-auto w-full md:w-auto">
          {['ALL', 'RED', 'YELLOW', 'GREEN', 'MLC'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`text-xs px-2.5 py-1 rounded-lg font-bold transition whitespace-nowrap cursor-pointer ${
                filter === f
                  ? f === 'RED'
                    ? 'bg-red-600 text-white shadow-sm'
                    : f === 'YELLOW'
                    ? 'bg-amber-600 text-white shadow-sm'
                    : f === 'GREEN'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-slate-900 text-white shadow-sm'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              {f === 'ALL' ? 'All Encounters' : f === 'RED' ? '🔴 Priority 1 (Red)' : f === 'YELLOW' ? '🟡 Priority 2 (Yellow)' : f === 'GREEN' ? '🟢 Priority 3 (Green)' : '⚖️ Medico-Legal (MLC)'}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Triage Dashboard Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="bg-red-50/80 border border-red-200 rounded-xl p-3 shadow-2xs">
          <div className="flex justify-between items-center text-red-700 font-semibold mb-1">
            <span>Priority 1 (Red)</span>
            <AlertOctagon className="w-4 h-4 text-red-600 animate-pulse" />
          </div>
          <div className="text-2xl font-bold text-red-950 font-mono">
            {stats?.red_priority_count || 0}
          </div>
          <span className="text-[10px] text-red-800 font-medium mt-1 block">
            Crash Cart · Immediate Resuscitation
          </span>
        </div>

        <div className="bg-amber-50/80 border border-amber-200 rounded-xl p-3 shadow-2xs">
          <div className="flex justify-between items-center text-amber-700 font-semibold mb-1">
            <span>Priority 2 (Yellow)</span>
            <Activity className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-2xl font-bold text-amber-950 font-mono">
            {stats?.yellow_priority_count || 0}
          </div>
          <span className="text-[10px] text-amber-800 font-medium mt-1 block">
            Urgent · Bedside Stabilization &lt; 15m
          </span>
        </div>

        <div className="bg-emerald-50/80 border border-emerald-200 rounded-xl p-3 shadow-2xs">
          <div className="flex justify-between items-center text-emerald-700 font-semibold mb-1">
            <span>Priority 3 (Green)</span>
            <HeartPulse className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-bold text-emerald-950 font-mono">
            {stats?.green_priority_count || 0}
          </div>
          <span className="text-[10px] text-emerald-800 font-medium mt-1 block">
            Ambulatory · Fast-track ER Care
          </span>
        </div>

        <div className="bg-purple-50/80 border border-purple-200 rounded-xl p-3 shadow-2xs">
          <div className="flex justify-between items-center text-purple-700 font-semibold mb-1">
            <span>Medico-Legal Cases (MLC)</span>
            <ShieldAlert className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-2xl font-bold text-purple-950 font-mono">
            {stats?.mlc_count || 0}
          </div>
          <span className="text-[10px] text-purple-800 font-medium mt-1 block">
            Police Notified · Form F/EPH/ER/04
          </span>
        </div>
      </div>

      {/* Main 2-Column: Triage List & Case Examination */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: ER Encounter Queue (5 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col max-h-[600px]">
          <div className="p-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <span className="font-bold text-slate-800 text-xs flex items-center space-x-1.5">
              <Siren className="w-3.5 h-3.5 text-rose-600" />
              <span>Live Emergency Queue ({encounters.length})</span>
            </span>
            <span className="text-[10px] text-slate-500 font-mono">24x7 Realtime</span>
          </div>

          <div className="overflow-y-auto divide-y divide-slate-100 flex-1">
            {encounters.map(item => {
              const isSelected = selectedCase?.id === item.id;
              const isRed = item.triage_level === 'RED';
              const isYellow = item.triage_level === 'YELLOW';
              return (
                <div
                  key={item.id}
                  onClick={() => setSelectedCase(item)}
                  className={`p-3.5 transition cursor-pointer text-xs ${
                    isSelected ? 'bg-red-50/80 border-l-4 border-l-red-600' : 'hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center space-x-2">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isRed
                          ? 'bg-red-600 text-white animate-pulse'
                          : isYellow
                          ? 'bg-amber-100 text-amber-800 border border-amber-300'
                          : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                      }`}>
                        {item.triage_level} · {item.triage_score}
                      </span>
                      {item.is_mlc && (
                        <span className="text-[9px] bg-purple-100 text-purple-800 font-bold px-1.5 py-0.2 rounded border border-purple-200">
                          MLC
                        </span>
                      )}
                    </div>
                    <span className="font-mono text-[10px] text-slate-400">
                      {new Date(item.arrival_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <h4 className="font-bold text-slate-900 text-sm">{item.patient_name}</h4>
                  <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{item.chief_complaint}</p>

                  <div className="flex items-center justify-between mt-2 pt-1 border-t border-slate-100 text-[10px] text-slate-500">
                    <span>GCS: <b className="text-slate-700">{item.gcs_score.split(' ')[0]}</b></span>
                    <span>BP: <b className="text-slate-700">{item.vitals?.BP || '120/80'}</b></span>
                    <span>SpO2: <b className="text-slate-700">{item.vitals?.SpO2 || '98%'}</b></span>
                    <span className="font-semibold text-rose-700">{item.disposition.replace('_', ' ')}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Case Deep-Dive & Clinical Interventions (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200/90 shadow-sm p-5 space-y-4">
          {selectedCase ? (
            <>
              {/* Header Box */}
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-slate-200 gap-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="font-bold text-base text-slate-900">{selectedCase.patient_name}</h3>
                    <span className="text-xs text-slate-500">({selectedCase.age}Y · {selectedCase.gender})</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      selectedCase.triage_level === 'RED'
                        ? 'bg-red-600 text-white'
                        : selectedCase.triage_level === 'YELLOW'
                        ? 'bg-amber-600 text-white'
                        : 'bg-emerald-600 text-white'
                    }`}>
                      {selectedCase.triage_level} PRIORITY
                    </span>
                  </div>
                  <div className="flex items-center space-x-3 text-xs text-slate-500 mt-1">
                    <span>Encounter: <b className="font-mono text-slate-700">{selectedCase.id}</b></span>
                    <span>·</span>
                    <span>Brought By: <b className="text-slate-700">{selectedCase.brought_by}</b></span>
                  </div>
                </div>

                {selectedCase.disposition !== 'ADMITTED_ICU' && (
                  <button
                    onClick={() => handleAdmitIcu(selectedCase.id)}
                    className="flex items-center space-x-1.5 bg-red-600 hover:bg-red-700 text-white text-xs px-3 py-1.5 rounded-lg font-bold shadow-sm transition cursor-pointer"
                  >
                    <Zap className="w-3.5 h-3.5" />
                    <span>Fast-Track to ICU</span>
                  </button>
                )}
              </div>

              {/* Medico-Legal Box (if MLC) */}
              {selectedCase.is_mlc && (
                <div className="p-3.5 bg-purple-50 border border-purple-200 rounded-xl text-xs space-y-1.5">
                  <div className="flex items-center space-x-2 text-purple-900 font-bold">
                    <ShieldAlert className="w-4 h-4 text-purple-700" />
                    <span>Medico-Legal Case (MLC Registered: {selectedCase.mlc_no})</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-[11px] text-purple-950">
                    <div>Police Station: <b>{selectedCase.police_station}</b></div>
                    <div>Nature of Injury: <b>{selectedCase.injury_nature || 'Blunt Trauma'}</b></div>
                    <div>Alcohol Screen: <b>{selectedCase.alcohol_influence ? 'Positive (Blood Draw Sent)' : 'Negative'}</b></div>
                    <div>Police Intimation: <b>Form F/EPH/ER/04 Dispatched</b></div>
                  </div>
                </div>
              )}

              {/* Chief Complaint & Triage Assessment */}
              <div className="space-y-1.5">
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                  Triage Assessment & Chief Complaint
                </span>
                <p className="text-xs bg-slate-50 p-3 rounded-lg border border-slate-200 leading-relaxed text-slate-800 font-medium">
                  {selectedCase.chief_complaint}
                </p>
              </div>

              {/* ER Vitals Grid */}
              <div className="grid grid-cols-3 sm:grid-cols-6 gap-2 text-xs">
                {Object.entries(selectedCase.vitals || {}).map(([key, val]) => (
                  <div key={key} className="bg-slate-50 border border-slate-200 p-2 rounded-lg text-center">
                    <span className="text-[10px] text-slate-500 font-semibold block uppercase">{key}</span>
                    <span className="text-xs font-bold text-slate-900 font-mono mt-0.5 block">{val}</span>
                  </div>
                ))}
              </div>

              {/* Emergency Interventions Ordered */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-bold text-slate-800 uppercase tracking-wide">
                    Emergency Orders & Interventions Done
                  </span>
                  {selectedCase.crash_cart_activated && (
                    <span className="text-[10px] font-bold text-red-700 bg-red-100 px-2 py-0.5 rounded-full border border-red-200 animate-pulse">
                      ⚡ Crash Cart Activated
                    </span>
                  )}
                </div>
                <div className="space-y-1.5 text-xs">
                  {selectedCase.emergency_interventions?.map((order, i) => (
                    <div key={i} className="flex items-center space-x-2 p-2 bg-emerald-50/70 border border-emerald-200 rounded-lg text-emerald-950 font-medium">
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                      <span>{order}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Disposition & Consultant Footer */}
              <div className="pt-3 border-t border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center text-xs text-slate-600 gap-2">
                <div>
                  Current Disposition: <b className="text-slate-900 font-semibold">{selectedCase.disposition}</b>
                  {selectedCase.disposition_ward && (
                    <span className="text-slate-500 font-mono ml-1">({selectedCase.disposition_ward})</span>
                  )}
                </div>
                <div>
                  Attending ER Physician: <b className="text-slate-900">{selectedCase.attending_er_physician}</b> ({selectedCase.physician_reg_no})
                </div>
              </div>
            </>
          ) : (
            <div className="p-12 text-center text-slate-400 text-xs">
              Select an emergency encounter to review clinical triage.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
