#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from matplotlib import colors
from database.db_config import create_connection


def go_back(current_window, parent_window=None):
    current_window.withdraw()
    if parent_window:
        parent_window.deiconify()
    else:
        from views.admin_view import open_admin_dashboard
        open_admin_dashboard()


def open_reports_view(parent_window=None):
    ctk.set_appearance_mode("light")

    if parent_window:
        parent_window.withdraw()

    window = ctk.CTk()
    window.title("Reports Management")
    window.geometry("1000x750")
    window.configure(bg="#B3E0F2")

    header_frame = ctk.CTkFrame(window, fg_color="#1A4D72", height=100)
    header_frame.pack(fill="x")

    header_label = ctk.CTkLabel(header_frame, text="REPORTS MANAGEMENT", font=("Impact", 28), text_color="white")
    header_label.pack(pady=10)

    back_button = ctk.CTkButton(
        header_frame, text="Back", width=80, fg_color="#1A4D72",
        text_color="white", font=("Arial", 16),
        command=lambda: go_back(window, parent_window)
    )
    back_button.place(relx=0.95, rely=0.1, anchor="ne")

    content_frame = ctk.CTkScrollableFrame(window, fg_color="#7DD6EF")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Month/Year selection
    month_year_frame = ctk.CTkFrame(content_frame, fg_color="#7DD6EF")
    month_year_frame.pack(pady=(10, 5), fill="x", padx=10)

    months = list(calendar.month_name)[1:]
    years = [str(y) for y in range(2020, datetime.now().year + 1)]

    month_label = ctk.CTkLabel(month_year_frame, text="Select Month:", font=("Arial", 14), text_color="#1A4D72")
    month_label.pack(side="left", padx=(0, 10))
    month_menu = ctk.CTkOptionMenu(month_year_frame, values=months, font=("Arial", 14))
    month_menu.set(months[0])
    month_menu.pack(side="left")

    year_label = ctk.CTkLabel(month_year_frame, text="Select Year:", font=("Arial", 14), text_color="#1A4D72")
    year_label.pack(side="left", padx=(20, 10))
    year_menu = ctk.CTkOptionMenu(month_year_frame, values=years, font=("Arial", 14))
    year_menu.set(str(datetime.now().year))
    year_menu.pack(side="left")

    # Banners
    banner_bg = "#E0F0FF"
    label_font = ("Arial", 18, "bold")
    label_color = "#1A4D72"

    summary_frame = ctk.CTkFrame(content_frame, fg_color="transparent")

    sales_label = ctk.CTkLabel(summary_frame, text="", font=label_font,
                               text_color=label_color, bg_color=banner_bg,
                               corner_radius=10, height=50)
    count_label = ctk.CTkLabel(summary_frame, text="", font=label_font,
                               text_color=label_color, bg_color=banner_bg,
                               corner_radius=10, height=50)

    # Chart
    chart_frame = ctk.CTkFrame(content_frame, fg_color="white", height=300)
    chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Low stock section
    low_stock_frame = ctk.CTkFrame(content_frame, fg_color="#FFE4E1")
    low_stock_title = ctk.CTkLabel(low_stock_frame, text="Low Stock Products", font=("Arial", 16, "bold"),
                                   text_color="#B22222")
    low_stock_list = ctk.CTkLabel(low_stock_frame, text="", font=("Arial", 14),
                                  text_color="#B22222", justify="left")

    low_stock_title.pack(pady=(5, 2))
    low_stock_list.pack(pady=(0, 5))

    # --- DB FUNCTIONS ---

    def get_sales_data_by_range(start_date, end_date):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT p.name, SUM(o.quantity) as qty, SUM(o.quantity * p.price) AS total_sales
                FROM orders o
                JOIN products p ON o.product_id = p.id
                WHERE DATE(o.order_date) BETWEEN %s AND %s AND o.status = 'Completed'
                GROUP BY p.name
            """, (start_date, end_date))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return []
        finally:
            cursor.close()
            connection.close()

    def get_low_stock_products(threshold=10):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name, stock_quantity FROM products WHERE stock_quantity < %s ORDER BY stock_quantity", (threshold,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return []
        finally:
            cursor.close()
            connection.close()

    # --- GENERATE REPORT ---

    def generate_report():
        for widget in chart_frame.winfo_children():
            widget.destroy()

        month_name = month_menu.get()
        year = year_menu.get()

        try:
            month_number = list(calendar.month_name).index(month_name)
            start_date = f"{year}-{month_number:02d}-01"
            end_day = calendar.monthrange(int(year), month_number)[1]
            end_date = f"{year}-{month_number:02d}-{end_day:02d}"
        except:
            sales_label.configure(text="Invalid month/year selection.")
            return

        data = get_sales_data_by_range(start_date, end_date)
        if not data:
            sales_label.configure(text="No data found for this selection.")
            return

        data.sort(key=lambda x: x[1], reverse=True)
        products = [row[0] for row in data]
        quantities = [int(row[1]) for row in data]
        sales = [float(row[2]) for row in data]

        total_sales = sum(sales)
        total_products_sold = sum(quantities)

        # Show banners
        sales_label.configure(text=f"Total Sales: ${total_sales:,.2f}")
        count_label.configure(text=f"Total Products Sold: {total_products_sold}")

        summary_frame.pack(fill="x", padx=10, pady=5)
        sales_label.pack(side="left", fill="x", expand=True, padx=(0, 5))
        count_label.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Chart
        top_index = quantities.index(max(quantities))
        bar_colors = ['#0D47A1' if i == top_index else '#90CAF9' for i in range(len(quantities))]

        fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(products, quantities, color=bar_colors)
        ax.set_title(f"Top Products - {month_name} {year}")
        ax.set_ylabel("Quantity Sold")
        ax.set_xlabel("Product")
        ax.tick_params(axis='x', rotation=0)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        chart_frame.selected_date = f"{month_name}_{year}"
        chart_frame.sales_data = data
        chart_frame.low_stock_data = get_low_stock_products()

        # Show low stock section
        if chart_frame.low_stock_data:
            low_stock_text = "\n".join([f"• {name}: {qty} left" for name, qty in chart_frame.low_stock_data])
            low_stock_list.configure(text=low_stock_text)
            low_stock_frame.pack(fill="x", padx=10, pady=10)
        else:
            low_stock_frame.pack_forget()

    # --- EXPORT TO EXCEL ---

    def export_to_excel():
        if not hasattr(chart_frame, "sales_data"):
            messagebox.showwarning("No Data", "Generate report before exporting.")
            return

        date_text = chart_frame.selected_date
        default_filename = f"sales_report_{date_text}.xlsx"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=default_filename,
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Report As"
        )

        if file_path:
            df_sales = pd.DataFrame(chart_frame.sales_data, columns=["Product", "Quantity Sold", "Total Sales"])
            df_low_stock = pd.DataFrame(chart_frame.low_stock_data, columns=["Product", "Stock Quantity"])

            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                # Sales Sheet
                df_sales.to_excel(writer, index=False, sheet_name="Sales Report", startrow=2)
                sheet = writer.sheets["Sales Report"]
                sheet.write(0, 0, f"Sales Report for {date_text.replace('_', ' ')}")
                title_format = writer.book.add_format({'bold': True, 'font_size': 14})
                sheet.set_row(0, None, title_format)

                # Low Stock Sheet
                df_low_stock.to_excel(writer, index=False, sheet_name="Low Stock Products")

            messagebox.showinfo("Success", "Report exported successfully.")

    # Buttons
    button_frame = ctk.CTkFrame(content_frame, fg_color="#7DD6EF")
    button_frame.pack(pady=10, fill="x", padx=10)

    generate_button = ctk.CTkButton(button_frame, text="Generate Report", fg_color="#1A4D72", text_color="white",
                                    font=("Arial", 16), corner_radius=10, command=generate_report)
    generate_button.pack(side="left", padx=20, expand=True)

    export_button = ctk.CTkButton(button_frame, text="Export to Excel", fg_color="#00796B", text_color="white",
                                  font=("Arial", 16), corner_radius=10, command=export_to_excel)
    export_button.pack(side="left", padx=20, expand=True)

    window.mainloop()
