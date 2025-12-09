import csv
from db import get_connection
from datetime import datetime

def export_payroll_csv(month, year, filename=None):
    if not filename:
        filename = f"payroll_{year}_{month:02d}.csv"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, e.full_name, e.department, e.role FROM payroll p
        JOIN employees e ON p.employee_id = e.id
        WHERE p.month = ? AND p.year = ?
    """, (month, year))
    rows = cur.fetchall()
    conn.close()

    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Employee ID","Name","Department","Role","Hours Worked","Overtime","Gross Pay","Deductions","Allowances","Net Pay","Generated At"])
        for r in rows:
            writer.writerow([r["employee_id"], r["full_name"], r["department"], r["role"],
                             r["hours_worked"], r["overtime_hours"], r["gross_pay"],
                             r["deductions"], r["allowances"], r["net_pay"], r["created_at"]])
    print(f"Payroll CSV exported to {filename}")

def export_attendance_csv(employee_id, filename=None):
    if not filename:
        filename = f"attendance_emp_{employee_id}.csv"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.*, e.full_name FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        WHERE a.employee_id = ?
        ORDER BY date DESC
    """, (employee_id,))
    rows = cur.fetchall()
    conn.close()

    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Attendance ID","Date","Time In","Time Out","Hours Worked","Corrected"])
        for r in rows:
            writer.writerow([r["id"], r["date"], r["time_in"], r["time_out"], r["hours_worked"], r["corrected"]])
    print(f"Attendance CSV exported to {filename}")
