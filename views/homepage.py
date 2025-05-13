import customtkinter as ctk
from PIL import Image
import os
from views.login_view import open_login_view

# Set assets folder path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../assets")

def open_home_page():
    ctk.set_appearance_mode("light")
    window = ctk.CTk()
    window.title("AK Boss Retailers - Home")
    window.geometry("900x600")
    window.configure(bg="#B3E0F2")

    # Main Frame
    main_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=15)
    main_frame.pack(padx=60, pady=40, fill="both", expand=True)

    # Header
    title = ctk.CTkLabel(main_frame, text="AK BOSS RETAILERS", font=("Impact", 36, "bold"), text_color="#22668B")
    title.pack(pady=(30, 5))

    tagline = ctk.CTkLabel(main_frame, text="Smart Retail Solutions Made Simple", font=("Arial", 18), text_color="#555555")
    tagline.pack(pady=(0, 15))

    # Image (smaller size)
    homepage_icon_path = os.path.join(ASSETS_PATH, "homepage_icon.png")
    if os.path.exists(homepage_icon_path):
        homepage_icon = ctk.CTkImage(light_image=Image.open(homepage_icon_path), size=(250, 250))
        label_image = ctk.CTkLabel(main_frame, image=homepage_icon, text="")
        label_image.pack(pady=(5, 10))

    # Login Button
    btn_login = ctk.CTkButton(
        main_frame,
        text="LOGIN",
        command=lambda: [window.destroy(), open_login_view()],
        fg_color="#22668B",
        hover_color="#1B4B6E",
        font=("Arial", 20, "bold"),
        text_color="white",
        corner_radius=25,
        width=180,
        height=45
    )
    btn_login.pack(pady=(10, 20))

    # Footer
    footer = ctk.CTkLabel(
        main_frame,
        text="© 2025 AK Boss Retailers. All rights reserved.",
        font=("Arial", 12),
        text_color="#888888"
    )
    footer.pack(side="bottom", pady=10)

    window.mainloop()
