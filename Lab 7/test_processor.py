from hypothesis import given, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed

@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    # To-Do:Using try and except complete this function.
    pass