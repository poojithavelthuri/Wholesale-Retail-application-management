#BIS698W1700_Group03_Wholesale/Retail application management
#Importing all necessary functions
from database.product_model import get_all_products, add_product
from database.order_model import get_all_orders, update_order_status
from database.customer_model import get_all_customers

# ---- FUNCTION: Load all products ----
def load_products():
    return get_all_products()

# ---- FUNCTION: Add a new product ----
def add_new_product(name, price, stock_quantity):
    add_product(name, price, stock_quantity)

# ---- FUNCTION: Load all orders ----
def load_orders():
    return get_all_orders()

# ---- FUNCTION: Update order status ----
def update_order_status_function(order_id, new_status):
    update_order_status(order_id, new_status)

# ---- FUNCTION: Load all customers ----
def load_customers():
    return get_all_customers()
