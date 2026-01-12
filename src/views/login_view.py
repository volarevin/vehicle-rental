import tkinter as tk
from tkinter import messagebox
from src.utils.gui_helpers import RoundedFrame, RoundedButton

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#ecf0f1")
        self.pack(fill="both", expand=True)
        
        # Make full screen
        try:
            self.controller.state('zoomed')
        except:
            self.controller.attributes('-fullscreen', True)

        # Center Card
        self.center_card = RoundedFrame(self, width=400, height=500, corner_radius=20, bg_color="white")
        self.center_card.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame = self.center_card.inner_frame
        
        self.show_login_form()

    def clear_center(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.clear_center()
        
        tk.Label(self.center_frame, text="Vehicle Rental System", font=("Segoe UI", 24, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 30))

        # Username
        tk.Label(self.center_frame, text="Username", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.username_entry = tk.Entry(self.center_frame, width=30, font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.username_entry.pack(pady=(5, 15), ipady=5)

        # Password
        tk.Label(self.center_frame, text="Password", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.password_entry = tk.Entry(self.center_frame, show="*", width=30, font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.password_entry.pack(pady=(5, 20), ipady=5)

        # Login Button
        RoundedButton(self.center_frame, width=280, height=40, corner_radius=20, bg_color="#3498db", fg_color="white", 
                      text="LOGIN", command=self.login).pack(pady=10)
        
        # Register Link
        tk.Button(self.center_frame, text="Create New Account", command=self.show_register_form, 
                 bg="white", fg="#3498db", font=("Segoe UI", 10), relief="flat", cursor="hand2").pack(pady=5)

    def show_register_form(self):
        self.clear_center()
        
        tk.Label(self.center_frame, text="Create Account", font=("Segoe UI", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # First Name
        tk.Label(self.center_frame, text="First Name", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.reg_fname = tk.Entry(self.center_frame, width=30, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_fname.pack(pady=(2, 10), ipady=3)

        # Last Name
        tk.Label(self.center_frame, text="Last Name", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.reg_lname = tk.Entry(self.center_frame, width=30, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_lname.pack(pady=(2, 10), ipady=3)

        # Username
        tk.Label(self.center_frame, text="Username", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.reg_user = tk.Entry(self.center_frame, width=30, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_user.pack(pady=(2, 10), ipady=3)

        # Password
        tk.Label(self.center_frame, text="Password", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        self.reg_pass = tk.Entry(self.center_frame, show="*", width=30, font=("Segoe UI", 11), relief="solid", borderwidth=1)
        self.reg_pass.pack(pady=(2, 20), ipady=3)

        # Register Button
        RoundedButton(self.center_frame, width=280, height=40, corner_radius=20, bg_color="#27ae60", fg_color="white", 
                      text="REGISTER", command=self.register).pack(pady=10)
        
        # Back Link
        tk.Button(self.center_frame, text="Back to Login", command=self.show_login_form, 
                 bg="white", fg="#7f8c8d", font=("Segoe UI", 10), relief="flat", cursor="hand2").pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.controller.authenticate(username, password):
            pass # Controller handles switch
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
