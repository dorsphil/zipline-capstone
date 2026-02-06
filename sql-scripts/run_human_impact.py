import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def run_impact_analysis(sql_filename):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # Read and clean SQL file
        with open(sql_filename, 'r') as f:
            content = f.read()
            clean_content = re.sub(r'--.*', '', content)
            commands = clean_content.split(';')

        print(" ZIPLINE HUMAN IMPACT REPORT\n" + "="*60)

        for command in commands:
            query = command.strip()
            if query:
                # Execute the query
                cursor.execute(query)
                
                # Extract metadata
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # Print a descriptive header for the table
                # We use the first column or the specific keywords to label the section
                section_title = columns[0].replace('_', ' ').upper()
                print(f"\n {section_title}")
                
                width = (len(columns) * 25)
                print("-" * width)
                print(" | ".join(f"{col:^23}" for col in columns))
                print("-" * width)

                if not results:
                    print("   (No matching data found)")
                else:
                    for row in results:
                        # Formatting for the report: Round floats to 2 decimal places
                        formatted_row = [f"{val:.2f}" if isinstance(val, float) else str(val) for val in row]
                        print(" | ".join(f"{val:^23}" for val in formatted_row))

        print("\n" + "="*60 + "\n Human Impact Analysis Complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    except FileNotFoundError:
        print(f" Error: File '{sql_filename}' not found. Check your filename spelling!")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# Double-check this filename matches exactly what you saved!
run_impact_analysis('sql-scripts/07_humanimpact_analysis.sql')