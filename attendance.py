from db import get_connection
from datetime import datetime

def sign_in(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    #today's date
    today = datetime.now().date().isoformat()
    now_iso = datetime.now().isoformat(timespec='seconds')

    #check kung nag signed in today without signing out
    cur.execute("""
        SELECT * FROM attendance
        WHERE employee_id = ? AND date = ? AND time_out IS NULL
    """, (employee_id, today))
    existing = cur.fetchone()
    if existing:
        print("Warning: You already have an open sign-in for today (no sign-out).")
        conn.close()
        return

    cur.execute("""
        INSERT INTO attendance (employee_id, date, time_in)
        VALUES (?, ?, ?)
    """, (employee_id, today, now_iso))
    conn.commit()
    conn.close()
    print(f"Sign-in recorded at {now_iso} for employee {employee_id}")

def sign_out(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().date().isoformat()
    now_iso = datetime.now().isoformat(timespec='seconds')

    #find the latest open attendance for today
    cur.execute("""
        SELECT * FROM attendance
        WHERE employee_id = ? AND date = ? AND time_out IS NULL
        ORDER BY id DESC LIMIT 1
    """, (employee_id, today))
    row = cur.fetchone()
    if not row:
        print("No open sign-in found for today. Maybe employee forgot to sign in.")
        conn.close()
        return

    time_in = datetime.fromisoformat(row["time_in"])
    time_out = datetime.fromisoformat(now_iso)
    delta = time_out - time_in
    hours = round(delta.total_seconds() / 3600, 2)

    cur.execute("""
        UPDATE attendance
        SET time_out = ?, hours_worked = ?
        WHERE id = ?
    """, (now_iso, hours, row["id"]))
    conn.commit()
    conn.close()
    print(f"Sign-out recorded at {now_iso}. Hours worked this session: {hours}")

def list_attendance_for_employee(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM attendance WHERE employee_id = ? ORDER BY date DESC, id DESC
    """, (employee_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def hr_correct_attendance(attendance_id, new_time_in=None, new_time_out=None):
    #only HR should call this function (CLI will request admin password)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance WHERE id = ?", (attendance_id,))
    row = cur.fetchone()
    if not row:
        print("Attendance record not found.")
        conn.close()
        return

    #prepare new values: if not provided, keep old
    time_in = new_time_in if new_time_in else row["time_in"]
    time_out = new_time_out if new_time_out else row["time_out"]

    hours = 0.0
    if time_in and time_out:
        try:
            t_in = datetime.fromisoformat(time_in)
            t_out = datetime.fromisoformat(time_out)
            hours = round((t_out - t_in).total_seconds() / 3600, 2)
        except Exception as e:
            print("Error calculating hours:", e)

    cur.execute("""
        UPDATE attendance
        SET time_in = ?, time_out = ?, hours_worked = ?, corrected = 1
        WHERE id = ?
    """, (time_in, time_out, hours, attendance_id))
    conn.commit()
    conn.close()
    print("Attendance corrected. New hours:", hours)
