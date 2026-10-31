import React, { useState, useEffect } from 'react';
import {
  CreditCard,
  Receipt,
  FileText,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Printer,
  DollarSign,
  Building,
  ArrowUpRight,
  Landmark,
  BadgePercent
} from 'lucide-react';

export default function BillingStation({ selectedPatient }) {
  const [invoices, setInvoices] = useState([]);
  const [financialStats, setFinancialStats] = useState(null);
  const [patientInvoice, setPatientInvoice] = useState(null);
  const [filterType, setFilterType] = useState('ALL'); // 'ALL', 'IPD', 'OPD'
  const [loading, setLoading] = useState(false);
  const [settling, setSettling] = useState(false);

  const fetchBillingData = async () => {
    setLoading(true);
    try {
      const url = filterType === 'ALL'
        ? '/api/billing/invoices?limit=50'
        : `/api/billing/invoices?encounter_type=${filterType}&limit=50`;
      
      const [invRes, statsRes] = await Promise.all([
        fetch(url),
        fetch('/api/billing/stats')
      ]);

      const invData = await invRes.json();
      const statsData = await statsRes.json();

      setInvoices(invData.data || []);
      setFinancialStats(statsData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchPatientInvoice = async () => {
    if (!selectedPatient) return;
    try {
      const res = await fetch(`/api/billing/patient/${selectedPatient.id}`);
      if (res.ok) {
        const data = await res.json();
        setPatientInvoice(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchBillingData();
  }, [filterType]);

  useEffect(() => {
    fetchPatientInvoice();
  }, [selectedPatient]);

  const handleSettle = async (invNo) => {
    setSettling(true);
    try {
      await fetch(`/api/billing/settle/${invNo}?payment_mode=UPI`, { method: 'POST' });
      await fetchBillingData();
      await fetchPatientInvoice();
    } catch (e) {
      console.error(e);
    } finally {
      setSettling(false);
    }
  };

  return (
    <div className="space-y-5 animate-in fade-in duration-150">
      {/* Station Header */}
      <div className="bg-white rounded-xl border border-slate-200/90 p-4 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-700 flex items-center justify-center text-white shadow-md shadow-indigo-900/30">
            <Receipt className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Hospital Billing & Cashier Counter
              </h2>
              <span className="text-[10px] bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded-full border border-blue-200">
                AYUSHMAN BHARAT EMPOWERED
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Form F/EPH/BILL/01 · OPD Consultation Fees · IPD Bed & Procedural Package Billing
            </p>
          </div>
        </div>

        {/* Filter buttons */}
        <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-xl">
          {['ALL', 'IPD', 'OPD'].map(t => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`text-xs px-3 py-1.5 rounded-lg font-bold transition cursor-pointer ${
                filterType === t ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {t === 'ALL' ? 'All Invoices' : t === 'IPD' ? 'IPD Inpatient Bills' : 'OPD Slips (Rs. 120)'}
            </button>
          ))}
        </div>
      </div>

      {/* Financial KPI Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Total Daily Invoices</span>
          <span className="text-2xl font-bold text-slate-900 font-mono mt-0.5 block">
            {financialStats?.total_invoices_generated?.toLocaleString() || 2800} Bills
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            ✓ 2,600 OPD + 200 IPD Encounters
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Gross Encounter Value</span>
          <span className="text-2xl font-bold text-indigo-700 font-mono mt-0.5 block">
            ₹{financialStats ? (financialStats.gross_billing_inr / 100000).toFixed(2) : '18.4'} Lakhs
          </span>
          <span className="text-[10px] text-slate-500 font-medium mt-1 block">
            Standard CGHS / EPH Tariff
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">PMJAY & Scheme Subsidy</span>
          <span className="text-2xl font-bold text-emerald-700 font-mono mt-0.5 block">
            ₹{financialStats ? (financialStats.government_scheme_subsidy_inr / 100000).toFixed(2) : '15.2'} Lakhs
          </span>
          <span className="text-[10px] text-emerald-700 font-medium mt-1 block">
            Ayushman Bharat PMJAY 100% Cashless
          </span>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-3 shadow-2xs">
          <span className="text-slate-500 font-medium block">Net Collections / Cash</span>
          <span className="text-2xl font-bold text-slate-800 font-mono mt-0.5 block">
            ₹{financialStats ? (financialStats.actual_collections_inr / 1000).toFixed(1) : '312.0'} K
          </span>
          <span className="text-[10px] text-blue-700 font-medium mt-1 block">
            UPI / Cash Counter Collections
          </span>
        </div>
      </div>

      {/* Main 2-Column: Patient Active Bill & Hospital Invoices Ledger */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left: Active Patient Bill Breakdown (5 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200/90 shadow-sm p-4 space-y-3.5">
          <div className="flex justify-between items-center pb-3 border-b border-slate-200">
            <div>
              <h3 className="font-bold text-sm text-slate-900">Patient Active Bill</h3>
              <p className="text-xs text-slate-500">
                {selectedPatient ? selectedPatient.name : 'Select a patient'}
              </p>
            </div>
            {patientInvoice && (
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                patientInvoice.payment_status === 'PAID' || patientInvoice.payment_status === 'CLAIM_APPROVED'
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : 'bg-amber-100 text-amber-800 border border-amber-300'
              }`}>
                {patientInvoice.payment_status}
              </span>
            )}
          </div>

          {patientInvoice ? (
            <div className="space-y-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">Invoice No:</span>
                  <b className="font-mono text-slate-800">{patientInvoice.invoice_no}</b>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Payer Scheme:</span>
                  <b className="text-indigo-700">{patientInvoice.payer_scheme}</b>
                </div>
                {patientInvoice.claim_preauth_id && (
                  <div className="flex justify-between text-emerald-700 font-semibold">
                    <span>PMJAY Pre-Auth ID:</span>
                    <span className="font-mono">{patientInvoice.claim_preauth_id}</span>
                  </div>
                )}
              </div>

              {/* Itemized Line Items */}
              <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
                <span className="text-[11px] font-bold text-slate-700 uppercase">Itemized Charges</span>
                {patientInvoice.line_items?.map((item, idx) => (
                  <div key={idx} className="flex justify-between items-center p-2 rounded bg-slate-50/60 border border-slate-100 text-[11px]">
                    <div>
                      <span className="font-semibold text-slate-900 block">{item.description}</span>
                      <span className="text-[10px] text-slate-400">Qty: {item.quantity} · Rate: ₹{item.unit_rate_inr}</span>
                    </div>
                    <span className="font-mono font-bold text-slate-800">₹{item.total_amount_inr.toFixed(2)}</span>
                  </div>
                ))}
              </div>

              {/* Totals Box */}
              <div className="p-3 bg-slate-900 text-white rounded-xl space-y-1 text-xs">
                <div className="flex justify-between text-slate-300">
                  <span>Gross Total:</span>
                  <span className="font-mono">₹{patientInvoice.gross_total_inr.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-emerald-400 font-medium">
                  <span>Scheme Concession:</span>
                  <span className="font-mono">- ₹{patientInvoice.scheme_discount_inr.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm font-bold pt-1 border-t border-slate-800">
                  <span>Net Payable:</span>
                  <span className="font-mono text-amber-400">₹{patientInvoice.net_payable_inr.toFixed(2)}</span>
                </div>
              </div>

              {/* Action */}
              {patientInvoice.payment_status !== 'PAID' && patientInvoice.payment_status !== 'CLAIM_APPROVED' && (
                <button
                  onClick={() => handleSettle(patientInvoice.invoice_no)}
                  disabled={settling}
                  className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs shadow-sm transition cursor-pointer"
                >
                  {settling ? 'Processing...' : 'Settle Payment / Verify Cashless'}
                </button>
              )}
            </div>
          ) : (
            <div className="p-8 text-center text-slate-400 text-xs">
              No invoice loaded. Select a patient from the sidebar.
            </div>
          )}
        </div>

        {/* Right: All Daily Invoices Ledger (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col max-h-[580px]">
          <div className="p-3.5 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
            <span className="font-bold text-xs text-slate-800">Hospital Billing Ledger</span>
            <span className="text-[10px] text-slate-500 font-mono">Showing 50 recent encounters</span>
          </div>

          <div className="overflow-y-auto divide-y divide-slate-100 flex-1">
            {invoices.map(inv => (
              <div key={inv.invoice_no} className="p-3 hover:bg-slate-50 transition text-xs flex justify-between items-center">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-900">{inv.patient_name}</span>
                    <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded ${
                      inv.encounter_type === 'IPD' ? 'bg-blue-100 text-blue-800' : 'bg-slate-100 text-slate-700'
                    }`}>
                      {inv.encounter_type}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400">{inv.invoice_no}</span>
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    Scheme: <span className="text-indigo-700 font-medium">{inv.payer_scheme}</span> · Mode: {inv.payment_mode}
                  </div>
                </div>

                <div className="text-right">
                  <div className="font-mono font-bold text-slate-900 text-sm">
                    ₹{inv.net_payable_inr.toFixed(2)}
                  </div>
                  <span className={`text-[9px] font-bold px-2 py-0.2 rounded-full inline-block mt-0.5 ${
                    inv.payment_status === 'CLAIM_APPROVED'
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  }`}>
                    {inv.payment_status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
