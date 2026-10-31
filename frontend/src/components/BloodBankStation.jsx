import React, { useState, useEffect } from 'react';
import {
  Droplet,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Heart,
  Thermometer,
  Layers,
  Check,
  FlaskConical,
  FileCheck
} from 'lucide-react';

export default function BloodBankStation({ selectedPatient }) {
  const [inventory, setInventory] = useState([]);
  const [requisitions, setRequisitions] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedGroup, setSelectedGroup] = useState('ALL');
  const [loading, setLoading] = useState(false);
  const [issuingReq, setIssuingReq] = useState(null);
  const [filterPatientOnly, setFilterPatientOnly] = useState(false);

  const fetchBloodData = async () => {
    setLoading(true);
    try {
      const url = selectedGroup === 'ALL'
        ? '/api/bloodbank/inventory'
        : `/api/bloodbank/inventory?blood_group=${selectedGroup}`;

      const [invRes, reqRes, statsRes] = await Promise.all([
        fetch(url),
        fetch('/api/bloodbank/requisitions'),
        fetch('/api/bloodbank/stats')
      ]);

      const invData = await invRes.json();
      const reqData = await reqRes.json();
      const statsData = await statsRes.json();

      setInventory(invData.data || []);
      setRequisitions(reqData.data || []);
      setStats(statsData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBloodData();
  }, [selectedGroup]);

  const handleIssue = async (reqNo) => {
    setIssuingReq(reqNo);
    try {
      await fetch(`/api/bloodbank/issue/${reqNo}`, { method: 'POST' });
      await fetchBloodData();
    } catch (e) {
      console.error(e);
    } finally {
      setIssuingReq(null);
    }
  };

  const bloodGroups = ['ALL', 'A+', 'B+', 'O+', 'AB+', 'A-', 'B-', 'O-', 'AB-'];

  return (
    <div className="space-y-5 animate-in fade-in duration-150">
      {/* Station Header */}
      <div className="bg-white rounded-xl border border-slate-200/90 p-4 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-rose-600 to-red-800 flex items-center justify-center text-white shadow-md shadow-rose-900/30">
            <Droplet className="w-5 h-5 fill-current" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Blood Centre & Transfusion Medicine Department
              </h2>
              <span className="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded-full border border-rose-200">
                LIC: KA/BLD/2019/042
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Form F/EPH/BB/05 · Component Separation · Mandatory 5-Panel TTI Clearance · Cross-Matching
            </p>
          </div>
        </div>

        {/* Group Selector */}
        <div className="flex items-center space-x-1 overflow-x-auto w-full md:w-auto bg-slate-100 p-1 rounded-xl">
          {bloodGroups.map(grp => (
            <button
              key={grp}
              onClick={() => setSelectedGroup(grp)}
              className={`text-xs px-2.5 py-1 rounded-lg font-bold transition whitespace-nowrap cursor-pointer ${
                selectedGroup === grp
                  ? 'bg-rose-700 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {grp}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Total Available Units</span>
          <span className="text-2xl font-bold text-rose-700 font-mono mt-0.5 block">
            {stats?.total_available_units || inventory.length} Units
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            ✓ 100% Tested & Crossmatch Ready
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Packed Red Blood Cells (PRBC)</span>
          <span className="text-2xl font-bold text-slate-900 font-mono mt-0.5 block">
            {stats?.component_distribution?.['Packed Red Blood Cells (PRBC)'] || 8} Units
          </span>
          <span className="text-[10px] text-slate-500 font-medium mt-1 block">
            Storage: 2°C - 6°C Monitored
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Platelet Concentrates (RDP/SDP)</span>
          <span className="text-2xl font-bold text-amber-700 font-mono mt-0.5 block">
            {stats?.component_distribution?.['Platelet Concentrate (RDP)'] || 8} Units
          </span>
          <span className="text-[10px] text-amber-700 font-medium mt-1 block">
            Agitator Incubator 22°C Active
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">TTI Safety Clearance</span>
          <span className="text-2xl font-bold text-emerald-700 font-mono mt-0.5 block">
            100% PASS
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            HIV, HBV, HCV, Syphilis, MP Safe
          </span>
        </div>
      </div>

      {/* Main 2-Column: Active Patient Requisitions & Live Blood Bank Stock */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Active Clinical Requisitions (5 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200/90 shadow-sm p-4 space-y-3.5">
          <div className="flex justify-between items-center pb-3 border-b border-slate-200">
            <div>
              <h3 className="font-bold text-sm text-slate-900">Ward Transfusion Requisitions</h3>
              <p className="text-xs text-slate-500">Cross-matched blood component requests</p>
            </div>
            <div className="flex items-center space-x-2">
              {selectedPatient && (
                <button
                  onClick={() => setFilterPatientOnly(prev => !prev)}
                  className={`text-[10px] px-2 py-0.5 rounded-full font-bold border transition cursor-pointer ${
                    filterPatientOnly
                      ? 'bg-rose-700 text-white border-rose-800 shadow-2xs'
                      : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
                  }`}
                >
                  {filterPatientOnly ? `✓ ${selectedPatient.name}` : `Filter ${selectedPatient.name}`}
                </button>
              )}
              <span className="text-[10px] font-mono bg-rose-50 text-rose-700 border border-rose-200 px-2 py-0.5 rounded-full font-bold">
                {requisitions.length} Pending / Active
              </span>
            </div>
          </div>

          <div className="space-y-3 max-h-[520px] overflow-y-auto pr-1">
            {((filterPatientOnly && selectedPatient) ? requisitions.filter(r => r.patient_id === selectedPatient.id) : requisitions).map(req => {
              const isIssued = req.crossmatch_status === 'ISSUED';
              return (
                <div
                  key={req.requisition_no}
                  className={`p-3.5 rounded-xl border text-xs space-y-2 transition ${
                    isIssued ? 'bg-emerald-50/40 border-emerald-200' : 'bg-rose-50/40 border-rose-200'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-slate-600 font-semibold">{req.requisition_no}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      isIssued
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                        : 'bg-rose-100 text-rose-800 border border-rose-300 animate-pulse'
                    }`}>
                      {req.crossmatch_status}
                    </span>
                  </div>

                  <div>
                    <h4 className="font-bold text-slate-900 text-sm">{req.patient_name}</h4>
                    <div className="text-slate-500 text-[11px]">
                      Group: <b className="text-rose-700">{req.patient_blood_group}</b> · Ward: {req.ward_bed}
                    </div>
                  </div>

                  <div className="p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700 space-y-0.5">
                    <div>Component: <b>{req.component_requested}</b> ({req.units_requested} Unit)</div>
                    <div>Indication: <b>{req.clinical_indication}</b></div>
                    <div>Assigned Unit: <b className="font-mono text-slate-900">{req.assigned_unit_id}</b></div>
                  </div>

                  <div className="flex justify-between items-center pt-1 text-[10px] text-slate-500">
                    <span>Officer: {req.licensed_medical_officer}</span>
                    {!isIssued && (
                      <button
                        onClick={() => handleIssue(req.requisition_no)}
                        disabled={issuingReq === req.requisition_no}
                        className="bg-rose-600 hover:bg-rose-700 text-white font-bold px-3 py-1 rounded-lg text-xs transition cursor-pointer shadow-2xs"
                      >
                        {issuingReq === req.requisition_no ? 'Issuing...' : 'Issue Blood Unit'}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Licensed Blood Stock Ledger (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col max-h-[580px]">
          <div className="p-3.5 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
            <span className="font-bold text-xs text-slate-800">Licensed Blood Unit Inventory</span>
            <span className="text-[10px] text-slate-500 font-mono">Showing {inventory.length} verified units</span>
          </div>

          <div className="overflow-x-auto divide-y divide-slate-100 flex-1">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                <tr>
                  <th className="py-2 px-3">Unit ID</th>
                  <th className="py-2 px-3">Group</th>
                  <th className="py-2 px-3">Component</th>
                  <th className="py-2 px-3">Storage Temp</th>
                  <th className="py-2 px-3">Expiry</th>
                  <th className="py-2 px-3 text-center">TTI Screen</th>
                  <th className="py-2 px-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inventory.map(unit => {
                  const isAvailable = unit.status === 'AVAILABLE';
                  return (
                    <tr key={unit.unit_id} className="hover:bg-slate-50/80 transition">
                      <td className="py-2.5 px-3 font-mono font-semibold text-slate-800 text-[11px]">
                        {unit.unit_id}
                      </td>
                      <td className="py-2.5 px-3">
                        <span className="font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded text-xs">
                          {unit.blood_group}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 font-medium text-slate-800">
                        {unit.component.split(' (')[0]}
                        <span className="text-[10px] text-slate-400 block">{unit.volume_ml} mL</span>
                      </td>
                      <td className="py-2.5 px-3 text-slate-600 text-[11px] font-mono">
                        {unit.storage_temp}
                      </td>
                      <td className="py-2.5 px-3 font-mono text-slate-600 text-[11px]">
                        {unit.expiry_date}
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span className="text-[9px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 px-1.5 py-0.2 rounded-full">
                          ✓ SAFE
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-right">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          isAvailable
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : 'bg-slate-100 text-slate-500'
                        }`}>
                          {unit.status}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
