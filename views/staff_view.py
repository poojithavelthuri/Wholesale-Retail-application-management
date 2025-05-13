import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

from views.orders_view import open_orders_view
from views.customers_view import open_customers_view
from views.view_products import view_product
from views.place_order_view import open_place_order
from views.edit_customers import edit_customer
from views.staff_reports_view import open_reports_view

# Set assets path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def open_staff_dashboard():
    ctk.set_appearance_mode("light")
    window = ctk.CTk()
    window.title("Staff Dashboard")
    window.geometry("900x600")

    # === Main frame ===
    main_frame = ctk.CTkFrame(window, fg_color="white")
    main_frame.pack(fill="both", expand=True)

    # === Sidebar ===
    sidebar = ctk.CTkFrame(main_frame, fg_color="#22668B", width=200)
    sidebar.pack(side="left", fill="y")

    staff_icon_path = os.path.join(ASSETS_PATH, "staff_icon.png")
    staff_icon = ctk.CTkImage(light_image=Image.open(staff_icon_path), size=(50, 50)) if os.path.exists(staff_icon_path) else None

    label_staff = ctk.CTkLabel(sidebar, text="STAFF", font=("Impact", 24), text_color="white", image=staff_icon, compound="left")
    label_staff.pack(pady=(20, 10))

    menu_items = [
        ("Orders", "orders_icon.png"),
        ("Customers", "customers_icon.png"),
        ("Products", "products_icon.png"),
        ("Reports", "reports_icon.png")
    ]

    for btn_text, icon_name in menu_items:
        icon_path = os.path.join(ASSETS_PATH, icon_name)
        icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50)) if os.path.exists(icon_path) else None

        ctk.CTkLabel(sidebar, text=btn_text, image=icon, compound="left", fg_color="#22668B", font=("Impact", 18), text_color="white").pack(pady=10, padx=10, fill="x")

    # === Sign Out Button ===
    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            window.destroy()

    sign_out_btn = ctk.CTkButton(
        sidebar, text="Sign Out", fg_color="#E74C3C", hover_color="#C0392B",
        text_color="white", font=("Arial", 14), corner_radius=10, command=sign_out
    )
    sign_out_btn.pack(side="bottom", pady=20, padx=10, fill="x")

    # === Header ===
    header = ctk.CTkFrame(main_frame, fg_color="#54C2E7", height=80)
    header.pack(fill="x")

    # === Back Button ===
    back_button = ctk.CTkButton(
        header, text="Back", fg_color="#22668B", text_color="white",
        font=("Impact", 18), command=lambda: go_back(window)
    )
    back_button.pack(side="right", padx=20, pady=20)

    label_dashboard = ctk.CTkLabel(header, text="STAFF DASHBOARD", font=("Impact", 28), text_color="#1B3A57")
    label_dashboard.pack(pady=20)

    # === Content Area ===
    content_frame = ctk.CTkFrame(main_frame, fg_color="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    sections = [
        ("Orders Management", [("View Orders", open_orders_view), ("Place Order", open_place_order)], "orders_icon.png"),
        ("Customer Management", [("View Customers", open_customers_view), ("Edit Customers", edit_customer)], "customers_icon.png"),
        ("Product Management", [("View Products", view_product)], "products_icon.png"),
        ("Reports", [("Generate Invoice", open_reports_view)], "reports_icon.png")
    ]

    row_val, col_val = 0, 0
    for section, btns, icon_name in sections:
        frame = ctk.CTkFrame(content_frame, fg_color="#D6EAF8", corner_radius=10)
        frame.grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")

        icon_path = os.path.join(ASSETS_PATH, icon_name)
        icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(60, 60)) if os.path.exists(icon_path) else None

        label = ctk.CTkLabel(frame, text=section, font=("Impact", 20), text_color="#1B3A57", image=icon, compound="top")
        label.pack(pady=(10, 5))

        for btn_text, command in btns:
            btn = ctk.CTkButton(
                frame, text=btn_text, fg_color="#22668B", text_color="white", font=("Arial", 14), corner_radius=10,
                command=command if command else lambda: messagebox.showinfo("Info", f"{btn_text} clicked")
            )
            btn.pack(pady=5, padx=10, fill="x")

        col_val += 1
        if col_val > 1:
            col_val = 0
            row_val += 1

    content_frame.grid_rowconfigure(row_val, weight=1)
    content_frame.grid_columnconfigure(col_val, weight=1)

    window.mainloop()

# === Helper function for going back ===
def go_back(window):
    window.destroy()
    from views.login_view import open_login_view
    open_login_view()
