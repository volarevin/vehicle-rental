import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.admin_controller import AdminController
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame

class AdminDashboard(tk.Frame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        self.controller = AdminController()
        self.pack(fill="both", expand=True)
        
        self.create_layout()
        self.show_overview_view()

    def create_layout(self):
        # Top Bar
        self.top_bar = tk.Frame(self, bg="#2c3e50", height=60)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)

        tk.Label(self.top_bar, text="Admin Dashboard", bg="#2c3e50", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        
        user_info = tk.Frame(self.top_bar, bg="#2c3e50")
        user_info.pack(side="right", padx=20)
        
        tk.Label(user_info, text=f"Admin: {self.user.full_name}", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 12)).pack(side="left", padx=10)
        RoundedButton(user_info, width=80, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # Side Bar
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=200)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.create_sidebar_button("Overview", self.show_overview_view)
        self.create_sidebar_button("Reservations", self.show_reservations_view)
        self.create_sidebar_button("Analytics", self.show_analytics_view)
        self.create_sidebar_button("User Management", self.show_users_view)

        # Content Area
        self.content_area = tk.Frame(self.main_container, bg="white")
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def create_sidebar_button(self, text, command):
        btn = RoundedButton(self.side_bar, width=180, height=40, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command)
        btn.pack(pady=5)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- Overview View ---
    def show_overview_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Overview", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.overview_frame = tk.Frame(self.content_area, bg="white")
        self.overview_frame.pack(fill="both", expand=True)
        self.setup_overview_view()

    def setup_overview_view(self):
        stats = self.controller.get_dashboard_stats()
        
        container = tk.Frame(self.overview_frame, bg="white")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Stat Cards
        self.create_stat_card(container, "Total Earnings", f"₱{stats['total_earnings']:,.2f}", "#27ae60", 0, 0)
        self.create_stat_card(container, "Active Rentals", str(stats['active_rentals']), "#3498db", 0, 1)
        self.create_stat_card(container, "Total Users", str(stats['total_users']), "#f39c12", 0, 2)
        self.create_stat_card(container, "Total Vehicles", str(stats['total_vehicles']), "#8e44ad", 0, 3)

        tk.Button(self.overview_frame, text="Refresh Data", command=self.show_overview_view, bg="#34495e", fg="white", relief="flat", pady=10).pack(pady=20)

    def create_stat_card(self, parent, title, value, color, row, col):
        card = RoundedFrame(parent, width=250, height=150, corner_radius=20, bg_color=color)
        card.grid(row=row, column=col, padx=15, pady=15)
        
        tk.Label(card.inner_frame, text=title, bg=color, fg="white", font=("Segoe UI", 14)).pack(pady=(20, 10))
        tk.Label(card.inner_frame, text=value, bg=color, fg="white", font=("Segoe UI", 24, "bold")).pack()

    # --- Reservations View ---
    def show_reservations_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Reservations", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.reservations_frame = tk.Frame(self.content_area, bg="white")
        self.reservations_frame.pack(fill="both", expand=True)
        self.setup_reservations_view()

    def setup_reservations_view(self):
        self.res_scroll = ScrollableFrame(self.reservations_frame)
        self.res_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_reservations()

    def load_reservations(self):
        for widget in self.res_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        reservations = self.controller.get_all_reservations()
        
        row, col = 0, 0
        columns = 3
        
        for r in reservations:
            card = RoundedFrame(self.res_scroll.scrollable_frame, width=300, height=180, corner_radius=15, bg_color="#ecf0f1")
            card.grid(row=row, column=col, padx=10, pady=10)
            
            # Content
            tk.Label(card.inner_frame, text=f"Res ID: {r['reservation_id']}", bg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"User: {r['username']}", bg="#ecf0f1", font=("Segoe UI", 11)).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"{r['brand']} {r['model']}", bg="#ecf0f1", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
            tk.Label(card.inner_frame, text=f"{r['start_date']} to {r['end_date']}", bg="#ecf0f1", font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"Total: ₱{r['total_cost']:,.2f}", bg="#ecf0f1", font=("Segoe UI", 11, "bold"), fg="#27ae60").pack(anchor="w")
            
            status_color = "#27ae60" if r['status'] == 'Active' else "#7f8c8d"
            tk.Label(card.inner_frame, text=r['status'], bg="#ecf0f1", fg=status_color, font=("Segoe UI", 10, "bold")).pack(anchor="e")

            col += 1
            if col >= columns:
                col = 0
                row += 1

    # --- Analytics View ---
    def show_analytics_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Analytics", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.analytics_frame = tk.Frame(self.content_area, bg="white")
        self.analytics_frame.pack(fill="both", expand=True)
        self.setup_analytics_view()

    def setup_analytics_view(self):
        tk.Label(self.analytics_frame, text="Earnings by Vehicle Type", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)
        
        self.chart_canvas = tk.Canvas(self.analytics_frame, bg="white", height=400)
        self.chart_canvas.pack(fill="x", padx=20)
        
        self.draw_chart()

    def draw_chart(self):
        self.chart_canvas.delete("all")
        data = self.controller.get_earnings_by_type()
        
        if not data:
            self.chart_canvas.create_text(400, 200, text="No data available", font=("Segoe UI", 14))
            return

        # Simple Bar Chart Logic
        max_val = float(max([d['earnings'] for d in data])) if data else 1.0
        c_width = 800
        c_height = 350
        bar_width = 50
        spacing = 40
        start_x = 50
        base_y = 350

        for i, item in enumerate(data):
            val = float(item['earnings'])
            bar_height = (val / max_val) * 300
            
            x0 = start_x + (i * (bar_width + spacing))
            y0 = base_y - bar_height
            x1 = x0 + bar_width
            y1 = base_y
            
            self.chart_canvas.create_rectangle(x0, y0, x1, y1, fill="#3498db", outline="")
            self.chart_canvas.create_text(x0 + bar_width/2, y1 + 15, text=item['type'])
            self.chart_canvas.create_text(x0 + bar_width/2, y0 - 10, text=f"₱{val:,.0f}")

    # --- User Management View ---
    def show_users_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="User Management", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.users_frame = tk.Frame(self.content_area, bg="white")
        self.users_frame.pack(fill="both", expand=True)
        self.setup_users_view()

    def setup_users_view(self):
        # Add User Form
        form_frame = tk.LabelFrame(self.users_frame, text="Add New User", bg="white")
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Username:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.u_username = tk.Entry(form_frame)
        self.u_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.u_password = tk.Entry(form_frame, show="*")
        self.u_password.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="First Name:", bg="white").grid(row=0, column=4, padx=5, pady=5)
        self.u_fname = tk.Entry(form_frame)
        self.u_fname.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(form_frame, text="Last Name:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.u_lname = tk.Entry(form_frame)
        self.u_lname.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Role:", bg="white").grid(row=1, column=2, padx=5, pady=5)
        self.u_role = ttk.Combobox(form_frame, values=["Member", "Receptionist", "Admin"])
        self.u_role.grid(row=1, column=3, padx=5, pady=5)

        RoundedButton(form_frame, width=100, height=30, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Add User", command=self.add_user).grid(row=1, column=4, padx=10, pady=5)

        # User List
        self.user_scroll = ScrollableFrame(self.users_frame)
        self.user_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users()

    def load_users(self):
        for widget in self.user_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        users = self.controller.get_all_users()
        
        row, col = 0, 0
        columns = 3
        
        for u in users:
            card = RoundedFrame(self.user_scroll.scrollable_frame, width=280, height=160, corner_radius=15, bg_color="#ecf0f1")
            card.grid(row=row, column=col, padx=10, pady=10)
            
            tk.Label(card.inner_frame, text=f"ID: {u['user_id']}", bg="#ecf0f1", font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(card.inner_frame, text=u['username'], bg="#ecf0f1", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"{u['first_name']} {u['last_name']}", bg="#ecf0f1", font=("Segoe UI", 11)).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"Role: {u['role']}", bg="#ecf0f1", fg="#2980b9", font=("Segoe UI", 10)).pack(anchor="w", pady=5)
            
            RoundedButton(card.inner_frame, width=80, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", 
                          text="Delete", command=lambda uid=u['user_id']: self.delete_user(uid)).pack(anchor="e", pady=5)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def add_user(self):
        fname = self.u_fname.get().strip()
        lname = self.u_lname.get().strip()
        username = self.u_username.get().strip()
        password = self.u_password.get()
        role = self.u_role.get()
        
        if not fname or not lname:
            messagebox.showerror("Error", "First name and last name are required")
            return
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        try:
            if self.controller.add_user(username, password, fname, lname, role):
                messagebox.showinfo("Success", "User added")
                self.load_users()
                # Clear
                for e in [self.u_username, self.u_password, self.u_fname, self.u_lname]:
                    e.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add user")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_user(self, user_id):
        if not messagebox.askyesno("Confirm", "Delete this user?"):
            return

        if self.controller.delete_user(user_id):
            messagebox.showinfo("Success", "User deleted")
            self.load_users()
