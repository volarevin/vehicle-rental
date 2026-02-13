import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from src.controllers.admin_controller import AdminController
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame
from src.utils.image_helper import ImageHelper
import os

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
        RoundedButton(user_info, width=130, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "logout.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # Side Bar
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=280)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.sidebar_content = tk.Frame(self.side_bar, bg="#34495e")
        self.sidebar_content.pack(fill="both", expand=True)

        tk.Frame(self.sidebar_content, bg="#34495e", height=70).pack(fill="x")

        self.sidebar_center = tk.Frame(self.sidebar_content, bg="#34495e")
        self.sidebar_center.pack(fill="x")

        side_header = tk.Frame(self.sidebar_center, bg="#34495e")
        side_header.pack(fill="x", pady=(0, 14))

        logo_img = ImageHelper.load_image(os.path.join(os.path.dirname(__file__), "..", "img", "icons", "logo.png"), (72, 72))
        if logo_img:
            logo_label = tk.Label(side_header, image=logo_img, bg="#34495e")
            logo_label.image = logo_img
            logo_label.pack(pady=(0, 8))

        tk.Label(
            side_header,
            text="Vehicle Rental System",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Segoe UI", 12, "bold")
        ).pack()

        self.sidebar_menu = tk.Frame(self.sidebar_center, bg="#34495e")
        self.sidebar_menu.pack()

        tk.Frame(self.sidebar_content, bg="#34495e").pack(fill="both", expand=True)

        self.create_sidebar_button("Overview", "overview.png", self.show_overview_view)
        self.create_sidebar_button("Reservations", "rental.png", self.show_reservations_view)
        self.create_sidebar_button("Analytics", "analytics.png", self.show_analytics_view)
        self.create_sidebar_button("User Management", "users.png", self.show_users_view)

        # Content Area
        self.content_area = tk.Frame(self.main_container, bg="white")
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def create_sidebar_button(self, text, icon_name, command):
        icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)
        btn = RoundedButton(self.sidebar_menu, width=260, height=50, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command, image_path=icon_path)
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
        monthly_stats = self.controller.get_monthly_overview_stats()
        top_type = self.controller.get_top_vehicle_type_this_month()
        
        container = tk.Frame(self.overview_frame, bg="white")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        header_row = tk.Frame(container, bg="white")
        header_row.pack(fill="x", pady=(0, 12))
        tk.Label(
            header_row,
            text="Operations Snapshot",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")
        RoundedButton(
            header_row,
            width=140,
            height=32,
            corner_radius=10,
            bg_color="#2980b9",
            fg_color="white",
            text="Refresh",
            command=self.show_overview_view,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "analytics.png"),
            icon_size=(18, 18),
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

        cards_frame = tk.Frame(container, bg="white")
        cards_frame.pack(fill="x", pady=(0, 10))

        self.create_stat_card(cards_frame, "Total Earnings", f"₱{stats['total_earnings']:,.2f}", "#27ae60", 0, 0, "total_earnings.png")
        self.create_stat_card(cards_frame, "Active Rentals", str(stats['active_rentals']), "#3498db", 0, 1, "active_rentals.png")
        self.create_stat_card(cards_frame, "Total Users", str(stats['total_users']), "#f39c12", 0, 2, "total_users.png")
        self.create_stat_card(cards_frame, "Total Vehicles", str(stats['total_vehicles']), "#8e44ad", 0, 3, "total_vehicles.png")
        self.create_stat_card(cards_frame, "This Month Revenue", f"₱{monthly_stats['month_revenue']:,.2f}", "#16a085", 1, 0, "analytics.png")
        self.create_stat_card(cards_frame, "This Month Bookings", str(monthly_stats['total_reservations']), "#2980b9", 1, 1, "rental.png")
        self.create_stat_card(cards_frame, "Completed (Month)", str(monthly_stats['completed_count']), "#2ecc71", 1, 2, "complete.png")
        self.create_stat_card(cards_frame, "Avg Ticket", f"₱{monthly_stats['avg_ticket']:,.0f}", "#d35400", 1, 3, "car.png")

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        cards_frame.grid_columnconfigure(3, weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)

        chart_section = tk.Frame(container, bg="white")
        chart_section.pack(fill="x", pady=(4, 0))
        chart_section.grid_rowconfigure(0, weight=1)
        chart_section.grid_columnconfigure(0, weight=1)

        self.draw_monthly_income_chart(chart_section, monthly_stats, top_type)

    def create_stat_card(self, parent, title, value, color, row, col, icon_name):
        card = RoundedFrame(parent, height=78, corner_radius=15, bg_color=color)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        inner_content = tk.Frame(card.inner_frame, bg=color)
        inner_content.pack(fill="both", expand=True, padx=10, pady=8)
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)
            icon_img = ImageHelper.load_image(icon_path, (24, 24))
            if icon_img:
                icon_lbl = tk.Label(inner_content, image=icon_img, bg=color)
                icon_lbl.image = icon_img
                icon_lbl.pack(side="left", padx=(0, 6))
        except Exception:
            pass

        text_content = tk.Frame(inner_content, bg=color)
        text_content.pack(side="left", fill="both")
        
        tk.Label(text_content, text=title, bg=color, fg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(text_content, text=value, bg=color, fg="white", font=("Segoe UI", 12, "bold")).pack(anchor="w")

    def draw_monthly_income_chart(self, parent, monthly_stats, top_type):
        container = RoundedFrame(parent, height=340, bg_color="#ecf0f1", corner_radius=15)
        container.grid(row=0, column=0, sticky="nsew")

        metric_row = tk.Frame(container.inner_frame, bg="#ecf0f1")
        metric_row.pack(fill="x", padx=14, pady=(8, 6))

        revenue_card = RoundedFrame(metric_row, width=170, height=38, corner_radius=10, bg_color="#d1f2eb")
        revenue_card.pack(side="left", padx=(0, 8))
        tk.Label(revenue_card.inner_frame, text="Revenue", bg="#d1f2eb", fg="#117864", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(revenue_card.inner_frame, text=f"₱{monthly_stats['month_revenue']:,.0f}", bg="#d1f2eb", fg="#117864", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        bookings_card = RoundedFrame(metric_row, width=140, height=38, corner_radius=10, bg_color="#d6eaf8")
        bookings_card.pack(side="left", padx=(0, 8))
        tk.Label(bookings_card.inner_frame, text="Bookings", bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(bookings_card.inner_frame, text=str(monthly_stats['total_reservations']), bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        cancelled_card = RoundedFrame(metric_row, width=140, height=38, corner_radius=10, bg_color="#fadbd8")
        cancelled_card.pack(side="left")
        tk.Label(cancelled_card.inner_frame, text="Cancelled", bg="#fadbd8", fg="#922b21", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(cancelled_card.inner_frame, text=str(monthly_stats['cancelled_count']), bg="#fadbd8", fg="#922b21", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        canvas = tk.Canvas(container.inner_frame, bg="#ecf0f1", highlightthickness=0, height=220)
        canvas.pack(fill="x", padx=14, pady=(0, 8))
        
        data = self.controller.get_monthly_earnings_data()
        
        if not data:
            canvas.create_text(30, 30, text="No earnings activity for this month yet", anchor="nw", fill="#7f8c8d", font=("Segoe UI", 11, "bold"))
            return

        canvas.update_idletasks()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 200:
            w = 660
        if h < 160:
            h = 220

        max_val = max(float(d['total']) for d in data)
        max_val = max_val * 1.1 if max_val > 0 else 1
        chart_left = 36
        chart_right = w - 14
        chart_top = 16
        chart_bottom = h - 40

        for step in range(4):
            y = chart_top + step * ((chart_bottom - chart_top) / 3)
            canvas.create_line(chart_left, y, chart_right, y, fill="#dfe6e9", width=1)

        bar_space = max(1, len(data))
        day_width = (chart_right - chart_left) / bar_space
        bar_width = day_width * 0.64

        for i, item in enumerate(data):
            total = float(item['total'])
            x = chart_left + (i * day_width) + (day_width - bar_width) / 2
            bar_height = (total / max_val) * (chart_bottom - chart_top)
            y1 = chart_bottom - bar_height

            canvas.create_rectangle(x, y1, x + bar_width, chart_bottom, fill="#3498db", outline="")
            canvas.create_text(x + bar_width / 2, chart_bottom + 9, text=item['day'], fill="#34495e", font=("Segoe UI", 7))
            canvas.create_text(x + bar_width / 2, y1 - 7, text=f"{total:,.0f}", fill="#2c3e50", font=("Segoe UI", 7, "bold"))

        canvas.create_text(
            w / 2,
            h - 2,
            text="This Month Analytics",
            anchor="s",
            fill="#2c3e50",
            font=("Segoe UI", 10, "bold")
        )

    def draw_status_overview(self, parent, reservation_status, vehicle_status):
        card = RoundedFrame(parent, bg_color="#ecf0f1", corner_radius=15)
        card.grid(row=1, column=0, sticky="nsew")

        tk.Label(card.inner_frame, text="Operations Health", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=16, pady=(12, 6))

        bars_container = tk.Frame(card.inner_frame, bg="#ecf0f1")
        bars_container.pack(fill="x", padx=16, pady=(0, 12))

        max_status_count = max(1, reservation_status.get("Pending", 0), reservation_status.get("Active", 0), reservation_status.get("Completed", 0), reservation_status.get("Cancelled", 0))

        self.draw_status_bar(bars_container, "Pending", reservation_status.get("Pending", 0), "#f39c12", max_status_count)
        self.draw_status_bar(bars_container, "Active", reservation_status.get("Active", 0), "#3498db", max_status_count)
        self.draw_status_bar(bars_container, "Completed", reservation_status.get("Completed", 0), "#27ae60", max_status_count)
        self.draw_status_bar(bars_container, "Cancelled", reservation_status.get("Cancelled", 0), "#e74c3c", max_status_count)

        footer = tk.Frame(card.inner_frame, bg="#ecf0f1")
        footer.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(
            footer,
            text=f"Vehicle availability: {vehicle_status.get('Available', 0)} available / {sum(vehicle_status.values()) if vehicle_status else 0} total",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        tk.Label(
            footer,
            text=f"Maintenance units: {vehicle_status.get('Maintenance', 0)}",
            bg="#ecf0f1",
            fg="#7f8c8d",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))

    def draw_status_bar(self, parent, label, value, color, max_value):
        row = tk.Frame(parent, bg="#ecf0f1")
        row.pack(fill="x", pady=5)

        tk.Label(row, text=label, bg="#ecf0f1", fg="#2c3e50", width=10, anchor="w", font=("Segoe UI", 10, "bold")).pack(side="left")
        bar_bg = tk.Frame(row, bg="#d5dbdb", height=14)
        bar_bg.pack(side="left", fill="x", expand=True, padx=8)
        bar_bg.pack_propagate(False)

        fill_width = min(1.0, value / max(1, max_value))
        tk.Frame(bar_bg, bg=color, width=max(8, int(240 * fill_width))).pack(side="left", fill="y")
        tk.Label(row, text=str(value), bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="right")

    def draw_recent_activity_list(self, parent):
        container = RoundedFrame(parent, bg_color="#ecf0f1", corner_radius=15)
        container.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        tk.Label(container.inner_frame, text="Recent Activity", bg="#ecf0f1", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=10)
        
        reservations = self.controller.get_recent_reservations(limit=7)
        
        activity_frame = tk.Frame(container.inner_frame, bg="#ecf0f1")
        activity_frame.pack(fill="both", expand=True, padx=10, pady=5)

        if not reservations:
             tk.Label(activity_frame, text="No recent activity", bg="#ecf0f1", fg="#7f8c8d").pack(pady=20)
             return

        for r in reservations:
            row = tk.Frame(activity_frame, bg="#ecf0f1")
            row.pack(fill="x", pady=5)
            
            details = tk.Frame(row, bg="#ecf0f1")
            details.pack(side="left", fill="x", expand=True) # Changed from pack directly to frame management
            
            tk.Label(details, text=f"{r['username']} reserved {r['brand']}", bg="#ecf0f1", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x")
            
            # Format Created At if needed, or pass as is
            tk.Label(details, text=str(r['created_at']), bg="#ecf0f1", fg="#7f8c8d", font=("Segoe UI", 8), anchor="w").pack(fill="x")
            
            tk.Label(row, text=f"₱{r['total_cost']:,.0f}", bg="#ecf0f1", fg="#27ae60", font=("Segoe UI", 10, "bold")).pack(side="right")
            
            ttk.Separator(activity_frame, orient="horizontal").pack(fill="x", pady=2)

    def draw_upcoming_returns(self, parent):
        container = RoundedFrame(parent, bg_color="#ecf0f1", corner_radius=15)
        container.grid(row=1, column=0, sticky="nsew")

        tk.Label(container.inner_frame, text="Upcoming Returns", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 8))

        data = self.controller.get_upcoming_returns(limit=5)
        body = tk.Frame(container.inner_frame, bg="#ecf0f1")
        body.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        if not data:
            tk.Label(body, text="No active rentals due soon", bg="#ecf0f1", fg="#7f8c8d", font=("Segoe UI", 10)).pack(anchor="w", padx=8, pady=8)
            return

        for item in data:
            row = tk.Frame(body, bg="#ecf0f1")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{item['brand']} {item['model']}", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(row, text=str(item['end_date']), bg="#ecf0f1", fg="#c0392b", font=("Segoe UI", 9, "bold")).pack(side="right")

            details = tk.Label(body, text=f"Member: {item['username']}  •  Ref #{item['reservation_id']}", bg="#ecf0f1", fg="#7f8c8d", font=("Segoe UI", 9))
            details.pack(anchor="w", padx=2)
            ttk.Separator(body, orient="horizontal").pack(fill="x", pady=2)

    # --- Reservations View ---
    def show_reservations_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Reservations", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.reservations_frame = tk.Frame(self.content_area, bg="white")
        self.reservations_frame.pack(fill="both", expand=True)
        self.setup_reservations_view()

    def setup_reservations_view(self):
        filter_bar = tk.Frame(self.reservations_frame, bg="white")
        filter_bar.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(filter_bar, text="Search", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.res_search_var = tk.StringVar()
        self.res_search_entry = tk.Entry(filter_bar, textvariable=self.res_search_var, font=("Segoe UI", 10), width=24)
        self.res_search_entry.pack(side="left", padx=(0, 8))

        RoundedButton(filter_bar, width=122, height=32, corner_radius=10, bg_color="#1f618d", fg_color="white", text="Search", command=self.load_reservations, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "search.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 12))

        tk.Label(filter_bar, text="Status", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.res_status_var = tk.StringVar(value="All")
        self.res_status_cb = ttk.Combobox(filter_bar, textvariable=self.res_status_var, values=["All", "Pending", "Active", "Completed", "Cancelled", "Rejected"], state="readonly", width=14)
        self.res_status_cb.pack(side="left", padx=(0, 10))

        RoundedButton(filter_bar, width=130, height=32, corner_radius=10, bg_color="#2980b9", fg_color="white", text="Filter", command=self.load_reservations, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "apply_filter.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        RoundedButton(filter_bar, width=120, height=32, corner_radius=10, bg_color="#7f8c8d", fg_color="white", text="Reset", command=self.reset_reservation_filters, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "reset.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")

        self.reservations_summary = tk.Frame(self.reservations_frame, bg="white")
        self.reservations_summary.pack(fill="x", padx=10, pady=(0, 8))

        self.res_scroll = ScrollableFrame(self.reservations_frame)
        self.res_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_reservations()

    def reset_reservation_filters(self):
        self.res_search_var.set("")
        self.res_status_var.set("All")
        self.load_reservations()

    def get_reservation_status_style(self, status):
        styles = {
            "Pending": {"card": "#fff4db", "pill": "#f39c12", "text": "#7d6608"},
            "Active": {"card": "#eaf4ff", "pill": "#3498db", "text": "#1b4f72"},
            "Completed": {"card": "#eafaf1", "pill": "#27ae60", "text": "#145a32"},
            "Cancelled": {"card": "#fdecea", "pill": "#e74c3c", "text": "#922b21"},
            "Rejected": {"card": "#f0f3f4", "pill": "#7f8c8d", "text": "#2e4053"}
        }
        return styles.get(status, {"card": "#ecf0f1", "pill": "#7f8c8d", "text": "#2c3e50"})

    def load_reservations(self):
        for widget in self.reservations_summary.winfo_children():
            widget.destroy()
        for widget in self.res_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        reservations = self.controller.get_all_reservations()

        search_text = (self.res_search_var.get().strip().lower() if hasattr(self, 'res_search_var') else "")
        status_filter = (self.res_status_var.get() if hasattr(self, 'res_status_var') else "All")

        if search_text:
            reservations = [
                r for r in reservations
                if search_text in str(r['reservation_id']).lower()
                or search_text in str(r['username']).lower()
                or search_text in str(r['brand']).lower()
                or search_text in str(r['model']).lower()
            ]

        if status_filter != "All":
            reservations = [r for r in reservations if r.get('status') == status_filter]

        status_counts = {"Pending": 0, "Active": 0, "Completed": 0, "Cancelled": 0, "Rejected": 0}
        for reservation in reservations:
            status = reservation.get('status', 'Pending')
            status_counts[status] = status_counts.get(status, 0) + 1

        for idx, status in enumerate(["Pending", "Active", "Completed", "Cancelled", "Rejected"]):
            style = self.get_reservation_status_style(status)
            card = RoundedFrame(self.reservations_summary, height=56, corner_radius=12, bg_color=style['card'])
            card.grid(row=0, column=idx, padx=6, pady=4, sticky="ew")
            icon_map = {
                "Pending": "history.png",
                "Active": "active_rentals.png",
                "Completed": "complete.png",
                "Cancelled": "delete.png",
                "Rejected": "list.png"
            }
            row_icon = tk.Frame(card.inner_frame, bg=style['card'])
            row_icon.pack(fill="x")
            icon = ImageHelper.load_image(os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_map.get(status, "list.png")), (16, 16))
            if icon:
                icon_lbl = tk.Label(row_icon, image=icon, bg=style['card'])
                icon_lbl.image = icon
                icon_lbl.pack(side="left", padx=(0, 4))
            tk.Label(row_icon, text=status, bg=style['card'], fg=style['text'], font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(card.inner_frame, text=str(status_counts.get(status, 0)), bg=style['card'], fg=style['pill'], font=("Segoe UI", 14, "bold")).pack(anchor="w")
            self.reservations_summary.grid_columnconfigure(idx, weight=1)
        
        row, col = 0, 0
        columns = 3
        
        for r in reservations:
            style = self.get_reservation_status_style(r['status'])
            card = RoundedFrame(self.res_scroll.scrollable_frame, width=320, height=210, corner_radius=15, bg_color=style['card'])
            card.grid(row=row, column=col, padx=10, pady=10)

            top_row = tk.Frame(card.inner_frame, bg=style['card'])
            top_row.pack(fill="x", pady=(2, 6))
            tk.Label(top_row, text=f"Reservation #{r['reservation_id']}", bg=style['card'], fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(top_row, text=r['status'], bg=style['pill'], fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="right")
            
            body = tk.Frame(card.inner_frame, bg=style['card'])
            body.pack(fill="both", expand=True)

            tk.Label(body, text=f"Member: {r['username']}", bg=style['card'], fg="#2c3e50", font=("Segoe UI", 11)).pack(anchor="w")
            tk.Label(body, text=f"Vehicle: {r['brand']} {r['model']}", bg=style['card'], fg="#2c3e50", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 6))
            tk.Label(body, text=f"Start: {r['start_date']}", bg=style['card'], fg="#34495e", font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(body, text=f"End: {r['end_date']}", bg=style['card'], fg="#34495e", font=("Segoe UI", 10)).pack(anchor="w")
            ttk.Separator(body, orient="horizontal").pack(fill="x", pady=6)
            total_label = tk.Label(body, text=f"Total: ₱{r['total_cost']:,.2f}", bg=style['card'], fg="#1e8449", font=("Segoe UI", 12, "bold"))
            if r.get('status') in ['Cancelled', 'Rejected']:
                strike_font = tkfont.Font(font=("Segoe UI", 12, "bold"))
                strike_font.configure(overstrike=1)
                total_label.configure(font=strike_font, fg="#c0392b")
            total_label.pack(anchor="w")

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
        filters = tk.Frame(self.analytics_frame, bg="white")
        filters.pack(fill="x", padx=12, pady=(0, 10))

        tk.Label(filters, text="Month:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.analytics_month_var = tk.StringVar(value="All")
        month_values = ["All"]
        self.analytics_month_map = {"All": "All"}
        for m in self.controller.get_available_analytics_months():
            month_values.append(m['month_label'])
            self.analytics_month_map[m['month_label']] = m['month_key']

        self.analytics_month_cb = ttk.Combobox(filters, textvariable=self.analytics_month_var, values=month_values, state="readonly", width=18)
        self.analytics_month_cb.pack(side="left", padx=(0, 12))

        tk.Label(filters, text="Status:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.analytics_status_var = tk.StringVar(value="All")
        self.analytics_status_cb = ttk.Combobox(filters, textvariable=self.analytics_status_var, values=["All", "Pending", "Active", "Completed", "Cancelled", "Rejected"], state="readonly", width=14)
        self.analytics_status_cb.pack(side="left", padx=(0, 12))

        RoundedButton(
            filters,
            width=160,
            height=32,
            corner_radius=10,
            bg_color="#2980b9",
            fg_color="white",
            text="Apply Filter",
            command=self.load_analytics_data,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "apply_filter.png"),
            icon_size=(18, 18),
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        summary_frame = tk.Frame(self.analytics_frame, bg="white")
        summary_frame.pack(fill="x", padx=12, pady=(0, 10))
        self.analytics_summary_frame = summary_frame

        chart_grid = tk.Frame(self.analytics_frame, bg="white")
        chart_grid.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        chart_grid.grid_columnconfigure(0, weight=1)
        chart_grid.grid_columnconfigure(1, weight=1)
        chart_grid.grid_rowconfigure(0, weight=1)

        earnings_card = RoundedFrame(chart_grid, bg_color="#ecf0f1", corner_radius=15)
        earnings_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(earnings_card.inner_frame, text="Earnings by Vehicle Type", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(10, 6))
        self.analytics_earnings_canvas = tk.Canvas(earnings_card.inner_frame, bg="#ecf0f1", highlightthickness=0, height=360)
        self.analytics_earnings_canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        status_card = RoundedFrame(chart_grid, bg_color="#ecf0f1", corner_radius=15)
        status_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        tk.Label(status_card.inner_frame, text="Reservation Status Breakdown", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(10, 6))
        self.analytics_status_canvas = tk.Canvas(status_card.inner_frame, bg="#ecf0f1", highlightthickness=0, height=360)
        self.analytics_status_canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.load_analytics_data()

    def create_analytics_stat_card(self, parent, title, value, color, column):
        card = RoundedFrame(parent, height=86, corner_radius=13, bg_color=color)
        card.grid(row=0, column=column, sticky="nsew", padx=6)
        tk.Label(card.inner_frame, text=title, bg=color, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(card.inner_frame, text=value, bg=color, fg="white", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(6, 0))
        parent.grid_columnconfigure(column, weight=1)

    def load_analytics_data(self):
        month_label = self.analytics_month_var.get()
        month_key = self.analytics_month_map.get(month_label, "All")
        status_filter = self.analytics_status_var.get()

        summary = self.controller.get_filtered_analytics_summary(month_key, status_filter)
        earnings_data = self.controller.get_filtered_earnings_by_type(month_key, status_filter)
        status_data = self.controller.get_filtered_reservation_status_breakdown(month_key)

        for widget in self.analytics_summary_frame.winfo_children():
            widget.destroy()

        self.create_analytics_stat_card(self.analytics_summary_frame, "Reservations", str(summary['reservation_count']), "#2980b9", 0)
        self.create_analytics_stat_card(self.analytics_summary_frame, "Revenue", f"₱{summary['total_revenue']:,.0f}", "#16a085", 1)
        self.create_analytics_stat_card(self.analytics_summary_frame, "Avg Ticket", f"₱{summary['avg_revenue']:,.0f}", "#d35400", 2)
        self.create_analytics_stat_card(self.analytics_summary_frame, "Customers", str(summary['customer_count']), "#8e44ad", 3)

        self.draw_analytics_earnings_chart(earnings_data)
        self.draw_analytics_status_chart(status_data)

    def draw_analytics_earnings_chart(self, data):
        canvas = self.analytics_earnings_canvas
        canvas.delete("all")

        if not data:
            canvas.create_text(200, 120, text="No earnings data for selected filter", fill="#7f8c8d", font=("Segoe UI", 11, "bold"))
            return

        canvas.update_idletasks()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 220:
            w = 220
        if h < 220:
            h = 220

        left = 44
        right = w - 14
        top = 28
        bottom = h - 42
        chart_width = max(40, right - left)
        chart_height = max(60, bottom - top)

        max_val = max(float(item['earnings']) for item in data)
        max_val = max(max_val, 1)

        for step in range(4):
            y = top + step * (chart_height / 3)
            canvas.create_line(left, y, right, y, fill="#d5dbdb")

        col_w = chart_width / max(len(data), 1)
        bar_w = max(8, col_w * 0.58)
        show_values = col_w >= 52

        for index, item in enumerate(data):
            val = float(item['earnings'])
            bar_h = (val / max_val) * chart_height
            x = left + (index * col_w) + (col_w - bar_w) / 2
            y = bottom - bar_h
            canvas.create_rectangle(x, y, x + bar_w, bottom, fill="#3498db", outline="")
            canvas.create_text(x + bar_w / 2, bottom + 12, text=item['type'], fill="#34495e", font=("Segoe UI", 9, "bold"))
            if show_values:
                canvas.create_text(x + bar_w / 2, max(top - 8, y - 10), text=f"₱{val:,.0f}", fill="#2c3e50", font=("Segoe UI", 8))

    def draw_analytics_status_chart(self, data):
        canvas = self.analytics_status_canvas
        canvas.delete("all")

        if not data:
            canvas.create_text(200, 120, text="No status data for selected filter", fill="#7f8c8d", font=("Segoe UI", 11, "bold"))
            return

        canvas.update_idletasks()
        w = max(canvas.winfo_width(), 460)
        h = max(canvas.winfo_height(), 300)

        total = sum(int(item['total']) for item in data)
        max_val = max(int(item['total']) for item in data)
        max_val = max(max_val, 1)

        canvas.create_text(26, 10, text=f"Total Reservations: {total}", anchor="w", fill="#2c3e50", font=("Segoe UI", 9, "bold"))

        colors = {
            "Pending": "#f39c12",
            "Active": "#3498db",
            "Completed": "#27ae60",
            "Cancelled": "#e74c3c",
            "Rejected": "#7f8c8d"
        }

        left = 26
        bar_left = 160
        right = w - 26
        top = 24
        row_h = max(32, (h - 42) / max(len(data), 1))

        for i, item in enumerate(data):
            status = item['status']
            value = int(item['total'])
            y = top + i * row_h
            fill = colors.get(status, "#95a5a6")
            bar_w = ((right - bar_left) * value) / max_val

            canvas.create_text(left, y + 10, text=status, anchor="w", fill="#2c3e50", font=("Segoe UI", 10, "bold"))
            canvas.create_text(left + 72, y + 10, text=f"Count: {value}", anchor="w", fill="#5d6d7e", font=("Segoe UI", 9, "bold"))
            canvas.create_rectangle(bar_left, y, bar_left + bar_w, y + 18, fill=fill, outline="")
            pct = (value / total * 100) if total else 0
            canvas.create_text(right, y + 10, text=f"{pct:.0f}%", anchor="e", fill="#2c3e50", font=("Segoe UI", 9, "bold"))

    # --- User Management View ---
    def show_users_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="User Management", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.users_frame = tk.Frame(self.content_area, bg="white")
        self.users_frame.pack(fill="both", expand=True)
        self.setup_users_view()

    def setup_users_view(self):
        form_card = RoundedFrame(self.users_frame, height=190, corner_radius=15, bg_color="#ecf0f1")
        form_card.pack(fill="x", padx=10, pady=(6, 10))

        header = tk.Frame(form_card.inner_frame, bg="#ecf0f1")
        header.pack(fill="x", pady=(4, 10))
        icon = ImageHelper.load_image(os.path.join(os.path.dirname(__file__), "..", "img", "icons", "add.png"), (24, 24))
        if icon:
            lbl_icon = tk.Label(header, image=icon, bg="#ecf0f1")
            lbl_icon.image = icon
            lbl_icon.pack(side="left", padx=(0, 8))
        tk.Label(header, text="Add New User", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(side="left")

        fields = tk.Frame(form_card.inner_frame, bg="#ecf0f1")
        fields.pack(fill="x")

        tk.Label(fields, text="Username", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=6, pady=(0, 4), sticky="w")
        tk.Label(fields, text="Password", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=6, pady=(0, 4), sticky="w")
        tk.Label(fields, text="First Name", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=6, pady=(0, 4), sticky="w")
        tk.Label(fields, text="Last Name", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=6, pady=(0, 4), sticky="w")
        tk.Label(fields, text="Role", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=6, pady=(0, 4), sticky="w")

        self.u_username = tk.Entry(fields, font=("Segoe UI", 10))
        self.u_username.grid(row=1, column=0, padx=6, pady=(0, 8), sticky="ew")
        self.u_password = tk.Entry(fields, show="*", font=("Segoe UI", 10))
        self.u_password.grid(row=1, column=1, padx=6, pady=(0, 8), sticky="ew")
        self.u_fname = tk.Entry(fields, font=("Segoe UI", 10))
        self.u_fname.grid(row=1, column=2, padx=6, pady=(0, 8), sticky="ew")
        self.u_lname = tk.Entry(fields, font=("Segoe UI", 10))
        self.u_lname.grid(row=1, column=3, padx=6, pady=(0, 8), sticky="ew")
        self.u_role = ttk.Combobox(fields, values=["Member", "Receptionist", "Admin"], state="readonly", font=("Segoe UI", 10))
        self.u_role.set("Member")
        self.u_role.grid(row=1, column=4, padx=6, pady=(0, 8), sticky="ew")

        for i in range(5):
            fields.grid_columnconfigure(i, weight=1)

        actions = tk.Frame(form_card.inner_frame, bg="#ecf0f1")
        actions.pack(fill="x")
        RoundedButton(actions, width=160, height=34, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Create User", command=self.add_user, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "create_user.png"), icon_size=(18, 18), font=("Segoe UI", 9, "bold")).pack(side="right")

        user_filter_bar = tk.Frame(self.users_frame, bg="white")
        user_filter_bar.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(user_filter_bar, text="Search", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.user_search_var = tk.StringVar()
        self.user_search_entry = tk.Entry(user_filter_bar, textvariable=self.user_search_var, font=("Segoe UI", 10), width=24)
        self.user_search_entry.pack(side="left", padx=(0, 8))

        RoundedButton(user_filter_bar, width=122, height=32, corner_radius=10, bg_color="#1f618d", fg_color="white", text="Search", command=self.load_users, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "search.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 12))

        tk.Label(user_filter_bar, text="Role", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        self.user_role_filter_var = tk.StringVar(value="All")
        self.user_role_filter_cb = ttk.Combobox(user_filter_bar, textvariable=self.user_role_filter_var, values=["All", "Admin", "Receptionist", "Member"], state="readonly", width=14)
        self.user_role_filter_cb.pack(side="left", padx=(0, 10))

        RoundedButton(user_filter_bar, width=130, height=32, corner_radius=10, bg_color="#2980b9", fg_color="white", text="Filter", command=self.load_users, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "apply_filter.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        RoundedButton(user_filter_bar, width=120, height=32, corner_radius=10, bg_color="#7f8c8d", fg_color="white", text="Reset", command=self.reset_user_filters, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "reset.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")

        # User List
        self.user_scroll = ScrollableFrame(self.users_frame)
        self.user_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users()

    def reset_user_filters(self):
        self.user_search_var.set("")
        self.user_role_filter_var.set("All")
        self.load_users()

    def get_role_style(self, role):
        styles = {
            "Admin": {
                "card": "#f4ecf7",
                "accent": "#8e44ad",
                "icon": "admin.png"
            },
            "Receptionist": {
                "card": "#eafaf1",
                "accent": "#27ae60",
                "icon": "receptionist.png"
            },
            "Member": {
                "card": "#f2f3f4",
                "accent": "#7f8c8d",
                "icon": "user.png"
            }
        }
        return styles.get(role, {"card": "#ecf0f1", "accent": "#7f8c8d", "icon": "users.png"})

    def load_users(self):
        for widget in self.user_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        users = self.controller.get_all_users()

        search_text = (self.user_search_var.get().strip().lower() if hasattr(self, 'user_search_var') else "")
        role_filter = (self.user_role_filter_var.get() if hasattr(self, 'user_role_filter_var') else "All")

        if search_text:
            users = [
                u for u in users
                if search_text in str(u['username']).lower()
                or search_text in str(u['first_name']).lower()
                or search_text in str(u['last_name']).lower()
                or search_text in str(u['user_id']).lower()
            ]

        if role_filter != "All":
            users = [u for u in users if u.get('role') == role_filter]
        
        row, col = 0, 0
        columns = 3
        
        for u in users:
            style = self.get_role_style(u['role'])
            card = RoundedFrame(self.user_scroll.scrollable_frame, width=330, height=220, corner_radius=16, bg_color=style['card'])
            card.grid(row=row, column=col, padx=10, pady=10)

            top = tk.Frame(card.inner_frame, bg=style['card'])
            top.pack(fill="x", pady=(2, 8))

            role_icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", style['icon'])
            role_icon = ImageHelper.load_image(role_icon_path, (24, 24))
            if role_icon:
                icon_lbl = tk.Label(top, image=role_icon, bg=style['card'])
                icon_lbl.image = role_icon
                icon_lbl.pack(side="left", padx=(0, 8))
            tk.Label(top, text=f"ID #{u['user_id']}", bg="#ffffff", fg="#5d6d7e", font=("Segoe UI", 8, "bold"), padx=8, pady=2).pack(side="left")
            tk.Label(top, text=u['role'], bg=style['accent'], fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="right")
            
            tk.Label(card.inner_frame, text=u['username'], bg=style['card'], fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(anchor="w")
            tk.Label(card.inner_frame, text=f"{u['first_name']} {u['last_name']}", bg=style['card'], fg="#34495e", font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 2))
            tk.Label(card.inner_frame, text=f"{u['role']} Account", bg=style['card'], fg=style['accent'], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))
            
            actions = tk.Frame(card.inner_frame, bg=style['card'])
            actions.pack(fill="x", pady=(6, 4))

            RoundedButton(
                actions,
                width=96,
                height=32,
                corner_radius=10,
                bg_color="#8e44ad",
                fg_color="white",
                text="Promote",
                command=lambda uid=u['user_id']: self.promote_user(uid),
                image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "promote.png"),
                icon_size=(14, 14),
                font=("Segoe UI", 8, "bold"),
                text_align="center"
            ).pack(side="left", padx=(0, 6))

            can_demote = not (u['role'] == 'Admin' and u['user_id'] == self.user.user_id)
            demote_bg = "#7f8c8d" if can_demote else "#bdc3c7"
            demote_fg = "white" if can_demote else "#5d6d7e"
            RoundedButton(
                actions,
                width=96,
                height=32,
                corner_radius=10,
                bg_color=demote_bg,
                fg_color=demote_fg,
                text="Demote",
                command=(lambda uid=u['user_id']: self.demote_user(uid)) if can_demote else (lambda: None),
                image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "return.png"),
                icon_size=(14, 14),
                font=("Segoe UI", 8, "bold"),
                text_align="center"
            ).pack(side="left", padx=(0, 6))

            RoundedButton(
                actions,
                width=96,
                height=32,
                corner_radius=10,
                bg_color="#e74c3c",
                fg_color="white",
                text="Delete",
                command=lambda uid=u['user_id']: self.delete_user(uid),
                image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "delete.png"),
                icon_size=(14, 14),
                font=("Segoe UI", 8, "bold"),
                text_align="center"
            ).pack(side="left")

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

    def promote_user(self, user_id):
        if not messagebox.askyesno("Confirm", "Promote this user to the next role?"):
            return

        success, message = self.controller.promote_user(user_id)
        if success:
            messagebox.showinfo("Success", message)
            self.load_users()
        else:
            messagebox.showwarning("Notice", message)

    def demote_user(self, user_id):
        if user_id == self.user.user_id:
            messagebox.showwarning("Notice", "You cannot demote your own admin account")
            return

        if not messagebox.askyesno("Confirm", "Demote this user to the previous role?"):
            return

        success, message = self.controller.demote_user(user_id)
        if success:
            messagebox.showinfo("Success", message)
            self.load_users()
        else:
            messagebox.showwarning("Notice", message)
