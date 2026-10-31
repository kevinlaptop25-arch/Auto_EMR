import React, { useState, useEffect } from 'react';
import {
  Stethoscope,
  HeartPulse,
  FlaskConical,
  Film,
  ShieldCheck,
  BarChart3,
  FileText,
  Siren,
  Pill,
  Receipt,
  Droplet
} from 'lucide-react';

import Navbar from './components/Navbar';
import PatientSidebar from './components/PatientSidebar';
import PatientBanner from './components/PatientBanner';
import DoctorStation from './components/DoctorStation';
import NurseStation from './components/NurseStation';
import LabStation from './components/LabStation';
import PacsStation from './components/PacsStation';
import AbdmStation from './components/AbdmStation';
import AuditStation from './components/AuditStation';
import EmergencyStation from './components/EmergencyStation';
import PharmacyStation from './components/PharmacyStation';
import BillingStation from './components/BillingStation';
import BloodBankStation from './components/BloodBankStation';

export default function App() {
  const [activeStation, setActiveStation] = useState('doctor'); // 'doctor', 'nurse', 'labs', 'pacs', 'abdm', 'audit'
  const [timeline, setTimeline] = useState(null);
  const [activePreset, setActivePreset] = useState('INSPECTION_1PM');
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientBundle, setPatientBundle] = useState(null);

  // Filters
  const [filterType, setFilterType] = useState('IPD');
  const [department, setDepartment] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loadingList, setLoadingList] = useState(false);
  const [loadingBundle, setLoadingBundle] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // Modal for FHIR Inspection
  const [fhirModalJson, setFhirModalJson] = useState(null);

  // Fetch Timeline Clock
  const fetchTimeline = async () => {
    try {
      const res = await fetch('/api/audit/timeline');
      const data = await res.json();
      setTimeline(data);
      if (data.active_preset) {
        setActivePreset(data.active_preset);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Fetch Patients List
  const fetchPatients = async () => {
    setLoadingList(true);
    try {
      const params = new URLSearchParams();
      if (filterType !== 'ALL') params.append('filter_type', filterType);
      if (department) params.append('department', department);
      if (searchQuery) params.append('search', searchQuery);
      params.append('limit', '50');

      const res = await fetch(`/api/patients?${params.toString()}`);
      const data = await res.json();
      setPatients(data.data || []);

      // Auto-select first patient if none selected
      if (!selectedPatient && data.data && data.data.length > 0) {
        handleSelectPatient(data.data[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingList(false);
    }
  };

  // Fetch Patient Detailed Bundle
  const handleSelectPatient = async (patient, targetPreset) => {
    setSelectedPatient(patient);
    setLoadingBundle(true);
    try {
      const p = targetPreset || activePreset;
      const res = await fetch(`/api/patients/${patient.id}${p ? `?preset=${p}` : ''}`);
      const data = await res.json();
      setPatientBundle(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingBundle(false);
    }
  };

  // Change Timeline Preset
  const handlePresetChange = async (presetName) => {
    // 1. Optimistic UI update for immediate click feedback
    setActivePreset(presetName);
    try {
      await fetch(`/api/audit/timeline/set-preset?preset=${presetName}`, { method: 'POST' });
      await fetchTimeline();
      // Re-fetch active bundle to reflect new chronological filter
      if (selectedPatient) {
        await handleSelectPatient(selectedPatient, presetName);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Regenerate Cohort (Target 2,800+ Encounters: 2,600 OPD + 200 IPD, 21 Depts)
  const handleRefreshCohort = async () => {
    setIsGenerating(true);
    try {
      await fetch('/api/audit/generate-batch?count=2800', { method: 'POST' });
      await fetchPatients();
      if (selectedPatient) {
        handleSelectPatient(selectedPatient);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  // Instant 1-click ABHA generation (30% - 35% target)
  const handleQuickGenerateAbha = async (patientId) => {
    try {
      const res = await fetch(`/api/abdm/m1/quick-generate/${patientId}`, { method: 'POST' });
      const data = await res.json();
      if (data.status === 'SUCCESS' || data.status === 'ALREADY_LINKED') {
        handleLinkAbha(data.abha_id, data.abha_address);
        await fetchPatients();
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Download PDF Handler
  const handleDownloadPdf = (type) => {
    if (!selectedPatient) return;
    if (type === 'casesheet') {
      window.open(`/api/clinical/${selectedPatient.id}/pdf/casesheet`, '_blank');
    } else if (type === 'discharge') {
      window.open(`/api/clinical/${selectedPatient.id}/pdf/discharge`, '_blank');
    } else if (type === 'opd') {
      window.open(`/api/clinical/${selectedPatient.id}/pdf/opd-slip`, '_blank');
    }
  };

  // Convert OPD Patient to Inpatient (IPD)
  const handleAdmitToIpd = async () => {
    if (!selectedPatient) return;
    try {
      const res = await fetch(`/api/clinical/${selectedPatient.id}/admit-to-ipd`, { method: 'POST' });
      const data = await res.json();
      if (data.bundle) {
        setPatientBundle(data.bundle);
        setSelectedPatient(data.bundle.patient);
        await fetchPatients();
      }
    } catch (e) {
      alert("Error admitting patient to IPD");
    }
  };

  // Download Lab PDF Handler
  const handleDownloadLabPdf = (labId) => {
    if (!selectedPatient) return;
    window.open(`/api/labs/${selectedPatient.id}/${labId}/pdf`, '_blank');
  };

  // View Lab FHIR Handler
  const handleViewFhir = async (labId) => {
    if (!selectedPatient) return;
    try {
      const res = await fetch(`/api/labs/${selectedPatient.id}/${labId}/fhir`);
      const data = await res.json();
      setFhirModalJson(data);
    } catch (e) {
      alert("Error fetching FHIR bundle");
    }
  };

  // Update ABHA ID locally on linkage
  const handleLinkAbha = (abhaNo, abhaAddr) => {
    if (selectedPatient) {
      setSelectedPatient(prev => ({
        ...prev,
        abha_id: abhaNo,
        abha_address: abhaAddr,
        abha_verified: true
      }));
      if (patientBundle && patientBundle.patient) {
        patientBundle.patient.abha_id = abhaNo;
        patientBundle.patient.abha_address = abhaAddr;
        patientBundle.patient.abha_verified = true;
      }
    }
  };

  useEffect(() => {
    fetchTimeline();
    fetchPatients();
  }, [filterType, department, searchQuery]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-100 text-slate-900 font-sans antialiased">
      {/* Top Navbar with East Point Hospital branding & NMC timeline scrubber */}
      <Navbar
        timeline={timeline}
        activePreset={activePreset}
        onPresetChange={handlePresetChange}
        onRefreshCohort={handleRefreshCohort}
        isGenerating={isGenerating}
      />

      {/* Main Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar: Patients Cohort */}
        <PatientSidebar
          patients={patients}
          selectedPatient={selectedPatient}
          onSelectPatient={handleSelectPatient}
          filterType={filterType}
          setFilterType={setFilterType}
          department={department}
          setDepartment={setDepartment}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          loading={loadingList}
        />

        {/* Right Main Content Area */}
        <main className="flex-1 overflow-y-auto flex flex-col h-[calc(100vh-4rem)] bg-slate-100/90">
          {/* Station Selector Bar */}
          <div className="bg-white border-b border-slate-200/90 px-3 sm:px-6 py-2 flex items-center space-x-1.5 overflow-x-auto shadow-2xs sticky top-0 z-20 shrink-0">
            <button
              onClick={() => setActiveStation('doctor')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'doctor'
                  ? 'bg-red-600 text-white shadow-sm ring-1 ring-red-500'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Stethoscope className="w-3.5 h-3.5 shrink-0" />
              <span>Doctor Station</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'doctor' ? 'bg-red-800 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                MRD/39 & 40
              </span>
            </button>

            <button
              onClick={() => setActiveStation('nurse')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'nurse'
                  ? 'bg-blue-600 text-white shadow-sm ring-1 ring-blue-500'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <HeartPulse className="w-3.5 h-3.5 shrink-0" />
              <span>Nurse Station</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'nurse' ? 'bg-blue-800 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                MAR & TPR
              </span>
            </button>

            <button
              onClick={() => setActiveStation('emergency')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'emergency'
                  ? 'bg-rose-600 text-white shadow-sm ring-1 ring-rose-500'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Siren className="w-3.5 h-3.5 shrink-0" />
              <span>Emergency & Trauma</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'emergency' ? 'bg-rose-800 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                24x7 ESI
              </span>
            </button>

            <button
              onClick={() => setActiveStation('pharmacy')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'pharmacy'
                  ? 'bg-teal-700 text-white shadow-sm ring-1 ring-teal-600'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Pill className="w-3.5 h-3.5 shrink-0" />
              <span>Central Pharmacy</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'pharmacy' ? 'bg-teal-900 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                Formulary
              </span>
            </button>

            <button
              onClick={() => setActiveStation('billing')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'billing'
                  ? 'bg-indigo-700 text-white shadow-sm ring-1 ring-indigo-600'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Receipt className="w-3.5 h-3.5 shrink-0" />
              <span>Billing & Cashier</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'billing' ? 'bg-indigo-900 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                PMJAY/Cash
              </span>
            </button>

            <button
              onClick={() => setActiveStation('bloodbank')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'bloodbank'
                  ? 'bg-rose-800 text-white shadow-sm ring-1 ring-rose-700'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Droplet className="w-3.5 h-3.5 shrink-0" />
              <span>Blood Centre</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'bloodbank' ? 'bg-rose-950 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                KA/BLD/042
              </span>
            </button>

            <button
              onClick={() => setActiveStation('labs')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'labs'
                  ? 'bg-teal-700 text-white shadow-sm ring-1 ring-teal-600'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <FlaskConical className="w-3.5 h-3.5 shrink-0" />
              <span>Diagnostic Labs</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'labs' ? 'bg-teal-900 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                Path/Bio/Micro
              </span>
            </button>

            <button
              onClick={() => setActiveStation('pacs')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'pacs'
                  ? 'bg-violet-700 text-white shadow-sm ring-1 ring-violet-600'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Film className="w-3.5 h-3.5 shrink-0" />
              <span>PACS Radiology</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'pacs' ? 'bg-violet-900 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                DICOM
              </span>
            </button>

            <button
              onClick={() => setActiveStation('abdm')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'abdm'
                  ? 'bg-orange-600 text-white shadow-sm ring-1 ring-orange-500'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
              <span>ABDM Gateways</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'abdm' ? 'bg-orange-800 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                M1/M2/M3
              </span>
            </button>

            <button
              onClick={() => setActiveStation('audit')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                activeStation === 'audit'
                  ? 'bg-slate-900 text-white shadow-sm ring-1 ring-slate-800'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5 shrink-0" />
              <span>NMC Audit</span>
              <span className={`text-[9px] px-1.5 py-0.2 rounded font-mono font-semibold ${
                activeStation === 'audit' ? 'bg-slate-700 text-white' : 'bg-slate-100 text-slate-600'
              }`}>
                2,800+ Quota
              </span>
            </button>
          </div>

          {/* Active Station Viewport */}
          <div className="p-4 sm:p-6 max-w-7xl w-full mx-auto flex-1">
            {/* Unified Patient Banner across clinical stations */}
            {activeStation !== 'audit' && (
              <PatientBanner
                bundle={patientBundle}
                onDownloadPdf={handleDownloadPdf}
                onAdmitToIpd={handleAdmitToIpd}
                onQuickGenerateAbha={handleQuickGenerateAbha}
              />
            )}

            {loadingBundle ? (
              <div className="p-16 text-center text-slate-400 bg-white rounded-xl border border-slate-200">
                <div className="inline-block w-8 h-8 border-3 border-red-600 border-t-transparent rounded-full animate-spin mb-3"></div>
                <p className="text-xs font-medium text-slate-600">Retrieving patient medical record and applying live audit clock filters...</p>
              </div>
            ) : (
              <>
                {activeStation === 'doctor' && (
                  <DoctorStation
                    bundle={patientBundle}
                    onDownloadPdf={handleDownloadPdf}
                    onAdmitToIpd={handleAdmitToIpd}
                  />
                )}
                {activeStation === 'nurse' && (
                  <NurseStation
                    bundle={patientBundle}
                  />
                )}
                {activeStation === 'emergency' && (
                  <EmergencyStation
                    selectedPatient={selectedPatient}
                  />
                )}
                {activeStation === 'pharmacy' && (
                  <PharmacyStation
                    selectedPatient={selectedPatient}
                  />
                )}
                {activeStation === 'billing' && (
                  <BillingStation
                    selectedPatient={selectedPatient}
                  />
                )}
                {activeStation === 'bloodbank' && (
                  <BloodBankStation
                    selectedPatient={selectedPatient}
                  />
                )}
                {activeStation === 'labs' && (
                  <LabStation
                    bundle={patientBundle}
                    onDownloadLabPdf={handleDownloadLabPdf}
                    onViewFhir={handleViewFhir}
                  />
                )}
                {activeStation === 'pacs' && (
                  <PacsStation
                    bundle={patientBundle}
                  />
                )}
                {activeStation === 'abdm' && (
                  <AbdmStation
                    bundle={patientBundle}
                    onLinkAbha={handleLinkAbha}
                  />
                )}
                {activeStation === 'audit' && (
                  <AuditStation
                    timeline={timeline}
                    activePreset={activePreset}
                    onPresetChange={handlePresetChange}
                    onRefreshCohort={handleRefreshCohort}
                    isGenerating={isGenerating}
                  />
                )}
              </>
            )}
          </div>
        </main>
      </div>

      {/* ABDM M2 FHIR Inspection Modal */}
      {fhirModalJson && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden">
            <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
              <div>
                <h3 className="font-bold text-sm text-slate-900">
                  ABDM M2 FHIR R4 Diagnostic Report Record
                </h3>
                <p className="text-xs text-slate-500 font-mono">
                  Resource: Bundle (type: document) · LOINC Standardized Observations
                </p>
              </div>
              <button
                onClick={() => setFhirModalJson(null)}
                className="text-slate-400 hover:text-slate-700 text-sm font-bold px-2 py-1 rounded"
              >
                ✕ Close
              </button>
            </div>
            <div className="p-4 flex-1 overflow-auto bg-slate-950 text-emerald-400 font-mono text-xs">
              <pre>{JSON.stringify(fhirModalJson, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}