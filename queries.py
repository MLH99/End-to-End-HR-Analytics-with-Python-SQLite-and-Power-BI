import sqlite3
import pandas as pd

def get_salary_by_department(conn):
    query = '''SELECT departments.department_name, SUM(employees.salary) AS total_salary
                FROM departments
                JOIN employees ON departments.department_id=employees.department_id
                WHERE termination_date IS NULL
                GROUP BY departments.department_name
                ORDER BY departments.department_id;'''

    return pd.read_sql(query, conn)

def get_absence_by_department(conn, start_date, end_date):
    query = '''SELECT department_name, SUM(julianday(absences.end_date) - julianday(absences.start_date) + 1) AS total_absence
                FROM absences
                JOIN employees
                ON absences.employee_id = employees.employee_id
                JOIN departments
                ON employees.department_id = departments.department_id
                WHERE (absences.start_date >= ? AND absences.end_date =< ?
                GROUP BY department_name
                ORDER BY departments.department_id;'''
    
    return pd.read_sql(query, conn, params=(start_date, end_date))

def create_salary_by_department_view(conn):
    cursor = conn.cursor()
    cursor.execute("DROP VIEW IF EXISTS salary_by_department")
    
    query = '''CREATE VIEW IF NOT EXISTS salary_by_department AS
                SELECT departments.department_name, termination_date, employees.salary AS salary
                FROM departments
                JOIN employees ON departments.department_id=employees.department_id
                WHERE termination_date IS NULL'''
    
    
    cursor.execute(query)
    conn.commit()

def create_absence_by_department_view(conn):
    query = '''CREATE VIEW IF NOT EXISTS absence_by_department AS
                SELECT department_name, absences.start_date, absences.end_date, (julianday(absences.end_date) - julianday(absences.start_date) + 1) AS absence_days
                FROM absences
                JOIN employees
                ON absences.employee_id = employees.employee_id
                JOIN departments
                ON employees.department_id = departments.department_id'''
    
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

conn = sqlite3.connect("hr_data.db")

create_salary_by_department_view(conn)
create_absence_by_department_view(conn)