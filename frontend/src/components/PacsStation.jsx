import React, { useState, useEffect } from 'react';
import { ZoomIn, ZoomOut, RotateCcw, Contrast, SunMedium, Eye, Film, FileCheck } from 'lucide-react';

export default function PacsStation({ bundle }) {
  const [zoom, setZoom] = useState(1);
  const [invert, setInvert] = useState(false);
  const [brightness, setBrightness] = useState(100);
  const [contrast, setContrast] = useState(100);

  if (!bundle || !bundle.patient) {
    return <div className="p-8 text-center text-slate-400">Select a patient to inspect PACS studies.</div>;
  }

  const study = bundle.radiology_study;
  const patient = bundle.patient;

  const handleReset = () => {
    setZoom(1);
    setInvert(false);
    setBrightness(100);
    setContrast(100);
  };

  return (
    <div className="space-y-6">
      {/* Station Header */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-4 flex justify-between items-center">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-violet-800 bg-violet-50 border border-violet-200 px-2 py-0.5 rounded">
              DIGITAL RADIOLOGY
            </span>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <Film className="w-5 h-5 text-violet-600" />
              <span>EAST POINT PACS & DICOM VIEWER</span>
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Zero-film digital radiology integration for {patient.name} (MRN: {patient.mr_no})
          </p>
        </div>

        {study && (
          <span className="font-mono text-xs bg-slate-100 text-slate-700 px-2.5 py-1 rounded border border-slate-200 font-semibold">
            Accession: {study.accession_no}
          </span>
        )}
      </div>

      {study ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* DICOM Viewer Canvas (2 Cols) */}
          <div className="lg:col-span-2 bg-slate-950 rounded-lg border border-slate-800 shadow-2xl flex flex-col overflow-hidden">
            {/* Viewer Toolbar */}
            <div className="bg-slate-900 border-b border-slate-800 px-4 py-2.5 flex items-center justify-between text-xs text-slate-300">
              <div className="flex items-center space-x-4">
                <span className="font-bold text-white tracking-wider flex items-center space-x-1">
                  <Film className="w-3.5 h-3.5 text-violet-400" />
                  <span>{study.modality} · {study.body_part}</span>
                </span>
                <span className="text-slate-500">|</span>
                <div className="flex items-center space-x-2">
                  <SunMedium className="w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="range"
                    min="50"
                    max="180"
                    value={brightness}
                    onChange={(e) => setBrightness(Number(e.target.value))}
                    className="w-16 h-1 bg-slate-700 rounded appearance-none cursor-pointer"
                    title="Brightness / Window Level"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <Contrast className="w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="range"
                    min="50"
                    max="200"
                    value={contrast}
                    onChange={(e) => setContrast(Number(e.target.value))}
                    className="w-16 h-1 bg-slate-700 rounded appearance-none cursor-pointer"
                    title="Contrast / Window Width"
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setZoom((z) => Math.min(z + 0.2, 2.5))}
                  className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                  title="Zoom In"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setZoom((z) => Math.max(z - 0.2, 0.6))}
                  className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                  title="Zoom Out"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setInvert((inv) => !inv)}
                  className={`px-2 py-1 rounded text-[11px] font-semibold transition ${
                    invert ? 'bg-violet-600 text-white' : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
                  }`}
                  title="Invert Grayscale LUT"
                >
                  Invert
                </button>
                <button
                  onClick={handleReset}
                  className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                  title="Reset View"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Viewport Screen */}
            <div className="relative flex-1 min-h-[460px] flex items-center justify-center p-4 overflow-hidden select-none bg-black">
              {/* Top-Left DICOM Patient Overlay */}
              <div className="absolute top-3 left-3 text-[11px] font-mono text-emerald-400/90 leading-tight pointer-events-none drop-shadow">
                <p className="font-bold">{patient.name.toUpperCase()}</p>
                <p>MRN: {patient.mr_no}</p>
                <p>AGE/SEX: {patient.age}Y / {patient.gender[0]}</p>
                <p className="text-slate-400 text-[10px] mt-1">EAST POINT HOSPITAL</p>
              </div>

              {/* Top-Right DICOM Study Overlay */}
              <div className="absolute top-3 right-3 text-right text-[11px] font-mono text-emerald-400/90 leading-tight pointer-events-none drop-shadow">
                <p className="font-bold">{study.study_description}</p>
                <p>MOD: {study.modality} · KV: 120</p>
                <p>{new Date(study.study_datetime).toLocaleDateString()}</p>
                <p className="text-slate-400 text-[10px] mt-1">ACC: {study.accession_no}</p>
              </div>

              {/* Bottom-Left DICOM LUT Overlay */}
              <div className="absolute bottom-3 left-3 text-[10px] font-mono text-emerald-400/80 pointer-events-none drop-shadow">
                <p>WL: {Math.round(brightness * 0.4)} / WW: {Math.round(contrast * 4)}</p>
                <p>ZOOM: {Math.round(zoom * 100)}% · 512x512 16-BIT</p>
              </div>

              {/* Bottom-Right Orientation Marker */}
              <div className="absolute bottom-3 right-3 text-lg font-bold font-mono text-emerald-400/90 pointer-events-none drop-shadow">
                R
              </div>

              {/* Rendered Radiological Image */}
              <div
                style={{
                  transform: `scale(${zoom})`,
                  filter: `brightness(${brightness}%) contrast(${contrast}%) ${invert ? 'invert(1)' : ''}`,
                  transition: 'transform 0.1s ease-out'
                }}
              >
                <img
                  src={study.instances[0]?.image_url || "/api/pacs/images/sample.png"}
                  alt="DICOM Radiological Instance"
                  className="max-h-[420px] object-contain border border-slate-900 rounded shadow-2xl"
                />
              </div>
            </div>
          </div>

          {/* Radiology Interpretation Report (1 Col) */}
          <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 space-y-4 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="pb-3 border-b border-slate-200">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wide">
                  Official Radiology Report
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-0.5">
                  {study.study_description}
                </h3>
                <p className="text-xs text-slate-500 font-mono mt-0.5">
                  Ordering: {study.ordering_doctor}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wide mb-1">
                  Radiological Findings:
                </h4>
                <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded border border-slate-200 leading-relaxed font-sans">
                  {study.findings}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wide mb-1">
                  Impression:
                </h4>
                <div className="p-3 bg-violet-50 border border-violet-200 rounded text-xs text-violet-950 font-semibold leading-relaxed">
                  {study.impression}
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
              <div>
                <span className="font-bold text-slate-900 block">{study.radiologist_name}</span>
                <span className="font-mono text-slate-500 text-[11px]">{study.radiologist_reg}</span>
              </div>
              <div className="flex items-center space-x-1 text-emerald-700 font-medium">
                <FileCheck className="w-4 h-4 text-emerald-600" />
                <span>PACS Signed</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center text-xs text-slate-400 bg-white rounded-lg border border-slate-200">
          No radiological imaging study ordered for this patient encounter.
        </div>
      )}
    </div>
  );
}
