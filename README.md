# End-to-End HR Analytics with Python, SQLite and Power BI

A full data pipeline project that transforms raw HR data from Excel into an interactive Power BI dashboard — covering database design, data ingestion, SQL views, and visualization.

---

## 📋 Project Overview

This project simulates a real-world HR analytics solution for a mid-sized company (~150 employees). The goal is to replace manual Excel-based reporting with a structured database and interactive dashboard that answers two key business questions:

- **What is the total salary cost per department?**
- **Which departments have the most absence days?**

---
## Dashboard Preview

<img width="739" height="410" alt="HRAnalytics" src="https://github.com/user-attachments/assets/1c228f4a-9e1d-4fb1-82bc-203bd0bed4cb" />

---

## 🗂️ Project Structure

```
hr-analytics/
│
├── data/
│   └── personal.xlsx        # Source data (Employees, Absences, Overtime)
│
├── create_db.py             # Creates SQLite database and tables
├── import_data.py           # Reads Excel and loads data into SQLite
├── queries.py               # SQL views for Power BI
│
└── hr_data.db               # SQLite database (generated)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Storage | SQLite |
| Data Processing | Python, Pandas |
| ORM / DB Connection | SQLAlchemy, sqlite3 |
| Visualization | Power BI Desktop |
| Source Data | Excel (.xlsx) |

---

## 🗄️ Database Schema

Four normalized tables:

- **departments** — department_id, department_name
- **employees** — employee_id, name, title, salary, employment_date, termination_date, department_id, is_department_head
- **absences** — absence_id, employee_id, start_date, end_date, absence_type
- **overtime** — overtime_id, employee_id, start_date, end_date, hours

---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install pandas openpyxl sqlalchemy
```

### 2. Create the database
```bash
python create_db.py
```

### 3. Import data from Excel
```bash
python import_data.py
```

### 4. Create SQL views
```bash
python queries.py
```

### 5. Connect Power BI
- Open Power BI Desktop
- Get Data → ODBC
- Connection string: `Driver={SQLite3 ODBC Driver};Database=C:\path\to\hr_data.db`
- Load the views `salary_by_department` and `absence_by_department`

---

## 📊 Dashboard Features

- **Total Salary by Department** — bar chart showing aggregated salary costs per department, excluding terminated employees
- **Total Absence Days by Department** — bar chart showing total absence days per department
- **Date Range Slicer** — filter absence data by custom date range

---

## 📌 Key Concepts Demonstrated

- Relational database design with foreign keys and normalization
- ETL pipeline: Extract (Excel) → Transform (Pandas) → Load (SQLite)
- SQL views for aggregated reporting
- ODBC connection between SQLite and Power BI
- Upsert logic to avoid duplicate imports
