#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import mysql.connector
from database.db_config import create_connection  # Handles your DB connection

# Fetch all orders with customer name and total amount
def get_all_orders():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
        o.id AS order_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        p.name AS product_name,
        o.quantity,
        p.price AS product_price,
        (o.quantity * p.price) AS total_amount,
        o.status,
        o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN products p ON o.product_id = p.id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Get column names from the cursor description
    columns = [column[0] for column in cursor.description]

    # Convert each row to a dictionary
    orders = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()

    return orders


# Update the status of a single order row
def update_order_status(order_id, new_status):
    connection = create_connection()
    cursor = connection.cursor()

    query = "UPDATE orders SET status = %s WHERE id = %s"
    cursor.execute(query, (new_status, order_id))
    connection.commit()

    cursor.close()
    connection.close()


# Save order: one order row per product (matches your schema)
def save_order(customer_id, order_items):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        connection.start_transaction()

        for item in order_items:
            # Insert one order row per product
            insert_order_query = """
                INSERT INTO orders (customer_id, product_id, quantity, order_date, status)
                VALUES (%s, %s, %s, NOW(), 'Pending')
            """
            cursor.execute(insert_order_query, (customer_id, item['product_id'], item['quantity']))

            # Update stock in products
            update_stock_query = """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
            """
            cursor.execute(update_stock_query, (item['quantity'], item['product_id']))

        connection.commit()
        return True

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
        return False

    finally:
        cursor.close()
        connection.close()
