# login_controller.py
#BIS698W1700_Group03_Wholesale/Retail application management
#Importing all necessary functions
from database.user_model import authenticate_user
from views.admin_view import open_admin_dashboard
from views.staff_view import open_staff_dashboard
from tkinter import messagebox

def on_login(username, password):
    user = authenticate_user(username, password)
    if user:
        role = user[3]  
        return user, role 
    return None, None  
