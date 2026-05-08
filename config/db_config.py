import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass123",
            database="invoices"
        )
        return conn
    except Error as e:
        print("Database connection failed:",e)
        return None
    
