from utils import load_json, save_json, current_time, parse_time, input_pos_int, input_str, HR_PIN
from datetime import datetime
import csv
import os

ATT_FILE = 'db/attendance.json'  #updated to db folder
EMP_FILE = 'db/employees.json'   #reference for employees

#sign in
def sign_in(employee_id=None):
    if employee_id is None:
        print("\n--- Sign In --- (0 to go back)")
        employee_id = input_pos_int("Enter Employee ID: ")
        if employee_id == 0: return
    records = load_json(ATT_FILE)
    timestamp = current_time()
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": employee_id, "type": "in", "time": timestamp, "corrected_by": None})
    save_json(ATT_FILE, records)
    print(f"Employee {employee_id} signed in at {timestamp}")

#sign out
def sign_out(employee_id=None):
    if employee_id is None:
        print("\n--- Sign Out --- (0 to go back)")
        employee_id = input_pos_int("Enter Employee ID: ")
        if employee_id == 0: return
    records = load_json(ATT_FILE)
    timestamp = current_time()
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": employee_id, "type": "out", "time": timestamp, "corrected_by": None})
    save_json(ATT_FILE, records)
    print(f"Employee {employee_id} signed out at {timestamp}")

#view attendance logs
def view_attendance(wait=True):
    records = load_json(ATT_FILE)
    if not records:
        print("No attendance records.")
    else:
        print("\n--- Attendance Records ---")
        for r in sorted(records, key=lambda x: x['time']):
            print(f"RecID:{r['id']} | Emp:{r['employee_id']} | {r['type']} | {r['time']} | corrected_by:{r.get('corrected_by')}")
    if wait:
        input("Press Enter to go back...")

#hr: add attendance record
def hr_add_record():
    print("\n--- HR Add Attendance Record ---")
    pin = input_str("Enter HR PIN (0 to go back): ")
    if pin == "0": return
    if pin != HR_PIN:
        print("Invalid HR PIN.")
        return
    employee_id = input_pos_int("Employee ID: ")
    if employee_id == 0: return
    ttype = input_str("Type (in/out): ").lower()
    if ttype == "0": return
    if ttype not in ["in", "out"]:
        print("Invalid type. Must be 'in' or 'out'.")
        return
    timestr = input_str("Timestamp (YYYY-MM-DD HH:MM:SS) or 'now': ")
    if timestr == "0": return
    if timestr.lower() == "now":
        timestr = current_time()
    else:
        try:
            datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        except Exception:
            print("Invalid timestamp format.")
            return
    records = load_json(ATT_FILE)
    rec_id = 1 if not records else max(r['id'] for r in records) + 1
    records.append({"id": rec_id, "employee_id": employee_id, "type": ttype, "time": timestr, "corrected_by": "HR"})
    save_json(ATT_FILE, records)
    print("Attendance record added by HR.")

#hr: edit attendance record
def hr_edit_record():
    print("\n--- HR Edit Attendance Record ---")
    pin = input_str("Enter HR PIN (0 to go back): ")
    if pin == "0": return
    if pin != HR_PIN:
        print("Invalid HR PIN.")
        return
    records = load_json(ATT_FILE)
    if not records:
        print("No records.")
        return
    rec_id = input_pos_int("Enter Record ID to edit: ")
    if rec_id == 0: return
    rec = next((r for r in records if r['id'] == rec_id), None)
    if not rec:
        print("Record not found.")
        return
    print(f"Current: {rec}")
    new_type = input(f"Type ({rec['type']}): ").strip()
    if new_type != "":
        if new_type not in ["in", "out"]:
            print("Invalid type. Keeping old.")
        else:
            rec['type'] = new_type
    new_time = input(f"Time ({rec['time']}): ").strip()
    if new_time != "":
        try:
            datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            rec['time'] = new_time
        except Exception:
            print("Invalid time format. Keeping old.")
    rec['corrected_by'] = "HR"
    save_json(ATT_FILE, records)
    print("Record updated by HR.")

#hr: delete attendance record
def hr_delete_record():
    print("\n--- HR Delete Attendance Record ---")
    pin = input_str("Enter HR PIN (0 to go back): ")
    if pin == "0": return
    if pin != HR_PIN:
        print("Invalid HR PIN.")
        return
    records = load_json(ATT_FILE)
    if not records:
        print("No records.")
        return
    rec_id = input_pos_int("Enter Record ID to delete: ")
    if rec_id == 0: return
    newlist = [r for r in records if r['id'] != rec_id]
    if len(newlist) == len(records):
        print("Record not found.")
    else:
        save_json(ATT_FILE, newlist)
        print("Record deleted by HR.")

#calculate hours for a specific employee on a date
def get_hours_for_date(employee_id, date_str):
    records = load_json(ATT_FILE)
    day_recs = [r for r in records if r['employee_id'] == employee_id and r['time'].startswith(date_str)]
    day_recs.sort(key=lambda x: x['time'])
    hours = 0.0
    in_time = None
    for r in day_recs:
        if r['type'] == 'in':
            in_time = r['time']
        elif r['type'] == 'out' and in_time:
            try:
                t_in = parse_time(in_time)
                t_out = parse_time(r['time'])
                diff = (t_out - t_in).total_seconds() / 3600.0
                if diff > 0:
                    hours += diff
            except Exception:
                pass
            in_time = None
    return round(hours, 2)

#get list of dates employee has records in a month
def _get_dates_in_month(employee_id, month, year):
    records = load_json(ATT_FILE)
    dates = set()
    for r in records:
        if r['employee_id'] != employee_id:
            continue
        try:
            dt = parse_time(r['time'])
        except Exception:
            continue
        if dt.month == month and dt.year == year:
            dates.add(dt.strftime("%Y-%m-%d"))
    return sorted(list(dates))

#get total regular + overtime hours for a month 
def get_month_hours(employee_id, month, year):
    dates = _get_dates_in_month(employee_id, month, year)
    total_regular = 0.0
    total_overtime = 0.0
    for d in dates:
        h = get_hours_for_date(employee_id, d)
        reg = min(h, 8.0)
        ot = max(0.0, h - 8.0)
        total_regular += reg
        total_overtime += ot
    return round(total_regular, 2), round(total_overtime, 2)

#export monthly attendance history for a specific employee to csv
def export_attendance_history(employee_id):
    records = [r for r in load_json(ATT_FILE) if r['employee_id'] == employee_id]
    if not records:
        print("No attendance records for that employee.")
        return
    path = os.path.join('exports', f"attendance_history_emp{employee_id}.csv")
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "employee_id", "type", "time", "corrected_by"])
        writer.writeheader()
        for r in sorted(records, key=lambda x: x['time']):
            writer.writerow(r)
    print(f"Attendance history exported to {path}")

#export overtime report for a given month/year
def export_overtime_report(month, year):
    employees = load_json(EMP_FILE)
    path = os.path.join('exports', f"overtime_report_{month}_{year}.csv")
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["employee_id", "name", "regular_hours", "overtime_hours"])
        for emp in employees:
            reg, ot = get_month_hours(emp['id'], month, year)
            writer.writerow([emp['id'], emp['name'], reg, ot])
    print(f"Overtime report exported to {path}")

#export daily attendance summary for a given date
def export_daily_summary(date_str):
    records = load_json(ATT_FILE)
    employees = load_json(EMP_FILE)
    path = os.path.join('exports', f"daily_summary_{date_str}.csv")
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["employee_id", "name", "hours_worked"])
        for emp in employees:
            h = get_hours_for_date(emp['id'], date_str)
            writer.writerow([emp['id'], emp['name'], h])
    print(f"Daily attendance summary exported to {path}")