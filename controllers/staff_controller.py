#BIS698W1700_Group03_Wholesale/Retail application management
#Importing all necessary functions
from database.db_config import create_connection

def get_all_orders():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE status = 'Pending'") 
    orders = cursor.fetchall()
    connection.close()
    return orders

def generate_invoice(order_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()

    if order:
        # Invoice generation logic here, saving it to a file or generating PDF
        connection.close()
        return True
    else:
        connection.close()
        return False
