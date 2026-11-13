def parse_vitals_summary(vitals_csv):
    parts = vitals_csv.split(',')
    hr = float(parts[0])
    spo2 = float(parts[1])
    temp = float(parts[2])
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"

def compute_patient_bmi(bmi_string):
    w_str, h_str = bmi_string.split('/')
    weight = float(w_str)
    height = float(h_str)
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def assign_ward_bed(allocation_code):
    ward, bed_str = allocation_code.strip().split('-')
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }
    bed_num = int(bed_str)
    return f"{ward_names[ward.upper()]} Bed #{bed_num}"

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