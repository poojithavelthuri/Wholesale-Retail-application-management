import os
import csv
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from database.order_model import get_all_orders

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def open_orders_view():
    def load_orders(filtered_orders=None):
        for widget in content_frame.winfo_children()[1:]:
            widget.destroy()

        orders_to_display = filtered_orders if filtered_orders is not None else get_all_orders()

        if not orders_to_display:
            no_data = ctk.CTkLabel(content_frame, text="No Orders Available", font=("Arial", 14), text_color="#1D5C83")
            no_data.pack(pady=20)
        else:
            for order in orders_to_display:
                row_frame = ctk.CTkFrame(content_frame, fg_color="white")
                row_frame.pack(fill="x", padx=10, pady=3)

                values = [
                    order["order_id"],
                    order["customer_name"],
                    order["product_name"],
                    order["quantity"],
                    f"${order['total_amount']:.2f}",
                    order["status"],
                    order["order_date"]
                ]

                for val, width in zip(values, column_widths):
                    val_label = ctk.CTkLabel(row_frame, text=val, font=("Arial", 12), text_color="black", width=width, anchor="w")
                    val_label.pack(side="left", padx=5)

    def search_orders():
        query = search_entry.get().lower().strip()
        if not query:
            return

        filtered = [
            order for order in get_all_orders()
            if query in order["customer_name"].lower()
            or query in order["product_name"].lower()
            or query in order["status"].lower()
        ]
        load_orders(filtered)

    def clear_search():
        search_entry.delete(0, 'end')
        load_orders()

    def export_to_csv():
        orders_to_export = get_all_orders()
        if not orders_to_export:
            messagebox.showinfo("Export", "No orders to export.")
            return

        current_date = datetime.now().strftime("%Y-%m-%d")
        default_filename = f"orders_{current_date}.csv"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv")],
            title="Save Orders As"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Order ID", "Customer", "Product", "Quantity", "Total", "Status", "Date"])
                for order in orders_to_export:
                    writer.writerow([
                        order["order_id"],
                        order["customer_name"],
                        order["product_name"],
                        order["quantity"],
                        f"{order['total_amount']:.2f}",
                        order["status"],
                        order["order_date"]
                    ])
            messagebox.showinfo("Success", f"Orders exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV:\n{e}")

    window = ctk.CTkToplevel()
    window.title("View Orders")
    window.geometry("1300x750")
    window.configure(bg="#B3E0F2")
    window.icon_image_ref = None

    header_frame = ctk.CTkFrame(window, fg_color="#1D5C83", height=70)
    header_frame.pack(fill="x")

    header_content = ctk.CTkFrame(header_frame, fg_color="#1D5C83")
    header_content.pack(side="left", padx=20)

    icon_path = os.path.join(ASSETS_PATH, "orders_icon.png")
    if os.path.exists(icon_path):
        try:
            icon_image = Image.open(icon_path).resize((70, 70), Image.Resampling.LANCZOS)
            orders_icon = CTkImage(light_image=icon_image, size=(70, 70))
            window.icon_image_ref = orders_icon
            icon_label = ctk.CTkLabel(header_content, image=orders_icon, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Error loading image:", e)

    header_label = ctk.CTkLabel(header_content, text="VIEW ORDERS", font=("Impact", 24), text_color="white")
    header_label.pack(side="left", pady=10)

    back_button = ctk.CTkButton(
        header_frame,
        text="← Back",
        width=100,
        font=("Arial", 14),
        fg_color="#1D5C83",
        hover_color="#17496F",
        text_color="white",
        command=window.destroy
    )
    back_button.pack(side="right", padx=20)

    search_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    search_frame.pack(fill="x", padx=20, pady=10)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by customer, product, or status")
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    search_button = ctk.CTkButton(
        search_frame, text="Search",
        fg_color="#1D5C83", hover_color="#17496F",
        text_color="white", width=100,
        command=search_orders
    )
    search_button.pack(side="left", padx=(0, 5))

    clear_button = ctk.CTkButton(
        search_frame, text="Clear",
        fg_color="#1D5C83", hover_color="#17496F",
        text_color="white", width=100,
        command=clear_search
    )
    clear_button.pack(side="left", padx=(0, 5))

    export_button = ctk.CTkButton(
        search_frame, text="Export CSV",
        fg_color="#1D5C83", hover_color="#17496F",
        text_color="white", width=120,
        command=export_to_csv
    )
    export_button.pack(side="left")

    headers = ["Order ID", "Customer", "Product", "Quantity", "Total ($)", "Status", "Date"]
    column_widths = [80, 160, 160, 100, 120, 120, 260]

    content_frame = ctk.CTkScrollableFrame(window, fg_color="#B3E0F2")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    header_row = ctk.CTkFrame(content_frame, fg_color="#1D5C83")
    header_row.pack(fill="x", padx=10, pady=(0, 5))

    for title, width in zip(headers, column_widths):
        lbl = ctk.CTkLabel(header_row, text=title, font=("Arial", 14, "bold"), text_color="white", width=width, anchor="w")
        lbl.pack(side="left", padx=5)

    load_orders()

    window.mainloop()
