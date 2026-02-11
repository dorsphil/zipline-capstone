import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from the .env file (DB credentials)
load_dotenv()

def create_analysis_views(sql_filename):
    """
    Connects to MySQL, reads a SQL file to create database Views, 
    and prints the resulting table structure for confirmation.
    """
    try:
        # Establish connection using credentials stored in environment variables
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        # Open the SQL file in read mode
        with open(sql_filename, 'r') as f:
            # List Comprehension: Reads file line-by-line and ignores any line starting with '--'
            # This prevents MySQL from getting confused by SQL comments
            sql_script = "".join([line for line in f if not line.strip().startswith('--')])
            
            # Split the script into a list of individual commands using the semicolon as the separator
            commands = sql_script.split(';')

        # Loop through each command extracted from the file
        for command in commands:
            clean_cmd = command.strip()  # Remove extra whitespace/newlines
            if clean_cmd:
                print(f" Executing SQL Task...")
                cursor.execute(clean_cmd)
                print(" Task successful!")

        # Verification: Run a 'DESCRIBE' command to show the columns of the new View
        print("\n Table Structure Verification:")
        cursor.execute("DESCRIBE deliveries_complete")
        
        # Fetchall() retrieves all rows from the last executed query
        for column in cursor.fetchall():
            # column[0] is the Name, column[1] is the Data Type
            print(f"   - {column[0]} ({column[1]})")

        # Save changes to the database
        db.commit()

    except mysql.connector.Error as err:
        # Catch and display any database-specific errors 
        print(f" MySQL Error: {err}")
    
    finally:
        # Ensure the connection is closed even if the script crashes
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


create_analysis_views('../sql-scripts/04_create_views.sql')
