from hypothesis import given, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed

@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    try:
        result = parse_vitals_summary(s)
        assert isinstance(result, str)
    except ValueError:
        pass

@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    try:
        result = compute_patient_bmi(s)
        assert isinstance(result, float)
    except ValueError:
        pass

@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    try:
        result = assign_ward_bed(s)
        assert isinstance(result, str)
    except ValueError:
        pass