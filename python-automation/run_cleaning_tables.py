import mysql.connector
import os
import re
from dotenv import load_dotenv

load_dotenv()

def run_cleaning_pipeline(sql_filename):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        with open(sql_filename, 'r') as f:
            content = f.read()
            # Removes multi-line comments /* ... */
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            # Removes single-line comments --
            clean_content = re.sub(r'--.*', '', content)
            commands = clean_content.split(';')

        for command in commands:
            clean_cmd = command.strip()
            if clean_cmd:
                print(f"\n⚡ Executing: {clean_cmd[:60]}...")
                cursor.execute(clean_cmd)
                
                # If it's a SELECT statement, show us the results
                if clean_cmd.upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    if results:
                        print(f" Found {len(results)} rows:")
                        for row in results[:5]: # Shows first 5 rows so terminal isn't overwhelmed
                            print(f"   {row}")
                    else:
                        print("✨ No issues found (0 rows).")
                
                # If it's an UPDATE or CREATE, show rows affected
                else:
                    print(f" Done. Rows affected: {cursor.rowcount}")

        db.commit()
        print("\n🚀 Zipline Data Cleaning Complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

run_cleaning_pipeline('sql-scripts/03_cleaning_tables.sql')