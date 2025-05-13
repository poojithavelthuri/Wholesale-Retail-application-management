#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import mysql.connector
from database.db_config import create_connection

# Retrieves all products from the database.
# If include_hidden is False, it excludes products marked as hidden.
def get_all_products(include_hidden=False):
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access to column names

    query = "SELECT id, name, price, stock_quantity, is_hidden FROM products"
    if not include_hidden:
        query += " WHERE is_hidden = 0"  # Filter out hidden products if flag is False

    cursor.execute(query)
    products = cursor.fetchall()  # Fetch all product records

    cursor.close()
    conn.close()  # Close cursor and connection
    return products


# Adds a new product to the database using provided dictionary data
def add_product(product):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO products (name, price, stock_quantity)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (product['name'], product['price'], product['stock_quantity']))  # Insert new product
    conn.commit()  # Save changes

    cursor.close()
    conn.close()


# Updates an existing product's details in the database
def update_product(product):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
    UPDATE products
    SET name = %s, price = %s, stock_quantity = %s
    WHERE id = %s
    """
    cursor.execute(query, (product['name'], product['price'], product['stock_quantity'], product['id']))  # Update product info
    conn.commit()

    cursor.close()
    conn.close()


# Marks a product as hidden (soft delete)
def hide_product(product_id):
    conn = create_connection()
    cursor = conn.cursor()

    query = "UPDATE products SET is_hidden = 1 WHERE id = %s"
    cursor.execute(query, (product_id,))  # Set is_hidden flag to 1
    conn.commit()

    cursor.close()
    conn.close()


# Restores a previously hidden product
def restore_product(product_id):
    conn = create_connection()
    cursor = conn.cursor()

    query = "UPDATE products SET is_hidden = 0 WHERE id = %s"
    cursor.execute(query, (product_id,))  # Set is_hidden flag to 0
    conn.commit()

    cursor.close()
    conn.close()
