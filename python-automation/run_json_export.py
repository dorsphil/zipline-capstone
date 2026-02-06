import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load your database credentials
load_dotenv()

def run_json_export(sql_filename):
    try:
        # 1. Connect to the database
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # 2. Read the SQL file
        with open(sql_filename, 'r') as f:
            content = f.read()
            
            # Strip out single-line comments so they don't interfere with execution
            clean_content = re.sub(r'--.*', '', content)
            
            # Split into individual commands
            commands = clean_content.split(';')

        print(f"🚀 Running JSON export automation from: {sql_filename}")

        # 3. Execute each query exactly as written
        for command in commands:
            query = command.strip()
            if query:
                print(f" Executing export command...")
                cursor.execute(query)
                # Note: No print(results) here because INTO OUTFILE doesn't return rows to Python
        
        db.commit()
        print("\n Execution finished. If no errors appeared, your JSON files have been generated.")

    except mysql.connector.Error as err:
        # This will catch the 'File already exists' error (Error 1086) 
        # or permission errors (Error 1290/13)
        print(f" MySQL Error: {err}")
    except Exception as e:
        print(f" System Error: {e}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# Run the automation
run_json_export('sql-scripts/08_sqljson_conversion.sql')