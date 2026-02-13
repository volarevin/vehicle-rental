import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from src.controllers.rental_controller import RentalController
from src.utils.image_helper import ImageHelper
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame
import tkinter.filedialog as filedialog
import os
import shutil

class ReceptionistDashboard(tk.Frame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        self.rental_controller = RentalController()
        self.current_view = "returns"
        self.current_items = []
        self.pack(fill="both", expand=True)
        
        self.create_layout()
        self.show_returns_view()

    def create_layout(self):
        # Top Bar
        self.top_bar = tk.Frame(self, bg="#2c3e50", height=60)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)

        tk.Label(self.top_bar, text="Receptionist Dashboard", bg="#2c3e50", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        
        user_info = tk.Frame(self.top_bar, bg="#2c3e50")
        user_info.pack(side="right", padx=20)
        
        tk.Label(user_info, text=f"User: {self.user.full_name}", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 12)).pack(side="left", padx=10)
        RoundedButton(user_info, width=130, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "logout.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # 1. Left Sidebar
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=240)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.sidebar_content = tk.Frame(self.side_bar, bg="#34495e")
        self.sidebar_content.pack(fill="both", expand=True)

        tk.Frame(self.sidebar_content, bg="#34495e", height=70).pack(fill="x")

        self.sidebar_center = tk.Frame(self.sidebar_content, bg="#34495e")
        self.sidebar_center.pack(fill="x")

        sidebar_header = tk.Frame(self.sidebar_center, bg="#34495e")
        sidebar_header.pack(fill="x", pady=(0, 14))

        logo_img = ImageHelper.load_image(os.path.join(os.path.dirname(__file__), "..", "img", "icons", "logo.png"), (72, 72))
        if logo_img:
            logo_label = tk.Label(sidebar_header, image=logo_img, bg="#34495e")
            logo_label.image = logo_img
            logo_label.pack(pady=(0, 8))

        tk.Label(
            sidebar_header,
            text="Vehicle Rental System",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Segoe UI", 12, "bold")
        ).pack()

        self.sidebar_menu = tk.Frame(self.sidebar_center, bg="#34495e")
        self.sidebar_menu.pack()

        tk.Frame(self.sidebar_content, bg="#34495e").pack(fill="both", expand=True)

        self.create_sidebar_button("Process Returns", "return.png", self.show_returns_view)
        self.create_sidebar_button("Approve Requests", "list.png", self.show_approvals_view)
        self.create_sidebar_button("Manage Fleet", "car.png", self.show_fleet_view)
        self.create_sidebar_button("Vehicle History", "history.png", self.show_history_view)

        # 2. Middle List Pane (wider to avoid cramped controls)
        self.list_pane = tk.Frame(self.main_container, bg="#f8f9fa", width=640)
        self.list_pane.pack(side="left", fill="both", expand=True)
        self.list_pane.pack_propagate(False)
        
        # Header for List Pane
        self.list_header = tk.Label(self.list_pane, text="Select Item", bg="#f8f9fa", font=("Segoe UI", 14, "bold"), anchor="w", padx=20, pady=12)
        self.list_header.pack(fill="x")

        self.summary_bar = tk.Frame(self.list_pane, bg="#f8f9fa")
        self.summary_bar.pack(fill="x", padx=10, pady=(0, 8))

        self.controls_bar = tk.Frame(self.list_pane, bg="#f8f9fa")
        self.controls_bar.pack(fill="x", padx=10, pady=(0, 8))

        self.controls_top_row = tk.Frame(self.controls_bar, bg="#f8f9fa")
        self.controls_top_row.pack(fill="x", pady=(0, 6))

        self.controls_actions_row = tk.Frame(self.controls_bar, bg="#f8f9fa")
        self.controls_actions_row.pack(fill="x")

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        tk.Label(self.controls_top_row, text="Search", bg="#f8f9fa", fg="#2c3e50", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.search_entry = tk.Entry(self.controls_top_row, textvariable=self.search_var, font=("Segoe UI", 10), width=20)
        self.search_entry.pack(side="left", padx=(0, 6), ipady=4)

        RoundedButton(
            self.controls_top_row,
            width=114,
            height=36,
            corner_radius=10,
            bg_color="#1f618d",
            fg_color="white",
            text="Search",
            command=self.apply_list_filters,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "search.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold"),
            text_align="center"
        ).pack(side="left", padx=(0, 8))

        tk.Label(self.controls_top_row, text="Filter", bg="#f8f9fa", fg="#2c3e50", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.filter_combo = ttk.Combobox(self.controls_top_row, textvariable=self.filter_var, values=["All"], state="readonly", width=16)
        self.filter_combo.pack(side="left", padx=(0, 6))

        RoundedButton(
            self.controls_top_row,
            width=106,
            height=36,
            corner_radius=10,
            bg_color="#2980b9",
            fg_color="white",
            text="Apply",
            command=self.apply_list_filters,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "apply_filter.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold"),
            text_align="center"
        ).pack(side="left", padx=(0, 6))

        RoundedButton(
            self.controls_actions_row,
            width=106,
            height=36,
            corner_radius=10,
            bg_color="#7f8c8d",
            fg_color="white",
            text="Reset",
            command=self.reset_list_filters,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "reset.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold"),
            text_align="center"
        ).pack(side="left", padx=(0, 6))

        RoundedButton(
            self.controls_actions_row,
            width=114,
            height=36,
            corner_radius=10,
            bg_color="#16a085",
            fg_color="white",
            text="Refresh",
            command=self.refresh_current_view,
            image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "analytics.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold"),
            text_align="center"
        ).pack(side="left")

        self.extra_action_holder = tk.Frame(self.controls_actions_row, bg="#f8f9fa")
        self.extra_action_holder.pack(side="right")
        
        self.list_scroll = ScrollableFrame(self.list_pane, bg="#f8f9fa")
        self.list_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # 3. Right Detail Pane (narrower so center pane has more room)
        self.detail_pane = tk.Frame(self.main_container, bg="white", width=420)
        self.detail_pane.pack(side="left", fill="both", expand=True)
        self.detail_pane.pack_propagate(False)
        
        # Container inside detail pane so we can clear it easily
        self.detail_container = tk.Frame(self.detail_pane, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=24, pady=24)

        self.show_placeholder_detail()

    def create_sidebar_button(self, text, icon_name, command):
        # Fix path: go up from src/views/ to src/img/icons
        icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)
        
        btn = RoundedButton(self.sidebar_menu, width=220, height=50, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command, image_path=icon_path)
        btn.pack(pady=5)

    def clear_list(self):
        for widget in self.list_scroll.scrollable_frame.winfo_children():
            widget.destroy()

    def update_summary_cards(self):
        for widget in self.summary_bar.winfo_children():
            widget.destroy()

        stats = self.rental_controller.get_receptionist_dashboard_stats()
        cards = [
            ("Active Rentals", str(stats['active_rentals']), "#3498db", "active_rentals.png"),
            ("Pending Requests", str(stats['pending_requests']), "#f39c12", "list.png"),
            ("Available Fleet", str(stats['available_vehicles']), "#27ae60", "car.png"),
            ("Due Today", str(stats['due_today']), "#e67e22", "return.png")
        ]

        for idx, (title, value, color, icon) in enumerate(cards):
            card = RoundedFrame(self.summary_bar, height=74, corner_radius=10, bg_color="white")
            card.grid(row=0, column=idx, padx=4, sticky="nsew")
            self.summary_bar.grid_columnconfigure(idx, weight=1)

            row = tk.Frame(card.inner_frame, bg="white")
            row.pack(fill="both", expand=True, padx=8, pady=6)
            icon_img = ImageHelper.load_image(os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon), (18, 18))
            if icon_img:
                lbl = tk.Label(row, image=icon_img, bg="white")
                lbl.image = icon_img
                lbl.pack(side="left", padx=(0, 6))

            text_col = tk.Frame(row, bg="white")
            text_col.pack(side="left", fill="both", expand=True)
            tk.Label(text_col, text=title, bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(text_col, text=value, bg="white", fg=color, font=("Segoe UI", 14, "bold")).pack(anchor="w")

    def get_vehicle_status_style(self, status):
        palette = {
            'Available': {'bg': '#eafaf1', 'fg': '#1e8449', 'card': '#ffffff'},
            'Rented': {'bg': '#fdecea', 'fg': '#c0392b', 'card': '#fffdfd'},
            'Maintenance': {'bg': '#f4ecf7', 'fg': '#7d3c98', 'card': '#fdfbff'}
        }
        return palette.get(status, {'bg': '#ecf0f1', 'fg': '#2c3e50', 'card': '#ffffff'})

    def get_reservation_status_style(self, status):
        palette = {
            'Active': {'bg': '#eaf4ff', 'fg': '#1b4f72', 'card': '#ffffff'},
            'Pending': {'bg': '#fff4db', 'fg': '#7d6608', 'card': '#ffffff'},
            'Completed': {'bg': '#eafaf1', 'fg': '#145a32', 'card': '#ffffff'},
            'Cancelled': {'bg': '#fdecea', 'fg': '#922b21', 'card': '#fffdfd'},
            'Rejected': {'bg': '#f0f3f4', 'fg': '#2e4053', 'card': '#ffffff'}
        }
        return palette.get(status, {'bg': '#ecf0f1', 'fg': '#2c3e50', 'card': '#ffffff'})

    def bind_click_recursive(self, widget, callback):
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            self.bind_click_recursive(child, callback)

    def _prompt_reason_dialog(self, title, prompt_text):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.configure(bg="white")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.resizable(False, False)

        w, h = 460, 300
        px = self.winfo_rootx() + max((self.winfo_width() - w) // 2, 0)
        py = self.winfo_rooty() + max((self.winfo_height() - h) // 2, 0)
        dialog.geometry(f"{w}x{h}+{px}+{py}")

        tk.Label(dialog, text=title, bg="white", fg="#2c3e50", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=18, pady=(16, 6))
        tk.Label(dialog, text=prompt_text, bg="white", fg="#5d6d7e", font=("Segoe UI", 10), wraplength=420, justify="left").pack(anchor="w", padx=18, pady=(0, 10))

        text_box = tk.Text(dialog, height=7, width=52, font=("Segoe UI", 10), bd=1, relief="solid")
        text_box.pack(padx=18, pady=(0, 14), fill="x")
        text_box.focus_set()

        result = {"value": None}

        def submit():
            reason = text_box.get("1.0", "end").strip()
            if not reason:
                messagebox.showwarning("Notice", "Reason is required", parent=dialog)
                return
            result["value"] = reason
            dialog.destroy()

        def cancel():
            dialog.destroy()

        buttons = tk.Frame(dialog, bg="white")
        buttons.pack(fill="x", padx=18, pady=(0, 16))
        RoundedButton(buttons, width=106, height=36, corner_radius=10, bg_color="#7f8c8d", fg_color="white", text="Cancel", command=cancel, font=("Segoe UI", 9, "bold"), text_align="center").pack(side="right")
        RoundedButton(buttons, width=134, height=36, corner_radius=10, bg_color="#1f618d", fg_color="white", text="Submit Reason", command=submit, font=("Segoe UI", 9, "bold"), text_align="center").pack(side="right", padx=(0, 8))

        dialog.bind("<Escape>", lambda e: cancel())
        dialog.bind("<Return>", lambda e: submit())
        self.wait_window(dialog)
        return result["value"]

    def create_vehicle_rich_list_item(self, vehicle, click_callback):
        style = self.get_vehicle_status_style(vehicle.get('status', 'Available'))
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=700, height=146, corner_radius=12, bg_color=style['card'])
        frame.pack(fill="x", pady=6)

        row = tk.Frame(frame.inner_frame, bg=style['card'])
        row.pack(fill="both", expand=True, padx=12, pady=10)

        img_path = self.get_image_path(vehicle)
        img = ImageHelper.load_image(img_path, size=(132, 88))
        if img:
            lbl = tk.Label(row, image=img, bg=style['card'])
            lbl.image = img
            lbl.pack(side="left", padx=(0, 12))

        body = tk.Frame(row, bg=style['card'])
        body.pack(side="left", fill="both", expand=True)

        top = tk.Frame(body, bg=style['card'])
        top.pack(fill="x")
        tk.Label(top, text=f"{vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 13, "bold"), bg=style['card'], fg="#2c3e50").pack(side="left")
        tk.Label(top, text=vehicle.get('status', 'Unknown'), bg=style['bg'], fg=style['fg'], font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        tk.Label(body, text=f"Plate: {vehicle['license_plate']}  •  Type: {vehicle['type']}  •  Year: {vehicle['year']}", font=("Segoe UI", 10), bg=style['card'], fg="#5d6d7e").pack(anchor="w", pady=(5, 4))

        bottom = tk.Frame(body, bg=style['card'])
        bottom.pack(fill="x", pady=(4, 0))
        tk.Label(bottom, text=f"₱{float(vehicle['daily_rate']):,.0f} / day", bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left")
        tk.Label(bottom, text=f"ID #{vehicle['vehicle_id']}", bg="#f2f3f4", fg="#566573", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(8, 0))

        self.bind_click_recursive(frame, click_callback)

    def configure_controls_for_view(self):
        for widget in self.extra_action_holder.winfo_children():
            widget.destroy()

        if self.current_view == "returns":
            self.filter_combo.configure(values=["All", "Due Today", "Due Tomorrow", "Overdue"])
            self.filter_var.set("All")
        elif self.current_view == "approvals":
            self.filter_combo.configure(values=["All", "Car", "Truck", "SUV", "Van", "Motorcycle"])
            self.filter_var.set("All")
        elif self.current_view == "fleet":
            self.filter_combo.configure(values=["All", "Available", "Rented", "Maintenance"])
            self.filter_var.set("All")
            RoundedButton(
                self.extra_action_holder,
                width=140,
                height=30,
                corner_radius=10,
                bg_color="#27ae60",
                fg_color="white",
                text="Add Vehicle",
                command=self.show_add_vehicle_form,
                image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "add.png"),
                icon_size=(14, 14),
                font=("Segoe UI", 8, "bold")
            ).pack(side="right")
        else:
            self.filter_combo.configure(values=["All", "Available", "Rented", "Maintenance"])
            self.filter_var.set("All")

    def refresh_current_view(self):
        if self.current_view == "returns":
            self.show_returns_view()
        elif self.current_view == "approvals":
            self.show_approvals_view()
        elif self.current_view == "fleet":
            self.show_fleet_view()
        else:
            self.show_history_view()

    def reset_list_filters(self):
        self.search_var.set("")
        self.filter_var.set("All")
        self.apply_list_filters()

    def apply_list_filters(self):
        search_text = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()
        filtered = list(self.current_items)

        if search_text:
            if self.current_view == "returns":
                filtered = [
                    item for item in filtered
                    if search_text in str(item['username']).lower()
                    or search_text in str(item['brand']).lower()
                    or search_text in str(item['model']).lower()
                    or search_text in str(item['license_plate']).lower()
                ]
            elif self.current_view == "approvals":
                filtered = [
                    item for item in filtered
                    if search_text in str(item['username']).lower()
                    or search_text in str(item['brand']).lower()
                    or search_text in str(item['model']).lower()
                ]
            else:
                filtered = [
                    item for item in filtered
                    if search_text in str(item['brand']).lower()
                    or search_text in str(item['model']).lower()
                    or search_text in str(item['license_plate']).lower()
                ]

        if selected_filter != "All":
            if self.current_view == "returns":
                from datetime import date, timedelta
                today = date.today()
                tomorrow = today + timedelta(days=1)

                def matches_due(item):
                    due = item['end_date']
                    if hasattr(due, 'date'):
                        due = due.date()
                    if selected_filter == "Due Today":
                        return due == today
                    if selected_filter == "Due Tomorrow":
                        return due == tomorrow
                    if selected_filter == "Overdue":
                        return due < today
                    return True

                filtered = [item for item in filtered if matches_due(item)]
            elif self.current_view == "approvals":
                filtered = [item for item in filtered if item.get('type') == selected_filter]
            elif self.current_view == "fleet":
                filtered = [item for item in filtered if item.get('status') == selected_filter]
            else:
                filtered = [item for item in filtered if item.get('status') == selected_filter]

        self.render_list_items(filtered)

    def render_list_items(self, items):
        self.clear_list()
        for item in items:
            if self.current_view == "returns":
                self.create_rental_list_item(item)
            elif self.current_view == "approvals":
                self.create_approval_list_item(item)
            elif self.current_view == "fleet":
                self.create_fleet_list_item(item)
            else:
                self.create_vehicle_history_list_item(item)
        self.update_list_scroll()

    def update_list_scroll(self):
        self.list_scroll.scrollable_frame.update_idletasks()
        self.list_scroll.canvas.configure(scrollregion=self.list_scroll.canvas.bbox("all"))
        self.list_scroll.canvas.yview_moveto(0)

    def clear_detail(self):
        for widget in self.detail_container.winfo_children():
            widget.destroy()

    def show_placeholder_detail(self):
        self.clear_detail()
        tk.Label(self.detail_container, text="Select an item from the list to view details", 
                font=("Segoe UI", 14), fg="#bdc3c7", bg="white").pack(expand=True)

    # --- View Switchers ---

    def show_returns_view(self):
        self.current_view = "returns"
        self.list_header.config(text="Active Rentals")
        self.show_placeholder_detail()

        self.update_summary_cards()
        self.configure_controls_for_view()
        self.current_items = self.rental_controller.get_all_active_rentals()
        self.reset_list_filters()

    def show_approvals_view(self):
        self.current_view = "approvals"
        self.list_header.config(text="Pending Requests")
        self.show_placeholder_detail()

        self.update_summary_cards()
        self.configure_controls_for_view()
        self.current_items = self.rental_controller.get_pending_reservations()
        self.reset_list_filters()

    def show_fleet_view(self):
        self.current_view = "fleet"
        self.list_header.config(text="Vehicle Fleet")
        self.show_placeholder_detail()

        self.update_summary_cards()
        self.configure_controls_for_view()
        self.current_items = self.rental_controller.get_all_vehicles()
        self.reset_list_filters()

    # --- List Items Creation ---

    def create_rental_list_item(self, rental):
        style = self.get_reservation_status_style(rental.get('status', 'Active'))
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=700, height=146, corner_radius=12, bg_color=style['card'])
        frame.pack(fill="x", pady=6)

        row = tk.Frame(frame.inner_frame, bg=style['card'])
        row.pack(fill="both", expand=True, padx=12, pady=10)

        img_path = self.get_image_path(rental)
        img = ImageHelper.load_image(img_path, size=(132, 88))
        if img:
            lbl = tk.Label(row, image=img, bg=style['card'])
            lbl.image = img
            lbl.pack(side="left", padx=(0, 12))

        body = tk.Frame(row, bg=style['card'])
        body.pack(side="left", fill="both", expand=True)

        top = tk.Frame(body, bg=style['card'])
        top.pack(fill="x")
        tk.Label(top, text=f"{rental['brand']} {rental['model']}", font=("Segoe UI", 13, "bold"), bg=style['card'], fg="#2c3e50").pack(side="left")
        tk.Label(top, text=rental.get('status', 'Active'), bg=style['bg'], fg=style['fg'], font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        tk.Label(body, text=f"Customer: {rental['username']}  •  Plate: {rental['license_plate']}", font=("Segoe UI", 10), bg=style['card'], fg="#5d6d7e").pack(anchor="w", pady=(5, 4))

        bottom = tk.Frame(body, bg=style['card'])
        bottom.pack(fill="x", pady=(4, 0))
        tk.Label(bottom, text=f"Due: {rental['end_date']}", bg="#fadbd8", fg="#922b21", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left")
        tk.Label(bottom, text=f"Total: ₱{float(rental['total_cost']):,.0f}", bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(8, 0))

        def on_click(e):
            self.show_return_details(rental)

        self.bind_click_recursive(frame, on_click)

    def create_approval_list_item(self, reservation):
        style = self.get_reservation_status_style(reservation.get('status', 'Pending'))
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=700, height=146, corner_radius=12, bg_color=style['card'])
        frame.pack(fill="x", pady=6)

        row = tk.Frame(frame.inner_frame, bg=style['card'])
        row.pack(fill="both", expand=True, padx=12, pady=10)

        img_path = self.get_image_path(reservation)
        img = ImageHelper.load_image(img_path, size=(132, 88))
        if img:
            lbl = tk.Label(row, image=img, bg=style['card'])
            lbl.image = img
            lbl.pack(side="left", padx=(0, 12))

        body = tk.Frame(row, bg=style['card'])
        body.pack(side="left", fill="both", expand=True)

        top = tk.Frame(body, bg=style['card'])
        top.pack(fill="x")
        tk.Label(top, text=f"{reservation['brand']} {reservation['model']}", font=("Segoe UI", 13, "bold"), bg=style['card'], fg="#2c3e50").pack(side="left")
        tk.Label(top, text=reservation.get('status', 'Pending'), bg=style['bg'], fg=style['fg'], font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        tk.Label(body, text=f"Customer: {reservation['username']}  •  Dates: {reservation['start_date']} to {reservation['end_date']}", font=("Segoe UI", 10), bg=style['card'], fg="#5d6d7e").pack(anchor="w", pady=(5, 4))

        bottom = tk.Frame(body, bg=style['card'])
        bottom.pack(fill="x", pady=(4, 0))
        tk.Label(bottom, text=f"Total: ₱{float(reservation['total_cost']):,.0f}", bg="#d1f2eb", fg="#117864", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left")
        insurance_text = "Insurance: Yes" if reservation.get('insurance_added') else "Insurance: No"
        insurance_bg = "#d6eaf8" if reservation.get('insurance_added') else "#f2f3f4"
        insurance_fg = "#1b4f72" if reservation.get('insurance_added') else "#566573"
        tk.Label(bottom, text=insurance_text, bg=insurance_bg, fg=insurance_fg, font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(8, 0))

        def on_click(e):
            self.show_approval_details(reservation)

        self.bind_click_recursive(frame, on_click)

    def create_fleet_list_item(self, vehicle):
        def on_click(e): self.show_fleet_details(vehicle)
        self.create_vehicle_rich_list_item(vehicle, on_click)

    # --- Detail Views ---

    def show_return_details(self, rental):
        self.clear_detail()
        detail_scroll = ScrollableFrame(self.detail_container, bg="white")
        detail_scroll.pack(fill="both", expand=True)
        body = detail_scroll.scrollable_frame
        body.configure(bg="white")

        tk.Label(body, text="Return Vehicle", font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        img_path = self.get_image_path(rental)
        img = ImageHelper.load_image(img_path, size=(320, 210))
        if img:
            lbl = tk.Label(body, image=img, bg="white")
            lbl.image = img
            lbl.pack(anchor="w", pady=(0, 14))

        info_card = RoundedFrame(body, corner_radius=12, bg_color="#f8f9fa")
        info_card.pack(fill="x", pady=(0, 14))

        labels = [
            ("Reservation ID", rental['reservation_id']),
            ("Customer", rental['username']),
            ("Vehicle", f"{rental['brand']} {rental['model']}"),
            ("License Plate", rental['license_plate']),
            ("Due Date", rental['end_date'])
        ]

        for label, value in labels:
            row = tk.Frame(info_card.inner_frame, bg="#f8f9fa")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
            tk.Label(row, text=str(value), font=("Segoe UI", 10), bg="#f8f9fa", fg="#34495e").pack(side="left", padx=(8, 0))

        tk.Label(body, text="Return Processing", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(10, 10))

        tk.Label(body, text="Condition Notes:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        notes_entry = tk.Entry(body, font=("Segoe UI", 11), width=50)
        notes_entry.pack(anchor="w", pady=5)
        
        def confirm():
            notes = notes_entry.get() or "Standard return"
            if self.rental_controller.return_vehicle(rental['reservation_id'], rental['vehicle_id'], notes, self.user.user_id):
                messagebox.showinfo("Success", "Vehicle returned successfully")
                self.show_returns_view()
            else:
                messagebox.showerror("Error", "Failed to return vehicle")

        def cancel_active_reservation():
            if not messagebox.askyesno("Confirm", "Cancel this active reservation?"):
                return
            reason = self._prompt_reason_dialog("Cancel Rental", "Please enter the cancellation reason for this active reservation.")
            if reason is None:
                return
            if self.rental_controller.cancel_reservation(rental['reservation_id'], rental['vehicle_id'], reason):
                messagebox.showinfo("Success", "Reservation cancelled")
                self.show_returns_view()
            else:
                messagebox.showerror("Error", "Unable to cancel reservation")

        action_row = tk.Frame(body, bg="white")
        action_row.pack(anchor="w", pady=20)
        RoundedButton(action_row, width=190, height=45, corner_radius=10,
                     bg_color="#f39c12", fg_color="white", text="Confirm Return", command=confirm, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "return.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        RoundedButton(action_row, width=190, height=45, corner_radius=10,
                     bg_color="#e74c3c", fg_color="white", text="Cancel Rental", command=cancel_active_reservation, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "delete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")


    def show_approval_details(self, reservation):
        self.clear_detail()
        detail_scroll = ScrollableFrame(self.detail_container, bg="white")
        detail_scroll.pack(fill="both", expand=True)
        body = detail_scroll.scrollable_frame
        body.configure(bg="white")

        tk.Label(body, text="Review Rental Request", font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        img_path = self.get_image_path(reservation)
        img = ImageHelper.load_image(img_path, size=(320, 210))
        if img:
            lbl = tk.Label(body, image=img, bg="white")
            lbl.image = img
            lbl.pack(anchor="w", pady=(0, 14))

        info_card = RoundedFrame(body, corner_radius=12, bg_color="#f8f9fa")
        info_card.pack(fill="x", pady=(0, 14))

        labels = [
            ("Vehicle", f"{reservation['brand']} {reservation['model']}"),
            ("Customer", f"{reservation['first_name']} {reservation['last_name']} ({reservation['username']})"),
            ("Dates", f"{reservation['start_date']} to {reservation['end_date']}"),
            ("Total Cost", f"P{reservation['total_cost']}"),
            ("Insurance", "Yes" if reservation['insurance_added'] else "No"),
            ("Status", reservation['status'])
        ]

        for label, value in labels:
            row = tk.Frame(info_card.inner_frame, bg="#f8f9fa")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
            tk.Label(row, text=str(value), font=("Segoe UI", 10), bg="#f8f9fa", fg="#34495e").pack(side="left", padx=(8, 0))

        tk.Label(body, text="Actions", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(10, 10))

        btn_frame = tk.Frame(body, bg="white")
        btn_frame.pack(anchor="w")
        
        def approve():
            if self.rental_controller.approve_reservation(reservation['reservation_id']):
                messagebox.showinfo("Success", "Rental approved")
                self.show_approvals_view()
            else:
                messagebox.showerror("Error", "Failed to approve")

        def reject():
            reason = self._prompt_reason_dialog("Reject Request", "Please enter the reason for rejecting this rental request.")
            if reason is None:
                return
            if self.rental_controller.reject_reservation(reservation['reservation_id'], reason):
                messagebox.showinfo("Success", "Rental rejected")
                self.show_approvals_view()
            else:
                 messagebox.showerror("Error", "Failed to reject")

        RoundedButton(btn_frame, width=145, height=45, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Approve", command=approve, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "complete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        RoundedButton(btn_frame, width=145, height=45, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Reject", command=reject, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "delete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))


    def show_fleet_details(self, vehicle):
        self.clear_detail()
        self._create_fleet_form(is_edit=True, vehicle=vehicle)

    def show_add_vehicle_form(self):
        self.clear_detail()
        self._create_fleet_form(is_edit=False)

    def _create_fleet_form(self, is_edit, vehicle=None):
        detail_scroll = ScrollableFrame(self.detail_container, bg="white")
        detail_scroll.pack(fill="both", expand=True)
        body = detail_scroll.scrollable_frame
        body.configure(bg="white")

        title = f"Edit {vehicle['brand']} {vehicle['model']}" if is_edit else "Add New Vehicle"
        tk.Label(body, text=title, font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        if is_edit and vehicle:
            img_path = self.get_image_path(vehicle)
            img = ImageHelper.load_image(img_path, size=(300, 200))
            if img:
                lbl = tk.Label(body, image=img, bg="white")
                lbl.image = img
                lbl.pack(anchor="w", pady=(0, 20))

        form = tk.Frame(body, bg="white")
        form.pack(anchor="w", fill="x")

        entries = {}
        fields = ["Brand", "Model", "Year", "License Plate", "Type", "Daily Rate"]
        keys = ["brand", "model", "year", "license_plate", "type", "daily_rate"]

        for i, field in enumerate(fields):
            tk.Label(form, text=field, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=10)
            
            if field == "Type":
                entry = ttk.Combobox(form, values=["Car", "Truck", "SUV", "Van", "Motorcycle"], width=28)
            else:
                entry = tk.Entry(form, font=("Segoe UI", 10), width=30)
            
            entry.grid(row=i, column=1, sticky="w", padx=20, pady=10)
            entries[keys[i]] = entry
            
            if is_edit and vehicle:
                if field == "Type":
                    entry.set(vehicle[keys[i]])
                else:
                    entry.insert(0, str(vehicle[keys[i]]))

        tk.Label(form, text="Image", font=("Segoe UI", 10, "bold"), bg="white").grid(row=len(fields), column=0, sticky="w", pady=10)
        img_entry_frame = tk.Frame(form, bg="white")
        img_entry_frame.grid(row=len(fields), column=1, sticky="w", padx=20, pady=10)
        
        self.img_path_var = tk.StringVar()
        tk.Entry(img_entry_frame, textvariable=self.img_path_var, width=20).pack(side="left")
        tk.Button(img_entry_frame, text="Browse", command=self.browse_image).pack(side="left", padx=5)

        btn_frame = tk.Frame(body, bg="white")
        btn_frame.pack(anchor="w", pady=30)

        def save():
            data = {k: entries[k].get() for k in keys}
            new_image_path = self.img_path_var.get()
            
            if not all(data.values()): 
                 messagebox.showerror("Error", "All text fields are required")
                 return

            final_image_filename = vehicle['image'] if (is_edit and vehicle) else None
            
            if new_image_path:
                try:
                    ext = os.path.splitext(new_image_path)[1]
                    clean_model = data['model'].replace(" ", "").lower()
                    final_image_filename = f"{clean_model}{ext}"
                    dest_path = os.path.join(os.path.dirname(__file__), "..", "img", "vehicles", final_image_filename)
                    if not os.path.exists(os.path.dirname(dest_path)):
                         os.makedirs(os.path.dirname(dest_path))
                    shutil.copy(new_image_path, dest_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
                    return

            try:
                if is_edit:
                    self.rental_controller.update_vehicle(
                        vehicle['vehicle_id'], data['brand'], data['model'], data['year'], 
                        data['license_plate'], data['type'], data['daily_rate'], final_image_filename
                    )
                    messagebox.showinfo("Success", "Vehicle updated")
                else:
                    self.rental_controller.add_vehicle(
                        data['brand'], data['model'], data['year'], 
                        data['license_plate'], data['type'], data['daily_rate'], final_image_filename
                    )
                    messagebox.showinfo("Success", "Vehicle added")
                self.show_fleet_view()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        RoundedButton(btn_frame, width=132, height=42, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Save Vehicle", command=save, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))

        if is_edit:
            def toggle_status():
                if vehicle['status'] == 'Rented':
                    messagebox.showwarning("Notice", "Cannot toggle maintenance while the vehicle is rented")
                    return
                new_status = "Maintenance" if vehicle['status'] != 'Maintenance' else "Available"
                try:
                    self.rental_controller.set_vehicle_status(vehicle['vehicle_id'], new_status)
                    messagebox.showinfo("Success", f"Vehicle status set to {new_status}")
                    self.show_fleet_view()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            RoundedButton(btn_frame, width=160, height=42, corner_radius=10, bg_color="#8e44ad", fg_color="white", text="Toggle Maintenance", command=toggle_status, image_path=os.path.join(os.path.dirname(__file__), "..", "img", "icons", "car.png"), icon_size=(16, 16), font=("Segoe UI", 8, "bold"), text_align="center").pack(side="left", padx=(0, 8))

            def delete():
                if messagebox.askyesno("Confirm", "Delete this vehicle?"):
                    try:
                        self.rental_controller.delete_vehicle(vehicle['vehicle_id'])
                        messagebox.showinfo("Success", "Vehicle deleted")
                        self.show_fleet_view()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            
            RoundedButton(btn_frame, width=132, height=42, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Delete", command=delete, font=("Segoe UI", 9, "bold")).pack(side="left")

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.img_path_var.set(file_path)

    def get_image_path(self, vehicle_or_res):
        return ImageHelper.get_vehicle_image_path(vehicle_or_res.get('model', ''))

    def show_history_view(self):
        self.current_view = "history"
        self.list_header.config(text="Select Vehicle")
        self.show_placeholder_detail()

        self.update_summary_cards()
        self.configure_controls_for_view()
        self.current_items = self.rental_controller.get_all_vehicles()
        self.reset_list_filters()

    def create_vehicle_history_list_item(self, vehicle):
        def on_click(e): self.show_vehicle_history_details(vehicle)
        self.create_vehicle_rich_list_item(vehicle, on_click)

    def show_vehicle_history_details(self, vehicle):
        self.clear_detail()
        detail_scroll = ScrollableFrame(self.detail_container, bg="white")
        detail_scroll.pack(fill="both", expand=True)
        body = detail_scroll.scrollable_frame
        body.configure(bg="white")

        tk.Label(body, text=f"Vehicle History: {vehicle['brand']} {vehicle['model']}", 
                font=("Segoe UI", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 16))

        img_path = self.get_image_path(vehicle)
        img = ImageHelper.load_image(img_path, size=(280, 180))
        if img:
            lbl = tk.Label(body, image=img, bg="white")
            lbl.image = img
            lbl.pack(anchor="w", pady=(0, 12))

        info_card = RoundedFrame(body, corner_radius=12, bg_color="#f8f9fa")
        info_card.pack(fill="x", pady=(0, 14))

        status_color = "#27ae60" if vehicle['status'] == 'Available' else "#e74c3c"
        info_rows = [
            ("License Plate", vehicle['license_plate'], "#34495e"),
            ("Year", vehicle['year'], "#34495e"),
            ("Status", vehicle['status'], status_color),
            ("Rate", f"P{vehicle['daily_rate']}/day", "#34495e")
        ]
        for label, value, color in info_rows:
            row = tk.Frame(info_card.inner_frame, bg="#f8f9fa")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
            tk.Label(row, text=str(value), font=("Segoe UI", 10), bg="#f8f9fa", fg=color).pack(side="left", padx=(8, 0))

        tk.Label(body, text="Rental History", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(6, 10))

        history = self.rental_controller.get_vehicle_rental_history(vehicle['vehicle_id'])
        return_logs = self.rental_controller.get_vehicle_return_logs(vehicle['vehicle_id'])
        return_notes = [log.get('description') for log in return_logs if log.get('description')]
        completed_idx = 0

        if not history:
            tk.Label(body, text="No rental history found.", font=("Segoe UI", 11), fg="#7f8c8d", bg="white").pack(anchor="w")
            return

        for h in history:
            hist_card = RoundedFrame(body, corner_radius=12, bg_color="#ffffff")
            hist_card.pack(fill="x", pady=6)

            status = h.get('status', '')
            status_bg = "#eafaf1" if status == 'Completed' else ("#fff4db" if status == 'Pending' else ("#eaf4ff" if status == 'Active' else "#f0f3f4"))
            status_fg = "#145a32" if status == 'Completed' else ("#7d6608" if status == 'Pending' else ("#1b4f72" if status == 'Active' else "#2e4053"))

            top = tk.Frame(hist_card.inner_frame, bg="#ffffff")
            top.pack(fill="x")
            customer_name = f"{h['first_name']} {h['last_name']}"
            tk.Label(top, text=customer_name, font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").pack(side="left")
            tk.Label(top, text=status, bg=status_bg, fg=status_fg, font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

            tk.Label(hist_card.inner_frame, text=f"Dates: {h['start_date']} to {h['end_date']}", font=("Segoe UI", 10), bg="#ffffff", fg="#5d6d7e").pack(anchor="w", pady=(5, 2))
            cost_label = tk.Label(hist_card.inner_frame, text=f"Total Cost: P{h['total_cost']}", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#117864")
            if status in ['Cancelled', 'Rejected']:
                strike_font = tkfont.Font(font=("Segoe UI", 10, "bold"))
                strike_font.configure(overstrike=1)
                cost_label.configure(font=strike_font, fg="#c0392b")
            cost_label.pack(anchor="w")

            if status == 'Completed':
                note_text = return_notes[completed_idx] if completed_idx < len(return_notes) else "No return description recorded."
                completed_idx += 1
                tk.Label(
                    hist_card.inner_frame,
                    text=f"Return Description: {note_text}",
                    font=("Segoe UI", 9),
                    bg="#fcf3cf",
                    fg="#7d6608",
                    padx=10,
                    pady=6,
                    wraplength=430,
                    justify="left"
                ).pack(fill="x", pady=(8, 0))
            elif status == 'Cancelled':
                cancel_reason = h.get('cancel_reason') or 'No cancellation reason provided.'
                tk.Label(
                    hist_card.inner_frame,
                    text=f"Cancellation Reason: {cancel_reason}",
                    font=("Segoe UI", 9),
                    bg="#fdecea",
                    fg="#922b21",
                    padx=10,
                    pady=6,
                    wraplength=430,
                    justify="left"
                ).pack(fill="x", pady=(8, 0))
            elif status == 'Rejected':
                reject_reason = h.get('reject_reason') or 'No rejection reason provided.'
                tk.Label(
                    hist_card.inner_frame,
                    text=f"Rejection Reason: {reject_reason}",
                    font=("Segoe UI", 9),
                    bg="#f0f3f4",
                    fg="#2e4053",
                    padx=10,
                    pady=6,
                    wraplength=430,
                    justify="left"
                ).pack(fill="x", pady=(8, 0))
