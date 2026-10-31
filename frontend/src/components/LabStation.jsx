import React, { useState } from 'react';
import { FlaskConical, Download, Code, CheckCircle2, AlertOctagon } from 'lucide-react';

export default function LabStation({ bundle, onDownloadLabPdf, onViewFhir }) {
  const [activeDept, setActiveDept] = useState('Pathology');

  if (!bundle || !bundle.patient) {
    return <div className="p-8 text-center text-slate-400">Select a patient to inspect lab reports.</div>;
  }

  const reports = bundle.lab_reports || [];
  const depts = ['Pathology', 'Biochemistry', 'Microbiology'];
  const currentReport = reports.find((r) => r.department.toLowerCase() === activeDept.toLowerCase());

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-teal-800 bg-teal-50 border border-teal-200 px-2 py-0.5 rounded">
              DIAGNOSTIC SERVICES
            </span>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <FlaskConical className="w-5 h-5 text-teal-600" />
              <span>EAST POINT CENTRAL CLINICAL LABORATORIES</span>
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            NABH / NABL Accredited diagnostic results for {bundle.patient.name} (MRN: {bundle.patient.mr_no})
          </p>
        </div>

        {/* Dept Selector Tabs */}
        <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200">
          {depts.map((d) => (
            <button
              key={d}
              onClick={() => setActiveDept(d)}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
                activeDept === d
                  ? 'bg-teal-700 text-white shadow'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* Active Lab Report View */}
      {currentReport ? (
        <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-3 border-b border-slate-200 gap-2">
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase">Panel Category</span>
              <h3 className="text-base font-bold text-slate-900">{currentReport.test_category}</h3>
              <div className="text-[11px] text-slate-500 flex items-center space-x-2 mt-0.5">
                <span>Sample ID: <b>{currentReport.sample_id}</b></span>
                <span>·</span>
                <span>Type: <b>{currentReport.sample_type}</b></span>
                <span>·</span>
                <span>Reported: <b>{new Date(currentReport.reported_at).toLocaleString()}</b></span>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => onViewFhir(currentReport.id)}
                className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-900 text-slate-200 text-xs px-3 py-1.5 rounded-md font-mono transition"
              >
                <Code className="w-3.5 h-3.5 text-emerald-400" />
                <span>FHIR R4 (ABDM M2)</span>
              </button>
              <button
                onClick={() => onDownloadLabPdf(currentReport.id)}
                className="flex items-center space-x-1.5 bg-teal-700 hover:bg-teal-800 text-white text-xs px-3 py-1.5 rounded-md font-medium shadow transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Report PDF</span>
              </button>
            </div>
          </div>

          {/* Test Items Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-200 divide-y divide-slate-200">
              <thead className="bg-slate-900 text-white font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Investigation Parameter</th>
                  <th className="py-2.5 px-3">Observed Value</th>
                  <th className="py-2.5 px-2">Unit</th>
                  <th className="py-2.5 px-3">Biological Reference Interval</th>
                  <th className="py-2.5 px-2 text-center">Status / Flag</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {currentReport.items.map((item, idx) => {
                  const isCrit = item.flag === 'CRITICAL' || item.flag === 'POSITIVE';
                  const isHigh = item.flag === 'HIGH';
                  const isLow = item.flag === 'LOW';

                  return (
                    <tr key={idx} className={isCrit ? 'bg-red-50/60' : 'hover:bg-slate-50'}>
                      <td className="py-2.5 px-3 font-medium text-slate-900">{item.name}</td>
                      <td className={`py-2.5 px-3 font-mono font-bold text-sm ${isCrit ? 'text-red-700' : isHigh ? 'text-amber-700' : isLow ? 'text-blue-700' : 'text-slate-800'}`}>
                        {item.result_value}
                      </td>
                      <td className="py-2.5 px-2 text-slate-500 font-mono text-[11px]">{item.unit}</td>
                      <td className="py-2.5 px-3 text-slate-600 font-mono text-[11px]">{item.reference_range}</td>
                      <td className="py-2.5 px-2 text-center">
                        <span
                          className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-bold ${
                            isCrit
                              ? 'bg-red-100 text-red-800 border border-red-300'
                              : isHigh
                              ? 'bg-amber-100 text-amber-800 border border-amber-300'
                              : isLow
                              ? 'bg-blue-100 text-blue-800 border border-blue-300'
                              : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          {isCrit && <AlertOctagon className="w-2.5 h-2.5 text-red-600" />}
                          <span>{item.flag}</span>
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Clinical Impression */}
          {currentReport.clinical_impression && (
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-md text-xs">
              <span className="font-bold text-slate-700 block mb-0.5">Clinical Pathologist Interpretation:</span>
              <p className="text-slate-800 italic">{currentReport.clinical_impression}</p>
            </div>
          )}

          {/* Verification Sign */}
          <div className="pt-2 flex justify-between items-center text-xs text-slate-600 border-t border-slate-100">
            <span className="font-mono text-[11px]">Lab Acc: NABL/MC-2849</span>
            <div className="text-right">
              <span className="font-bold text-slate-900 block">{currentReport.pathologist_name}</span>
              <span className="font-mono text-slate-500 text-[11px]">{currentReport.pathologist_reg}</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center text-xs text-slate-400 bg-white rounded-lg border border-slate-200">
          No diagnostic report available for {activeDept} at the current simulation timestamp.
        </div>
      )}
    </div>
  );
}
