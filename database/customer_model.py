#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import mysql.connector
from database.db_config import create_connection

# Fetch all customers
def get_all_customers():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    cursor.close()
    connection.close()
    return customers

# Update customer details including address
def update_customer(id, first_name, last_name, email, phone_number,
                    street, city, state, zip_code, country):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
        UPDATE customers 
        SET first_name = %s, last_name = %s, email = %s, phone_number = %s,
            street = %s, city = %s, state = %s, zip_code = %s, country = %s
        WHERE id = %s
    """
    cursor.execute(query, (
        first_name, last_name, email, phone_number,
        street, city, state, zip_code, country, id
    ))

    connection.commit()
    cursor.close()
    connection.close()

# Add new customer including address
def add_customer(first_name, last_name, email, phone_number,
                 street, city, state, zip_code, country):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO customers 
        (first_name, last_name, email, phone_number, street, city, state, zip_code, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        first_name, last_name, email, phone_number,
        street, city, state, zip_code, country
    ))

    connection.commit()
    cursor.close()
    connection.close()
