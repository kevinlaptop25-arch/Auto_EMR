import React from 'react';
import { Clock, ShieldCheck, RefreshCw } from 'lucide-react';

export default function Navbar({ timeline, activePreset, onPresetChange, onRefreshCohort, isGenerating }) {
  const currentHourMinute = timeline?.hour_minute || "13:00";
  const displayDate = timeline?.display_time ? timeline.display_time.split(" ")[0] : "31-Oct-2026";

  // Determine active preset directly from activePreset state or timeline response
  const currentPreset = activePreset || timeline?.active_preset || "INSPECTION_1PM";
  const isInspection1PM = currentPreset === "INSPECTION_1PM";
  const isDay2 = currentPreset === "DAY2_COMORBIDITY";
  const isDay3 = currentPreset === "DAY3_LIAISON";
  const isDay4 = currentPreset === "DISCHARGE_READY" || currentPreset === "DAY4_DISCHARGE";

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white shadow-md shrink-0 z-30">
      <div className="w-full px-4 lg:px-6 h-16 flex items-center justify-between gap-2">
        {/* Left Branding */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-red-700 to-red-500 flex items-center justify-center font-bold text-sm shadow-md shadow-red-900/40 border border-red-400/30 text-white shrink-0">
            EPH
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-bold text-sm sm:text-base tracking-tight text-white whitespace-nowrap">
                EAST POINT HOSPITAL
              </h1>
              <span className="hidden sm:inline-block text-[9px] bg-red-950/80 text-red-400 border border-red-800/80 px-2 py-0.2 rounded-full font-mono font-semibold tracking-wider">
                POC
              </span>
            </div>
            <p className="text-[10px] text-slate-400 truncate hidden sm:block">
              Powered by Node4 Tech
            </p>
          </div>
        </div>

        {/* Center: Live Simulated Audit Clock & Scrubber */}
        <div className="flex items-center bg-slate-950/90 border border-slate-800 rounded-xl px-2.5 py-1 space-x-2.5 shadow-inner">
          <div className="flex items-center space-x-2 text-emerald-400 shrink-0">
            <Clock className="w-3.5 h-3.5 animate-pulse text-emerald-400 shrink-0" />
            <div className="text-xs font-mono leading-none">
              <span className="font-bold text-white text-xs sm:text-sm">
                {currentHourMinute}
              </span>
              <span className="text-slate-400 text-[10px] font-sans ml-1 hidden lg:inline">
                ({displayDate})
              </span>
            </div>
          </div>

          <div className="h-5 w-px bg-slate-800"></div>

          {/* Quick Presets Scrubber */}
          <div className="flex items-center space-x-1.5 bg-slate-900/60 p-0.5 rounded-lg border border-slate-800">
            <button
              type="button"
              onClick={() => onPresetChange("INSPECTION_1PM")}
              className={`text-xs px-2.5 py-1.5 rounded-md font-bold transition-all cursor-pointer whitespace-nowrap active:scale-95 flex items-center space-x-1.5 ${
                isInspection1PM
                  ? 'bg-red-600 text-white shadow-md shadow-red-950 ring-2 ring-red-400'
                  : 'bg-slate-800/90 hover:bg-slate-700/90 text-slate-300 hover:text-white border border-slate-700/60'
              }`}
              title="1:00 PM NMC Mid-Day Inspection (PRD Scenario: Suppress evening notes & premature discharges)"
            >
              {isInspection1PM && <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>}
              <span className="hidden sm:inline">01:00 PM (Audit Safe)</span>
              <span className="sm:hidden">1:00 PM</span>
            </button>

            <button
              type="button"
              onClick={() => onPresetChange("DAY2_COMORBIDITY")}
              className={`text-xs px-2.5 py-1.5 rounded-md font-medium transition-all cursor-pointer whitespace-nowrap active:scale-95 flex items-center space-x-1.5 ${
                isDay2
                  ? 'bg-amber-600 text-white font-bold shadow-md shadow-amber-950 ring-2 ring-amber-400'
                  : 'bg-slate-800/90 hover:bg-slate-700/90 text-slate-300 hover:text-white border border-slate-700/60'
              }`}
              title="Day 2 Morning Rounds: Secondary Comorbidities Identified (Diabetic charts, ABG, Warning signs)"
            >
              {isDay2 && <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>}
              <span className="hidden sm:inline">Day 2 (Comorbidities)</span>
              <span className="sm:hidden">Day 2</span>
            </button>

            <button
              type="button"
              onClick={() => onPresetChange("DAY3_LIAISON")}
              className={`text-xs px-2.5 py-1.5 rounded-md font-medium transition-all cursor-pointer whitespace-nowrap active:scale-95 flex items-center space-x-1.5 ${
                isDay3
                  ? 'bg-purple-600 text-white font-bold shadow-md shadow-purple-950 ring-2 ring-purple-400'
                  : 'bg-slate-800/90 hover:bg-slate-700/90 text-slate-300 hover:text-white border border-slate-700/60'
              }`}
              title="Day 3 Rounds: Specialist Liaisons & Viral Serology"
            >
              {isDay3 && <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>}
              <span className="hidden sm:inline">Day 3 (Liaisons)</span>
              <span className="sm:hidden">Day 3</span>
            </button>

            <button
              type="button"
              onClick={() => onPresetChange("DISCHARGE_READY")}
              className={`text-xs px-2.5 py-1.5 rounded-md font-bold transition-all cursor-pointer whitespace-nowrap active:scale-95 flex items-center space-x-1.5 ${
                isDay4
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950 ring-2 ring-emerald-400'
                  : 'bg-slate-800/90 hover:bg-slate-700/90 text-slate-300 hover:text-white border border-slate-700/60'
              }`}
              title="Day 4: Discharge Summary bound with all ICD codes reconciled"
            >
              {isDay4 && <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>}
              <span className="hidden sm:inline">Day 4 (Discharged)</span>
              <span className="sm:hidden">Day 4</span>
            </button>
          </div>
        </div>

        {/* Right Status */}
        <div className="flex items-center space-x-2 shrink-0">
          <div className="hidden xl:flex items-center space-x-1.5 bg-emerald-950/70 border border-emerald-800/80 text-emerald-300 px-2.5 py-1 rounded-lg text-xs font-medium">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span>2,800+ Encounters: <b>2.6k OPD · 200 IPD</b></span>
          </div>

          <div className="hidden 2xl:flex items-center space-x-1.5 bg-orange-950/70 border border-orange-800/80 text-orange-300 px-2 py-1 rounded-lg text-xs font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"></span>
            <span>ABHA: <b>33% (Target 30-35%)</b></span>
          </div>

          <button
            onClick={onRefreshCohort}
            disabled={isGenerating}
            className="flex items-center space-x-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-2.5 py-1.5 rounded-lg border border-slate-700 transition shadow-2xs font-medium cursor-pointer"
            title="Regenerate 2,800 records cohort (2,600 OPD + 200 IPD, 21 Depts)"
          >
            <RefreshCw className={`w-3 h-3 ${isGenerating ? 'animate-spin text-amber-400' : 'text-slate-400'}`} />
            <span className="hidden sm:inline">{isGenerating ? "Synthesizing 2.8k..." : "Reset 2.8k"}</span>
          </button>
        </div>
      </div>
    </header>
  );
}