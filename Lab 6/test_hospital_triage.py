import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def test_single_normal_patient():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_invalid_wards_and_score_are_rejected():
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_accepting_ward_covers_urgent_unconscious_and_invalid_patients():
    wards = [
        {"is_accepting": False, "patients": [{"spo2": 1, "hr": 1}]},
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 85, "hr": 130},
                {"unconscious": True},
                {"spo2": 0, "hr": 70},
            ],
            "icu_standby": True,
        },
    ]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 185, "status": "TRIAGE_STABLE"}


def test_outpatient_unconscious_patient_resets_score():
    result = process_triage_wards(
        [
            {
                "is_accepting": True,
                "tier": "outpatient",
                "patients": [{"unconscious": True}],
            }
        ],
        10,
    )
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_many_flagged_entries_raise_ward_alert():
    patients = [{"spo2": 0, "hr": 70} for _ in range(5)]
    result = process_triage_wards(
        [{"is_accepting": True, "patients": patients}], 10
    )
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_empty_or_nonurgent_wards_have_no_urgent_cases():
    assert process_triage_wards([], 10) == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES",
    }


def test_oxygen_monitor_handles_no_data_and_normal_pressure():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"
    assert monitor_oxygen_manifolds([[4.0, 3.9, 4.1], [5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_monitor_detects_two_consecutive_pressure_drops():
    assert monitor_oxygen_manifolds([[4.0, 3.9, 3.8]]) == "PRESSURE_FAILURE"


def test_patient_defaults_and_exact_urgent_boundaries():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{}, {"spo2": 90, "hr": 120}]}],
        7,
    )
    assert result == {"acuity_score": 14, "status": "TRIAGE_STABLE"}


def test_nonpositive_heart_rate_is_flagged():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{"spo2": 95, "hr": 0}]}], 7
    )
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_icu_standby_adds_acuity_to_empty_ward():
    result = process_triage_wards(
        [{"is_accepting": True, "icu_standby": True, "patients": []}], 7
    )
    assert result == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


def test_oxygen_pressure_recovers_after_a_single_drop():
    assert monitor_oxygen_manifolds([[3.9, 4.0, 3.9]]) == "PRESSURE_NORMAL"