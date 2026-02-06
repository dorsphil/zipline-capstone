#this file is to test if Python can actually see my MySQL server. 

import mysql.connector
import os
from dotenv import load_dotenv

# 1. Load the credentials from the .env file
load_dotenv()

try:
    # 2. Try to connect to MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    if connection.is_connected():
        print(" Connection Successful! Python is talking to MySQL.")
        
        # 3. Check what version we are running
        db_info = connection.get_server_info()
        print(f"MySQL Server Version: {db_info}")

except Exception as e:
    print(f" Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed safely.")