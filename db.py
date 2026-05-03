import mysql.connector 
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Debajit@Saha1237890",
        database="resume_system"
    )