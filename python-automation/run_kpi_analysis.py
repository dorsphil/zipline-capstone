import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def run_kpi_report(sql_filename):
    try:
        # 1. Connect to MySQL
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # 2. Read and clean the SQL script
        with open(sql_filename, 'r') as f:
            content = f.read()
            # Remove multi-line comments
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            # Remove single-line comments
            clean_content = re.sub(r'--.*', '', content)
            commands = clean_content.split(';')

        print("🚀 ZIPLINE KPI ANALYSIS REPORT\n" + "="*50)

        # 3. Execute queries and display results
        for command in commands:
            query = command.strip()
            if query:
                # Execute the query
                cursor.execute(query)
                
                # Extract headers and data
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # Section Header (using the first column name to identify the table)
                print(f"\n DATA TABLE: {columns[0].replace('_', ' ').upper()}")
                print("-" * (len(columns) * 22))
                
                # Print Column Headers
                header_row = " | ".join(f"{col:^20}" for col in columns)
                print(header_row)
                print("-" * (len(columns) * 22))

                # Print Data Rows
                if not results:
                    print("   (No data found)")
                else:
                    for row in results:
                        print(" | ".join(f"{str(val):^20}" for val in row))

        print("\n" + "="*50 + "\n KPI Report Generation Complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# Execute the script
run_kpi_report('sql-scripts/05_operationalvalue_analysis.sql')