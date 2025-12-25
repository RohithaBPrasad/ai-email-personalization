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
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DB"],
            port=int(os.getenv("MYSQL_PORT", 3306)),
            ssl_ca=os.getenv("MYSQL_SSL_CA")  # Optional (PlanetScale)
        )
        return conn

    except KeyError as e:
        raise RuntimeError(f"Missing environment variable: {e}")

    except Error as e:
        print(f"Database connection error: {e}")
        return None
