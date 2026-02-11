import mysql.connector
import os
from dotenv import load_dotenv

# Load the .env file so Python can access the DB_HOST, DB_USER, and DB_PASSWORD
load_dotenv()

def execute_sql_file(filename):
    """
    Connects to the MySQL server and builds the initial database 
    and table structures from a SQL file.
    """
    # Initialize the connection using variables from the .env file
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = db.cursor()

    # Step 1: Read the SQL file and perform "Text Cleaning"
    with open(filename, 'r') as f:
        # Read the file line by line into a list
        lines = f.readlines()
        
        # List Comprehension: Keep the line ONLY if it doesn't start with '--'
        # This strips out SQL comments that could break the Python-to-MySQL communication
        clean_lines = [line for line in lines if not line.strip().startswith('--')]
        
        # Join the list of lines back into one giant string of pure SQL code
        full_script = "".join(clean_lines)
        
        # Step 2: Split the giant string into individual commands using the semicolon (;)
        # This allows sending commands to MySQL one at a time
        sql_commands = full_script.split(';')

    # Step 3: Loops through the list of commands and execute them
    for command in sql_commands:
        clean_command = command.strip() # Remove extra spaces or empty lines
        if clean_command: 
            try:
                # Send the command to the MySQL server
                cursor.execute(clean_command)
                # Show a preview of the first 30 characters of the command for tracking
                print(f" Successfully executed: {clean_command[:30]}...")
            except Exception as e:
                # If a command fails (e.g., table already exists), catch the error and keep going
                print(f" Error on: {clean_command[:30]}...\nReason: {e}")

    # Commit ensures all the CREATE commands are permanently saved in the database
    db.commit()
    cursor.close()
    db.close()
    print("\n Database and Tables created successfully!")


execute_sql_file('../sql-scripts/01_create_tables.sql')
