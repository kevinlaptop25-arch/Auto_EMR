import React from 'react';
import { Pill, Activity, Syringe, HeartPulse, Check, UserCheck, ShieldCheck } from 'lucide-react';

export default function NurseStation({ bundle }) {
  if (!bundle || !bundle.patient) {
    return (
      <div className="p-16 text-center text-slate-400 bg-white rounded-2xl border border-slate-200">
        <HeartPulse className="w-10 h-10 text-slate-300 mx-auto mb-2" />
        <p className="text-sm font-medium text-slate-600">Please select an inpatient to view nursing charts and vital records.</p>
      </div>
    );
  }

  const { patient, medication_sheets = [], diabetic_entries = [], tpr_chart } = bundle;
  const isDiabetic = diabetic_entries.length > 0;

  return (
    <div className="space-y-6">
      {/* Station Subheader */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-blue-50 border border-blue-200 text-blue-600">
            <HeartPulse className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-blue-50 text-blue-800 border-blue-200">
                WARD NURSING WORKSTATION
              </span>
              <span className="text-xs font-mono text-slate-500">
                FORMS: F/EPH/MRD/58 · F/MRD/EPH/07 · F/EPH/MRD/54
              </span>
            </div>
            <h3 className="text-sm font-bold text-slate-900 mt-0.5">
              Inpatient Nursing Administration, TPR Graphic Logs & Diabetic Flowsheets
            </h3>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-600 font-medium">
          <span className="px-2.5 py-1 bg-slate-100 rounded-lg border border-slate-200">
            Assigned Ward: <b>{patient.department}</b>
          </span>
        </div>
      </div>

      {/* Form F/EPH/MRD/58: Medication Administration Sheet */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="flex justify-between items-center pb-3 border-b border-slate-200">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-2.5 py-1 rounded-md">
                FORM F/EPH/MRD/58
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Medication Administration Record (MAR / Drug Chart)
                </h4>
                <p className="text-[11px] text-slate-500">
                  Shift-wise nurse initials logged upon executing physician treatment orders.
                </p>
              </div>
            </div>
          </div>
          <Pill className="w-5 h-5 text-indigo-600 shrink-0" />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border border-slate-200 divide-y divide-slate-200 rounded-lg overflow-hidden">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="py-2.5 px-3">Drug / Formulation</th>
                <th className="py-2.5 px-2">Route</th>
                <th className="py-2.5 px-2">Frequency</th>
                <th className="py-2.5 px-2 text-center">06:00 AM</th>
                <th className="py-2.5 px-2 text-center">10:00 AM</th>
                <th className="py-2.5 px-2 text-center">02:00 PM</th>
                <th className="py-2.5 px-2 text-center">06:00 PM</th>
                <th className="py-2.5 px-2 text-center">10:00 PM</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {medication_sheets.map((med, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition">
                  <td className="py-2.5 px-3 font-semibold text-slate-900">{med.drug_name}</td>
                  <td className="py-2.5 px-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      med.route === 'IV' ? 'bg-red-100 text-red-800' : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {med.route}
                    </span>
                  </td>
                  <td className="py-2.5 px-2 font-mono text-slate-600">{med.frequency}</td>
                  <td className="py-2.5 px-2 text-center font-mono font-bold text-slate-700 bg-slate-50/50">
                    <span className="inline-block px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-indigo-800 text-[10px]">
                      {med.slots["06:00"] || "✓"}
                    </span>
                  </td>
                  <td className="py-2.5 px-2 text-center font-mono font-bold text-slate-700">
                    <span className="inline-block px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-indigo-800 text-[10px]">
                      {med.slots["10:00"] || "✓"}
                    </span>
                  </td>
                  <td className="py-2.5 px-2 text-center font-mono font-bold text-slate-700 bg-slate-50/50">
                    <span className="inline-block px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-indigo-800 text-[10px]">
                      {med.slots["14:00"] || "✓"}
                    </span>
                  </td>
                  <td className="py-2.5 px-2 text-center font-mono font-bold text-slate-700">
                    <span className="inline-block px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-indigo-800 text-[10px]">
                      {med.slots["18:00"] || "✓"}
                    </span>
                  </td>
                  <td className="py-2.5 px-2 text-center font-mono font-bold text-slate-700 bg-slate-50/50">
                    <span className="inline-block px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-indigo-800 text-[10px]">
                      {med.slots["22:00"] || "✓"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Form F/MRD/EPH/07: Graphic TPR Chart */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="flex justify-between items-center pb-3 border-b border-slate-200">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-1 rounded-md">
                FORM F/MRD/EPH/07
              </span>
              <div>
                <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Graphic TPR (Temperature - Pulse - Respiration) Log
                </h4>
                <p className="text-[11px] text-slate-500">
                  4-hourly physical vital observations and physiological stability monitoring.
                </p>
              </div>
            </div>
          </div>
          <Activity className="w-5 h-5 text-rose-600 shrink-0" />
        </div>

        {tpr_chart?.readings && tpr_chart.readings.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-200 divide-y divide-slate-200 rounded-lg overflow-hidden">
              <thead className="bg-slate-900 text-white font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Date / Time Slot</th>
                  <th className="py-2.5 px-2 text-center">Day</th>
                  <th className="py-2.5 px-2 text-center">Temp (°F)</th>
                  <th className="py-2.5 px-2 text-center">Pulse (bpm)</th>
                  <th className="py-2.5 px-2 text-center">Resp (cpm)</th>
                  <th className="py-2.5 px-2 text-center">Stool</th>
                  <th className="py-2.5 px-2 text-center">Urine</th>
                  <th className="py-2.5 px-2 text-center">Bath</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {tpr_chart.readings.map((r, i) => {
                  const isFever = r.temp_f >= 100.0;
                  return (
                    <tr key={i} className="hover:bg-slate-50/80 transition">
                      <td className="py-2.5 px-3 font-mono text-slate-800">
                        {new Date(r.timestamp).toLocaleDateString()} · {r.slot_label}
                      </td>
                      <td className="py-2.5 px-2 text-center font-bold text-slate-700">D{r.day_no}</td>
                      <td className={`py-2.5 px-2 text-center font-mono font-bold ${
                        isFever ? 'text-rose-700 bg-rose-50/80' : 'text-slate-800'
                      }`}>
                        {r.temp_f.toFixed(1)}°F
                      </td>
                      <td className="py-2.5 px-2 text-center font-mono font-bold text-blue-700">
                        {r.pulse_bpm}
                      </td>
                      <td className="py-2.5 px-2 text-center font-mono text-slate-700">
                        {r.resp_cpm}
                      </td>
                      <td className="py-2.5 px-2 text-center text-slate-600">{r.stool}</td>
                      <td className="py-2.5 px-2 text-center text-slate-600">{r.urine}</td>
                      <td className="py-2.5 px-2 text-center text-slate-600">{r.bath}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-xs text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200">
            No TPR vital readings recorded prior to current simulation clock.
          </div>
        )}
      </div>

      {/* Form F/EPH/MRD/54: Diabetic Chart (Only shown if patient has blood glucose tracking) */}
      {isDiabetic && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex justify-between items-center pb-3 border-b border-slate-200">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-amber-800 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-md">
                  FORM F/EPH/MRD/54
                </span>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                    Diabetic Flowsheet & Regular Insulin Sliding Scale Record
                  </h4>
                  <p className="text-[11px] text-slate-500">
                    Serial capillary blood glucose (GRBS) monitoring and subcutaneous Actrapid administration.
                  </p>
                </div>
              </div>
            </div>
            <Syringe className="w-5 h-5 text-amber-600 shrink-0" />
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-200 divide-y divide-slate-200 rounded-lg overflow-hidden">
              <thead className="bg-slate-900 text-white font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Date & Time</th>
                  <th className="py-2.5 px-3">Blood Sugar (GRBS)</th>
                  <th className="py-2.5 px-2">Urine Sugar</th>
                  <th className="py-2.5 px-2">Urine Ketones</th>
                  <th className="py-2.5 px-3">Insulin Administered</th>
                  <th className="py-2.5 px-2 text-center">Dose</th>
                  <th className="py-2.5 px-3">Nurse Verification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {diabetic_entries.map((entry) => {
                  const isHigh = entry.blood_sugar_grbs > 200;
                  return (
                    <tr key={entry.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-2.5 px-3 font-mono text-slate-800">
                        {new Date(entry.timestamp).toLocaleString()}
                      </td>
                      <td className={`py-2.5 px-3 font-mono font-bold text-sm ${
                        isHigh ? 'text-amber-800 bg-amber-50/80' : 'text-emerald-800'
                      }`}>
                        {entry.blood_sugar_grbs} mg/dL
                      </td>
                      <td className="py-2.5 px-2 font-mono text-slate-600">{entry.urine_sugar}</td>
                      <td className="py-2.5 px-2 font-mono text-slate-600">{entry.urine_ketone}</td>
                      <td className="py-2.5 px-3 font-semibold text-slate-800">{entry.insulin_medication}</td>
                      <td className="py-2.5 px-2 text-center font-mono font-bold text-blue-700">
                        {entry.dose_units > 0 ? `${entry.dose_units} Units` : 'Nil'}
                      </td>
                      <td className="py-2.5 px-3 text-slate-700 flex items-center space-x-1.5 font-medium">
                        <UserCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span>{entry.nurse_signature}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}