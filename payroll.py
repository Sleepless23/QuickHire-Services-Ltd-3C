from utils import load_json, save_json, input_pos_int
from attendance import get_month_hours
import csv
import os

EMP_FILE = 'db/employees.json'    
PAY_FILE = 'db/payroll.json'      

OT_MULTIPLIER = 1.3  #overtime multiplier

#generate payroll for a specific month & year
def generate_payroll_for_month():
    print("\n--- Generate Payroll for Month --- (0 to go back)")
    month = input_pos_int("Enter month (1-12): ")
    if month == 0: return
    if month < 1 or month > 12:
        print("Invalid month.")
        return
    year = input_pos_int("Enter year (e.g., 2025): ")
    if year == 0: return

    employees = load_json(EMP_FILE)
    if not employees:
        print("No employees to process.")
        return

    payroll_data = []
    for emp in employees:
        reg_hours, ot_hours = get_month_hours(emp['id'], month, year)
        reg_pay = round(reg_hours * emp['hourly_rate'], 2)
        ot_pay = round(ot_hours * emp['hourly_rate'] * OT_MULTIPLIER, 2)
        allowance = float(emp.get('allowance', 0))
        deduction = float(emp.get('deduction', 0))
        gross = round(reg_pay + ot_pay + allowance, 2)
        net = round(gross - deduction, 2)
        payroll_data.append({
            "employee_id": emp['id'],
            "name": emp['name'],
            "month": month,
            "year": year,
            "regular_hours": reg_hours,
            "overtime_hours": ot_hours,
            "regular_pay": reg_pay,
            "overtime_pay": ot_pay,
            "allowance": allowance,
            "deduction": deduction,
            "gross_pay": gross,
            "net_pay": net
        })

    #save payroll data
    save_json(PAY_FILE, payroll_data)
    print(f"Payroll generated for {month}/{year}.")
    #create csv summary and payslips
    export_payroll_summary_csv(month, year, payroll_data)
    export_payslips(month, year, payroll_data)
    input("Press Enter to go back...")
    return payroll_data

#export payroll summary 
def export_payroll_summary_csv(month, year, payroll_data=None):
    if payroll_data is None:
        payroll_data = load_json(PAY_FILE)
    if not payroll_data:
        print("No payroll data found. Generate payroll first.")
        return
    if not os.path.isdir('exports'):
        os.makedirs('exports')
    path = os.path.join('exports', f"payroll_{month}_{year}.csv")
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ["employee_id","name","month","year","regular_hours","overtime_hours","regular_pay",
                      "overtime_pay","allowance","deduction","gross_pay","net_pay"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in payroll_data:
            writer.writerow(p)
    print(f"Payroll summary exported to {path}")

#export payslip per employee
def export_payslips(month, year, payroll_data=None):
    if payroll_data is None:
        payroll_data = load_json(PAY_FILE)
    if not payroll_data:
        print("No payroll data to export.")
        return
    if not os.path.isdir('exports'):
        os.makedirs('exports')
    for p in payroll_data:
        path = os.path.join('exports', f"payslip_emp{p['employee_id']}_{p['month']}_{p['year']}.csv")
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Payslip for", p['name']])
            writer.writerow(["Employee ID", p['employee_id']])
            writer.writerow(["Month", p['month']])
            writer.writerow(["Year", p['year']])
            writer.writerow([])
            writer.writerow(["Regular Hours", p['regular_hours']])
            writer.writerow(["Overtime Hours", p['overtime_hours']])
            writer.writerow(["Regular Pay", p['regular_pay']])
            writer.writerow(["Overtime Pay", p['overtime_pay']])
            writer.writerow(["Allowance", p['allowance']])
            writer.writerow(["Deduction", p['deduction']])
            writer.writerow(["Gross Pay", p['gross_pay']])
            writer.writerow(["Net Pay", p['net_pay']])
    print("Payslips exported (one CSV per employee) to exports/")

#cli helper to export csv if needed
def export_payroll_csv_cli():
    payroll_data = load_json(PAY_FILE)
    if not payroll_data:
        print("No payroll data found. Generate payroll first.")
        return
    month = payroll_data[0]['month']
    year = payroll_data[0]['year']
    export_payroll_summary_csv(month, year, payroll_data)
    export_payslips(month, year, payroll_data)