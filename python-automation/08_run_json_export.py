import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials from the .env file
load_dotenv()

def run_json_export(sql_filename):
    """
    Executes SQL queries that use the 'INTO OUTFILE' command to 
    save analysis results directly from MySQL into JSON files.
    """
    try:
        # 1. Establish connection to the database
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # 2. Open and Read the SQL conversion script
        with open(sql_filename, 'r') as f:
            content = f.read()
            
            # REGEX CLEANING: 
            # Removes single-line comments (--). 
            # This is vital because comments inside the query can break the split(';') function.
            clean_content = re.sub(r'--.*', '', content)
            
            # Split the script into individual export commands
            commands = clean_content.split(';')

        print(f" Running JSON export automation from: {sql_filename}")

        # 3. Iterate through each export command
        for command in commands:
            query = command.strip()
            if query:
                print(f"  Sending export command to MySQL engine...")
                # We execute the query, but we DO NOT use fetchall().
                # This is because 'INTO OUTFILE' writes the data directly to your disk,
                # so there are no rows sent back to Python to display.
                cursor.execute(query)
        
        # Save any changes 
        db.commit()
        print("\n Execution finished. If no 'File already exists' errors appeared, your JSON files are ready!")

    except mysql.connector.Error as err:
        # Catch specific MySQL errors:
        print(f" MySQL Error: {err}")
    except Exception as e:
        # Catch general Python errors (like file path issues)
        print(f" System Error: {e}")
    finally:
        # Always close the connection
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

run_json_export('../sql-scripts/08_sqljson_conversion.sql')
