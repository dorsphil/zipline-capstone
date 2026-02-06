import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials (host, user, password) from the .env file
load_dotenv()

def load_csv_data(sql_filename):
    """
    Connects to MySQL and runs the 'LOAD DATA LOCAL INFILE' commands
    to import raw CSV datasets into the database.
    """
    try:
        # Establish connection with a special flag: 'allow_local_infile=True'
        # This flag is mandatory to give Python permission to send local files to the MySQL server.
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db",
            allow_local_infile=True 
        )
        cursor = db.cursor()

        # Step 1: Read the SQL import script
        with open(sql_filename, 'r') as f:
            content = f.read()
            
            # REGEX CLEANING:
            # Removes single-line comments (--). This is crucial because SQL comments 
            # inside a long string can break the split(';') logic.
            clean_content = re.sub(r'--.*', '', content)
            
            # Split the script into a list of individual 'LOAD DATA' commands
            commands = clean_content.split(';')

        print(f"📂 Starting data import from: {sql_filename}")

        # Step 2: Loop through each import command
        for command in commands:
            clean_cmd = command.strip()
            if clean_cmd:
                print(f" Running import command...")
                cursor.execute(clean_cmd)
                print(" Data chunk loaded successfully!")

        # Finalize the transaction to ensure all data is saved to the tables
        db.commit()
        print("\n Data import complete! Your raw tables are now populated.")

    except mysql.connector.Error as err:
        # Catches common issues like 'File Not Found' or 'Permission Denied' within MySQL
        print(f" MySQL Error: {err}")
    finally:
        # Close the connection to prevent the database from hanging
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# PATH ADJUSTMENT: '../' moves out of 'python_automation_files' to locate 'sql-scripts'
load_csv_data('../sql-scripts/02_import_datasets.sql')