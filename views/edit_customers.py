import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from database.customer_model import get_all_customers, update_customer, add_customer

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def edit_customer():
    window = ctk.CTkToplevel()
    window.title("Edit Customers")
    window.geometry("1000x600")
    window.configure(bg="#B3E0F2")

    # ========== Header ==========
    header_frame = ctk.CTkFrame(window, fg_color="#1D5C83", height=70)
    header_frame.pack(fill="x")

    customers_icon = None
    customers_img_path = os.path.join(ASSETS_PATH, "customers_icon.png")
    if os.path.exists(customers_img_path):
        try:
            customers_img = Image.open(customers_img_path).resize((70, 70), Image.Resampling.LANCZOS)
            customers_icon = CTkImage(light_image=customers_img, size=(70, 70))
        except Exception as e:
            print("Error loading image:", e)

    if customers_icon:
        ctk.CTkLabel(header_frame, image=customers_icon, text="").pack(side="left", padx=10, pady=5)

    ctk.CTkLabel(header_frame, text="EDIT CUSTOMERS", font=("Impact", 26), text_color="white").pack(side="left", padx=10)

    ctk.CTkButton(
        header_frame, text="← Back", width=100, font=("Arial", 14),
        fg_color="#1D5C83", hover_color="#17496F", text_color="white",
        command=window.destroy
    ).pack(side="right", padx=20, pady=10)

    # ========== Search / Filter / Add ==========
    search_frame = ctk.CTkFrame(window, fg_color="#D6EAF8")
    search_frame.pack(fill="x", padx=20, pady=10)

    search_var = ctk.StringVar()
    ctk.CTkEntry(search_frame, placeholder_text="Search by customer name", textvariable=search_var, width=300).pack(side="left", padx=10)

    def filter_customers():
        query = search_var.get().lower()
        all_customers = get_all_customers()
        filtered = [c for c in all_customers if query in c["first_name"].lower() or query in c["last_name"].lower()]
        load_customers(filtered)

    def clear_search():
        search_var.set("")
        refresh_data()

    ctk.CTkButton(search_frame, text="Search", fg_color="#1D5C83", text_color="white", command=filter_customers).pack(side="left", padx=5)
    ctk.CTkButton(search_frame, text="Clear", fg_color="#888", text_color="white", command=clear_search).pack(side="left", padx=(0, 20))

    ctk.CTkButton(
        search_frame, text="Add New Customer", fg_color="#1D5C83",
        text_color="white", width=170, font=("Arial", 14),
        command=lambda: open_add_customer_window(window)
    ).pack(side="left")

    # ========== Customer List ==========
    content_frame = ctk.CTkScrollableFrame(window, fg_color="#B3E0F2")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    customer_widgets = []

    def load_customers(customers):
        nonlocal customer_widgets
        for widget in customer_widgets:
            widget.destroy()
        customer_widgets = []

        if not customers:
            ctk.CTkLabel(content_frame, text="No customers available", font=("Arial", 16), text_color="#1F4E78").pack(pady=20)
            return

        for customer in customers:
            frame = ctk.CTkFrame(content_frame, fg_color="white")
            frame.pack(fill="x", pady=5, padx=10)
            customer_widgets.append(frame)

            label_frame = ctk.CTkFrame(frame, fg_color="white")
            label_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            fields = [
                ("Customer ID", customer['id']),
                ("First Name", customer['first_name']),
                ("Last Name", customer['last_name']),
                ("Email", customer['email']),
                ("Phone Number", customer['phone_number']),
                ("Street", customer['street']),
                ("City", customer['city']),
                ("State", customer['state']),
                ("Zip Code", customer['zip_code']),
                ("Country", customer['country'])
            ]

            entry_vars = {}

            for field, value in fields:
                row = ctk.CTkFrame(label_frame, fg_color="white")
                row.pack(fill="x", pady=1)
                label_title = ctk.CTkLabel(row, text=f"{field}:", width=120, anchor="w", font=("Arial", 12), text_color="black")
                label_title.pack(side="left")
                entry_var = ctk.StringVar(value=value)
                entry_vars[field] = entry_var
                ctk.CTkEntry(row, textvariable=entry_var, width=200).pack(side="left", padx=10)

            ctk.CTkButton(
                frame, text="Edit Customer", fg_color="#1D5C83", text_color="white", width=120,
                command=lambda c=customer, vars=entry_vars: open_update_window(c, vars)
            ).pack(side="right", padx=10, pady=10)

    def refresh_data():
        all_customers = get_all_customers()
        load_customers(all_customers)

    def open_update_window(customer, entry_vars):
        customer_id = customer["id"]

        update_window = ctk.CTkToplevel(window)
        update_window.title("Update Customer")
        update_window.geometry("450x500")

        ctk.CTkLabel(update_window, text=f"Customer ID: {customer_id}", font=("Arial", 14)).pack(pady=10)

        field_names = [
            "First Name", "Last Name", "Email", "Phone Number",
            "Street", "City", "State", "Zip Code", "Country"
        ]

        updated_data = {}
        for field in field_names:
            updated_data[field] = entry_vars[field]

        def save_changes():
            update_customer(
                customer_id,
                updated_data["First Name"].get(),
                updated_data["Last Name"].get(),
                updated_data["Email"].get(),
                updated_data["Phone Number"].get(),
                updated_data["Street"].get(),
                updated_data["City"].get(),
                updated_data["State"].get(),
                updated_data["Zip Code"].get(),
                updated_data["Country"].get()
            )
            messagebox.showinfo("Success", f"Customer {customer_id} updated.")
            update_window.destroy()
            refresh_data()

        ctk.CTkButton(update_window, text="Save Changes", fg_color="#1D5C83", text_color="white", command=save_changes).pack(pady=30)

    def open_add_customer_window(parent_window):
        add_window = ctk.CTkToplevel(parent_window)
        add_window.title("Add New Customer")
        add_window.geometry("500x750")
        add_window.configure(bg="#B3E0F2")

        # Header
        header_frame = ctk.CTkFrame(add_window, fg_color="#1D5C83", height=70)
        header_frame.pack(fill="x")

        ctk.CTkLabel(header_frame, text="ADD CUSTOMER", font=("Impact", 24), text_color="white").pack(side="left", padx=20, pady=10)
        ctk.CTkButton(
            header_frame, text="← Back", width=100, font=("Arial", 14),
            fg_color="#1D5C83", hover_color="#17496F", text_color="white",
            command=add_window.destroy
        ).pack(side="right", padx=20, pady=10)

        # Scrollable form
        form_frame = ctk.CTkScrollableFrame(add_window, fg_color="#B3E0F2", height=650)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Variables
        vars = {
            "First Name": ctk.StringVar(),
            "Last Name": ctk.StringVar(),
            "Email": ctk.StringVar(),
            "Phone Number": ctk.StringVar(),
            "Street": ctk.StringVar(),
            "City": ctk.StringVar(),
            "State": ctk.StringVar(),
            "Zip Code": ctk.StringVar(),
            "Country": ctk.StringVar()
        }

        # Form layout
        for label_text, var in vars.items():
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=8, padx=10)

            ctk.CTkLabel(row, text=label_text + ":", font=("Arial", 13), text_color="black", width=120, anchor="w").grid(row=0, column=0, sticky="w")
            ctk.CTkEntry(row, textvariable=var, width=300).grid(row=0, column=1, padx=(10, 0))

        def save_new_customer():
            add_customer(
                vars["First Name"].get(),
                vars["Last Name"].get(),
                vars["Email"].get(),
                vars["Phone Number"].get(),
                vars["Street"].get(),
                vars["City"].get(),
                vars["State"].get(),
                vars["Zip Code"].get(),
                vars["Country"].get()
            )
            messagebox.showinfo("Success", "New customer added.")
            add_window.destroy()
            refresh_data()

        # Save Button
        save_btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        save_btn_frame.pack(pady=30)
        ctk.CTkButton(
            save_btn_frame, text="Save New Customer",
            fg_color="#1D5C83", text_color="white",
            width=300, height=45, font=("Arial", 16),
            command=save_new_customer
        ).pack()

    refresh_data()
    window.mainloop()
