# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def get_connection():
#     try:
#         conn = mysql.connector.connect(
#             host=os.getenv("MYSQL_HOST", "localhost"),
#             user=os.getenv("MYSQL_USER", "root"),
#             password=os.getenv("MYSQL_PASSWORD", ""),
#             database=os.getenv("MYSQL_DB", "email_ai")
#         )
#         return conn
#     except Error as e:
#         print(f"Error: {e}")
#         return None
import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            ssl_ca="/etc/ssl/cert.pem"  # REQUIRED for PlanetScale on Render
        )

    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None
