#BIS698W1700_Group03_Wholesale/Retail application management
#Importing necessary libraries and functions
import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from database.product_model import add_product  # Import database method to add a product

# Define path to assets folder
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

# Function to open the "Add Product" window
def open_add_product_view(parent):
    parent.withdraw()  # Hide the parent window
    window = ctk.CTkToplevel()  # Create a new top-level window
    window.title("Add Product")
    window.geometry("700x500")
    window.configure(bg="#7BD3EE")  # Set background color

    # ---------------- HEADER ----------------
    header_frame = ctk.CTkFrame(window, fg_color="#1D5C83", height=80)
    header_frame.pack(fill="x")

    # Load and display product icon
    product_icon = None
    product_img_path = os.path.join(ASSETS_PATH, "products_icon.png")
    if os.path.exists(product_img_path):
        try:
            product_img = Image.open(product_img_path).resize((70, 70), Image.Resampling.LANCZOS)
            product_icon = CTkImage(light_image=product_img, size=(70, 70))
        except Exception as e:
            print("Error loading image:", e)

    if product_icon:
        img_label = ctk.CTkLabel(header_frame, image=product_icon, text="")
        img_label.image = product_icon  # Keep a reference to prevent garbage collection
        img_label.pack(side="left", padx=20, pady=10)

    # Header text
    header_label = ctk.CTkLabel(header_frame, text="ADD PRODUCT", font=("Impact", 26), text_color="white")
    header_label.pack(side="top", pady=10)

    # Back button to return to parent window
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

    # ---------------- FORM ----------------
    form_frame = ctk.CTkFrame(window, fg_color="#7BD3EE")
    form_frame.pack(fill="both", expand=True, padx=40, pady=30)

    # Configure grid columns for layout
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

    # Labels and Entry fields
    labels = ["Product Name", "Price", "Stock"]
    entries = []

    for i, label_text in enumerate(labels):
        label = ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 16), text_color="#1D5C83")
        label.grid(row=i, column=0, padx=10, pady=15, sticky="e")

        entry = ctk.CTkEntry(form_frame, width=300)
        entry.grid(row=i, column=1, padx=10, pady=15, sticky="w")
        entries.append(entry)

    # ---------------- FUNCTIONALITY ----------------
    def add_product_to_db():
        # Get input from entries
        name, price, stock = [entry.get() for entry in entries]

        # Check for empty fields
        if not name or not price or not stock:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            # Validate numeric values
            price = float(price)
            stock = int(stock)

            # Package data and call database function
            product_data = {
                'name': name,
                'price': price,
                'stock_quantity': stock
            }

            add_product(product_data)  # Insert product into database
            messagebox.showinfo("Success", "Product added successfully.")
            window.destroy()  # Close this window
            parent.deiconify()  # Show the parent window again

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for Price and Stock.")

    # ---------------- ADD BUTTON ----------------
    add_button = ctk.CTkButton(
        window,
        text="Add Product +",
        command=add_product_to_db,
        fg_color="#1D5C83",
        text_color="white",
        font=("Impact", 18),
        width=250,
        height=40
    )
    add_button.pack(pady=20)

    window.mainloop()  # Start event loop for this window
