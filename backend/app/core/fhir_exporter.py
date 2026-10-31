import uuid
from datetime import datetime
from typing import Dict, Any, List

from app.models.patient import Patient
from app.models.lab import LabReport

class FhirExporter:
    """
    ABDM Milestone 2 (M2) FHIR R4 Document Generator.
    Produces valid HL7 FHIR R4 bundles compliant with ABDM standards
    (National Health Authority of India).
    """

    @staticmethod
    def generate_diagnostic_report_bundle(patient: Patient, lab: LabReport) -> Dict[str, Any]:
        bundle_id = str(uuid.uuid4())
        composition_id = str(uuid.uuid4())
        patient_ref_id = patient.id
        practitioner_id = str(uuid.uuid4())
        org_id = "org-eph-01"

        entries = []

        # 1. Composition Resource
        composition = {
            "fullUrl": f"urn:uuid:{composition_id}",
            "resource": {
                "resourceType": "Composition",
                "id": composition_id,
                "status": "final",
                "type": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "721981007",
                            "display": "Diagnostic studies report"
                        }
                    ],
                    "text": f"Diagnostic Report - {lab.test_category}"
                },
                "subject": {
                    "reference": f"urn:uuid:{patient_ref_id}",
                    "display": patient.name
                },
                "date": lab.reported_at.isoformat(),
                "author": [
                    {
                        "reference": f"urn:uuid:{practitioner_id}",
                        "display": lab.pathologist_name
                    }
                ],
                "title": f"Laboratory Report: {lab.test_category}",
                "custodian": {
                    "reference": f"urn:uuid:{org_id}",
                    "display": "East Point Hospital & Research Centre"
                },
                "section": [
                    {
                        "title": lab.test_category,
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "11502-2",
                                    "display": "Laboratory report"
                                }
                            ]
                        },
                        "entry": []
                    }
                ]
            }
        }
        entries.append(composition)

        # 2. Patient Resource (with ABHA ID)
        patient_resource = {
            "fullUrl": f"urn:uuid:{patient_ref_id}",
            "resource": {
                "resourceType": "Patient",
                "id": patient_ref_id,
                "identifier": [
                    {
                        "type": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                    "code": "MR",
                                    "display": "Medical Record Number"
                                }
                            ]
                        },
                        "system": "https://eastpointhospital.org/mrn",
                        "value": patient.mr_no
                    },
                    {
                        "type": {
                            "coding": [
                                {
                                    "system": "https://healthid.ndhm.gov.in",
                                    "code": "ABHA",
                                    "display": "Ayushman Bharat Health Account Number"
                                }
                            ]
                        },
                        "system": "https://healthid.ndhm.gov.in",
                        "value": patient.abha_id or "91-0000-0000-0000"
                    }
                ],
                "name": [
                    {
                        "use": "official",
                        "text": patient.name
                    }
                ],
                "gender": patient.gender.lower(),
                "telecom": [
                    {
                        "system": "phone",
                        "value": patient.phone,
                        "use": "mobile"
                    }
                ],
                "address": [
                    {
                        "line": [patient.address],
                        "city": patient.city,
                        "country": "IND"
                    }
                ]
            }
        }
        entries.append(patient_resource)

        # 3. Practitioner Resource
        practitioner_resource = {
            "fullUrl": f"urn:uuid:{practitioner_id}",
            "resource": {
                "resourceType": "Practitioner",
                "id": practitioner_id,
                "identifier": [
                    {
                        "system": "https://doctor.ndhm.gov.in",
                        "value": lab.pathologist_reg
                    }
                ],
                "name": [
                    {
                        "text": lab.pathologist_name
                    }
                ]
            }
        }
        entries.append(practitioner_resource)

        # 4. Organization Resource
        org_resource = {
            "fullUrl": f"urn:uuid:{org_id}",
            "resource": {
                "resourceType": "Organization",
                "id": org_id,
                "identifier": [
                    {
                        "system": "https://facility.ndhm.gov.in",
                        "value": "IN2910000123"  # ABDM Facility ID
                    }
                ],
                "name": "East Point Hospital and Research Centre",
                "telecom": [
                    {"system": "phone", "value": "+91-7866911911"},
                    {"system": "email", "value": "reception.eph@eastpoint.ac.in"}
                ]
            }
        }
        entries.append(org_resource)

        # 5. Observation Resources (for each lab item)
        observation_refs = []
        for item in lab.items:
            obs_id = str(uuid.uuid4())
            obs_resource = {
                "fullUrl": f"urn:uuid:{obs_id}",
                "resource": {
                    "resourceType": "Observation",
                    "id": obs_id,
                    "status": "final",
                    "category": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                    "code": "laboratory",
                                    "display": "Laboratory"
                                }
                            ]
                        }
                    ],
                    "code": {
                        "text": item.name
                    },
                    "subject": {
                        "reference": f"urn:uuid:{patient_ref_id}"
                    },
                    "effectiveDateTime": lab.reported_at.isoformat(),
                    "valueString": f"{item.result_value} {item.unit}".strip(),
                    "interpretation": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                                    "code": item.flag,
                                    "display": item.flag
                                }
                            ]
                        }
                    ],
                    "referenceRange": [
                        {
                            "text": item.reference_range
                        }
                    ]
                }
            }
            entries.append(obs_resource)
            observation_refs.append({"reference": f"urn:uuid:{obs_id}"})

        # 6. DiagnosticReport Resource
        diag_id = str(uuid.uuid4())
        diagnostic_report = {
            "fullUrl": f"urn:uuid:{diag_id}",
            "resource": {
                "resourceType": "DiagnosticReport",
                "id": diag_id,
                "status": "final",
                "code": {
                    "text": lab.test_category
                },
                "subject": {
                    "reference": f"urn:uuid:{patient_ref_id}"
                },
                "effectiveDateTime": lab.reported_at.isoformat(),
                "issued": lab.reported_at.isoformat(),
                "performer": [
                    {
                        "reference": f"urn:uuid:{practitioner_id}"
                    }
                ],
                "result": observation_refs,
                "conclusion": lab.clinical_impression or "Completed without anomaly."
            }
        }
        entries.append(diagnostic_report)

        # Attach to composition
        composition["resource"]["section"][0]["entry"] = observation_refs

        return {
            "resourceType": "Bundle",
            "id": bundle_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": datetime.now().isoformat(),
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReportRecord"]
            },
            "type": "document",
            "timestamp": datetime.now().isoformat(),
            "entry": entries
        }
