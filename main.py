from db import initialize_db
import employee
import attendance
import payroll
import reports
from datetime import datetime

ADMIN_PASSWORD = "admin"   #admin password for HR functions

def input_float(prompt, default=0.0):
    try:
        v = input(prompt).strip()
        return float(v) if v else default
    except:
        return default

def employee_menu():
    while True:
        print("\n--- Employee Management ---")
        print("1. Add employee")
        print("2. List employees")
        print("3. Update employee")
        print("4. Delete employee")
        print("0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            
    #validation - all inputs shouldn't be empty
            while True:
                name = input("Full name: ").strip()
                if name:
                    break
                print("Full name cannot be empty. Please try again.")

            while True:
                role = input("Role: ").strip()
                if role:
                    break
                print("Role cannot be empty. Please try again.")

            while True:
                dept = input("Department: ").strip()
                if dept:
                    break
                print("Department cannot be empty. Please try again.")

            while True:
                rate_input = input("Hourly rate: ").strip()
                if not rate_input:
                    rate = 0.0
                    break
                try:
                    rate = float(rate_input)
                    break
                except ValueError:
                    print("Invalid number. Please enter a numeric hourly rate.")

            contact = input("Contact (optional): ").strip()

            employee.add_employee(name, role, dept, rate, contact)


        elif choice == "2":
            rows = employee.list_employees()
            print("\nEmployees:")
            for r in rows:
                print(f"{r['id']}: {r['full_name']} | {r['role']} | {r['department']} | rate={r['hourly_rate']}")
        elif choice == "3":
            emp_id = int(input("Employee ID to update: "))
            emp = employee.get_employee(emp_id)
            if not emp:
                print("Employee not found.")
                continue
            print("Leave field blank to keep current value.")
            name = input(f"Full name [{emp['full_name']}]: ") or emp['full_name']
            role = input(f"Role [{emp['role']}]: ") or emp['role']
            dept = input(f"Department [{emp['department']}]: ") or emp['department']
            rate_input = input(f"Hourly rate [{emp['hourly_rate']}]: ").strip()
            rate = float(rate_input) if rate_input else emp['hourly_rate']
            contact = input(f"Contact [{emp['contact']}]: ") or emp['contact']
            employee.update_employee(emp_id, name, role, dept, rate, contact)
        elif choice == "4":
            emp_id = int(input("Employee ID to delete: "))
            confirm = input("Are you sure? y/n: ")
            if confirm.lower() == "y":
                employee.delete_employee(emp_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def attendance_menu():
    while True:
        print("\n--- Attendance ---")
        print("1. Employee sign in")
        print("2. Employee sign out")
        print("3. View attendance for employee")
        print("4. HR correct attendance (admin only)")
        print("0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            emp_id = int(input("Employee ID: "))
            attendance.sign_in(emp_id)
        elif choice == "2":
            emp_id = int(input("Employee ID: "))
            attendance.sign_out(emp_id)
        elif choice == "3":
            emp_id = int(input("Employee ID: "))
            rows = attendance.list_attendance_for_employee(emp_id)
            for r in rows:
                print(f"{r['id']} | {r['date']} | in:{r['time_in']} out:{r['time_out']} hours:{r['hours_worked']} corrected:{r['corrected']}")
        elif choice == "4":
            pwd = input("Admin password: ")
            if pwd != ADMIN_PASSWORD:
                print("Wrong password.")
                continue
            att_id = int(input("Attendance ID to correct: "))
            print("Enter new timestamps in ISO format (YYYY-MM-DDTHH:MM:SS) or leave blank")
            new_in = input("New time_in: ").strip() or None
            new_out = input("New time_out: ").strip() or None
            attendance.hr_correct_attendance(att_id, new_in, new_out)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def payroll_menu():
    while True:
        print("\n--- Payroll ---")
        print("1. Generate payroll for one employee")
        print("2. Generate payroll for all employees")
        print("3. View payroll table (recent)")
        print("0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            emp_id = int(input("Employee ID: "))
            month = int(input("Month (1-12): "))
            year = int(input("Year (e.g. 2025): "))
            allow = input("Allowances (optional, default 0): ").strip()
            ded = input("Deductions (optional, default 0): ").strip()
            r = payroll.compute_pay_for_employee(emp_id, month, year, float(allow or 0), float(ded or 0))
            if r:
                print("Payroll generated:", r)
        elif choice == "2":
            month = int(input("Month (1-12): "))
            year = int(input("Year (e.g. 2025): "))
            allow = float(input("Default allowances per employee (0): ") or 0)
            ded = float(input("Default deductions per employee (0): ") or 0)
            results = payroll.generate_payroll_for_all(month, year, allow, ded)
            print("Payroll snapshots saved for employees:", len(results))
        elif choice == "3":
            from db import get_connection
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT p.*, e.full_name FROM payroll p JOIN employees e ON p.employee_id = e.id ORDER BY p.created_at DESC LIMIT 50")
            rows = cur.fetchall()
            conn.close()
            for r in rows:
                print(f"{r['id']} | {r['full_name']} | {r['month']}/{r['year']} | net: {r['net_pay']} | created: {r['created_at']}")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def reports_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Export payroll CSV for month")
        print("2. Export attendance CSV for employee")
        print("0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))
            fname = input("Filename (leave blank for default): ").strip() or None
            reports.export_payroll_csv(month, year, fname)
        elif choice == "2":
            emp_id = int(input("Employee ID: "))
            fname = input("Filename (leave blank for default): ").strip() or None
            reports.export_attendance_csv(emp_id, fname)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def main_menu():
    initialize_db()
    print("QuickHire Attendance & Payroll System (Beginner CLI)")
    while True:
        print("\nMain Menu")
        print("1. Employee Management")
        print("2. Attendance")
        print("3. Payroll")
        print("4. Reports")
        print("0. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            employee_menu()
        elif choice == "2":
            attendance_menu()
        elif choice == "3":
            payroll_menu()
        elif choice == "4":
            reports_menu()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
