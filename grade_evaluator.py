import csv
import os

# check if file exists
if not os.path.exists("grades.csv"):
    print("Error: grades.csv file not found.")
    exit()

def evaluate_grades(grades.csv):
    # --- File Reading ---
    try:
        with open(grades.csv, mode='r') as file:
            reader = csv.DictReader(file)
            grades = list(reader)
    except FileNotFoundError:
        print("Error: grades.csv not found.")
        return

    # --- Empty File Check ---
    if not grades:
        print("Error: CSV file is empty.")
        return

    # --- Initialise Accumulators ---
    total_formative = 0.0
    total_summative = 0.0
    formative_weights = 0.0
    summative_weights = 0.0
    failed_formatives = []

    # --- Process Each Row ---
    for row in grades:
        try:
            assignment = row['assignment']
            score = float(row['score'])
            weight = float(row['weight'])
            assignment_type = row['group']
        except (KeyError, ValueError) as e:
            print(f"Error: Malformed row in CSV — {e}")
            return

        # Grade Validation (0–100)
        if not (0 <= score <= 100):
            print(f"Error: Invalid score '{score}' for assignment '{assignment}'. Must be between 0 and 100.")
            return

        weighted_score = (score * weight) / 100

        if assignment_type == "Formative":
            total_formative += weighted_score
            formative_weights += weight
            if score < 50:
                failed_formatives.append(row)
        elif assignment_type == "Summative":
            total_summative += weighted_score
            summative_weights += weight
        else:
            print(f"Error: Unknown assignment type '{assignment_type}' for '{assignment}'.")
            return

    # --- Weight Validation ---
    if round(formative_weights) != 60:
        print(f"Error: Formative weights sum to {formative_weights}, expected 60.")
        return
    if round(summative_weights) != 40:
        print(f"Error: Summative weights sum to {summative_weights}, expected 40.")
        return
    if round(formative_weights + summative_weights) != 100:
        print(f"Error: Total weights sum to {formative_weights + summative_weights}, expected 100.")
        return

    # --- GPA Calculation ---
    final_grade = total_formative + total_summative
    gpa = (final_grade / 100) * 5.0

    # --- Pass/Fail Decision ---
    # Student must score >= 50% in BOTH categories independently
    # 50% of 60 (formative) = 30, 50% of 40 (summative) = 20
    formative_passed = total_formative >= 30
    summative_passed = total_summative >= 20
    status = "PASSED" if (formative_passed and summative_passed) else "FAILED"

    # --- Output ---
    print("=" * 45)
    print("         GRADE EVALUATION REPORT")
    print("=" * 45)
    print(f"  Formative Score : {total_formative:.2f} / 60.00  {'✓' if formative_passed else '✗'}")
    print(f"  Summative Score : {total_summative:.2f} / 40.00  {'✓' if summative_passed else '✗'}")
    print(f"  Final Grade     : {final_grade:.2f} / 100.00")
    print(f"  GPA             : {gpa:.2f} / 5.00")
    print(f"  Status          : {status}")
    print("=" * 45)

    # --- Resubmission Logic ---
    # Always check — a student can pass overall but still have failed formatives
    if failed_formatives:
        max_weight = max(float(f['weight']) for f in failed_formatives)
        to_redo = [f['assignment'] for f in failed_formatives if float(f['weight']) == max_weight]
        print(f"\n  Eligible for resubmission: {', '.join(to_redo)}")
        print(f"  (Failed formative(s) with highest weight: {max_weight})")
    else:
        print("\n  No formative assignments eligible for resubmission.")

    print("=" * 45)


if __name__ == "__main__":
    evaluate_grades("grades.csv")
