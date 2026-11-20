import math


def parse_vitals_summary(vitals_csv):
    if not isinstance(vitals_csv, str):
        raise ValueError("vitals must be a comma-separated string")

    parts = [part.strip() for part in vitals_csv.split(',')]
    if len(parts) != 3:
        raise ValueError("vitals must contain HR, SpO2, and temperature")

    try:
        hr, spo2, temp = (float(part) for part in parts)
    except ValueError as exc:
        raise ValueError("vitals must contain numeric values") from exc

    if not all(math.isfinite(value) and value > 0 for value in (hr, spo2, temp)):
        raise ValueError("vitals must contain finite positive values")

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        raise ValueError("BMI must be provided as weight/height")

    parts = [part.strip() for part in bmi_string.split('/')]
    if len(parts) != 2:
        raise ValueError("BMI must contain weight and height")

    try:
        weight, height = (float(part) for part in parts)
    except ValueError as exc:
        raise ValueError("BMI weight and height must be numeric") from exc

    if not all(math.isfinite(value) and value > 0 for value in (weight, height)):
        raise ValueError("BMI weight and height must be finite positive values")

    bmi = weight / (height ** 2)
    return round(bmi, 2)


def assign_ward_bed(allocation_code):
    if not isinstance(allocation_code, str):
        raise ValueError("allocation must be a ward-bed string")

    parts = [part.strip() for part in allocation_code.split('-')]
    if len(parts) != 2:
        raise ValueError("allocation must contain one ward and one bed number")

    ward, bed_str = parts
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }
    try:
        ward_name = ward_names[ward.upper()]
        bed_num = int(bed_str)
    except (KeyError, ValueError) as exc:
        raise ValueError("allocation must contain a known ward and numeric bed") from exc

    if bed_num <= 0:
        raise ValueError("bed number must be positive")

    return f"{ward_name} Bed #{bed_num}"

def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))

if __name__ == "__main__":
    main()