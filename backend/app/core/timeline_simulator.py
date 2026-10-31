from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Any, List

class TimelineSimulator:
    """
    Simulates a live chronological hospital flow.
    Enforces that an auditor reviewing at 1:00 PM only sees events that occurred
    up to 1:00 PM, preventing the dumping of afternoon notes or discharge summaries mid-day.
    """
    def __init__(self):
        # Default to today at 13:00 (1:00 PM) for NMC audit safe demo
        today = datetime.now().date()
        self.simulated_time: datetime = datetime(today.year, today.month, today.day, 13, 0)
        self.active_preset: str = "INSPECTION_1PM"
        self.is_paused: bool = False
        self.speed_multiplier: float = 1.0
        self._sync_from_storage()

    def _sync_from_storage(self):
        try:
            if os.path.exists("/tmp/emr_preset.txt"):
                with open("/tmp/emr_preset.txt", "r") as f:
                    saved = f.read().strip()
                    if saved:
                        today = datetime.now().date()
                        presets = {
                            "MORNING_ADMISSION": datetime(today.year, today.month, today.day, 7, 30),
                            "ROUNDS_10AM": datetime(today.year, today.month, today.day, 10, 0),
                            "INSPECTION_1PM": datetime(today.year, today.month, today.day, 13, 0),
                            "AFTERNOON_4PM": datetime(today.year, today.month, today.day, 16, 0),
                            "EVENING_ROUNDS_7PM": datetime(today.year, today.month, today.day, 19, 0),
                            "DAY2_COMORBIDITY": datetime(today.year, today.month, today.day, 11, 0) + timedelta(days=1),
                            "DAY3_LIAISON": datetime(today.year, today.month, today.day, 11, 0) + timedelta(days=2),
                            "DAY4_DISCHARGE": datetime(today.year, today.month, today.day, 18, 0) + timedelta(days=3),
                            "DISCHARGE_READY": datetime(today.year, today.month, today.day, 18, 0) + timedelta(days=3)
                        }
                        if saved in presets:
                            self.simulated_time = presets[saved]
                            self.active_preset = saved
        except Exception:
            pass

    def set_simulated_time(self, new_time: datetime):
        self.simulated_time = new_time
        self.active_preset = "CUSTOM"

    def set_demo_preset(self, preset_name: str) -> datetime:
        """
        Convenience presets for NMC inspector audit demos.
        """
        today = datetime.now().date()
        presets = {
            "MORNING_ADMISSION": datetime(today.year, today.month, today.day, 7, 30),
            "ROUNDS_10AM": datetime(today.year, today.month, today.day, 10, 0),
            "INSPECTION_1PM": datetime(today.year, today.month, today.day, 13, 0),   # 1:00 PM PRD example
            "AFTERNOON_4PM": datetime(today.year, today.month, today.day, 16, 0),
            "EVENING_ROUNDS_7PM": datetime(today.year, today.month, today.day, 19, 0),
            "DAY2_COMORBIDITY": datetime(today.year, today.month, today.day, 11, 0) + timedelta(days=1),
            "DAY3_LIAISON": datetime(today.year, today.month, today.day, 11, 0) + timedelta(days=2),
            "DAY4_DISCHARGE": datetime(today.year, today.month, today.day, 18, 0) + timedelta(days=3),
            "DISCHARGE_READY": datetime(today.year, today.month, today.day, 18, 0) + timedelta(days=3)
        }
        if preset_name in presets:
            self.simulated_time = presets[preset_name]
            self.active_preset = preset_name
            try:
                with open("/tmp/emr_preset.txt", "w") as f:
                    f.write(preset_name)
            except Exception:
                pass
        return self.simulated_time

    def get_active_preset(self) -> str:
        self._sync_from_storage()
        return getattr(self, "active_preset", "INSPECTION_1PM")

    def get_current_time(self) -> datetime:
        self._sync_from_storage()
        return self.simulated_time

    def filter_bundle(self, bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies strict chronological cut-off to a patient clinical bundle.
        Any note, lab report, or discharge recorded AFTER simulated_time is masked.
        """
        curr = self.simulated_time
        patient = bundle["patient"]

        # Check if patient is admitted yet
        if patient.admission_time > curr:
            return {
                "patient": patient,
                "admitted": False,
                "message": f"Patient scheduled for admission at {patient.admission_time.strftime('%H:%M')}, current time is {curr.strftime('%H:%M')}."
            }

        filtered = {
            "patient": patient,
            "admitted": True,
            "opd_slip": bundle.get("opd_slip"),
            "hp_exam": bundle["hp_exam"] if bundle["hp_exam"].admission_timestamp <= curr else None,
            "progress_notes": [n for n in bundle["progress_notes"] if n.timestamp <= curr],
            "lab_reports": [l for l in bundle["lab_reports"] if l.reported_at <= curr],
            "radiology_study": bundle["radiology_study"] if bundle["radiology_study"] and bundle["radiology_study"].study_datetime <= curr else None,
            "medication_sheets": bundle["medication_sheets"],
            "diabetic_entries": [d for d in bundle["diabetic_entries"] if d.timestamp <= curr],
            "tpr_chart": {
                "patient_id": patient.id,
                "readings": [r for r in bundle["tpr_chart"].readings if r.timestamp <= curr]
            },
            # Discharge summary is ONLY visible if discharge_time has already occurred
            "discharge_summary": bundle["discharge_summary"] if (bundle["discharge_summary"] and bundle["discharge_summary"].discharge_timestamp <= curr) else None,
            "status_at_timestamp": "DISCHARGED" if (patient.discharge_time and patient.discharge_time <= curr) else "IPD_ACTIVE"
        }
        return filtered

timeline_manager = TimelineSimulator()
