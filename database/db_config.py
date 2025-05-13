#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="141.209.241.57",
            user="velth1p",  
            password="mypass",  
            database="BIS698W1700_GRP3"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
