import React from 'react';
import { Search, User, Bed, Tag, Shield, Activity, Sparkles, Filter } from 'lucide-react';

export default function PatientSidebar({
  patients,
  selectedPatient,
  onSelectPatient,
  filterType,
  setFilterType,
  department,
  setDepartment,
  searchQuery,
  setSearchQuery,
  loading
}) {
  const departments = [
    "All Departments",
    // 14 Central Workflows
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
    "Pathology & Transfusion Medicine",
    // 7 Allied & Super-Specialty
    "Cardiology",
    "Neurology",
    "Nephrology",
    "Gastroenterology",
    "Urology",
    "Plastic Surgery",
    "Dentistry & Maxillofacial"
  ];

  // Clinical Highlight Tag Helper for client presentation
  const getCaseHighlight = (patient) => {
    const name = patient.name.toLowerCase();
    if (name.includes("devendra")) return { label: "Malaria + DM + Hep B (Multi-ICD)", color: "bg-red-50 text-red-700 border-red-200" };
    if (name.includes("narasimhapa")) return { label: "Type 2 DM + Neuropathy + Nephropathy", color: "bg-amber-50 text-amber-800 border-amber-200" };
    if (name.includes("venkateshappa")) return { label: "COPD Exacerbation + BiPAP + Cor Pulmonale", color: "bg-sky-50 text-sky-800 border-sky-200" };
    if (name.includes("shanthamma")) return { label: "Dengue Fever + Warning Signs + Hepatitis", color: "bg-orange-50 text-orange-800 border-orange-200" };
    if (name.includes("subbamma")) return { label: "L4-L5 Spondylosis + L5 Radiculopathy", color: "bg-purple-50 text-purple-800 border-purple-200" };
    if (name.includes("radhika")) return { label: "Repeat LSCS + Gestational HTN", color: "bg-rose-50 text-rose-800 border-rose-200" };
    return null;
  };

  return (
    <aside className="w-80 md:w-88 bg-white border-r border-slate-200/90 flex flex-col h-[calc(100vh-4rem)] shrink-0 shadow-xs">
      {/* Search & Filters Header */}
      <div className="p-3.5 border-b border-slate-200 space-y-2.5 bg-slate-50/70">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center space-x-1.5">
            <User className="w-3.5 h-3.5 text-slate-500" />
            <span>Patient Registry</span>
          </span>
          <span className="text-[10px] bg-slate-200/80 text-slate-700 font-mono font-bold px-2 py-0.5 rounded-full">
            2,800+ Encounters
          </span>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by name, MRN, IP No..."
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition placeholder:text-slate-400"
          />
        </div>

        {/* Filter Type Pills: ALL, IPD, OPD */}
        <div className="grid grid-cols-3 gap-1 bg-slate-200/70 p-1 rounded-lg text-xs font-medium">
          <button
            onClick={() => setFilterType("ALL")}
            className={`py-1 rounded-md text-center transition ${
              filterType === "ALL"
                ? "bg-white text-slate-900 font-bold shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            All (2,800)
          </button>
          <button
            onClick={() => setFilterType("IPD")}
            className={`py-1 rounded-md text-center transition ${
              filterType === "IPD"
                ? "bg-blue-600 text-white font-bold shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            IPD (200)
          </button>
          <button
            onClick={() => setFilterType("OPD")}
            className={`py-1 rounded-md text-center transition ${
              filterType === "OPD"
                ? "bg-emerald-600 text-white font-bold shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            OPD (2,600)
          </button>
        </div>

        {/* Department Dropdown */}
        <div className="relative">
          <select
            value={department || "All Departments"}
            onChange={(e) => setDepartment(e.target.value === "All Departments" ? "" : e.target.value)}
            className="w-full py-1.5 px-2.5 text-xs bg-white border border-slate-300 rounded-lg text-slate-700 focus:outline-none focus:ring-1 focus:ring-slate-400 appearance-none font-medium cursor-pointer"
          >
            {departments.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
          <Filter className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
        </div>
      </div>

      {/* Patient List Viewport */}
      <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading cohort records...</div>
        ) : patients.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-400">No matching patients found.</div>
        ) : (
          patients.map((p) => {
            const isSelected = selectedPatient?.id === p.id;
            const isIpd = Boolean(p.ip_no);
            const highlight = getCaseHighlight(p);

            return (
              <div
                key={p.id}
                onClick={() => onSelectPatient(p)}
                className={`p-3 cursor-pointer transition select-none relative ${
                  isSelected
                    ? "bg-red-50/70 border-l-4 border-red-600"
                    : "hover:bg-slate-50 border-l-4 border-transparent"
                }`}
              >
                {/* Name & IPD/OPD Tag */}
                <div className="flex items-start justify-between gap-1">
                  <div className="font-bold text-xs text-slate-900 truncate flex items-center space-x-1.5">
                    <span>{p.name}</span>
                  </div>
                  <span
                    className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-bold shrink-0 ${
                      isIpd
                        ? "bg-blue-100 text-blue-800 border border-blue-200"
                        : "bg-slate-100 text-slate-600 border border-slate-200"
                    }`}
                  >
                    {isIpd ? "IPD" : "OPD"}
                  </span>
                </div>

                {/* Case Highlight Badge if key demonstration case */}
                {highlight && (
                  <div className="mt-1">
                    <span className={`inline-block text-[9px] font-semibold px-1.5 py-0.5 rounded border truncate max-w-full ${highlight.color}`}>
                      ★ {highlight.label}
                    </span>
                  </div>
                )}

                {/* Age, Gender, MRN */}
                <div className="text-[11px] text-slate-500 mt-1 flex items-center space-x-2">
                  <span className="font-medium text-slate-700">{p.age} Y / {p.gender[0]}</span>
                  <span>·</span>
                  <span className="font-mono text-slate-600">MR: {p.mr_no}</span>
                  {p.ip_no && (
                    <>
                      <span>·</span>
                      <span className="font-mono text-blue-700 font-semibold">IP: {p.ip_no}</span>
                    </>
                  )}
                </div>

                {/* Department */}
                <div className="text-[11px] text-slate-700 font-medium truncate mt-0.5">
                  {p.department}
                </div>

                {/* Ward & Bed / ABHA */}
                <div className="flex items-center justify-between mt-1 text-[10px] text-slate-500">
                  <div className="flex items-center space-x-1 truncate max-w-[170px]">
                    {isIpd && <Bed className="w-3 h-3 text-slate-400 shrink-0" />}
                    <span className="truncate">{p.ward_bed}</span>
                  </div>

                  {p.abha_verified && (
                    <span className="flex items-center space-x-0.5 text-emerald-700 bg-emerald-50 px-1 py-0.2 rounded border border-emerald-200 font-mono text-[9px]">
                      <Shield className="w-2.5 h-2.5" />
                      <span>ABHA</span>
                    </span>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div className="p-2.5 border-t border-slate-200 bg-slate-50 text-[10px] text-slate-500 flex justify-between items-center">
        <span>East Point Hospital Records</span>
        <span className="font-semibold text-emerald-700 flex items-center space-x-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>NMC Audit Ready</span>
        </span>
      </div>
    </aside>
  );
}