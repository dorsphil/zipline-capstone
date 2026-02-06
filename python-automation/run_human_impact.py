import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials from the .env file
load_dotenv()

def run_impact_analysis(sql_filename):
    """
    Executes queries focused on the human element of Zipline's operations.
    Includes dynamic headers for reporting and specific error catching 
    for file path issues.
    """
    try:
        # Establish connection to the MySQL database
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # Step 1: Read and clean the SQL file
        with open(sql_filename, 'r') as f:
            content = f.read()
            # Remove single-line comments so Python sends clean SQL to the server
            clean_content = re.sub(r'--.*', '', content)
            # Separate the file into individual analysis tasks
            commands = clean_content.split(';')

        print(" ZIPLINE HUMAN IMPACT REPORT\n" + "="*60)

        # Step 2: Iterate through each impact query
        for command in commands:
            query = command.strip()
            if query:
                # Execute the specific impact metric query
                cursor.execute(query)
                
                # Fetch metadata (column names) and data rows
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # DYNAMIC HEADER LOGIC:
                # Takes the first column name (e.g., 'DISTRICT') and turns it into a section title
                section_title = columns[0].replace('_', ' ').upper()
                print(f"\n {section_title} ANALYSIS")
                
                # Table formatting: Calculate width based on the number of columns
                width = (len(columns) * 25)
                print("-" * width)
                print(" | ".join(f"{col:^23}" for col in columns))
                print("-" * width)

                # Step 3: Print the results
                if not results:
                    print("   (No matching data found)")
                else:
                    for row in results:
                        # DATA FORMATTING: 
                        # Rounds decimals (floats) to 2 places for a professional look
                        formatted_row = [f"{val:.2f}" if isinstance(val, float) else str(val) for val in row]
                        print(" | ".join(f"{val:^23}" for val in formatted_row))

        print("\n" + "="*60 + "\n Human Impact Analysis Complete!")

    except mysql.connector.Error as err:
        # Catch database-side errors (syntax, connection, etc.)
        print(f" MySQL Error: {err}")
    except FileNotFoundError:
        # Catch Python-side errors (wrong file path or missing file)
        print(f" Error: File '{sql_filename}' not found. Check your '../' path logic!")
    finally:
        # Ensure the database connection closes regardless of success or failure
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# PATH UPDATE: Using '../' to go back one level from 'python_automation_files'
run_impact_analysis('../sql-scripts/07_humanimpact_analysis.sql')