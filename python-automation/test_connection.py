# This file is a diagnostic tool to verify the connection 
# between Python and the MySQL server.

import mysql.connector
import os
from dotenv import load_dotenv

# 1. Load the credentials from the .env file
# This reads the 'DB_HOST', 'DB_USER', and 'DB_PASSWORD' so they can be used below.
load_dotenv()

try:
    # 2. Try to connect to MySQL
    # We pass the environment variables as the "key" to open the database door.
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    # If the logic reaches this point without jumping to the 'except' block, we are in!
    if connection.is_connected():
        print(" Connection Successful! Python is talking to MySQL.")
        
        # 3. Metadata Check: Get the server version
        # This confirms not just that we are connected, but that the server is responsive.
        db_info = connection.get_server_info()
        print(f"🖥️ MySQL Server Version: {db_info}")

except Exception as e:
    # If the password is wrong or the server is off, this block catches the error
    # and tells you exactly what went wrong instead of just crashing.
    print(f" Error: {e}")

finally:
    # THE CLEANUP: 
    # Whether the connection worked or failed, we must ensure we don't leave
    # an "open line" hanging. This saves memory and prevents server lag.
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print(" Connection closed safely.")