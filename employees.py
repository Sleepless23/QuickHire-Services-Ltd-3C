from utils import load_json, save_json, input_str, input_float, input_pos_int

EMP_FILE = 'db/employees.json'  

#add new employee 
def add_employee():
    employees = load_json(EMP_FILE)
    print("\n--- Add New Employee --- (enter 0 at any prompt to go back)")
    name = input_str("Full Name: ")
    if name == "0": return
    role = input_str("Role: ")
    if role == "0": return
    department = input_str("Department: ")
    if department == "0": return
    rate = input_float("Hourly Rate: ")
    allowance = input_float("Allowance amount (0 if none): ")
    deduction = input_float("Deduction amount (0 if none): ")
    contact = input_str("Contact Details: ")
    if contact == "0": return

    emp_id = 1 if not employees else max(e['id'] for e in employees) + 1
    employee = {
        "id": emp_id,
        "name": name,
        "role": role,
        "department": department,
        "hourly_rate": rate,
        "allowance": allowance,
        "deduction": deduction,
        "contact": contact
    }
    employees.append(employee)
    save_json(EMP_FILE, employees)
    print("Employee added successfully!")

#view all employees
def view_employees(wait=True):
    employees = load_json(EMP_FILE)
    if not employees:
        print("No employees found.")
    else:
        print("\n--- Employees ---")
        for emp in employees:
            print(f"ID:{emp['id']} | {emp['name']} | {emp['role']} | {emp['department']} | Rate:{emp['hourly_rate']} | Allow:{emp.get('allowance',0)} | Deduct:{emp.get('deduction',0)}")
    if wait:
        input("Press Enter to go back...")

#edit employee
def edit_employee():
    employees = load_json(EMP_FILE)
    print("\n--- Edit Employee --- (0 to go back)")
    emp_id = input_pos_int("Enter Employee ID: ")
    if emp_id == 0: return
    emp = next((e for e in employees if e['id'] == emp_id), None)
    if not emp:
        print("Employee not found!")
        return
    print("Leave blank to keep current value (enter 0 to cancel).")
    name = input(f"Name ({emp['name']}): ").strip()
    if name == "0": return
    if name != "": emp['name'] = name
    role = input(f"Role ({emp['role']}): ").strip()
    if role == "0": return
    if role != "": emp['role'] = role
    dept = input(f"Department ({emp['department']}): ").strip()
    if dept == "0": return
    if dept != "": emp['department'] = dept
    rate_in = input(f"Hourly Rate ({emp['hourly_rate']}): ").strip()
    if rate_in == "0": return
    if rate_in != "":
        try: emp['hourly_rate'] = float(rate_in)
        except ValueError: print("Invalid rate input. Keeping old rate.")
    allow_in = input(f"Allowance ({emp.get('allowance',0)}): ").strip()
    if allow_in == "0": return
    if allow_in != "":
        try: emp['allowance'] = float(allow_in)
        except ValueError: print("Invalid allowance. Keeping old.")
    ded_in = input(f"Deduction ({emp.get('deduction',0)}): ").strip()
    if ded_in == "0": return
    if ded_in != "":
        try: emp['deduction'] = float(ded_in)
        except ValueError: print("Invalid deduction. Keeping old.")
    contact = input(f"Contact ({emp['contact']}): ").strip()
    if contact == "0": return
    if contact != "": emp['contact'] = contact
    save_json(EMP_FILE, employees)
    print("Employee updated!")

#remove employee
def remove_employee():
    employees = load_json(EMP_FILE)
    print("\n--- Remove Employee --- (0 to go back)")
    emp_id = input_pos_int("Enter Employee ID to remove: ")
    if emp_id == 0: return
    new_list = [e for e in employees if e['id'] != emp_id]
    if len(new_list) == len(employees):
        print("Employee not found.")
    else:
        save_json(EMP_FILE, new_list)
        print("Employee removed.")