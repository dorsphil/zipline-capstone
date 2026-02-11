import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials from the .env file
load_dotenv()

def run_coverage_analysis(sql_filename):
    """
    Connects to MySQL to analyze Zipline's geographic reach.
    This script is specialized to handle float formatting (decimals)
    and clean out complex multi-line SQL comments.
    """
    try:
        # Establish a connection to the Zipline database
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # Step 1: Read the SQL file
        with open(sql_filename, 'r') as f:
            content = f.read()
            
            # COMPLEX CLEANING:
            # 1. re.DOTALL allows the '.*?' to match across multiple lines.
            # This removes large blocks of text wrapped in /* ... */
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            # 2. Standard removal of single-line comments starting with '--'
            clean_content = re.sub(r'--.*', '', content)
            
            # 3. Splitting by semicolon to isolate each analysis query
            commands = clean_content.split(';')

        print(" ZIPLINE GEOGRAPHIC & FACILITY COVERAGE REPORT\n" + "="*60)

        # Step 2: Processing each query
        for command in commands:
            query = command.strip()
            if query:
                cursor.execute(query)
                
                # Metadata: description[0] gives us the column headers
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # Table UI: Creates a dynamic header based on the first column name
                # .replace('_', ' ') makes "FACILITY_TYPE" look like "FACILITY TYPE"
                print(f"\n ANALYSIS: {columns[0].replace('_', ' ').upper()}")
                line_width = (len(columns) * 25)
                print("-" * line_width)
                print(" | ".join(f"{col:^23}" for col in columns))
                print("-" * line_width)

                if not results:
                    print("   (No data found for this segment)")
                else:
                    # Step 3: Formatting Data for the Terminal
                    for row in results:
                        # List Comprehension with an 'if' check:
                        # If the value is a float (decimal), format it to 2 decimal places (e.g., 12.34).
                        # Otherwise, just turn it into a string.
                        formatted_row = [f"{val:.2f}" if isinstance(val, float) else str(val) for val in row]
                        print(" | ".join(f"{val:^23}" for val in formatted_row))

        print("\n" + "="*60 + "\n Coverage Report Complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        # Close connection to maintain database health
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


run_coverage_analysis('../sql-scripts/06_geo-facilitycoverage_analysis.sql')
