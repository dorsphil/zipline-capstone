import mysql.connector
import os
import re
from dotenv import load_dotenv

# Load database credentials from  .env file for security
load_dotenv()

def run_kpi_report(sql_filename):
    """
    Connects to MySQL, executes high-level KPI queries, and 
    auto-formats the results into a clean table in the terminal.
    """
    try:
        # 1. Connect to MySQL using credentials stored in environment variables
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
            
            # REGEX CLEANING:
            # Removes multi-line comments (/*...*/) and single-line comments (--)
            # so they don't cause syntax errors during the split process.
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            clean_content = re.sub(r'--.*', '', content)
            
            # Split the giant string into a list of individual SQL commands
            commands = clean_content.split(';')

        print(" ZIPLINE KPI ANALYSIS REPORT\n" + "="*50)

        # 3. Execute queries and display results
        for command in commands:
            query = command.strip()
            if query:
                # Execute the current query in the loop
                cursor.execute(query)
                
                # METADATA: Get column names from the cursor description
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

                # DYNAMIC UI: Create a table header based on the first column name
                # .replace('_', ' ') makes "DELIVERY_KEY" look like "DELIVERY KEY"
                print(f"\n DATA TABLE: {columns[0].replace('_', ' ').upper()}")
                
                # Create a visual line that scales with the number of columns
                line_width = (len(columns) * 22)
                print("-" * line_width)
                
                # COLUMN FORMATTING: ^20 centers the text in a 20-character block
                header_row = " | ".join(f"{col:^20}" for col in columns)
                print(header_row)
                print("-" * line_width)

                # 4. Print Data Rows
                if not results:
                    print("   (No data found)")
                else:
                    for row in results:
                        # Convert each piece of data to a string and center it for alignment
                        print(" | ".join(f"{str(val):^20}" for val in row))

        print("\n" + "="*50 + "\n KPI Report Generation Complete!")

    except mysql.connector.Error as err:
        # Catches database connection or SQL syntax errors
        print(f" MySQL Error: {err}")
    finally:
        # Ensures the database connection is closed safely
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

run_kpi_report('../sql-scripts/05_operationalvalue_analysis.sql')
