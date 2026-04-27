import pandas as pd
import sqlite3
from sqlalchemy import create_engine

class DataImporter:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def engine(self):
        path = 'sqlite:///' + self.db_path
        return create_engine(path)
    
    # method that gets the data, parses it to fit into sqlite database and inserts it into the database
    def import_data(self, file_path):
        
        engine = self.engine()
        
        df_employees = pd.read_excel(file_path, sheet_name='Employees', converters={'employment_date': str})
        
        df_absences = pd.read_excel(file_path, sheet_name='Absences', converters = {'start_date': str, 'end_date' : str})
        
        df_overtime = pd.read_excel(file_path, sheet_name='Overtime', converters={'start_date': str, 'end_date': str})
        
        df_employees.to_sql('employees',con=engine, if_exists='append', index=False)
        
        df_absences.to_sql('absences', con=engine, if_exists='append', index=False)
        
        df_overtime.to_sql('overtime', con=engine, if_exists='append', index=False)
        
        con.close()


con = sqlite3.connect('hr_data.db')

# Enter your file path here
file_path = 'data/personal.xlsx'

# Enter your database path here
db_path = 'hr_data.db'

importer = DataImporter('hr_data.db')
importer.import_data(file_path)
print('Data successfully imported from excel')



