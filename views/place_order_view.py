import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import tkinter as tk  # Required for Spinbox

from database.product_model import get_all_products
from database.customer_model import get_all_customers
from database.order_model import save_order

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

order_items = []

def open_place_order():
    window = ctk.CTkToplevel()
    window.title("Place Order")
    window.geometry("900x600")
    ctk.set_appearance_mode("light")

    def go_back():
        window.destroy()
        from views.homepage import open_home_page
        open_home_page()

    def refresh_order_summary():
        for widget in order_summary_frame.winfo_children():
            widget.destroy()

        total = 0
        for item in order_items:
            text = f"{item['product_name']} x {item['quantity']} = ₹{item['total']}"
            ctk.CTkLabel(order_summary_frame, text=text, font=("Arial", 14)).pack(anchor="w")
            total += item['total']

        total_label.configure(text=f"Total: ₹{total}")

    def add_to_order():
        customer = customer_dropdown.get()
        product_name = product_dropdown.get()
        quantity = quantity_spinbox.get()

        if not (customer and product_name and quantity.isdigit()):
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        quantity_int = int(quantity)
        product = next((p for p in products if p['name'] == product_name), None)
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return

        if quantity_int > product['stock_quantity']:
            messagebox.showerror("Error", f"Not enough stock for {product['name']}.")
            return

        item_total = product['price'] * quantity_int
        order_items.append({
            "customer": customer,
            "product_id": product['id'],
            "product_name": product['name'],
            "quantity": quantity_int,
            "total": item_total
        })
        refresh_order_summary()

    def place_order():
        if not order_items:
            messagebox.showwarning("Warning", "No items in order.")
            return

        customer_name = customer_dropdown.get()
        customer = next((c for c in customers if f"{c['first_name']} {c['last_name']}" == customer_name), None)
        if not customer:
            messagebox.showerror("Error", "Customer not found.")
            return

        success = save_order(customer['id'], order_items)
        if success:
            messagebox.showinfo("Success", "Order placed successfully.")
            order_items.clear()
            refresh_order_summary()
        else:
            messagebox.showerror("Error", "Failed to place order.")

    def search_customers():
        search_text = customer_search_entry.get().lower()
        filtered_customers = [f"{c['first_name']} {c['last_name']}" for c in customers if search_text in f"{c['first_name']} {c['last_name']}".lower()]
        customer_dropdown.configure(values=filtered_customers)

    def search_products():
        search_text = product_search_entry.get().lower()
        filtered_products = [p['name'] for p in products if search_text in p['name'].lower()]
        product_dropdown.configure(values=filtered_products)

    def clear_search_customers():
        customer_search_entry.delete(0, tk.END)
        customer_dropdown.configure(values=[f"{c['first_name']} {c['last_name']}" for c in customers])

    def clear_search_products():
        product_search_entry.delete(0, tk.END)
        product_dropdown.configure(values=[p['name'] for p in products])

    # Load data
    products = get_all_products()
    customers = get_all_customers()

    # HEADER with Back Button
    header = ctk.CTkFrame(window, fg_color="#1D5C83",height=80)
    header.pack(fill="x")

    # Product Icon
    if os.path.exists(os.path.join(ASSETS_PATH, "products_icon.png")):
        img = Image.open(os.path.join(ASSETS_PATH, "products_icon.png"))
        img = ctk.CTkImage(light_image=img, dark_image=img, size=(50, 50))
        ctk.CTkLabel(header, text="", image=img).pack(side="left", padx=20, pady=15)

    # Title Frame
    title_frame = ctk.CTkFrame(header, fg_color="transparent")
    title_frame.pack(side="left", expand=True, padx=10)

    ctk.CTkLabel(title_frame, text="PLACE ORDER", font=("Impact", 28), text_color="white").pack(anchor="center", pady=15)

    # Back Button
    ctk.CTkButton(header, text="Back", command=go_back, width=80, height=35).pack(side="right", padx=20, pady=20)

    # FORM SECTION
    form_frame = ctk.CTkFrame(window, fg_color="white")
    form_frame.pack(padx=20, pady=10, fill="x")

    # Customer
    ctk.CTkLabel(form_frame, text="Customer:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    customer_names = [f"{c['first_name']} {c['last_name']}" for c in customers]
    customer_dropdown = ctk.CTkComboBox(form_frame, values=customer_names, width=200)
    customer_dropdown.grid(row=0, column=1, padx=10, pady=5)

    customer_search_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    customer_search_frame.grid(row=0, column=2, padx=10, pady=5)
    
    customer_search_entry = ctk.CTkEntry(customer_search_frame, width=200)
    customer_search_entry.grid(row=0, column=0, padx=5)
    
    customer_search_btn = ctk.CTkButton(customer_search_frame, text="Search", command=search_customers)
    customer_search_btn.grid(row=0, column=1, padx=5)
    
    customer_clear_btn = ctk.CTkButton(customer_search_frame, text="Clear", command=clear_search_customers)
    customer_clear_btn.grid(row=0, column=2, padx=5)

    # Product
    ctk.CTkLabel(form_frame, text="Product:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    product_names = [p['name'] for p in products]
    product_dropdown = ctk.CTkComboBox(form_frame, values=product_names, width=200)
    product_dropdown.grid(row=1, column=1, padx=10, pady=5)

    product_search_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    product_search_frame.grid(row=1, column=2, padx=10, pady=5)
    
    product_search_entry = ctk.CTkEntry(product_search_frame, width=200)
    product_search_entry.grid(row=0, column=0, padx=5)
    
    product_search_btn = ctk.CTkButton(product_search_frame, text="Search", command=search_products)
    product_search_btn.grid(row=0, column=1, padx=5)
    
    product_clear_btn = ctk.CTkButton(product_search_frame, text="Clear", command=clear_search_products)
    product_clear_btn.grid(row=0, column=2, padx=5)

    # Quantity with Spinbox
    ctk.CTkLabel(form_frame, text="Quantity:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    quantity_container = ctk.CTkFrame(form_frame, fg_color="transparent")
    quantity_container.grid(row=2, column=1, padx=10, pady=5)

    quantity_spinbox = tk.Spinbox(quantity_container, from_=1, to=1000, width=5, font=("Arial", 12))
    quantity_spinbox.pack()

    # Add to Order Button
    add_btn = ctk.CTkButton(form_frame, text="Add to Order", command=add_to_order, fg_color="#22668B", text_color="white")
    add_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Order Summary
    order_summary_frame = ctk.CTkFrame(window, fg_color="#D6EAF8", corner_radius=10)
    order_summary_frame.pack(padx=20, pady=10, fill="both", expand=True)

    total_label = ctk.CTkLabel(order_summary_frame, text="Total: ₹0", font=("Arial", 16, "bold"))
    total_label.pack(pady=10)

    # Final Place Order Button
    place_btn = ctk.CTkButton(window, text="Place Order", command=place_order,
                               fg_color="#28A745", text_color="white", font=("Arial", 16))
    place_btn.pack(pady=10)

    window.mainloop()
