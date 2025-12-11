from employees import add_employee, view_employees, edit_employee, remove_employee
from attendance import sign_in, sign_out, view_attendance, hr_add_record, hr_edit_record, hr_delete_record, export_attendance_history, export_overtime_report, export_daily_summary
from payroll import generate_payroll_for_month, export_payroll_csv_cli
from utils import input_pos_int, input_str
import os

#ensure db folder exists
if not os.path.isdir('db'):
    os.makedirs('db')

def main_menu():
    while True:
        print("\n--- QuickHire Attendance & Payroll ---")
        print("1. Manage Employees")
        print("2. Attendance")
        print("3. HR Attendance Corrections")
        print("4. Payroll")
        print("5. Reports / Exports")
        print("0. Exit")
        choice = input_pos_int("Select option: ")

        if choice == 1:
            while True:
                print("\n--- Employee Menu ---")
                print("1. Add Employee\n2. View Employees\n3. Edit Employee\n4. Remove Employee\n0. Back")
                c = input_pos_int("Choose option: ")
                if c == 1: add_employee()
                elif c == 2: view_employees()
                elif c == 3: edit_employee()
                elif c == 4: remove_employee()
                elif c == 0: break
                else: print("Invalid choice!")

        elif choice == 2:
            while True:
                print("\n--- Attendance Menu ---")
                print("1. Sign In\n2. Sign Out\n3. View Attendance\n0. Back")
                c = input_pos_int("Choose option: ")
                if c == 1: sign_in()
                elif c == 2: sign_out()
                elif c == 3: view_attendance()
                elif c == 0: break
                else: print("Invalid choice!")

        elif choice == 3:
            while True:
                print("\n--- HR Attendance Corrections ---")
                print("1. Add Record\n2. Edit Record\n3. Delete Record\n0. Back")
                c = input_pos_int("Choose option: ")
                if c == 1: hr_add_record()
                elif c == 2: hr_edit_record()
                elif c == 3: hr_delete_record()
                elif c == 0: break
                else: print("Invalid choice!")

        elif choice == 4:
            while True:
                print("\n--- Payroll Menu ---")
                print("1. Generate Payroll for Month\n2. Export payroll (if previously generated)\n0. Back")
                c = input_pos_int("Choose option: ")
                if c == 1: generate_payroll_for_month()
                elif c == 2: export_payroll_csv_cli()
                elif c == 0: break
                else: print("Invalid choice!")

        elif choice == 5:
            while True:
                print("\n--- Reports / Exports ---")
                print("1. Export attendance history (per employee)")
                print("2. Export overtime report (month)")
                print("3. Export daily attendance summary (day)")
                print("0. Back")
                c = input_pos_int("Choose option: ")
                if c == 1:
                    emp_id = input_pos_int("Employee ID (0 to go back): ")
                    if emp_id == 0: continue
                    export_attendance_history(emp_id)
                elif c == 2:
                    month = input_pos_int("Month (1-12, 0 to go back): ")
                    if month == 0: continue
                    year = input_pos_int("Year (0 to go back): ")
                    if year == 0: continue
                    export_overtime_report(month, year)
                elif c == 3:
                    date = input_str("Date (YYYY-MM-DD) (0 to go back): ")
                    if date == "0": continue
                    export_daily_summary(date)
                elif c == 0:
                    break
                else:
                    print("Invalid choice!")

        elif choice == 0:
            print("Exiting program...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()