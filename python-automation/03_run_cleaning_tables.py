import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials from the .env file
load_dotenv()

def run_cleaning_pipeline(sql_filename):
    """
    Connects to MySQL and executes data cleaning scripts. 
    It intelligently displays results for 'SELECT' checks and 
    confirms row changes for 'UPDATE' or 'CREATE' tasks.
    """
    try:
        # Establish the connection to the database
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # Step 1: Read the SQL file into Python
        with open(sql_filename, 'r') as f:
            content = f.read()
            
            # REGEX CLEANING: 
            # 1. Removes multi-line comments
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            # 2. Removes single-line comments (-- comment)
            clean_content = re.sub(r'--.*', '', content)
            
            # 3. Split the text into separate SQL commands using the semicolon (;)
            commands = clean_content.split(';')

        # Step 2: Loop through and execute each command
        for command in commands:
            clean_cmd = command.strip()
            if clean_cmd:
                # Display the first 60 characters of the command so we know what's running
                print(f"\n⚡ Executing: {clean_cmd[:60]}...")
                cursor.execute(clean_cmd)
                
                # CONDITIONAL LOGIC: Check if the command is meant to 'fetch' data or 'change' data
                if clean_cmd.upper().startswith("SELECT"):
                    # For SELECT: We want to see if any errors/duplicates were found
                    results = cursor.fetchall()
                    if results:
                        print(f" 🔍 Issues Identified! Found {len(results)} rows:")
                        for row in results[:5]: # Only show the first 5 rows to keep it tidy
                            print(f"   {row}")
                    else:
                        print(" Data looks good! (0 rows returned).")
                
                else:
                    # For UPDATE/CREATE/INSERT: Show how many rows were actually modified
                    print(f"  Success. Rows affected: {cursor.rowcount}")

        # Finalize all changes made during the cleaning process
        db.commit()
        print("\n Zipline Data Cleaning Complete!")

    except mysql.connector.Error as err:
        # Prints specific MySQL error codes 
        print(f"  MySQL Error: {err}")
    finally:
        #  close the connection to free up system resources
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

run_cleaning_pipeline('../sql-scripts/03_cleaning_tables.sql')
