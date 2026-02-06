import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def run_coverage_analysis(sql_filename):
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
            # 1. Remove multi-line comments /* ... */
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            # 2. Remove single-line comments --
            clean_content = re.sub(r'--.*', '', content)
            commands = clean_content.split(';')

        print(" ZIPLINE GEOGRAPHIC & FACILITY COVERAGE REPORT\n" + "="*60)

        for command in commands:
            query = command.strip()
            if query:
                # Execute query
                cursor.execute(query)
                
                # Fetch metadata and results
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # Table Header Styling
                print(f"\n📍 ANALYSIS: {columns[0].replace('_', ' ').upper()}")
                line_width = (len(columns) * 25)
                print("-" * line_width)
                print(" | ".join(f"{col:^23}" for col in columns))
                print("-" * line_width)

                if not results:
                    print("   (No data found for this segment)")
                else:
                    for row in results:
                        # Format numbers to look cleaner in the table
                        formatted_row = [f"{val:.2f}" if isinstance(val, float) else str(val) for val in row]
                        print(" | ".join(f"{val:^23}" for val in formatted_row))

        print("\n" + "="*60 + "\n Coverage Report Complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# Ensure the filename matches your SQL file
run_coverage_analysis('sql-scripts/06_geo-facilitycoverage_analysis.sql')