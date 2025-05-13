#BIS698W1700_Group03_Wholesale/Retail application management
#Importing all necessary functions
from database.db_config import create_connection  # Import function to create a database connection

# Function to generate a report of the total number of orders placed per date
def generate_order_report():
    """
    Generates a report of total orders placed per date.
    Returns a formatted string of report data or an error message.
    """
    try:
        connection = create_connection()  # Establish database connection
        if connection:
            cursor = connection.cursor()
            # Query to count number of orders grouped by date
            cursor.execute("SELECT order_date, COUNT(id) AS order_count FROM orders GROUP BY order_date")
            report = cursor.fetchall()  # Fetch the results
            connection.close()  # Close the connection

            if not report:
                return "No order data available."  # Return message if no data found

            # Format each row of the report into a readable string
            report_data = "\n".join([f"Date: {row[0]}, Orders Placed: {row[1]}" for row in report])
            return report_data
    except Exception as e:
        # Return error message if something goes wrong during the process
        return f"Error generating order report: {str(e)}"
    
    return "Error generating order report."  # Fallback return in case no connection is made


# Function to generate a report showing the total quantity sold per product
def generate_product_report():
    """
    Generates a report of total quantity sold per product.
    Returns a formatted string of report data or an error message.
    """
    try:
        connection = create_connection()  # Establish database connection
        if connection:
            cursor = connection.cursor()
            # Query to sum quantities sold, grouped by product name
            cursor.execute("""
                SELECT products.name, SUM(orders.quantity) AS total_sold 
                FROM orders 
                INNER JOIN products ON orders.product_id = products.id 
                GROUP BY products.name
            """)
            report = cursor.fetchall()  # Fetch the results
            connection.close()  # Close the connection

            if not report:
                return "No product sales data available."  # Return message if no data found

            # Format each row of the report into a readable string
            report_data = "\n".join([f"Product: {row[0]}, Total Sold: {row[1]}" for row in report])
            return report_data
    except Exception as e:
        # Return error message if something goes wrong during the process
        return f"Error generating product report: {str(e)}"
    
    return "Error generating product report."  # Fallback return in case no connection is made
