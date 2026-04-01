import csv
import sys
import os
 
def load_csv_data():
   """
   Prompts the user for a filename, checks if it exists,
   and extracts all fields into a list of dictionaries.
   """
   filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
 
   if not os.path.exists(filename):
       print(f"Error: The file '{filename}' was not found.")
       sys.exit(1)
 
   assignments = []
 
   try:
       with open(filename, mode='r', encoding='utf-8') as file:
           reader = csv.DictReader(file)
           for row in reader:
               # Convert numeric fields to floats for calculations
               assignments.append({
                   'assignment': row['assignment'],
                   'group': row['group'],
                   'score': float(row['score']),
                   'weight': float(row['weight'])
               })
       if not assignments:
           print("Error: CSV file is empty.")
           sys.exit(1)
       return assignments
   except Exception as e:
       print(f"An error occurred while reading the file: {e}")
       sys.exit(1)
 
def evaluate_grades(data):
   """
   Implement your logic here.
   'data' is a list of dictionaries containing the assignment records.
   """
   print("\n--- Processing Grades ---")
 
   # --- Initialise Accumulators ---
   total_formative = 0.0
   total_summative = 0.0
   formative_weights = 0.0
   summative_weights = 0.0
   failed_formatives = []
 
   # a) Check if all scores are percentage based (0-100)
   for item in data:
       if not (0 <= item['score'] <= 100):
           print(f"Error: Invalid score '{item['score']}' for assignment '{item['assignment']}'. Must be between 0 and 100.")
           sys.exit(1)
 
   # b) Validate total weights (Total=100, Summative=40, Formative=60)
   for item in data:
       if item['group'] == "Formative":
           formative_weights += item['weight']
       elif item['group'] == "Summative":
           summative_weights += item['weight']
       else:
           print(f"Error: Unknown assignment type '{item['group']}' for '{item['assignment']}'.")
           sys.exit(1)
 
   if round(formative_weights) != 60:
       print(f"Error: Formative weights sum to {formative_weights}, expected 60.")
       sys.exit(1)
   if round(summative_weights) != 40:
       print(f"Error: Summative weights sum to {summative_weights}, expected 40.")
       sys.exit(1)
   if round(formative_weights + summative_weights) != 100:
       print(f"Error: Total weights sum to {formative_weights + summative_weights}, expected 100.")
       sys.exit(1)
 
   # c) Calculate the Final Grade and GPA
   for item in data:
       weighted_score = (item['score'] * item['weight']) / 100
       if item['group'] == "Formative":
           total_formative += weighted_score
           # e) Check for failed formative assignments (< 50%)
           if item['score'] < 50:
               failed_formatives.append(item)
       elif item['group'] == "Summative":
           total_summative += weighted_score
 
   final_grade = total_formative + total_summative
   gpa = (final_grade / 100) * 5.0
 
   # d) Determine Pass/Fail status (>= 50% in BOTH categories)
   # 50% of 60 (formative) = 30, 50% of 40 (summative) = 20
   formative_passed = total_formative >= 30
   summative_passed = total_summative >= 20
   status = "PASSED" if (formative_passed and summative_passed) else "FAILED"
 
   # f) Print the final decision and resubmission options
   print("=" * 45)
   print("         GRADE EVALUATION REPORT")
   print("=" * 45)
   print(f"  Formative Score : {total_formative:.2f} / 60.00  {'✓' if formative_passed else '✗'}")
   print(f"  Summative Score : {total_summative:.2f} / 40.00  {'✓' if summative_passed else '✗'}")
   print(f"  Final Grade     : {final_grade:.2f} / 100.00")
   print(f"  GPA             : {gpa:.2f} / 5.00")
   print(f"  Status          : {status}")
   print("=" * 45)
 
   # Resubmission — highest weight failed formative(s), regardless of overall status
   if failed_formatives:
       max_weight = max(f['weight'] for f in failed_formatives)
       to_redo = [f['assignment'] for f in failed_formatives if f['weight'] == max_weight]
       print(f"\n  Eligible for resubmission: {', '.join(to_redo)}")
       print(f"  (Failed formative(s) with highest weight: {max_weight})")
   else:
       print("\n  No formative assignments eligible for resubmission.")
 
   print("=" * 45)
 
if __name__ == "__main__":
   # 1. Load the data
   course_data = load_csv_data()
 
   # 2. Process the features
   evaluate_grades(course_data)
 


