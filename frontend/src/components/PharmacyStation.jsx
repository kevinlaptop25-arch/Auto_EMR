import React, { useState, useEffect } from 'react';
import {
  Pill,
  Package,
  AlertTriangle,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Printer,
  Search,
  Check,
  Building2,
  FileSpreadsheet
} from 'lucide-react';

export default function PharmacyStation({ selectedPatient }) {
  const [activeTab, setActiveTab] = useState('queue'); // 'queue', 'formulary', 'narcotics'
  const [dispensations, setDispensations] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [narcotics, setNarcotics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [dispensingId, setDispensingId] = useState(null);
  const [filterPatientOnly, setFilterPatientOnly] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [dispRes, invRes, narcRes] = await Promise.all([
        fetch('/api/pharmacy/dispensations?limit=60'),
        fetch('/api/pharmacy/inventory'),
        fetch('/api/pharmacy/narcotics')
      ]);
      const dispData = await dispRes.json();
      const invData = await invRes.json();
      const narcData = await narcRes.json();

      setDispensations(dispData.data || []);
      setInventory(invData.data || []);
      setNarcotics(narcData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDispense = async (dispId) => {
    setDispensingId(dispId);
    try {
      await fetch(`/api/pharmacy/dispense/${dispId}`, { method: 'POST' });
      await fetchData();
    } catch (e) {
      console.error(e);
    } finally {
      setDispensingId(null);
    }
  };

  const filteredInventory = inventory.filter(i =>
    i.drug_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    i.generic_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    i.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-5 animate-in fade-in duration-150">
      {/* Station Header */}
      <div className="bg-white rounded-xl border border-slate-200/90 p-4 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-600 to-emerald-700 flex items-center justify-center text-white shadow-md shadow-teal-900/30">
            <Pill className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Central Pharmacy & Dispensation Counter
              </h2>
              <span className="text-[10px] bg-teal-100 text-teal-800 font-bold px-2 py-0.5 rounded-full border border-teal-200">
                DRUGS & COSMETICS ACT COMPLIANT
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Form F/EPH/PHARM/02 · Electronic Prescription Queue · Schedule X Controlled Register
            </p>
          </div>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('queue')}
            className={`text-xs px-3 py-1.5 rounded-lg font-bold transition cursor-pointer ${
              activeTab === 'queue' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Prescriptions Queue ({dispensations.length})
          </button>
          <button
            onClick={() => setActiveTab('formulary')}
            className={`text-xs px-3 py-1.5 rounded-lg font-bold transition cursor-pointer ${
              activeTab === 'formulary' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Drug Formulary & Stock ({inventory.length})
          </button>
          <button
            onClick={() => setActiveTab('narcotics')}
            className={`text-xs px-3 py-1.5 rounded-lg font-bold transition cursor-pointer ${
              activeTab === 'narcotics' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Schedule X Narcotics
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Total Dispensations</span>
          <span className="text-2xl font-bold text-slate-900 font-mono mt-0.5 block">
            {dispensations.length} Orders
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            ✓ Linked to OPD/IPD Encounters
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Essential Formulary SKUs</span>
          <span className="text-2xl font-bold text-teal-700 font-mono mt-0.5 block">
            {inventory.length} Items
          </span>
          <span className="text-[10px] text-slate-600 font-medium mt-1 block">
            NLEM & WHO Essential List
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Low Stock Alerts</span>
          <span className="text-2xl font-bold text-amber-600 font-mono mt-0.5 block">
            0 Items Critical
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            100% Stocked Above Buffer
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Cashless Scheme Coverage</span>
          <span className="text-2xl font-bold text-blue-700 font-mono mt-0.5 block">
            100% PMJAY / AB-ARK
          </span>
          <span className="text-[10px] text-blue-700 font-medium mt-1 block">
            Zero Out-of-Pocket for Schemes
          </span>
        </div>
      </div>

      {/* Tab 1: Prescriptions Queue */}
      {activeTab === 'queue' && (
        <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="font-bold text-sm text-slate-900">
                  Doctor Prescription & Dispensation Queue
                </h3>
                {selectedPatient && (
                  <button
                    onClick={() => setFilterPatientOnly(prev => !prev)}
                    className={`text-[11px] px-2.5 py-0.5 rounded-full font-bold border transition cursor-pointer ${
                      filterPatientOnly
                        ? 'bg-teal-700 text-white border-teal-800 shadow-2xs'
                        : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
                    }`}
                  >
                    {filterPatientOnly ? `✓ Filter: ${selectedPatient.name}` : `Filter by ${selectedPatient.name}`}
                  </button>
                )}
              </div>
              <p className="text-xs text-slate-500">
                Prescriptions auto-populated from OPD consultation slips and daily IPD round orders
              </p>
            </div>
            <span className="text-xs font-mono bg-teal-50 text-teal-800 border border-teal-200 px-2 py-1 rounded-lg">
              Pharmacist: Shrikanth Joshi (KSPC: 48912)
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-4">Order ID</th>
                  <th className="py-2.5 px-4">Patient Name & MRN</th>
                  <th className="py-2.5 px-4">Type</th>
                  <th className="py-2.5 px-4">Prescribing Doctor</th>
                  <th className="py-2.5 px-4">Drugs & Quantity</th>
                  <th className="py-2.5 px-4">Billing Scheme</th>
                  <th className="py-2.5 px-4 text-center">Status</th>
                  <th className="py-2.5 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {((filterPatientOnly && selectedPatient) ? dispensations.filter(d => d.patient_id === selectedPatient.id) : dispensations).slice(0, 20).map(disp => (
                  <tr key={disp.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-4 font-mono font-semibold text-slate-800">
                      {disp.id}
                    </td>
                    <td className="py-3 px-4">
                      <b className="text-slate-900 block">{disp.patient_name}</b>
                      <span className="text-[10px] text-slate-400 font-mono">{disp.patient_id}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        disp.encounter_type === 'IPD' ? 'bg-blue-100 text-blue-800' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {disp.encounter_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-700">
                      <div className="font-medium">{disp.prescribed_by}</div>
                      <span className="text-[10px] text-slate-400">{disp.doctor_reg_no}</span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="space-y-0.5 max-w-xs">
                        {disp.items.slice(0, 2).map((item, idx) => (
                          <div key={idx} className="text-[11px] text-slate-800 truncate">
                            • <b>{item.drug_name}</b> ({item.quantity_prescribed} {item.dosage_form}s)
                          </div>
                        ))}
                        {disp.items.length > 2 && (
                          <span className="text-[10px] text-slate-500 font-semibold">
                            +{disp.items.length - 2} more items...
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-slate-600">
                      {disp.is_cashless_scheme ? (
                        <span className="text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-full">
                          PMJAY Cashless (Rs. 0)
                        </span>
                      ) : (
                        <span className="text-[10px] font-semibold text-slate-700">
                          Rs. {disp.total_amount_inr}
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className="inline-flex items-center space-x-1 text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded-full">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        <span>DISPENSED</span>
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDispense(disp.id)}
                        disabled={dispensingId === disp.id}
                        className="inline-flex items-center space-x-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs px-2.5 py-1 rounded-md font-medium border border-slate-300 transition cursor-pointer"
                      >
                        <Printer className="w-3 h-3 text-slate-500" />
                        <span>Slip</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 2: Formulary & Stock */}
      {activeTab === 'formulary' && (
        <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden">
          <div className="p-4 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <h3 className="font-bold text-sm text-slate-900">Hospital Drug Formulary & Live Inventory</h3>
              <p className="text-xs text-slate-500">Track batch numbers, manufacturing expiries, and unit rates in INR</p>
            </div>
            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search drug, generic, batch..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="w-full text-xs pl-8 pr-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-teal-500"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-4">Item Code</th>
                  <th className="py-2.5 px-4">Brand / Generic Name</th>
                  <th className="py-2.5 px-4">Dosage Form</th>
                  <th className="py-2.5 px-4">Therapeutic Category</th>
                  <th className="py-2.5 px-4">Batch Number</th>
                  <th className="py-2.5 px-4">Expiry</th>
                  <th className="py-2.5 px-4 text-right">Available Stock</th>
                  <th className="py-2.5 px-4 text-right">Unit Rate (INR)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredInventory.map(item => (
                  <tr key={item.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-4 font-mono font-semibold text-slate-800">{item.id}</td>
                    <td className="py-3 px-4">
                      <b className="text-slate-900 block">{item.drug_name}</b>
                      <span className="text-[10px] text-slate-500 italic">{item.generic_name}</span>
                    </td>
                    <td className="py-3 px-4 text-slate-700">{item.dosage_form} ({item.strength})</td>
                    <td className="py-3 px-4">
                      <span className="text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                        {item.category}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-700">{item.batch_no}</td>
                    <td className="py-3 px-4 font-mono text-slate-600">{item.expiry_date}</td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-teal-700">
                      {item.stock_quantity.toLocaleString()} units
                    </td>
                    <td className="py-3 px-4 text-right font-mono text-slate-900 font-semibold">
                      ₹{item.unit_price_inr.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Narcotics & Schedule X */}
      {activeTab === 'narcotics' && narcotics && (
        <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-slate-200 gap-2">
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="font-bold text-sm text-slate-900">{narcotics.register_title}</h3>
                <span className="text-[10px] bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded-full border border-red-200">
                  SCHEDULE X CONTROLLED
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1">{narcotics.audit_standard}</p>
            </div>
            <div className="text-xs bg-slate-50 border border-slate-200 p-2 rounded-lg">
              Responsible Pharmacist: <b>{narcotics.authorized_pharmacist}</b>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {narcotics.controlled_items?.map((item, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-red-200 bg-red-50/30 space-y-2 text-xs">
                <div className="flex justify-between items-center">
                  <h4 className="font-bold text-red-950 text-sm">{item.drug_name}</h4>
                  <span className="font-mono text-red-700 font-bold">{item.batch_no}</span>
                </div>
                <div className="text-slate-600 text-[11px] space-y-0.5">
                  <div>Generic: <b>{item.generic_name}</b> ({item.strength})</div>
                  <div>Storage: <b>Double-Locked Narcotic Vault (Pharmacy Room 04)</b></div>
                  <div>Expiry: <b>{item.expiry_date}</b> · Stock: <b>{item.stock_quantity} ampoules</b></div>
                  <div>Dispensation Policy: <b>Requires Attending Consultant Countersignature & KMC ID</b></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
