from db import get_connection
from datetime import datetime

STANDARD_MONTH_HOURS = 160  #40 hours/week * 4 weeks

def compute_pay_for_employee(employee_id, month, year, allowances=0.0, deductions=0.0):
    conn = get_connection()
    cur = conn.cursor()

    #get hourly rate
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    emp = cur.fetchone()
    if not emp:
        conn.close()
        return None

    hourly_rate = emp["hourly_rate"] or 0.0

    #sum hours_worked for that month
    start = f"{year:04d}-{month:02d}-01"
    #naive way: get rows where date LIKE 'YYYY-MM-%'
    cur.execute("""
        SELECT SUM(hours_worked) as total_hours FROM attendance
        WHERE employee_id = ? AND date LIKE ?
    """, (employee_id, f"{year:04d}-{month:02d}-%"))
    row = cur.fetchone()
    total_hours = row["total_hours"] or 0.0

    overtime = 0.0
    if total_hours > STANDARD_MONTH_HOURS:
        overtime = total_hours - STANDARD_MONTH_HOURS
        regular_hours = STANDARD_MONTH_HOURS
    else:
        regular_hours = total_hours

    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime * hourly_rate * 1.5
    gross_pay = round(regular_pay + overtime_pay + allowances, 2)
    net_pay = round(gross_pay - deductions, 2)

    #save payroll
    now_iso = datetime.now().isoformat(timespec='seconds')
    cur.execute("""
        INSERT INTO payroll
        (employee_id, month, year, hours_worked, overtime_hours, gross_pay, deductions, allowances, net_pay, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (employee_id, month, year, total_hours, overtime, gross_pay, deductions, allowances, net_pay, now_iso))
    conn.commit()
    conn.close()

    return {
        "employee_id": employee_id,
        "month": month,
        "year": year,
        "hours_worked": total_hours,
        "overtime_hours": overtime,
        "gross_pay": gross_pay,
        "deductions": deductions,
        "allowances": allowances,
        "net_pay": net_pay
    }

def generate_payroll_for_all(month, year, default_allowance=0.0, default_deduction=0.0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM employees")
    employees = cur.fetchall()
    conn.close()

    results = []
    for e in employees:
        r = compute_pay_for_employee(e["id"], month, year, default_allowance, default_deduction)
        if r:
            results.append(r)
    return results
