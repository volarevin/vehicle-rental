import tkinter as tk
from tkinter import messagebox
import os
from src.utils.gui_helpers import RoundedButton, RoundedFrame, ImageHelper

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#ecf0f1")
        self.pack(fill="both", expand=True)
        
        # Maximize Window
        try:
            self.controller.state('zoomed')
        except:
            self.controller.attributes('-fullscreen', True)
        
        self.create_layout()
        self.bind("<Configure>", self._on_resize)
        self.show_login_form()

    def _on_resize(self, event):
        if event.widget is self:
            self._resize_form_card()

    def _toggle_login_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.login_show_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.login_show_btn.config(text="Show")

    def _toggle_register_password(self):
        if self.reg_pass.cget("show") == "*":
            self.reg_pass.config(show="")
            self.register_show_btn.config(text="Hide")
        else:
            self.reg_pass.config(show="*")
            self.register_show_btn.config(text="Show")

    def _get_icon_path(self, icon_name):
        return os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)

    def create_layout(self):
        self.left_panel = tk.Frame(self, bg="#1f2d3a")
        self.left_panel.place(relx=0, rely=0, relwidth=0.46, relheight=1.0)
        
        self.right_panel = tk.Frame(self, bg="#f5f7fb")
        self.right_panel.place(relx=0.46, rely=0, relwidth=0.54, relheight=1.0)

        branding_wrap = tk.Frame(self.left_panel, bg="#1f2d3a")
        branding_wrap.place(relx=0.5, rely=0.48, anchor="center")

        logo_path = self._get_icon_path("logo.png")
        if os.path.exists(logo_path):
            self.logo_img = ImageHelper.load_image(logo_path, (170, 170))
            tk.Label(branding_wrap, image=self.logo_img, bg="#1f2d3a").pack(pady=(0, 16))
        else:
            tk.Label(branding_wrap, text="[LOGO]", font=("Segoe UI", 22, "bold"), bg="#1f2d3a", fg="white").pack(pady=(0, 16))

        tk.Label(
            branding_wrap,
            text="Vehicle Rental System",
            font=("Segoe UI", 30, "bold"),
            bg="#1f2d3a",
            fg="white"
        ).pack()
        tk.Label(
            branding_wrap,
            text="Manage reservations, users, and analytics in one place.",
            font=("Segoe UI", 12),
            bg="#1f2d3a",
            fg="#cfd8e3"
        ).pack(pady=(10, 22))

        self.form_card = RoundedFrame(self.right_panel, width=480, height=560, corner_radius=20, bg_color="white")
        self.form_card.place(relx=0.5, rely=0.5, anchor="center")

        self.form_container = tk.Frame(self.form_card.inner_frame, bg="white")
        self.form_container.pack(fill="both", expand=True, padx=32, pady=30)

        self.after(0, self._resize_form_card)

    def _resize_form_card(self):
        self.update_idletasks()
        right_width = max(self.right_panel.winfo_width(), 1)
        right_height = max(self.right_panel.winfo_height(), 1)

        target_width = max(360, min(480, right_width - 48))
        target_height = max(430, min(560, right_height - 40))
        self.form_card.configure(width=target_width, height=target_height)

    def clear_right_panel(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.clear_right_panel()

        header = tk.Frame(self.form_container, bg="white")
        header.pack(pady=(0, 18))
        header_icon = ImageHelper.load_image(self._get_icon_path("user.png"), (28, 28))
        if header_icon:
            icon_lbl = tk.Label(header, image=header_icon, bg="white")
            icon_lbl.image = header_icon
            icon_lbl.pack(side="left", padx=(0, 8))
        tk.Label(header, text="Welcome Back", font=("Segoe UI", 30, "bold"), bg="white", fg="#2c3e50").pack(side="left")

        tk.Label(self.form_container, text="Sign in to continue to your dashboard", font=("Segoe UI", 12), bg="white", fg="#7f8c8d", justify="center").pack(pady=(0, 24))

        tk.Label(self.form_container, text="Username", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        self.username_entry = tk.Entry(self.form_container, width=35, font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.username_entry.pack(fill="x", pady=(6, 14), ipady=8)

        tk.Label(self.form_container, text="Password", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        login_pw_row = tk.Frame(self.form_container, bg="white")
        login_pw_row.pack(fill="x", pady=(6, 22))
        self.password_entry = tk.Entry(login_pw_row, show="*", width=35, font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.login_show_btn = tk.Button(login_pw_row, text="Show", command=self._toggle_login_password,
                                        bg="white", fg="#3498db", font=("Segoe UI", 9, "bold"),
                                        relief="flat", cursor="hand2")
        self.login_show_btn.pack(side="left", padx=(8, 0))

        RoundedButton(
            self.form_container,
            width=390,
            height=46,
            corner_radius=22,
            bg_color="#3498db",
            fg_color="white",
            text="Sign In",
            command=self.login,
            image_path=self._get_icon_path("user.png"),
            icon_size=(18, 18),
            font=("Segoe UI", 11, "bold"),
            text_align="center"
        ).pack(pady=(4, 16))

        footer = tk.Frame(self.form_container, bg="white")
        footer.pack()
        tk.Label(footer, text="Don't have an account?", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(side="left")
        tk.Button(footer, text="Create account", command=self.show_register_form,
                  bg="white", fg="#3498db", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2").pack(side="left", padx=5)

        self.username_entry.focus_set()
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda e: self.login())

    def show_register_form(self):
        self.clear_right_panel()

        header = tk.Frame(self.form_container, bg="white")
        header.pack(pady=(0, 16))
        icon = ImageHelper.load_image(self._get_icon_path("create_user.png"), (28, 28))
        if icon:
            icon_lbl = tk.Label(header, image=icon, bg="white")
            icon_lbl.image = icon
            icon_lbl.pack(side="left", padx=(0, 8))
        tk.Label(header, text="Create Account", font=("Segoe UI", 28, "bold"), bg="white", fg="#2c3e50").pack(side="left")

        tk.Label(self.form_container, text="Fill in your details to register", font=("Segoe UI", 11), bg="white", fg="#7f8c8d", justify="center").pack(pady=(0, 14))

        tk.Label(self.form_container, text="First Name", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        self.reg_fname = tk.Entry(self.form_container, width=35, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_fname.pack(fill="x", pady=(4, 10), ipady=6)

        tk.Label(self.form_container, text="Last Name", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        self.reg_lname = tk.Entry(self.form_container, width=35, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_lname.pack(fill="x", pady=(4, 10), ipady=6)

        tk.Label(self.form_container, text="Username", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        self.reg_user = tk.Entry(self.form_container, width=35, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_user.pack(fill="x", pady=(4, 10), ipady=6)

        tk.Label(self.form_container, text="Password", font=("Segoe UI", 10, "bold"), bg="white", fg="#566573", justify="center").pack()
        reg_pw_row = tk.Frame(self.form_container, bg="white")
        reg_pw_row.pack(fill="x", pady=(4, 18))
        self.reg_pass = tk.Entry(reg_pw_row, show="*", width=35, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_pass.pack(side="left", fill="x", expand=True, ipady=6)
        self.register_show_btn = tk.Button(reg_pw_row, text="Show", command=self._toggle_register_password,
                                           bg="white", fg="#27ae60", font=("Segoe UI", 9, "bold"),
                                           relief="flat", cursor="hand2")
        self.register_show_btn.pack(side="left", padx=(8, 0))

        RoundedButton(
            self.form_container,
            width=390,
            height=46,
            corner_radius=22,
            bg_color="#27ae60",
            fg_color="white",
            text="Register",
            command=self.register,
            image_path=self._get_icon_path("create_user.png"),
            icon_size=(18, 18),
            font=("Segoe UI", 11, "bold"),
            text_align="center"
        ).pack(pady=(4, 10))

        tk.Button(self.form_container, text="Back to Login", command=self.show_login_form,
                  bg="white", fg="#7f8c8d", font=("Segoe UI", 10), relief="flat", cursor="hand2").pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.controller.authenticate(username, password):
            pass 
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        fname = self.reg_fname.get()
        lname = self.reg_lname.get()
        user = self.reg_user.get()
        pwd = self.reg_pass.get()

        if not all([fname, lname, user, pwd]):
            messagebox.showerror("Error", "All fields are required")
            return

        success, msg = self.controller.auth_controller.register(user, pwd, fname, lname)
        if success:
            messagebox.showinfo("Success", msg)
            self.show_login_form()
        else:
            messagebox.showerror("Error", msg)
