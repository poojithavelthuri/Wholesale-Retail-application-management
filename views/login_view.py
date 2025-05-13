import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from controllers.login_controller import on_login
from views.admin_view import open_admin_dashboard
from views.staff_view import open_staff_dashboard

# Set assets folder path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def open_login_view():
    ctk.set_appearance_mode("light")
    window = ctk.CTk()
    window.title("Login")
    window.geometry("900x600")
    window.configure(bg="#B3E0F2")

    # Main Frame
    main_frame = ctk.CTkFrame(window, fg_color="white")
    main_frame.pack(fill="both", expand=True)

    # Left Frame
    left_frame = ctk.CTkFrame(main_frame, fg_color="white", width=450)
    left_frame.pack(side="left", fill="both", expand=True)

    label_title = ctk.CTkLabel(
        left_frame, text="AK BOSS RETAILERS",
        font=("Impact", 30, "bold"), text_color="#22668B"
    )
    label_title.pack(pady=(20, 10))

    # Background image
    bg_image_path = os.path.join(ASSETS_PATH, "login_background.png")
    if os.path.exists(bg_image_path):
        bg_image = ctk.CTkImage(light_image=Image.open(bg_image_path), size=(400, 400))
        label_image = ctk.CTkLabel(left_frame, image=bg_image, text="")
        label_image.pack(pady=(20, 0))

    # Right Frame
    right_frame = ctk.CTkFrame(main_frame, fg_color="#D6F4FB", width=450)
    right_frame.pack(side="right", fill="both", expand=True)

    # Top: User icon and label
    if os.path.exists(os.path.join(ASSETS_PATH, "user_icon.png")):
        user_icon = ctk.CTkImage(light_image=Image.open(os.path.join(ASSETS_PATH, "user_icon.png")), size=(50, 50))
        label_user_icon = ctk.CTkLabel(right_frame, image=user_icon, text="")
        label_user_icon.grid(row=0, column=0, padx=(10, 5), pady=(20, 5), sticky="w")

    label_login = ctk.CTkLabel(right_frame, text="USER LOGIN", font=("Impact", 20), text_color="#22668B")
    label_login.grid(row=0, column=1, padx=(5, 10), pady=(20, 5), sticky="w")

    # Form Frame (contains inputs)
    form_frame = ctk.CTkFrame(right_frame, fg_color="#D6F4FB")
    form_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Username Label and Entry
    label_username = ctk.CTkLabel(form_frame, text="User Name", font=("Arial", 15), text_color="#22668B")
    label_username.grid(row=0, column=0, sticky="w", pady=(10, 0))
    entry_username = ctk.CTkEntry(form_frame, placeholder_text="Username", width=280, height=40)
    entry_username.grid(row=1, column=0, pady=(5, 15))

    # Password Label and Entry
    label_password = ctk.CTkLabel(form_frame, text="Password", font=("Arial", 15), text_color="#22668B")
    label_password.grid(row=2, column=0, sticky="w", pady=(0, 0))
    entry_password = ctk.CTkEntry(form_frame, placeholder_text="Password", show="*", width=280, height=40)
    entry_password.grid(row=3, column=0, pady=(5, 10))

    # Show Password Checkbox
    show_password_var = ctk.BooleanVar()

    def toggle_password():
        entry_password.configure(show="" if show_password_var.get() else "*")

    show_password_checkbox = ctk.CTkCheckBox(
        form_frame, text="Show Password", variable=show_password_var,
        command=toggle_password, font=("Arial", 14), text_color="#22668B"
    )
    show_password_checkbox.grid(row=4, column=0, sticky="w", pady=(0, 15))

    # Login Function
    def login():
        username = entry_username.get()
        password = entry_password.get()
        user, role = on_login(username, password)

        if user:
            window.destroy()
            if role == "Admin":
                open_admin_dashboard()
            elif role == "Staff":
                open_staff_dashboard()
            else:
                messagebox.showerror("Invalid Role", "The user role is not recognized.")
        else:
            messagebox.showerror("Invalid Credentials", "The username or password is incorrect.")

    # Login Button
    btn_login = ctk.CTkButton(
        form_frame, text="LOGIN", command=login,
        fg_color="#22668B", font=("Impact", 15),
        text_color="white", corner_radius=25,
        width=150, height=40
    )
    btn_login.grid(row=5, column=0, pady=10)

    # Back Button
    def go_back():
        window.destroy()
        from views.homepage import open_home_page
        open_home_page()

    back_button = ctk.CTkButton(
        right_frame, text="← Back", text_color="#003366",
        font=("Arial", 15), fg_color="transparent", command=go_back
    )
    # Fix: Adjust placement using x, y instead of padx, pady
    back_button.place(relx=1.0, rely=0.05, anchor="ne", x=-10, y=10)

    window.mainloop()
