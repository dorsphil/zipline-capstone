import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_analysis_views(sql_filename):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db"
        )
        cursor = db.cursor()

        with open(sql_filename, 'r') as f:
            # We'll use our reliable cleaning logic to ignore comments
            sql_script = "".join([line for line in f if not line.strip().startswith('--')])
            commands = sql_script.split(';')

        for command in commands:
            clean_cmd = command.strip()
            if clean_cmd:
                print(f"⏳ Creating View...")
                cursor.execute(clean_cmd)
                print(" View created successfully!")

        # Verification Step: Show the columns of the new view
        print("\n Table Structure for 'deliveries_complete':")
        cursor.execute("DESCRIBE deliveries_complete")
        for column in cursor.fetchall():
            print(f"   - {column[0]} ({column[1]})")

        db.commit()
    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# Make sure the path matches your folder structure
create_analysis_views('sql-scripts/04_create_views.sql')