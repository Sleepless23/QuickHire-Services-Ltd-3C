from flask import Flask, jsonify, request
from utils import load_json, save_json, current_time, HR_PIN
from attendance import get_month_hours, export_attendance_history, export_overtime_report, export_daily_summary
from payroll import export_payroll_summary_csv
from employees import view_employees
from payroll import generate_payroll_for_month
import os

app = Flask(__name__)


#employees list
@app.route('/employees', methods=['GET'])
def api_employees():
    data = load_json('db/employees.json')
    return jsonify(data)

#attendance: sign in
@app.route('/attendance/signin', methods=['POST'])
def api_signin():
    body = request.get_json() or {}
    emp_id = body.get('employee_id')
    if not isinstance(emp_id, int):
        return jsonify({"error":"employee_id must be int"}), 400
    records = load_json('db/attendance.json')
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": emp_id, "type": "in", "time": current_time(), "corrected_by": None})
    save_json('db/attendance.json', records)
    return jsonify({"message":"Signed in", "record_id": rec_id})

#attendance: sign out
@app.route('/attendance/signout', methods=['POST'])
def api_signout():
    body = request.get_json() or {}
    emp_id = body.get('employee_id')
    if not isinstance(emp_id, int):
        return jsonify({"error":"employee_id must be int"}), 400
    records = load_json('db/attendance.json')
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": emp_id, "type": "out", "time": current_time(), "corrected_by": None})
    save_json('db/attendance.json', records)
    return jsonify({"message":"Signed out", "record_id": rec_id})


#hr add attendance via api
@app.route('/attendance/hr/add', methods=['POST'])
def api_hr_add():
    body = request.get_json() or {}
    hr_pin = body.get('hr_pin')
    if hr_pin != HR_PIN:
        return jsonify({"error":"Invalid HR PIN"}), 403
    try:
        emp_id = int(body.get('employee_id'))
    except Exception:
        return jsonify({"error":"employee_id required and must be int"}), 400
    ttype = body.get('type')
    if ttype not in ['in','out']:
        return jsonify({"error":"type must be 'in' or 'out'"}), 400
    timestr = body.get('time', 'now')
    if timestr == 'now':
        from utils import current_time as nowf
        timestr = nowf()
    records = load_json('db/attendance.json')
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": emp_id, "type": ttype, "time": timestr, "corrected_by": "HR"})
    save_json('db/attendance.json', records)
    return jsonify({"message":"HR record added", "record_id": rec_id})

#payroll generation via API
@app.route('/payroll/generate', methods=['POST'])
def api_generate_payroll():
    body = request.get_json() or {}
    try:
        month = int(body.get('month'))
        year = int(body.get('year'))
    except Exception:
        return jsonify({"error":"month and year required as integers"}), 400

    from payroll import OT_MULTIPLIER
    employees = load_json('db/employees.json')
    payroll_data = []
    for emp in employees:
        reg, ot = get_month_hours(emp['id'], month, year)
        reg_pay = round(reg * emp['hourly_rate'], 2)
        ot_pay = round(ot * emp['hourly_rate'] * OT_MULTIPLIER, 2)
        allowance = float(emp.get('allowance', 0))
        deduction = float(emp.get('deduction', 0))
        gross = round(reg_pay + ot_pay + allowance, 2)
        net = round(gross - deduction, 2)
        payroll_data.append({
            "employee_id": emp['id'],
            "name": emp['name'],
            "month": month,
            "year": year,
            "regular_hours": reg,
            "overtime_hours": ot,
            "regular_pay": reg_pay,
            "overtime_pay": ot_pay,
            "allowance": allowance,
            "deduction": deduction,
            "gross_pay": gross,
            "net_pay": net
        })
    save_json('db/payroll.json', payroll_data)
    export_payroll_summary_csv(month, year, payroll_data)
    return jsonify({"message":"Payroll generated and CSV exported", "count": len(payroll_data)})

#reports/exports
@app.route('/reports/attendance/<int:emp_id>', methods=['GET'])
def api_export_attendance_history(emp_id):
    export_attendance_history(emp_id)
    return jsonify({"message": f"Attendance history exported for employee {emp_id} (see exports/)"})

@app.route('/reports/overtime', methods=['POST'])
def api_export_overtime():
    body = request.get_json() or {}
    try:
        month = int(body.get('month')); year = int(body.get('year'))
    except Exception:
        return jsonify({"error":"month and year required"}), 400
    export_overtime_report(month, year)
    return jsonify({"message":f"Overtime report exported for {month}/{year}"})

@app.route('/reports/daily', methods=['POST'])
def api_export_daily():
    body = request.get_json() or {}
    date_str = body.get('date')
    if not date_str:
        return jsonify({"error":"date required (YYYY-MM-DD)"}), 400
    export_daily_summary(date_str)
    return jsonify({"message":f"Daily summary exported for {date_str}"})

#base routes for clarity
@app.route('/attendance', methods=['GET'])
def attendance_home():
    return jsonify({
        "message": "Attendance API endpoints",
        "endpoints": [
            "/attendance/signin (POST)",
            "/attendance/signout (POST)",
            "/attendance/hr/add (POST)"
        ]
    })

@app.route('/payroll', methods=['GET'])
def payroll_home():
    return jsonify({
        "message": "Payroll API endpoints",
        "endpoints": [
            "/payroll/generate (POST)"
        ]
    })

@app.route('/reports', methods=['GET'])
def reports_home():
    return jsonify({
        "message": "Reports API endpoints",
        "endpoints": [
            "/reports/attendance/<emp_id> (GET)",
            "/reports/overtime (POST)",
            "/reports/daily (POST)"
        ]
    })

#home
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message":"QuickHire API running. Use /employees, /attendance, /payroll and /reports endpoints."
    })

#run
if __name__ == "__main__":
    print("Starting API on http://127.0.0.1:5000")
    app.run(port=5000)