import os
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from database.product_model import get_all_products

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def view_product():
    window = ctk.CTkToplevel()
    window.title("View Products")
    window.geometry("1000x600")
    window.configure(bg="#B3E0F2")

    # ================== Header Section ==================
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
            icon_label.image = product_icon
            icon_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Error loading image:", e)

    header_label = ctk.CTkLabel(header_content, text="VIEW PRODUCTS", font=("Impact", 24), text_color="white")
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
    back_button.pack(side="right", padx=20, pady=10)

    # ================== Search Section ==================
    search_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    search_frame.pack(fill="x", padx=20, pady=(5, 0))

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search by product name", textvariable=search_var)
    search_entry.pack(side="left", padx=10)

    def filter_products():
        query = search_var.get().strip().lower()
        if not query:
            load_products()
        else:
            filtered = [p for p in get_all_products() if query in p["name"].lower()]
            load_products(filtered)

    def clear_search():
        search_var.set("")
        load_products()

    search_button = ctk.CTkButton(search_frame, text="Search", command=filter_products, fg_color="#1D5C83", text_color="white")
    search_button.pack(side="left", padx=5)

    clear_button = ctk.CTkButton(search_frame, text="Clear", command=clear_search, fg_color="#1D5C83", text_color="white")
    clear_button.pack(side="left", padx=5)

    # ================== Scrollable Table Section ==================
    table_frame = ctk.CTkFrame(window, fg_color="#B3E0F2")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = ctk.CTkCanvas(table_frame, bg="#B3E0F2", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(table_frame, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#B3E0F2")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    headers = ["Product ID", "Name", "Price", "Stock"]
    column_widths = [120, 250, 150, 120]

    def load_products(filtered_products=None):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for col, (header, width) in enumerate(zip(headers, column_widths)):
            label = ctk.CTkLabel(
                scrollable_frame, text=header, font=("Arial", 14, "bold"),
                text_color="white", fg_color="#1F4E78", width=width
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        products = filtered_products if filtered_products is not None else get_all_products()

        if not products:
            empty_label = ctk.CTkLabel(scrollable_frame, text="No Products Found", font=("Arial", 14), text_color="#1D5C83")
            empty_label.grid(row=1, column=0, columnspan=len(headers), pady=20)
        else:
            for row, product in enumerate(products, start=1):
                values = [
                    product["id"],
                    product["name"],
                    f"${product['price']:.2f}",
                    product["stock_quantity"]
                ]
                for col, (value, width) in enumerate(zip(values, column_widths)):
                    label = ctk.CTkLabel(
                        scrollable_frame, text=str(value), font=("Arial", 12),
                        text_color="black", fg_color="white", width=width
                    )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

    search_entry.bind("<Return>", lambda e: filter_products())
    load_products()
