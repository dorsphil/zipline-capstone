import mysql.connector
import os
import re
from dotenv import load_dotenv

load_dotenv()

def load_csv_data(sql_filename):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="zipline_db",
            allow_local_infile=True 
        )
        cursor = db.cursor()

        with open(sql_filename, 'r') as f:
            content = f.read()
            # This regex removes all lines starting with -- AND comments at the end of lines
            clean_content = re.sub(r'--.*', '', content)
            commands = clean_content.split(';')

        for command in commands:
            clean_cmd = command.strip()
            if clean_cmd:
                print(f" Running command...")
                cursor.execute(clean_cmd)
                print(" Success!")

        db.commit()
        print("\n Data import complete!")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

load_csv_data('sql-scripts/02_import_datasets.sql')