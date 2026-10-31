import React, { useState } from 'react';
import { ShieldCheck, KeyRound, QrCode, Share2, FileCode, CheckCircle2, Lock, Building2, Copy, Check } from 'lucide-react';

export default function AbdmStation({ bundle, onLinkAbha }) {
  const [activeTab, setActiveTab] = useState('M1'); // 'M1', 'M2', 'M3'

  // M1 State
  const [m1Identifier, setM1Identifier] = useState('987654321098');
  const [m1TxnId, setM1TxnId] = useState(null);
  const [m1Otp, setM1Otp] = useState('123456');
  const [m1Profile, setM1Profile] = useState(null);
  const [m1Loading, setM1Loading] = useState(false);

  // M2 State
  const [fhirData, setFhirData] = useState(null);
  const [fhirLoading, setFhirLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  // M3 State
  const [consentRequest, setConsentRequest] = useState(null);
  const [externalRecords, setExternalRecords] = useState(null);
  const [m3Loading, setM3Loading] = useState(false);

  if (!bundle || !bundle.patient) {
    return <div className="p-8 text-center text-slate-400">Select a patient to interact with ABDM Gateways.</div>;
  }

  const patient = bundle.patient;

  // --- M1 Actions ---
  const handleGenerateOtp = async () => {
    setM1Loading(true);
    try {
      const res = await fetch('/api/abdm/m1/generate-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier: m1Identifier, auth_method: 'AADHAAR_OTP' })
      });
      const data = await res.json();
      setM1TxnId(data.txn_id);
    } catch (e) {
      alert("Error generating OTP");
    } finally {
      setM1Loading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setM1Loading(true);
    try {
      const res = await fetch('/api/abdm/m1/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ txn_id: m1TxnId, otp: m1Otp })
      });
      const data = await res.json();
      setM1Profile(data);
      if (onLinkAbha) onLinkAbha(data.abha_number, data.abha_address);
    } catch (e) {
      alert("Error verifying OTP");
    } finally {
      setM1Loading(false);
    }
  };

  // --- M2 Actions ---
  const handleFetchFhir = async () => {
    setFhirLoading(true);
    try {
      const res = await fetch(`/api/abdm/m2/fhir-export/${patient.id}`);
      const data = await res.json();
      setFhirData(data);
    } catch (e) {
      alert("Error exporting FHIR bundle");
    } finally {
      setFhirLoading(false);
    }
  };

  const handleCopyFhir = () => {
    if (fhirData) {
      navigator.clipboard.writeText(JSON.stringify(fhirData.fhir_bundle, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // --- M3 Actions ---
  const handleRequestConsent = async () => {
    setM3Loading(true);
    try {
      const res = await fetch(`/api/abdm/m3/request-consent?patient_id=${patient.id}`, { method: 'POST' });
      const data = await res.json();
      setConsentRequest(data);
    } catch (e) {
      alert("Error requesting HIU consent");
    } finally {
      setM3Loading(false);
    }
  };

  const handleApproveConsent = async () => {
    if (!consentRequest) return;
    setM3Loading(true);
    try {
      await fetch(`/api/abdm/m3/approve-consent/${consentRequest.consent_id}`, { method: 'POST' });
      setConsentRequest(prev => ({ ...prev, status: "GRANTED" }));

      // Fetch external records
      const res = await fetch(`/api/abdm/m3/fetch-external-records/${consentRequest.consent_id}`);
      const recs = await res.json();
      setExternalRecords(recs);
    } catch (e) {
      alert("Error approving consent");
    } finally {
      setM3Loading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-orange-800 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded">
              NATIONAL HEALTH AUTHORITY
            </span>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-orange-600" />
              <span>AYUSHMAN BHARAT DIGITAL MISSION (ABDM) GATEWAYS</span>
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Interoperability simulation for Patient: <b>{patient.name}</b> · East Point Hospital HIP/HIU Node
          </p>
        </div>

        {/* M1, M2, M3 Tabs */}
        <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200">
          <button
            onClick={() => setActiveTab('M1')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'M1' ? 'bg-orange-600 text-white shadow' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            M1: Identity (ABHA)
          </button>
          <button
            onClick={() => {
              setActiveTab('M2');
              if (!fhirData) handleFetchFhir();
            }}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'M2' ? 'bg-blue-600 text-white shadow' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            M2: Provider (FHIR)
          </button>
          <button
            onClick={() => setActiveTab('M3')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'M3' ? 'bg-emerald-600 text-white shadow' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            M3: User (HIU Consent)
          </button>
        </div>
      </div>

      {/* --- M1: IDENTITY (ABHA ID) --- */}
      {activeTab === 'M1' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* OTP Generation Box */}
          <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
            <div className="pb-3 border-b border-slate-200">
              <span className="text-xs font-bold text-orange-600 uppercase">Gateway M1 Authentication</span>
              <h3 className="text-sm font-bold text-slate-900">Aadhaar / Mobile ABHA Creation Workflow</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Simulates real-time OTP verification with the NHA Sandbox Registry.
              </p>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  Aadhaar (12-digits) or Mobile Number
                </label>
                <input
                  type="text"
                  value={m1Identifier}
                  onChange={(e) => setM1Identifier(e.target.value)}
                  className="w-full px-3 py-2 text-xs font-mono border border-slate-300 rounded-md focus:outline-none focus:ring-1 focus:ring-orange-500"
                />
              </div>

              {!m1TxnId ? (
                <button
                  onClick={handleGenerateOtp}
                  disabled={m1Loading}
                  className="w-full py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-md text-xs font-bold shadow transition flex items-center justify-center space-x-2"
                >
                  <KeyRound className="w-3.5 h-3.5" />
                  <span>{m1Loading ? "Sending OTP..." : "Generate ABDM Mock OTP"}</span>
                </button>
              ) : (
                <div className="space-y-3 pt-2">
                  <div className="p-2.5 bg-orange-50 border border-orange-200 rounded text-xs text-orange-800">
                    OTP sent to registered Aadhaar mobile. <b>Demo OTP: 123456</b>
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-700 block mb-1">Enter 6-Digit OTP</label>
                    <input
                      type="text"
                      value={m1Otp}
                      onChange={(e) => setM1Otp(e.target.value)}
                      className="w-full px-3 py-2 text-center text-sm font-mono tracking-widest border border-slate-300 rounded-md"
                    />
                  </div>
                  <button
                    onClick={handleVerifyOtp}
                    disabled={m1Loading}
                    className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-md text-xs font-bold shadow transition"
                  >
                    {m1Loading ? "Verifying..." : "Verify OTP & Issue ABHA Card"}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Rendered ABHA ID Card */}
          <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 flex flex-col justify-between">
            <div>
              <div className="pb-3 border-b border-slate-200 flex justify-between items-center">
                <span className="text-xs font-bold text-slate-500 uppercase">National Health ID Card</span>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-800 font-bold border border-emerald-300">
                  KYC VERIFIED
                </span>
              </div>

              {/* Graphic ABHA Card */}
              <div className="mt-4 p-5 rounded-xl bg-gradient-to-br from-orange-600 via-amber-600 to-emerald-700 text-white shadow-xl relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-widest text-orange-100">
                      Ayushman Bharat Health Account
                    </span>
                    <h4 className="text-base font-extrabold tracking-wide mt-0.5">
                      {m1Profile ? m1Profile.name : patient.name}
                    </h4>
                  </div>
                  <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center p-1.5 backdrop-blur-sm">
                    <QrCode className="w-full h-full text-white" />
                  </div>
                </div>

                <div className="mt-6 space-y-1">
                  <span className="text-[10px] uppercase text-orange-200 block font-semibold">ABHA Number</span>
                  <div className="text-sm font-mono font-bold tracking-widest bg-black/20 px-2.5 py-1 rounded inline-block">
                    {m1Profile ? m1Profile.abha_number : (patient.abha_id || "91-4829-1029-4482")}
                  </div>
                </div>

                <div className="mt-4 flex justify-between items-end text-xs">
                  <div>
                    <span className="text-[9px] uppercase text-orange-200 block">ABHA Address</span>
                    <span className="font-mono font-semibold">
                      {m1Profile ? m1Profile.abha_address : (patient.abha_address || `${patient.name.toLowerCase().split(' ')[0]}@abdm`)}
                    </span>
                  </div>
                  <span className="text-[10px] text-white/80 font-mono">Gender: {patient.gender[0]}</span>
                </div>
              </div>
            </div>

            <p className="text-[11px] text-slate-500 mt-4 text-center">
              Verified through Ayushman Bharat Digital Mission (NHA SandBox M1 Gateway).
            </p>
          </div>
        </div>
      )}

      {/* --- M2: INFORMATION PROVIDER (FHIR R4) --- */}
      {activeTab === 'M2' && (
        <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-3 border-b border-slate-200 gap-2">
            <div>
              <span className="text-xs font-bold text-blue-600 uppercase">Gateway M2 Information Provider</span>
              <h3 className="text-sm font-bold text-slate-900">HL7 FHIR R4 Standardized Health Data Bundle</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Compliant with NHA NRCES India FHIR Profile: <b>DiagnosticReportRecord</b>
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopyFhir}
                className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-900 text-white text-xs px-3 py-1.5 rounded-md font-mono transition"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? "Copied!" : "Copy JSON"}</span>
              </button>
              <button
                onClick={handleFetchFhir}
                disabled={fhirLoading}
                className="flex items-center space-x-1 bg-blue-600 hover:bg-blue-700 text-white text-xs px-3 py-1.5 rounded-md font-medium transition"
              >
                <span>{fhirLoading ? "Formatting..." : "Refresh FHIR"}</span>
              </button>
            </div>
          </div>

          {/* FHIR JSON Inspector */}
          {fhirData ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                <div className="p-2 bg-slate-50 border border-slate-200 rounded">
                  <span className="text-[10px] text-slate-400 block">Bundle Type</span>
                  <span className="font-mono font-bold text-blue-900">{fhirData.fhir_bundle.type}</span>
                </div>
                <div className="p-2 bg-slate-50 border border-slate-200 rounded">
                  <span className="text-[10px] text-slate-400 block">FHIR Resources</span>
                  <span className="font-mono font-bold text-slate-900">{fhirData.fhir_bundle.entry?.length || 0} entries</span>
                </div>
                <div className="p-2 bg-slate-50 border border-slate-200 rounded">
                  <span className="text-[10px] text-slate-400 block">HIP Facility ID</span>
                  <span className="font-mono font-bold text-slate-900">{fhirData.hip_id}</span>
                </div>
                <div className="p-2 bg-slate-50 border border-slate-200 rounded">
                  <span className="text-[10px] text-slate-400 block">Care Context</span>
                  <span className="font-mono font-bold text-slate-900">{fhirData.care_context?.careContextReference}</span>
                </div>
              </div>

              <div className="bg-slate-950 text-emerald-400 p-4 rounded-lg font-mono text-xs overflow-x-auto max-h-[380px] shadow-inner border border-slate-800">
                <pre>{JSON.stringify(fhirData.fhir_bundle, null, 2)}</pre>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-xs text-slate-400">Loading FHIR R4 Bundle...</div>
          )}
        </div>
      )}

      {/* --- M3: INFORMATION USER (HIU CONSENT) --- */}
      {activeTab === 'M3' && (
        <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="pb-3 border-b border-slate-200">
            <span className="text-xs font-bold text-emerald-600 uppercase">Gateway M3 Information User</span>
            <h3 className="text-sm font-bold text-slate-900">Physician Consent Artifact & External Records Fetch</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Attending doctor requests consent to view external hospital records from the ABDM Health Information Exchange.
            </p>
          </div>

          {!consentRequest ? (
            <div className="p-8 text-center bg-slate-50 rounded-lg border border-dashed border-slate-300 space-y-3">
              <Building2 className="w-8 h-8 text-slate-400 mx-auto" />
              <div>
                <h4 className="text-sm font-bold text-slate-800">Request External Health Records</h4>
                <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
                  Dr. B. R. Ramachandra requesting consent to fetch prior admissions, discharge summaries, and radiology reports from outside networks.
                </p>
              </div>
              <button
                onClick={handleRequestConsent}
                disabled={m3Loading}
                className="py-2 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-md text-xs font-bold shadow transition"
              >
                {m3Loading ? "Initiating..." : "Initiate ABDM Consent Request"}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Consent Pop-Up / Artifact */}
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono font-bold text-xs text-emerald-900 bg-emerald-200/70 px-2 py-0.5 rounded">
                      {consentRequest.consent_id}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${consentRequest.status === 'GRANTED' ? 'bg-emerald-600 text-white' : 'bg-amber-100 text-amber-800'}`}>
                      STATUS: {consentRequest.status}
                    </span>
                  </div>
                  <p className="text-xs text-emerald-950 font-semibold mt-1">
                    Purpose: Care Management (CAREMGT) · Requester: {consentRequest.requester_doctor} ({consentRequest.requester_doctor_reg})
                  </p>
                  <p className="text-[11px] text-emerald-800">
                    Patient ABHA ID: <b>{consentRequest.patient_abha_id}</b>
                  </p>
                </div>

                {consentRequest.status === 'REQUESTED' ? (
                  <button
                    onClick={handleApproveConsent}
                    disabled={m3Loading}
                    className="py-2 px-4 bg-emerald-700 hover:bg-emerald-800 text-white rounded-md text-xs font-bold shadow transition shrink-0"
                  >
                    {m3Loading ? "Approving..." : "Approve Consent (Mock Health Locker)"}
                  </button>
                ) : (
                  <div className="flex items-center space-x-1.5 text-xs font-bold text-emerald-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Consent Granted by Patient</span>
                  </div>
                )}
              </div>

              {/* Fetched External Records */}
              {externalRecords && (
                <div className="space-y-3 pt-2">
                  <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                    Records Retrieved from External ABDM Network
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {externalRecords.map((rec, i) => (
                      <div key={i} className="p-3.5 bg-white border border-slate-200 rounded-lg shadow-sm space-y-1.5 text-xs">
                        <div className="flex justify-between items-start">
                          <span className="font-bold text-slate-900">{rec.source_hospital}</span>
                          <span className="font-mono text-[10px] text-slate-500">{rec.date}</span>
                        </div>
                        <div className="text-[11px] font-semibold text-blue-700">
                          {rec.record_type}: {rec.diagnosis}
                        </div>
                        <p className="text-slate-600 text-[11px] leading-relaxed bg-slate-50 p-2 rounded">
                          {rec.summary}
                        </p>
                        <div className="text-[10px] text-slate-400 font-mono">
                          Physician: {rec.physician}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
