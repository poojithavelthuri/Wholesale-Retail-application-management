import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from database.customer_model import get_all_customers

# Set assets folder path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def open_customers_view():
    def load_customers(filtered=None):
        for widget in table_frame.winfo_children()[len(headers):]:  # Keep headers, clear rest
            widget.destroy()

        data = filtered if filtered is not None else get_all_customers()

        if not data:
            empty_label = ctk.CTkLabel(table_frame, text="No Customers Available", font=("Arial", 14), text_color="#1F4E78")
            empty_label.grid(row=1, column=0, columnspan=len(headers), pady=20)
        else:
            for row, customer in enumerate(data, start=1):
                values = [
                    customer.get("id", "N/A"),
                    customer.get("first_name", "N/A"),
                    customer.get("last_name", "N/A"),
                    customer.get("email", "N/A"),
                    customer.get("phone_number", "N/A"),
                    customer.get("street", "N/A"),
                    customer.get("city", "N/A"),
                    customer.get("state", "N/A"),
                    customer.get("zip_code", "N/A"),
                    customer.get("country", "N/A")
                ]
                for col, (value, width) in enumerate(zip(values, column_widths)):
                    label = ctk.CTkLabel(table_frame, text=value, font=("Arial", 12), text_color="black", fg_color="white", width=width)
                    label.grid(row=row, column=col, padx=2, pady=3, sticky="ew")

    def search_customers():
        query = search_entry.get().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search term.")
            return
        filtered = [c for c in get_all_customers() if
                    query in c.get("first_name", "").lower() or
                    query in c.get("last_name", "").lower() or
                    query in c.get("email", "").lower() or
                    query in c.get("phone_number", "").lower()]
        load_customers(filtered)

    def clear_search():
        search_entry.delete(0, 'end')
        load_customers()

    window = ctk.CTkToplevel()
    window.title("View Customers")
    window.geometry("1550x850")
    window.configure(bg="#B3E0F2")

    # Header
    header_frame = ctk.CTkFrame(window, fg_color="#1F4E78", height=120)
    header_frame.pack(fill="x", pady=20)

    # Customers Icon (Larger size)
    customers_icon = None
    customers_img_path = os.path.join(ASSETS_PATH, "customers_icon.png")
    if os.path.exists(customers_img_path):
        try:
            customers_img = Image.open(customers_img_path).resize((100, 100), Image.Resampling.LANCZOS)
            customers_icon = CTkImage(light_image=customers_img, size=(100, 100))
        except Exception as e:
            print("Error loading image:", e)

    if customers_icon:
        img_label = ctk.CTkLabel(header_frame, image=customers_icon, text="")
        img_label.image = customers_icon
        img_label.pack(side="left", padx=20, pady=10)

    # Header Text (Positioned a bit lower and larger size)
    header_label = ctk.CTkLabel(header_frame, text="VIEW CUSTOMERS", font=("Impact", 30), text_color="white")
    header_label.pack(side="top", pady=30)

    # Back Button (Larger size and slightly adjusted)
    back_button = ctk.CTkButton(header_frame, text="← Back", width=120, height=70, fg_color="#1F4E78", text_color="white", command=window.destroy)
    back_button.pack(side="right", padx=20, pady=10)

    # Search Bar and Buttons (Search entry left aligned and buttons beside it with dark blue color)
    search_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    search_frame.pack(fill="x", pady=10)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by name, email, or phone", width=500)
    search_entry.pack(side="left", padx=10, expand=True)

    search_button = ctk.CTkButton(search_frame, text="Search", command=search_customers, width=120, height=40, fg_color="#1F4E78", text_color="white")
    search_button.pack(side="left", padx=5)

    clear_button = ctk.CTkButton(search_frame, text="Clear", command=clear_search, width=120, height=40, fg_color="#1F4E78", text_color="white")
    clear_button.pack(side="left", padx=5)

    # Table Frame (Expanding to Fill Screen, remove empty space after "Country" field)
    table_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    headers = [
        "Customer ID", "First Name", "Last Name", "Email", "Phone Number",
        "Street", "City", "State", "Zip Code", "Country"
    ]
    column_widths = [100, 150, 150, 250, 130, 180, 130, 120, 120, 150]  # Adjusted widths

    for col, (header, width) in enumerate(zip(headers, column_widths)):
        label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), text_color="white", fg_color="#1F4E78", width=width)
        label.grid(row=0, column=col, padx=2, pady=5, sticky="ew")

    load_customers()

    window.mainloop()
