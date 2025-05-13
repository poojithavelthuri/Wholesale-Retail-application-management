import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime
from database.db_config import create_connection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")
invoice_display = {"label": None, "text": "", "order_id": ""}

def open_reports_view(parent_window=None):
    ctk.set_appearance_mode("light")

    if parent_window:
        parent_window.iconify()

    window = ctk.CTk()
    window.title("GENERATE INVOICE")
    window.geometry("960x700")
    window.configure(bg="white")

    # ---------- Header ----------
    header_frame = ctk.CTkFrame(window, fg_color="#22668B", height=60)
    header_frame.pack(fill="x")

    header_label = ctk.CTkLabel(
        header_frame, text="REPORTS MANAGEMENT",
        font=("Impact", 24), text_color="white"
    )
    header_label.pack(side="left", padx=20)

    back_button = ctk.CTkButton(
        header_frame, text="Back", width=80, fg_color="#22668B",
        text_color="white", font=("Arial", 16),
        command=lambda: go_back(window, parent_window)
    )
    back_button.pack(side="right", padx=10, pady=10)

    # ---------- Banner Summary ----------
    def fetch_order_counts():
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
            results = cursor.fetchall()
            summary = {"Pending": 0, "Completed": 0, "Cancelled": 0}
            for status, count in results:
                summary[status.capitalize()] = count
            return summary
        except:
            return {"Pending": 0, "Completed": 0, "Cancelled": 0}
        finally:
            cursor.close()
            conn.close()

    summary = fetch_order_counts()
    banner_frame = ctk.CTkFrame(window, fg_color="white")
    banner_frame.pack(fill="x", padx=20, pady=10)

    def create_banner_item(parent, label, count, color):
        item_frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=12, height=60)
        item_frame.pack(side="left", expand=True, fill="x", padx=10, pady=10)

        label_widget = ctk.CTkLabel(item_frame, text=f"{label} Orders", font=("Arial", 14, "bold"), text_color="white")
        count_widget = ctk.CTkLabel(item_frame, text=str(count), font=("Arial", 16), text_color="white")

        label_widget.pack(side="left", fill="x", expand=True, padx=(15, 5))
        count_widget.pack(side="right", fill="x", expand=True, padx=(5, 15))

    create_banner_item(banner_frame, "Pending", summary["Pending"], "#FFA500")
    create_banner_item(banner_frame, "Completed", summary["Completed"], "#4CAF50")
    create_banner_item(banner_frame, "Cancelled", summary["Cancelled"], "#F44336")

    # ---------- Main Content ----------
    content_frame = ctk.CTkScrollableFrame(window, fg_color="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Side-by-side input rows
    customer_row = ctk.CTkFrame(content_frame, fg_color="white")
    customer_row.pack(fill="x", padx=10, pady=(10, 5))
    customer_name_label = ctk.CTkLabel(customer_row, text="Enter Customer Name", font=("Arial", 14), text_color="#22668B", width=180)
    customer_name_label.pack(side="left", padx=5)
    customer_name_entry = ctk.CTkEntry(customer_row, font=("Arial", 14))
    customer_name_entry.pack(side="left", fill="x", expand=True, padx=5)

    order_id_row = ctk.CTkFrame(content_frame, fg_color="white")
    order_id_row.pack(fill="x", padx=10, pady=(5, 10))
    order_id_label = ctk.CTkLabel(order_id_row, text="Enter Order ID", font=("Arial", 14), text_color="#22668B", width=180)
    order_id_label.pack(side="left", padx=5)
    order_id_entry = ctk.CTkEntry(order_id_row, font=("Arial", 14))
    order_id_entry.pack(side="left", fill="x", expand=True, padx=5)

    selected_order_var = ctk.StringVar()
    order_data_dict = {}

    def show_selected_invoice(order_id):
        if not order_id or order_id not in order_data_dict:
            return

        order = order_data_dict[order_id]
        customer_name = f"{order[1]} {order[2]}"
        email = order[3]
        phone_number = order[4]
        address = f"{order[5]}, {order[6]}, {order[7]}, {order[8]}, {order[9]}"
        product_name = order[10]
        quantity = order[11]
        total_amount = order[12]
        order_status = order[13]
        order_date = order[14]

        single_invoice = f"""
-------------------------------
Invoice for Order ID: {order_id}

Customer Information:
Name: {customer_name}
Email: {email}
Phone: {phone_number}
Address: {address}

Order Information:
Product: {product_name}
Quantity: {quantity}
Total Amount: ${total_amount:,.2f}
Order Status: {order_status}
Order Date: {order_date.strftime('%B %d, %Y')}
-------------------------------\n
"""

        if invoice_display["label"]:
            invoice_display["label"].destroy()

        invoice_label = ctk.CTkLabel(content_frame, text=single_invoice.strip(), font=("Arial", 14), text_color="#22668B", justify="left")
        invoice_label.pack(pady=10)

        invoice_display["label"] = invoice_label
        invoice_display["text"] = single_invoice.strip()
        invoice_display["order_id"] = order_id

    dropdown_menu = ctk.CTkOptionMenu(content_frame, variable=selected_order_var, values=[], command=show_selected_invoice)
    dropdown_menu.pack(pady=5, padx=10)

    def generate_invoice():
        order_id_input = order_id_entry.get().strip()
        customer_name_input = customer_name_entry.get().strip()

        if not order_id_input and not customer_name_input:
            messagebox.showwarning("Input Error", "Please enter either an Order ID or Customer Name.")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            if order_id_input.isdigit():
                cursor.execute(""" 
                    SELECT o.id, c.first_name, c.last_name, c.email, c.phone_number,
                        c.street, c.city, c.state, c.zip_code, c.country,
                        p.name, o.quantity, (o.quantity * p.price), o.status, o.order_date
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    JOIN products p ON o.product_id = p.id
                    WHERE o.id = %s
                """, (order_id_input,))
            elif customer_name_input:
                cursor.execute(""" 
                    SELECT o.id, c.first_name, c.last_name, c.email, c.phone_number,
                        c.street, c.city, c.state, c.zip_code, c.country,
                        p.name, o.quantity, (o.quantity * p.price), o.status, o.order_date
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    JOIN products p ON o.product_id = p.id
                    WHERE c.first_name LIKE %s OR c.last_name LIKE %s
                """, (f"%{customer_name_input}%", f"%{customer_name_input}%"))

            orders = cursor.fetchall()
            if not orders:
                messagebox.showerror("Not Found", f"No matching invoice found for input.")
                return

            order_data_dict.clear()
            dropdown_menu.set("")
            dropdown_menu.configure(values=[])

            for order in orders:
                order_id = str(order[0])
                order_data_dict[order_id] = order

            first_order_id = list(order_data_dict.keys())[0]
            dropdown_menu.configure(values=list(order_data_dict.keys()))
            dropdown_menu.set(first_order_id)
            show_selected_invoice(first_order_id)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def print_invoice_to_file():
        invoice_text = invoice_display.get("text")
        order_id = invoice_display.get("order_id")

        if not invoice_text or not order_id:
            messagebox.showwarning("No Invoice", "No invoice to print. Please generate an invoice first.")
            return

        output_dir = os.path.join(os.path.dirname(__file__), "../invoices")
        os.makedirs(output_dir, exist_ok=True)

        filename = f"invoice_{order_id}.pdf"
        filepath = os.path.join(output_dir, filename)

        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter
            heading = "AK Boss Retailers"
            address = "123 Sample Street, City, Country, 12345"

            c.setFont("Helvetica-Bold", 18)
            c.drawString(50, height - 40, heading)
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 60, address)

            y_position = height - 80
            for line in invoice_text.strip().split("\n"):
                c.setFont("Helvetica", 12)
                c.drawString(50, y_position, line.strip())
                y_position -= 20
                if y_position < 50:
                    c.showPage()
                    y_position = height - 40

            c.save()
            messagebox.showinfo("Success", f"Invoice saved as PDF at '{filepath}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save invoice:\n{e}")

    # ---------- Buttons ----------
    button_frame = ctk.CTkFrame(content_frame)
    button_frame.pack(pady=10, fill="x", padx=10)

    invoice_button = ctk.CTkButton(button_frame, text="Generate Invoice", fg_color="#22668B", text_color="white",
                                   font=("Arial", 16), corner_radius=10, command=generate_invoice)
    invoice_button.pack(side="left", padx=20, expand=True)

    print_button = ctk.CTkButton(button_frame, text="Print Invoice", fg_color="#22668B", text_color="white",
                                 font=("Arial", 16), corner_radius=10, command=print_invoice_to_file)
    print_button.pack(side="left", padx=20, expand=True)

    search_button = ctk.CTkButton(button_frame, text="Search", fg_color="#22668B", text_color="white",
                                  font=("Arial", 16), corner_radius=10, command=generate_invoice)
    search_button.pack(side="left", padx=20, expand=True)

    clear_button = ctk.CTkButton(button_frame, text="Clear", fg_color="#22668B", text_color="white",
                                 font=("Arial", 16), corner_radius=10,
                                 command=lambda: [order_id_entry.delete(0, 'end'), customer_name_entry.delete(0, 'end')])
    clear_button.pack(side="left", padx=20, expand=True)

    window.mainloop()

def go_back(current_window, parent_window=None):
    current_window.destroy()
    if parent_window:
        parent_window.deiconify()
    else:
        from views.admin_view import open_admin_dashboard
        open_admin_dashboard()
