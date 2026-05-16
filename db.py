import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Creates and returns a MySQL database connection
    for Candidate Screening & Ranking System (ATS).
    """

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="####",          
            password="#####",          
            database="resume_system"
        )

        if conn.is_connected():
            return conn

    except Error as e:
        print("Database connection failed:", e)
        return None
