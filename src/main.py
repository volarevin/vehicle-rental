import sys
import os

# Add project root to path so 'src' module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from src.controllers.auth_controller import AuthController
from src.views.login_view import LoginView
from src.views.member_dashboard import MemberDashboard
from src.views.staff_dashboard import StaffDashboard
from src.views.admin_dashboard import AdminDashboard

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vehicle Rental System")
        self.geometry("1000x700")
        
        self.auth_controller = AuthController()
        self.current_user = None
        
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginView(self, self)

    def authenticate(self, username, password):
        user = self.auth_controller.login(username, password)
        if user:
            self.current_user = user
            self.show_dashboard()
            return True
        return False

    def show_dashboard(self):
        self.clear_window()
        if self.current_user.role == "Member":
            MemberDashboard(self, self.current_user, self.logout)
        elif self.current_user.role == "Admin":
            AdminDashboard(self, self.current_user, self.logout)
        else:
            StaffDashboard(self, self.current_user, self.logout)

    def logout(self):
        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
