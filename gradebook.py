"""
Gradebook Analyzer (simple)
Author: NavraJ Amgai
Date: 2025-11-20
Course: ETCCPP102 - Programming for Problem Solving Using Python
Signature: By NavraJ Amgai
Description:
Simple CLI tool to enter student marks manually or load from CSV,
compute mean/median/min/max, assign letter grades, list pass/fail,
and print a results table. Easy to explain in class.
"""

import csv
from statistics import mean, median

# ---------- Helper functions ----------
def read_csv(filename):
    """Read CSV with two columns: name,mark  (no header expected or optional)"""
    students = {}
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:  # skip empty lines
                    continue
                name = row[0].strip()
                try:
                    mark = float(row[1])
                except (IndexError, ValueError):
                    # skip invalid rows
                    continue
                students[name] = mark
    except FileNotFoundError:
        print("CSV file not found:", filename)
    return students

def manual_input():
    """Get student names and marks from user manually."""
    students = {}
    while True:
        try:
            n = int(input("How many students will you enter? "))
            if n <= 0:
                print("Enter a positive integer.")
            else:
                break
        except ValueError:
            print("Please enter a whole number.")
    for i in range(1, n+1):
        name = input(f"Name of student {i}: ").strip()
        while True:
            try:
                mark = float(input(f"Mark for {name}: "))
                if mark < 0:
                    print("Enter 0 or positive marks.")
                else:
                    break
            except ValueError:
                print("Please enter a number for the mark.")
        students[name] = mark
    return students

def assign_grade(mark):
    """Return letter grade for a numeric mark."""
    if mark >= 90:
        return 'A'
    if mark >= 80:
        return 'B'
    if mark >= 70:
        return 'C'
    if mark >= 60:
        return 'D'
    return 'F'  # below 60

def stats_from_marks(marks):
    """Return average, median, min, max"""
    avg = mean(marks) if marks else 0
    med = median(marks) if marks else 0
    mn = min(marks) if marks else 0
    mx = max(marks) if marks else 0
    return avg, med, mn, mx

def print_table(students, grades):
    """Print formatted table: Name | Mark | Grade"""
    print("\nName".ljust(20) + "Marks".ljust(10) + "Grade")
    print("-"*40)
    for name, mark in students.items():
        print(f"{name.ljust(20)}{str(round(mark,1)).ljust(10)}{grades[name]}")
    print("-"*40)

# ---------- Main CLI loop ----------
def main():
    print("=== Gradebook Analyzer ===")
    while True:
        print("\nMenu:")
        print("1. Manual entry")
        print("2. Load from CSV file (name,mark)")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == '1':
            students = manual_input()
        elif choice == '2':
            fname = input("Enter CSV filename (e.g., students.csv): ").strip()
            students = read_csv(fname)
            if not students:
                print("No valid data loaded from CSV.")
                continue
        elif choice == '3':
            print("Exiting Gradebook Analyzer. By NavraJ Amgai")
            break
        else:
            print("Please choose 1, 2 or 3.")
            continue

        # compute statistics and grades
        marks = list(students.values())
        avg, med, mn, mx = stats_from_marks(marks)
        grades = {name: assign_grade(mark) for name, mark in students.items()}

        # pass / fail lists (pass >= 40)
        passed = [name for name, mark in students.items() if mark >= 40]
        failed = [name for name, mark in students.items() if mark < 40]

        # grade distribution count
        distribution = {}
        for g in grades.values():
            distribution[g] = distribution.get(g, 0) + 1

        # print summary
        print("\n=== Analysis Summary ===")
        print(f"Students analysed: {len(students)}")
        print(f"Average: {avg:.2f} | Median: {med:.2f} | Min: {mn:.1f} | Max: {mx:.1f}")
        print("\nGrade distribution:")
        for g in ['A','B','C','D','F']:
            print(f"{g}: {distribution.get(g,0)}")
        print(f"\nPassed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
        print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")

        # results table
        print_table(students, grades)

        # optional: save result table to CSV (bonus)
        save = input("\nSave results table to CSV? (y/n): ").lower()
        if save == 'y':
            outname = input("Output filename (e.g., results.csv): ").strip()
            try:
                with open(outname, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Name','Mark','Grade'])
                    for name, mark in students.items():
                        writer.writerow([name, mark, grades[name]])
                print("Saved to", outname)
            except Exception as e:
                print("Failed to save:", e)

        cont = input("\nRun again? (y/n): ").lower()
        if cont != 'y':
            print("Done. By NavraJ Amgai")
            break

if __name__ == "__main__":
    main()
