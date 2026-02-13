import sys
import os

# Add project root to path so 'src' module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from src.controllers.auth_controller import AuthController
from src.views.login_view import LoginView
from src.views.member_dashboard import MemberDashboard
from src.views.receptionist_dashboard import ReceptionistDashboard
from src.views.admin_dashboard import AdminDashboard

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vehicle Rental System")
        self._configure_window_size()
        
        self.auth_controller = AuthController()
        self.current_user = None
        
        self.show_login()

    def _configure_window_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = min(1600, int(screen_width * 0.92))
        window_height = min(950, int(screen_height * 0.90))

        pos_x = max((screen_width - window_width) // 2, 0)
        pos_y = max((screen_height - window_height) // 2, 0)

        self.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        min_width = min(1024, max(880, screen_width - 80))
        min_height = min(620, max(560, screen_height - 80))
        self.minsize(min_width, min_height)

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
        elif self.current_user.role == "Receptionist":
            ReceptionistDashboard(self, self.current_user, self.logout)

    def logout(self):
        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        app.destroy()
        sys.exit(0)
