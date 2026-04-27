import sqlite3
import random
from datetime import datetime, timedelta

con = sqlite3.connect("hr_data.db")

cursor = con.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Departments table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS departments(
                   department_id INTEGER PRIMARY KEY,
                   department_name TEXT NOT NULL
               )''')

# Employee table with department_id as foreign key to departments table. Also bosses can be identified by the boolean
cursor.execute('''
               CREATE TABLE IF NOT EXISTS employees(
                   employee_id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   title TEXT,
                   salary REAL,
                   employment_date TEXT,
                   termination_date TEXT,
                   department_id INTEGER,
                   is_department_head BOOLEAN DEFAULT 0,
                   FOREIGN KEY (department_id) REFERENCES departments(department_id)
               )''')

# Absences table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS absences(
                   absence_id INTEGER PRIMARY KEY,
                   employee_id INTEGER,
                   start_date TEXT NOT NULL,
                   end_date TEXT,
                   absence_type TEXT NOT NULL,
                   CHECK (absence_type IN ('Vacation','Sick Leave', 'Family Leave', 'Unauthorized Absence')),
                   FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
               )''')

# Overtime table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS overtime(
                   overtime_id INTEGER PRIMARY KEY,
                   employee_id INTEGER,
                   start_date TEXT NOT NULL,
                   end_date TEXT,
                   hours REAL,
                   FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
               )''')


# Populate database with testdata:


con.commit()


def generate_test_data():
    con = sqlite3.connect("hr_data.db")
    cursor = con.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- 1. POPULATE DEPARTMENTS ---
    depts = [('Sales',), ('Engineering',), ('Human Resources',), ('Marketing',), ('Finance',)]
    cursor.executemany("INSERT INTO departments (department_name) VALUES (?)", depts)

    # --- 2. POPULATE EMPLOYEES ---
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", 
            "Karl", "Linda", "Mona", "Nils", "Oscar", "Petra", "Quinn", "Rolf", "Sanna", "Toby"]
    titles = ["Junior Developer", "Senior Developer", "Manager", "Analyst", "Coordinator"]

    for i, name in enumerate(names, start=1):
        dept_id = random.randint(1, 5)
        # Give everyone a hire date within the last 3 years
        hire_date = (datetime(2026, 1, 1) - timedelta(days=random.randint(300, 1000))).date().isoformat()
        salary = random.randint(35000, 85000)
        is_head = 1 if i <= 5 else 0  # Make the first 5 people department heads
        
        cursor.execute('''
            INSERT INTO employees (name, title, salary, employment_date, department_id, is_department_head)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, random.choice(titles), salary, hire_date, dept_id, is_head))
    con.commit()

    # --- 3. POPULATE ABSENCES (Last 2 Years) ---
    absence_types = ['Vacation', 'Sick Leave', 'Family Leave', 'Unauthorized Absence']
    for _ in range(150):  # Generate 150 absence records
        emp_id = random.randint(1, len(names))
        # Random start date between Jan 2024 and Dec 2025
        start = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))
        duration = random.randint(1, 10)
        end = start + timedelta(days=duration)
        
        cursor.execute('''
            INSERT INTO absences (employee_id, start_date, end_date, absence_type)
            VALUES (?, ?, ?, ?)
        ''', (emp_id, start.date().isoformat(), end.date().isoformat(), random.choice(absence_types)))

    # --- 4. POPULATE OVERTIME (Last 2 Years) ---
    for _ in range(200):  # Generate 200 overtime records
        emp_id = random.randint(1, len(names))
        ot_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))
        hours = round(random.uniform(1.0, 6.0), 1)
        
        cursor.execute('''
            INSERT INTO overtime (employee_id, start_date, hours)
            VALUES (?, ?, ?)
        ''', (emp_id, ot_date.date().isoformat(), hours))

    con.commit()
    print("Successfully generated test data for 2024-2025!")
    con.close()

generate_test_data()

