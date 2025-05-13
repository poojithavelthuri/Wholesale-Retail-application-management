import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv
from database.order_model import get_all_orders, update_order_status

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")
STATUS_OPTIONS = ["Pending", "Completed", "Cancelled"]

def update_orderstatus(parent_window=None):
    window = ctk.CTkToplevel()
    window.title("Update Order Status")
    window.geometry("1000x600")
    window.configure(bg="#B3E0F2")

    if parent_window:
        parent_window.iconify()

    # ============ Header ============
    header_frame = ctk.CTkFrame(window, fg_color="#1D5C83", height=70)
    header_frame.pack(fill="x")

    header_content = ctk.CTkFrame(header_frame, fg_color="#1D5C83")
    header_content.pack(side="left", padx=20)

    icon_path = os.path.join(ASSETS_PATH, "orders_icon.png")
    if os.path.exists(icon_path):
        try:
            from PIL import Image
            from customtkinter import CTkImage
            icon_image = Image.open(icon_path).resize((70, 70), Image.Resampling.LANCZOS)
            order_icon = CTkImage(light_image=icon_image, size=(70, 70))
            icon_label = ctk.CTkLabel(header_content, image=order_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Error loading image:", e)

    header_label = ctk.CTkLabel(header_content, text="UPDATE ORDER STATUS", font=("Impact", 24), text_color="white")
    header_label.pack(side="left", pady=10)

    back_button = ctk.CTkButton(
        header_frame,
        text="← Back",
        width=100,
        font=("Arial", 14),
        fg_color="#1D5C83",
        hover_color="#17496F",
        text_color="white",
        command=lambda: go_back(window, parent_window)
    )
    back_button.pack(side="right", padx=20, pady=10)

    # ============ Search/Filter ============
    search_frame = ctk.CTkFrame(window, fg_color="#D6EAF8")
    search_frame.pack(fill="x", padx=20, pady=10)

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by customer or status", textvariable=search_var, width=300)
    search_entry.pack(side="left", padx=10)

    def filter_orders():
        query = search_var.get().lower()
        filtered = [o for o in get_all_orders() if query in o["customer_name"].lower() or query in o["status"].lower()]
        load_orders(filtered)

    def clear_search():
        search_var.set("")
        refresh_data()

    ctk.CTkButton(search_frame, text="Search", fg_color="#1D5C83", text_color="white", command=filter_orders).pack(side="left", padx=5)
    ctk.CTkButton(search_frame, text="Clear", fg_color="#1D5C83", text_color="white", command=clear_search).pack(side="left", padx=5)

    def export_to_csv():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Order ID", "Customer", "Product", "Qty", "Price", "Total", "Status", "Date"])
                    for order in displayed_orders:
                        writer.writerow([
                            order['order_id'],
                            order['customer_name'],
                            order['product_name'],
                            order['quantity'],
                            f"{order['product_price']:.2f}",
                            f"{order['total_amount']:.2f}",
                            order['status'],
                            order['order_date']
                        ])
                messagebox.showinfo("Success", "Orders exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export orders: {e}")

    ctk.CTkButton(search_frame, text="Export to CSV", fg_color="#1D5C83", text_color="white", command=export_to_csv).pack(side="right", padx=10)

    # ============ Orders Display ============
    content_frame = ctk.CTkScrollableFrame(window, fg_color="#B3E0F2")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    displayed_orders = []
    order_widgets = []

    def load_orders(orders):
        nonlocal displayed_orders, order_widgets
        for widget in order_widgets:
            widget.destroy()
        order_widgets = []

        for order in orders:
            frame = ctk.CTkFrame(content_frame, fg_color="white")
            frame.pack(fill="x", pady=5, padx=10)
            order_widgets.append(frame)

            label_frame = ctk.CTkFrame(frame, fg_color="white")
            label_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            fields = [
                ("Order ID", order['order_id']),
                ("Customer", order['customer_name']),
                ("Product", order['product_name']),
                ("Qty", order['quantity']),
                ("Price", f"{order['product_price']:.2f}"),
                ("Total", f"{order['total_amount']:.2f}"),
                ("Status", order['status']),
                ("Date", order['order_date'])
            ]

            for field, value in fields:
                row = ctk.CTkFrame(label_frame, fg_color="white")
                row.pack(fill="x", pady=1)
                label_title = ctk.CTkLabel(row, text=f"{field}:", width=100, anchor="w")
                label_title.pack(side="left")
                label_value = ctk.CTkLabel(row, text=value, anchor="w")
                label_value.pack(side="left")

            update_button = ctk.CTkButton(
                frame,
                text="Edit Status",
                fg_color="#1D5C83",
                text_color="white",
                width=120,
                command=lambda o=order: open_update_window(o)
            )
            update_button.pack(side="right", padx=10, pady=10)

        displayed_orders = orders

    def open_update_window(order):
        order_id = order["order_id"]
        current_status = order["status"]

        update_window = ctk.CTkToplevel(window)
        update_window.title("Update Status")
        update_window.geometry("300x200")

        ctk.CTkLabel(update_window, text=f"Order ID: {order_id}", font=("Arial", 14)).pack(pady=10)

        status_var = ctk.StringVar(value=current_status)
        dropdown = ctk.CTkComboBox(update_window, values=STATUS_OPTIONS, variable=status_var)
        dropdown.pack(pady=10)

        def save_changes():
            new_status = status_var.get()
            if new_status != current_status:
                update_order_status(order_id, new_status)
                messagebox.showinfo("Success", f"Order {order_id} updated to {new_status}")
                update_window.destroy()
                refresh_data()
            else:
                messagebox.showinfo("No Change", "Status is already set to that value.")

        ctk.CTkButton(update_window, text="Save", fg_color="#1D5C83", text_color="white", command=save_changes).pack(pady=10)

    def refresh_data():
        all_orders = get_all_orders()
        load_orders(all_orders)

    refresh_data()
    window.mainloop()

# Helper for back navigation
def go_back(current_window, parent_window=None):
    current_window.destroy()
    if parent_window:
        parent_window.deiconify()
    else:
        from views.admin_view import open_admin_dashboard
        open_admin_dashboard()
