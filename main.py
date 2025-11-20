
from datetime import datetime

def load_data(filename):
    try:
        with open(filename, "r") as file:
            return eval(file.read())
    except:
        return{}
    
def save_data(filename,data):
    with open(filename, "w") as file:
        file.write(str(data))

employees_file = "employee.txt"
attendance_file = "attendance.txt"
payroll_file = "payroll.txt"

employees = load_data(employees_file)
attendance = load_data(attendance_file)
payroll = load_data(payroll_file)

def add_employee(emp_id, name, role, dept, rate, contact):
    employees(emp_id) = {
        "name": name,
        "role": role,
        "dept": dept,
        "role": role,
        "rate": float(rate),
        "contact": contact
    }
    save_data(employees_file, employees)
    print("✅Employees Successfully Added")


load_data()
save_data()
add_employee()