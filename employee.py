from db import get_connection

def add_employee(full_name, role, department, hourly_rate, contact):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employees (full_name, role, department, hourly_rate, contact)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, role, department, hourly_rate, contact))
    conn.commit()
    conn.close()
    print("Employee added.")

def list_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_employee(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_employee(emp_id, full_name, role, department, hourly_rate, contact):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE employees
        SET full_name = ?, role = ?, department = ?, hourly_rate = ?, contact = ?
        WHERE id = ?
    """, (full_name, role, department, hourly_rate, contact, emp_id))
    conn.commit()
    conn.close()
    print("Employee updated.")

def delete_employee(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()
    print("Employee deleted.")
