#BIS698W1700_Group03_Wholesale/Retail application management
#Importing all necessary functions
from database.db_config import create_connection

# Function to authenticate a user by checking the username and password against the database
def authenticate_user(username, password):
    connection = create_connection()  # Establish database connection
    if connection:
        cursor = connection.cursor()
        # Execute query to find a user matching the given username and password
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  # Fetch one matching user record (if any)
        connection.close()  # Close the connection
        return user  # Return user data if authentication is successful
    return None  # Return None if connection fails or user not found

