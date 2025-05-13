import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from database.product_model import get_all_products, update_product, hide_product, restore_product

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def edit_products(parent):
    parent.withdraw()  # Accept parent_window to go back
    window = ctk.CTkToplevel()
    window.title("Edit Products")
    window.geometry("1000x600")
    window.configure(bg="#B3E0F2")

    # ---------------- Header ----------------
    header_frame = ctk.CTkFrame(window, fg_color="#1D5C83", height=70)
    header_frame.pack(fill="x")

    header_content = ctk.CTkFrame(header_frame, fg_color="#1D5C83")
    header_content.pack(side="left", padx=20)

    icon_path = os.path.join(ASSETS_PATH, "products_icon.png")
    if os.path.exists(icon_path):
        try:
            icon_image = Image.open(icon_path).resize((70, 70), Image.Resampling.LANCZOS)
            product_icon = CTkImage(light_image=icon_image, size=(70, 70))
            icon_label = ctk.CTkLabel(header_content, image=product_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Error loading image:", e)

    header_label = ctk.CTkLabel(header_content, text="EDIT PRODUCTS", font=("Impact", 24), text_color="white")
    header_label.pack(side="left", pady=10)

    def go_back():
        window.destroy()
        parent.deiconify()

    back_button = ctk.CTkButton(
        header_frame,
        text="← Back",
        width=80,
        fg_color="#1D5C83",
        hover_color="#17496F",
        text_color="white",
        command=go_back
    )
    back_button.pack(side="right", padx=20, pady=10)

    # ---------------- Search Section ----------------
    search_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    search_frame.pack(fill="x", padx=20, pady=(5, 0))

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search by product name", textvariable=search_var)
    search_entry.pack(side="left", padx=10)

    def filter_products():
        query = search_var.get().strip().lower()
        if not query:
            refresh_table()
        else:
            all_products = get_all_products(include_hidden=True)
            filtered = [p for p in all_products if query in p["name"].lower()]
            refresh_table(filtered)

    def clear_search():
        search_var.set("")
        refresh_table()

    search_button = ctk.CTkButton(search_frame, text="Search", command=filter_products, fg_color="#1D5C83", text_color="white")
    search_button.pack(side="left", padx=5)

    clear_button = ctk.CTkButton(search_frame, text="Clear", command=clear_search, fg_color="#1D5C83", text_color="white")
    clear_button.pack(side="left", padx=5)

    # ---------------- Product Table ----------------
    table_container = ctk.CTkScrollableFrame(window, fg_color="#B3E0F2")
    table_container.pack(fill="both", expand=True, padx=20, pady=20)

    headers = ["Product ID", "Name", "Price", "Stock", "Edit", "Hide", "Restore"]
    column_widths = [120, 250, 150, 120, 80, 80, 80]

    def refresh_table(products=None):
        for widget in table_container.winfo_children():
            widget.destroy()

        for col, (header, width) in enumerate(zip(headers, column_widths)):
            label = ctk.CTkLabel(
                table_container, text=header, font=("Arial", 14, "bold"),
                text_color="white", fg_color="#1F4E78", width=width
            )
            label.grid(row=0, column=col, padx=5, pady=5)

        products = products if products is not None else get_all_products(include_hidden=True)

        if not products:
            messagebox.showinfo("No Products", "No products found in the database.")
            return

        for row, product in enumerate(products, start=1):
            product_id = product['id']
            name = product['name']
            price = product['price']
            stock = product['stock_quantity']
            is_hidden = product['is_hidden']

            values = [product_id, name, price, stock]

            for col, (value, width) in enumerate(zip(values, column_widths)):
                label = ctk.CTkLabel(
                    table_container, text=str(value), font=("Arial", 12),
                    text_color="black", fg_color="white", width=width
                )
                label.grid(row=row, column=col, padx=5, pady=5)

            if is_hidden == 0:
                ctk.CTkButton(
                    table_container, text="✏️ Edit", width=column_widths[4], text_color="black",
                    fg_color="grey", hover_color="#555",
                    command=lambda p=product: edit_product_popup(p)
                ).grid(row=row, column=4, padx=5, pady=5)

                ctk.CTkButton(
                    table_container, text="🔒 Hide", width=column_widths[5], text_color="black",
                    fg_color="grey", hover_color="#555",
                    command=lambda p=product: hide_product_action(p)
                ).grid(row=row, column=5, padx=5, pady=5)

            if is_hidden == 1:
                ctk.CTkButton(
                    table_container, text="🔓 Restore", width=column_widths[6], text_color="black",
                    fg_color="grey", hover_color="#555",
                    command=lambda p=product: restore_product_action(p)
                ).grid(row=row, column=6, padx=5, pady=5)

    def edit_product_popup(product):
        edit_window = ctk.CTkToplevel(window)
        edit_window.title("Edit Product")
        edit_window.geometry("400x320")
        edit_window.configure(bg="#E3F2FD")

        ctk.CTkLabel(edit_window, text="Edit Product", font=("Arial", 18, "bold")).pack(pady=(10, 5))

        ctk.CTkLabel(edit_window, text="Product", font=("Arial", 14)).pack(anchor="w", padx=20)
        name_entry = ctk.CTkEntry(edit_window, placeholder_text="Product Name")
        name_entry.insert(0, product['name'])
        name_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(edit_window, text="Price", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 0))
        price_entry = ctk.CTkEntry(edit_window, placeholder_text="Price")
        price_entry.insert(0, str(product['price']))
        price_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(edit_window, text="Stock", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 0))
        stock_entry = ctk.CTkEntry(edit_window, placeholder_text="Stock Quantity")
        stock_entry.insert(0, str(product['stock_quantity']))
        stock_entry.pack(pady=5, padx=20, fill="x")

        def save_changes():
            name = name_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            if not name or not price or not stock:
                messagebox.showwarning("Warning", "Please fill all fields.")
                return

            try:
                updated_product = {
                    'id': product['id'],
                    'name': name,
                    'price': float(price),
                    'stock_quantity': int(stock)
                }
                update_product(updated_product)
                messagebox.showinfo("Success", "Product updated successfully!")
                edit_window.destroy()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product: {e}")

        ctk.CTkButton(edit_window, text="Save", fg_color="#388E3C", command=save_changes).pack(pady=20)

    def hide_product_action(product):
        if messagebox.askyesno("Hide Confirmation", f"Hide product '{product['name']}'?"):
            try:
                hide_product(product['id'])
                messagebox.showinfo("Success", "Product hidden successfully!")
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to hide product: {e}")

    def restore_product_action(product):
        if messagebox.askyesno("Restore Confirmation", f"Restore product '{product['name']}'?"):
            try:
                restore_product(product['id'])
                messagebox.showinfo("Success", "Product restored successfully!")
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore product: {e}")

    # Initial load
    refresh_table()

