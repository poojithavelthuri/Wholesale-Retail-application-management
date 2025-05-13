#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox

# Views
from views.admin_add_product_view import open_add_product_view
from views.orders_view import open_orders_view
from views.customers_view import open_customers_view
from views.admin_reports_view import open_reports_view
from views.view_products import view_product
from views.edit_products import edit_products
from views.update_orderstatus import update_orderstatus
from views.edit_customers import edit_customer

# Set assets folder path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")


def open_admin_dashboard():
    ctk.set_appearance_mode("light")
    window = ctk.CTk()
    window.title("Admin Dashboard")
    window.geometry("900x600")

    # Main Frame
    main_frame = ctk.CTkFrame(window, fg_color="white")
    main_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(main_frame, fg_color="#22668B", width=200)
    sidebar.pack(side="left", fill="y")

    # Admin Label
    admin_icon_path = os.path.join(ASSETS_PATH, "admin_icon.png")
    admin_icon = ctk.CTkImage(light_image=Image.open(admin_icon_path), size=(50, 50)) if os.path.exists(admin_icon_path) else None

    label_admin = ctk.CTkLabel(
        sidebar, text="ADMIN", font=("Impact", 24),
        text_color="white", image=admin_icon, compound="left"
    )
    label_admin.pack(pady=(20, 10))

    # Sidebar Menu Items
    menu_items = [
        ("Orders", "orders_icon.png", open_orders_view),
        ("Customers", "customers_icon.png", open_customers_view),
        ("Products", "products_icon.png", lambda: open_add_product_view(window)),
        ("Reports", "reports_icon.png", open_reports_view)
    ]

    for btn_text, icon_name, command in menu_items:
        icon_path = os.path.join(ASSETS_PATH, icon_name)
        icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50)) if os.path.exists(icon_path) else None

        ctk.CTkButton(
            sidebar, text=btn_text, image=icon, compound="left",
            fg_color="#22668B", font=("Impact", 18), text_color="white",
            command=command
        ).pack(pady=10, padx=10, fill="x")

    # Sign Out Button
    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            window.destroy()

    ctk.CTkButton(
        sidebar, text="Sign Out", fg_color="#22668B",
        text_color="white", font=("Impact", 18), command=sign_out
    ).pack(side="bottom", pady=20)

    # Header
    header = ctk.CTkFrame(main_frame, fg_color="#54C2E7", height=80)
    header.pack(fill="x")

    # Back Button using lambda (delayed import to prevent circular import)
    back_button = ctk.CTkButton(
        header, text="Back", fg_color="#22668B", text_color="white",
        font=("Impact", 18), command=lambda: go_back(window)
    )
    back_button.pack(side="right", padx=20, pady=20)

    label_dashboard = ctk.CTkLabel(
        header, text="ADMIN DASHBOARD",
        font=("Impact", 28), text_color="#1B3A57"
    )
    label_dashboard.pack(pady=20)

    # Content Sections
    content_frame = ctk.CTkFrame(main_frame, fg_color="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    sections = [
        ("Orders Management", [
            ("View Orders", open_orders_view),
            ("Update Order Status", lambda: update_orderstatus(window))
        ], "orders_icon.png"),

        ("Customer Management", [
            ("View Customers", open_customers_view),
            ("Edit Customers", edit_customer)
        ], "customers_icon.png"),

        ("Product Management", [
            ("Add Products", lambda: open_add_product_view(window)),
            ("View Products", view_product),
            ("Edit Products", lambda: edit_products(window))
        ], "products_icon.png"),

        ("Reports", [
            ("Get Reports", open_reports_view)
        ], "reports_icon.png")
    ]

    row_val, col_val = 0, 0
    for section, btns, icon_name in sections:
        frame = ctk.CTkFrame(content_frame, fg_color="#D6EAF8", corner_radius=10)
        frame.grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")

        icon_path = os.path.join(ASSETS_PATH, icon_name)
        icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(60, 60)) if os.path.exists(icon_path) else None

        label = ctk.CTkLabel(frame, text=section, font=("Impact", 20),
                             text_color="#1B3A57", image=icon, compound="top")
        label.pack(pady=(10, 5))

        for btn_text, command in btns:
            ctk.CTkButton(
                frame, text=btn_text, fg_color="#22668B",
                text_color="white", font=("Arial", 14), corner_radius=10,
                command=command
            ).pack(pady=5, padx=10, fill="x")

        col_val += 1
        if col_val > 1:
            col_val = 0
            row_val += 1

    content_frame.grid_rowconfigure(row_val, weight=1)
    content_frame.grid_columnconfigure(col_val, weight=1)

    window.mainloop()


# Delayed import to avoid circular import issue
def go_back(window):
    window.destroy()
    from views.login_view import open_login_view
    open_login_view()
