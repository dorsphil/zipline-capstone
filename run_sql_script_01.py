import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def execute_sql_file(filename):
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = db.cursor()

    with open(filename, 'r') as f:
        # 1. Read the file and filter out the comment lines (starting with --)
        lines = f.readlines()
        clean_lines = [line for line in lines if not line.strip().startswith('--')]
        full_script = "".join(clean_lines)
        
        # 2. Split by semicolon to get individual commands
        sql_commands = full_script.split(';')

    for command in sql_commands:
        clean_command = command.strip()
        if clean_command: 
            try:
                # 3. Execute the cleaned command
                cursor.execute(clean_command)
                print(f" Successfully executed: {clean_command[:30]}...")
            except Exception as e:
                print(f" Error on: {clean_command[:30]}...\nReason: {e}")

    db.commit()
    cursor.close()
    db.close()
    print("\n Database and Tables created successfully!")

execute_sql_file('sql-scripts/01_create_tables.sql')