import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from tkcalendar import DateEntry
from src.controllers.auth_controller import AuthController
from src.controllers.rental_controller import RentalController
from datetime import date
from src.utils.image_helper import ImageHelper
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame
import os

class MemberDashboard(tk.Frame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        self.auth_controller = AuthController()
        self.rental_controller = RentalController()
        self.current_view = "rent"
        self.current_items = []
        self.rent_locked = False
        self.active_rental = None
        self.pack(fill="both", expand=True)
        
        self.create_layout()
        self.show_rent_view()

    def _icon_path(self, icon_name):
        return os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)

    def create_layout(self):
        self.top_bar = tk.Frame(self, bg="#2c3e50", height=60)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)

        tk.Label(self.top_bar, text="Member Dashboard", bg="#2c3e50", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        
        user_info = tk.Frame(self.top_bar, bg="#2c3e50")
        user_info.pack(side="right", padx=20)
        
        self.welcome_label = tk.Label(user_info, text=f"Welcome, {self.user.full_name}", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 12))
        self.welcome_label.pack(side="left", padx=10)
        RoundedButton(
            user_info,
            width=130,
            height=30,
            corner_radius=10,
            bg_color="#e74c3c",
            fg_color="white",
            text="Logout",
            command=self.logout_callback,
            image_path=self._icon_path("logout.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

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

        logo_img = ImageHelper.load_image(self._icon_path("logo.png"), (72, 72))
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

        self.create_sidebar_button("Rent a Vehicle", "car.png", self.show_rent_view)
        self.create_sidebar_button("My Reservations", "rental.png", self.show_history_view)
        self.create_sidebar_button("My Profile", "user.png", self.show_profile_view)

        self.list_pane = tk.Frame(self.main_container, bg="#f8f9fa", width=640)
        self.list_pane.pack(side="left", fill="both", expand=True)
        self.list_pane.pack_propagate(False)

        self.list_title = tk.Label(self.list_pane, text="Select Item", bg="#f8f9fa", font=("Segoe UI", 14, "bold"), anchor="w", padx=20, pady=12)
        self.list_title.pack(fill="x")

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
            image_path=self._icon_path("search.png"),
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
            image_path=self._icon_path("apply_filter.png"),
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
            image_path=self._icon_path("reset.png"),
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
            image_path=self._icon_path("analytics.png"),
            icon_size=(16, 16),
            font=("Segoe UI", 9, "bold"),
            text_align="center"
        ).pack(side="left")

        self.list_scroll = ScrollableFrame(self.list_pane, bg="#f8f9fa")
        self.list_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.detail_pane = tk.Frame(self.main_container, bg="white", width=420)
        self.detail_pane.pack(side="left", fill="both", expand=True)
        self.detail_pane.pack_propagate(False)
        
        self.detail_container = tk.Frame(self.detail_pane, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=24, pady=24)

        self.show_placeholder_detail()

    def create_sidebar_button(self, text, icon_name, command):
        icon_path = self._icon_path(icon_name)
        btn = RoundedButton(self.sidebar_menu, width=220, height=50, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command, image_path=icon_path)
        btn.pack(pady=5)

    def clear_list(self):
        for widget in self.list_scroll.scrollable_frame.winfo_children():
            widget.destroy()

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

    def get_image_path(self, vehicle_or_res):
        return ImageHelper.get_vehicle_image_path(vehicle_or_res.get('model', ''))

    def update_summary_cards(self):
        for widget in self.summary_bar.winfo_children():
            widget.destroy()

        all_res = self.rental_controller.get_user_reservations(self.user.user_id)
        available_count = len(self.rental_controller.get_available_vehicles())
        pending_count = len([item for item in all_res if item['status'] == 'Pending'])
        active_count = len([item for item in all_res if item['status'] == 'Active'])

        cards = [
            ("Available Cars", str(available_count), "#3498db", "car.png"),
            ("My Reservations", str(len(all_res)), "#8e44ad", "rental.png"),
            ("Pending", str(pending_count), "#f39c12", "list.png"),
            ("Active", str(active_count), "#27ae60", "active_rentals.png")
        ]

        for idx, (title, value, color, icon) in enumerate(cards):
            card = RoundedFrame(self.summary_bar, height=74, corner_radius=10, bg_color="white")
            card.grid(row=0, column=idx, padx=4, sticky="nsew")
            self.summary_bar.grid_columnconfigure(idx, weight=1)

            row = tk.Frame(card.inner_frame, bg="white")
            row.pack(fill="both", expand=True, padx=8, pady=6)
            icon_img = ImageHelper.load_image(self._icon_path(icon), (18, 18))
            if icon_img:
                lbl = tk.Label(row, image=icon_img, bg="white")
                lbl.image = icon_img
                lbl.pack(side="left", padx=(0, 6))

            text_col = tk.Frame(row, bg="white")
            text_col.pack(side="left", fill="both", expand=True)
            tk.Label(text_col, text=title, bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(text_col, text=value, bg="white", fg=color, font=("Segoe UI", 14, "bold")).pack(anchor="w")

    def set_profile_mode(self, enabled):
        if enabled:
            if self.summary_bar.winfo_manager():
                self.summary_bar.pack_forget()
            if self.controls_bar.winfo_manager():
                self.controls_bar.pack_forget()
        else:
            if not self.controls_bar.winfo_manager():
                self.controls_bar.pack(fill="x", padx=10, pady=(0, 8), before=self.list_scroll)
            if not self.summary_bar.winfo_manager():
                self.summary_bar.pack(fill="x", padx=10, pady=(0, 8), before=self.controls_bar)

    def show_profile_empty_detail(self):
        self.clear_detail()
        filler = tk.Frame(self.detail_container, bg="white")
        filler.pack(fill="both", expand=True)

    def configure_controls_for_view(self):
        if self.current_view == "rent":
            self.filter_combo.configure(values=["All", "Car", "Truck", "SUV", "Van", "Motorcycle"])
            self.filter_var.set("All")
        elif self.current_view == "profile":
            self.filter_combo.configure(values=["All"])
            self.filter_var.set("All")
        else:
            self.filter_combo.configure(values=["All", "Pending", "Active", "Completed", "Cancelled", "Rejected"])
            self.filter_var.set("All")

    def refresh_current_view(self):
        if self.current_view == "rent":
            self.show_rent_view()
        elif self.current_view == "profile":
            self.show_profile_view()
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
            if self.current_view == "rent":
                filtered = [
                    item for item in filtered
                    if search_text in str(item['brand']).lower()
                    or search_text in str(item['model']).lower()
                    or search_text in str(item['license_plate']).lower()
                ]
            elif self.current_view == "history":
                filtered = [
                    item for item in filtered
                    if search_text in str(item['brand']).lower()
                    or search_text in str(item['model']).lower()
                    or search_text in str(item['reservation_id']).lower()
                ]

        if selected_filter != "All":
            if self.current_view == "rent":
                filtered = [item for item in filtered if item.get('type') == selected_filter]
            elif self.current_view == "history":
                filtered = [item for item in filtered if item.get('status') == selected_filter]

        self.render_list_items(filtered)

    def render_list_items(self, items):
        self.clear_list()

        if self.current_view == "rent" and self.rent_locked:
            tk.Label(
                self.list_scroll.scrollable_frame,
                text="You are currently renting a vehicle and cannot rent another until the active rental is completed.",
                bg="#fcf3cf",
                fg="#7d6608",
                font=("Segoe UI", 10, "bold"),
                padx=12,
                pady=8,
                wraplength=660,
                justify="left"
            ).pack(fill="x", pady=(0, 8))

        for item in items:
            if self.current_view == "rent":
                self.create_vehicle_list_item(item)
            elif self.current_view == "history":
                self.create_reservation_list_item(item)
            elif self.current_view == "profile":
                self.create_profile_list_item(item)
        self.update_list_scroll()

    def get_vehicle_status_style(self, status):
        palette = {
            'Available': {'bg': '#eafaf1', 'fg': '#1e8449', 'card': '#ffffff'},
            'Active': {'bg': '#eaf4ff', 'fg': '#1b4f72', 'card': '#ffffff'},
            'Rented': {'bg': '#fdecea', 'fg': '#c0392b', 'card': '#fffdfd'},
            'Maintenance': {'bg': '#f4ecf7', 'fg': '#7d3c98', 'card': '#fdfbff'}
        }
        return palette.get(status, {'bg': '#ecf0f1', 'fg': '#2c3e50', 'card': '#ffffff'})

    def set_rent_controls_locked(self, locked):
        self.search_entry.config(state="disabled" if locked else "normal")
        self.filter_combo.configure(state="disabled" if locked else "readonly")

    def get_reservation_status_style(self, status):
        palette = {
            'Active': {'bg': '#eaf4ff', 'fg': '#1b4f72', 'card': '#ffffff'},
            'Pending': {'bg': '#fff4db', 'fg': '#7d6608', 'card': '#ffffff'},
            'Completed': {'bg': '#eafaf1', 'fg': '#145a32', 'card': '#ffffff'},
            'Cancelled': {'bg': '#fdecea', 'fg': '#922b21', 'card': '#fffdfd'},
            'Rejected': {'bg': '#f0f3f4', 'fg': '#2e4053', 'card': '#ffffff'}
        }
        return palette.get(status, {'bg': '#ecf0f1', 'fg': '#2c3e50', 'card': '#ffffff'})

    # --- RENT VIEW ---
    def show_rent_view(self):
        self.current_view = "rent"
        self.set_profile_mode(False)
        self.show_placeholder_detail()
        self.list_title.config(text="Rent a Vehicle")

        self.update_summary_cards()
        self.configure_controls_for_view()

        reservations = self.rental_controller.get_user_reservations(self.user.user_id)
        self.active_rental = next((item for item in reservations if item.get('status') == 'Active'), None)
        self.rent_locked = self.active_rental is not None
        self.set_rent_controls_locked(self.rent_locked)

        if self.rent_locked:
            self.list_title.config(text="Current Active Rental")
            self.search_var.set("")
            self.filter_var.set("All")
            active_item = dict(self.active_rental)
            active_item['status'] = 'Active'
            self.current_items = [active_item]
            self.render_list_items(self.current_items)
        else:
            self.current_items = self.rental_controller.get_member_vehicle_catalog()
            self.reset_list_filters()

    def create_vehicle_list_item(self, vehicle):
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
        tk.Label(top, text=vehicle.get('status', 'Available'), bg=style['bg'], fg=style['fg'], font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        vehicle_type = vehicle.get('type', 'N/A')
        vehicle_year = vehicle.get('year', 'N/A')
        tk.Label(body, text=f"Plate: {vehicle['license_plate']}  •  Type: {vehicle_type}  •  Year: {vehicle_year}", font=("Segoe UI", 10), bg=style['card'], fg="#5d6d7e").pack(anchor="w", pady=(5, 4))

        bottom = tk.Frame(body, bg=style['card'])
        bottom.pack(fill="x", pady=(4, 0))
        daily_rate = float(vehicle.get('daily_rate') or 0)
        tk.Label(bottom, text=f"₱{daily_rate:,.0f} / day", bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left")
        tk.Label(bottom, text=f"ID #{vehicle['vehicle_id']}", bg="#f2f3f4", fg="#566573", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(8, 0))

        if vehicle.get('status') == 'Maintenance':
            tk.Label(
                bottom,
                text="Unavailable for Renting",
                bg="#f4ecf7",
                fg="#7d3c98",
                font=("Segoe UI", 9, "bold"),
                padx=10,
                pady=3
            ).pack(side="right")

        def on_click(e):
            if self.rent_locked:
                self.show_active_rental_details(vehicle)
            else:
                self.show_rent_details(vehicle)

        self.bind_click_recursive(frame, on_click)

    def show_active_rental_details(self, rental):
        self.clear_detail()

        tk.Label(self.detail_container, text="Currently Renting", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 10))

        img_path = self.get_image_path(rental)
        img = ImageHelper.load_image(img_path, size=(400, 250))
        if img:
            lbl = tk.Label(self.detail_container, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)

        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=10)

        labels = [
            ("Vehicle:", f"{rental.get('brand', '')} {rental.get('model', '')}"),
            ("Reservation ID:", rental.get('reservation_id', '-')),
            ("Start Date:", rental.get('start_date', '-')),
            ("End Date:", rental.get('end_date', '-')),
            ("Status:", rental.get('status', 'Active'))
        ]

        for i, (l, v) in enumerate(labels):
            tk.Label(info_frame, text=l, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(info_frame, text=str(v), font=("Segoe UI", 10), bg="white").grid(row=i, column=1, sticky="w", padx=10, pady=3)

        tk.Label(
            self.detail_container,
            text="Please return the vehicle to our shop once your rental period ends. After a condition check, our receptionist will mark this reservation as completed.",
            font=("Segoe UI", 10, "bold"),
            fg="#b9770e",
            bg="#fcf3cf",
            padx=12,
            pady=8,
            wraplength=440,
            justify="left"
        ).pack(fill="x", pady=(10, 0))

    def show_rent_details(self, vehicle):
        if self.rent_locked:
            self.show_active_rental_details(self.active_rental or vehicle)
            return

        self.clear_detail()
        detail_scroll = ScrollableFrame(self.detail_container, bg="white")
        detail_scroll.pack(fill="both", expand=True)
        body = detail_scroll.scrollable_frame
        body.configure(bg="white")

        if vehicle.get('status') != 'Available':
            tk.Label(body, text=f"{vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 8))

            img_path = self.get_image_path(vehicle)
            img = ImageHelper.load_image(img_path, size=(400, 250))
            if img:
                lbl = tk.Label(body, image=img, bg="white")
                lbl.image = img
                lbl.pack(pady=10)

            status = vehicle.get('status', 'Unavailable')
            tk.Label(
                body,
                text=f"Status: {status}",
                font=("Segoe UI", 11, "bold"),
                bg="#f4ecf7",
                fg="#7d3c98",
                padx=12,
                pady=8
            ).pack(anchor="w", pady=(6, 10))

            tk.Label(
                body,
                text="This vehicle is currently under maintenance and unavailable for renting.",
                font=("Segoe UI", 11),
                fg="#5d6d7e",
                bg="white",
                wraplength=440,
                justify="left"
            ).pack(anchor="w")
            return
        
        tk.Label(body, text=f"Rent {vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 10))

        img_path = self.get_image_path(vehicle)
        img = ImageHelper.load_image(img_path, size=(400, 250))
        if img:
            lbl = tk.Label(body, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)

        # Details Grid
        details_frame = tk.Frame(body, bg="white")
        details_frame.pack(fill="x", pady=10)
        
        tk.Label(details_frame, text="Daily Rate:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(details_frame, text=f"P{vehicle['daily_rate']}", font=("Segoe UI", 10), bg="white").grid(row=0, column=1, sticky="w", padx=10)
        
        tk.Label(details_frame, text="Type:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w")
        tk.Label(details_frame, text=vehicle['type'], font=("Segoe UI", 10), bg="white").grid(row=1, column=1, sticky="w", padx=10)

        separator = ttk.Separator(body, orient='horizontal')
        separator.pack(fill='x', pady=15)

        # Form
        form_frame = tk.Frame(body, bg="white")
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Reservation Dates", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", pady=(0, 10))
        
        dates_grid = tk.Frame(form_frame, bg="white")
        dates_grid.pack(fill="x")
        
        tk.Label(dates_grid, text="Start Date:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        start_date = DateEntry(dates_grid, width=15, background='darkblue', foreground='white', borderwidth=2)
        start_date.grid(row=0, column=1, sticky="w", pady=5, padx=10)

        tk.Label(dates_grid, text="End Date:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        end_date = DateEntry(dates_grid, width=15, background='darkblue', foreground='white', borderwidth=2)
        end_date.grid(row=1, column=1, sticky="w", pady=5, padx=10)

        insurance_var = tk.BooleanVar()
        tk.Checkbutton(form_frame, text="Add Insurance (+500/day)", variable=insurance_var, bg="white", font=("Segoe UI", 10), command=lambda: calculate_total()).pack(anchor="w", pady=10)

        total_label = tk.Label(form_frame, text="Total Estimated Cost: P0", font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50")
        total_label.pack(pady=10)

        def calculate_total(*args):
            try:
                s_date = start_date.get_date()
                e_date = end_date.get_date()
                if s_date and e_date and e_date > s_date:
                    days = (e_date - s_date).days
                    daily_cost = vehicle['daily_rate'] + (500 if insurance_var.get() else 0)
                    total = days * daily_cost
                    total_label.config(text=f"Total Estimated Cost: P{total:,.2f}")
                else:
                    total_label.config(text="Total Estimated Cost: -")
            except Exception:
                total_label.config(text="Total Estimated Cost: -")

        start_date.bind("<<DateEntrySelected>>", calculate_total)
        end_date.bind("<<DateEntrySelected>>", calculate_total)
        
        # Initial calculation
        calculate_total()

        def confirm_rent():
            today = date.today()
            s_date = start_date.get_date()
            e_date = end_date.get_date()
            
            if s_date < today:
                messagebox.showerror("Error", "Start date cannot be in the past")
                return
            if e_date <= s_date:
                messagebox.showerror("Error", "End date must be after start date")
                return
                            
            if self.rental_controller.create_reservation(self.user.user_id, vehicle['vehicle_id'], s_date, e_date, insurance_var.get()):
                messagebox.showinfo("Success", "Reservation requested! Waiting for approval.")
                self.show_placeholder_detail()
                self.show_rent_view()
            else:
                messagebox.showerror("Error", "Failed to create reservation")

        def reset_form():
            start_date.set_date(date.today())
            end_date.set_date(date.today())
            insurance_var.set(False)
            calculate_total()

        actions = tk.Frame(body, bg="white")
        actions.pack(anchor="w", pady=24)
        RoundedButton(actions, width=190, height=45, corner_radius=10,
                     bg_color="#27ae60", fg_color="white", text="Confirm Reservation", command=confirm_rent,
                     image_path=self._icon_path("complete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        RoundedButton(actions, width=140, height=45, corner_radius=10,
                     bg_color="#7f8c8d", fg_color="white", text="Reset", command=reset_form,
                     image_path=self._icon_path("reset.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")


    # --- HISTORY VIEW ---
    def show_history_view(self):
        self.current_view = "history"
        self.rent_locked = False
        self.active_rental = None
        self.set_rent_controls_locked(False)
        self.set_profile_mode(False)
        self.show_placeholder_detail()
        self.list_title.config(text="My Reservations")

        self.update_summary_cards()
        self.configure_controls_for_view()
        self.current_items = self.rental_controller.get_user_reservations(self.user.user_id)
        self.reset_list_filters()

    def show_profile_view(self):
        self.current_view = "profile"
        self.rent_locked = False
        self.active_rental = None
        self.set_rent_controls_locked(False)
        self.list_title.config(text="My Profile")

        self.set_profile_mode(True)
        self.show_profile_empty_detail()
        self.render_profile_center()

    def create_profile_list_item(self, profile_item):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=700, height=110, corner_radius=12, bg_color="#ffffff")
        frame.pack(fill="x", pady=6)

        row = tk.Frame(frame.inner_frame, bg="#ffffff")
        row.pack(fill="both", expand=True, padx=12, pady=10)

        icon = ImageHelper.load_image(self._icon_path("user.png" if profile_item['card'] == 'Profile Information' else "history.png"), (24, 24))
        if icon:
            icon_lbl = tk.Label(row, image=icon, bg="#ffffff")
            icon_lbl.image = icon
            icon_lbl.pack(side="left", padx=(0, 10))

        text = tk.Frame(row, bg="#ffffff")
        text.pack(side="left", fill="both", expand=True)
        tk.Label(text, text=profile_item['card'], bg="#ffffff", fg="#2c3e50", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(text, text=f"{profile_item['full_name']} (@{profile_item['username']})", bg="#ffffff", fg="#5d6d7e", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        tk.Label(row, text="View", bg="#d6eaf8", fg="#1b4f72", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        def on_click(e):
            self.show_profile_details()

        self.bind_click_recursive(frame, on_click)

    def render_profile_center(self):
        self.clear_list()

        container = tk.Frame(self.list_scroll.scrollable_frame, bg="#f8f9fa")
        container.pack(fill="x", padx=6, pady=6)

        tk.Label(container, text="My Profile", font=("Segoe UI", 22, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 12))

        profile_card = RoundedFrame(container, width=700, height=220, corner_radius=14, bg_color="#ecf0f1")
        profile_card.pack(fill="x", pady=(0, 16))

        header = tk.Frame(profile_card.inner_frame, bg="#ecf0f1")
        header.pack(fill="x", pady=(4, 8))
        icon = ImageHelper.load_image(self._icon_path("user.png"), (24, 24))
        if icon:
            icon_lbl = tk.Label(header, image=icon, bg="#ecf0f1")
            icon_lbl.image = icon
            icon_lbl.pack(side="left", padx=(0, 8))
        tk.Label(header, text="Personal Information", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(side="left")

        form = tk.Frame(profile_card.inner_frame, bg="#ecf0f1")
        form.pack(fill="x")

        tk.Label(form, text="Username", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=4)
        tk.Label(form, text="First Name", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w", padx=4)
        tk.Label(form, text="Last Name", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=4)

        self.profile_username = tk.Entry(form, font=("Segoe UI", 10))
        self.profile_username.grid(row=1, column=0, sticky="ew", padx=4, pady=(4, 8), ipady=4)
        self.profile_username.insert(0, self.user.username)

        first_name, last_name = self.user.full_name.split(" ", 1) if " " in self.user.full_name else (self.user.full_name, "")
        self.profile_fname = tk.Entry(form, font=("Segoe UI", 10))
        self.profile_fname.grid(row=1, column=1, sticky="ew", padx=4, pady=(4, 8), ipady=4)
        self.profile_fname.insert(0, first_name)

        self.profile_lname = tk.Entry(form, font=("Segoe UI", 10))
        self.profile_lname.grid(row=1, column=2, sticky="ew", padx=4, pady=(4, 8), ipady=4)
        self.profile_lname.insert(0, last_name)

        for idx in range(3):
            form.grid_columnconfigure(idx, weight=1)

        def save_profile():
            username = self.profile_username.get().strip()
            first = self.profile_fname.get().strip()
            last = self.profile_lname.get().strip()
            ok, msg = self.auth_controller.update_user_profile(self.user.user_id, username, first, last)
            if not ok:
                messagebox.showerror("Error", msg)
                return

            self.user.update_profile_info(username, first, last)
            self.welcome_label.config(text=f"Welcome, {self.user.full_name}")
            messagebox.showinfo("Success", msg)
            self.show_profile_view()

        RoundedButton(profile_card.inner_frame, width=170, height=40, corner_radius=10,
                     bg_color="#2980b9", fg_color="white", text="Save Profile", command=save_profile,
                     image_path=self._icon_path("complete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(6, 0))

        password_card = RoundedFrame(container, width=700, height=250, corner_radius=14, bg_color="#ecf0f1")
        password_card.pack(fill="x")

        p_header = tk.Frame(password_card.inner_frame, bg="#ecf0f1")
        p_header.pack(fill="x", pady=(4, 8))
        p_icon = ImageHelper.load_image(self._icon_path("history.png"), (24, 24))
        if p_icon:
            p_lbl = tk.Label(p_header, image=p_icon, bg="#ecf0f1")
            p_lbl.image = p_icon
            p_lbl.pack(side="left", padx=(0, 8))
        tk.Label(p_header, text="Change Password", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(side="left")

        pass_form = tk.Frame(password_card.inner_frame, bg="#ecf0f1")
        pass_form.pack(fill="x")

        tk.Label(pass_form, text="Current Password", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=4)
        tk.Label(pass_form, text="New Password", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w", padx=4)
        tk.Label(pass_form, text="Confirm Password", bg="#ecf0f1", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=4)

        self.current_pass_entry = tk.Entry(pass_form, show="*", font=("Segoe UI", 10))
        self.current_pass_entry.grid(row=1, column=0, sticky="ew", padx=4, pady=(4, 8), ipady=4)

        self.new_pass_entry = tk.Entry(pass_form, show="*", font=("Segoe UI", 10))
        self.new_pass_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=(4, 8), ipady=4)

        self.confirm_pass_entry = tk.Entry(pass_form, show="*", font=("Segoe UI", 10))
        self.confirm_pass_entry.grid(row=1, column=2, sticky="ew", padx=4, pady=(4, 8), ipady=4)

        for idx in range(3):
            pass_form.grid_columnconfigure(idx, weight=1)

        def change_password():
            current_pass = self.current_pass_entry.get()
            new_pass = self.new_pass_entry.get()
            confirm_pass = self.confirm_pass_entry.get()

            if new_pass != confirm_pass:
                messagebox.showerror("Error", "New password and confirmation do not match")
                return

            ok, msg = self.auth_controller.change_user_password(self.user.user_id, current_pass, new_pass)
            if ok:
                messagebox.showinfo("Success", msg)
                self.current_pass_entry.delete(0, tk.END)
                self.new_pass_entry.delete(0, tk.END)
                self.confirm_pass_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", msg)

        RoundedButton(password_card.inner_frame, width=190, height=40, corner_radius=10,
                     bg_color="#8e44ad", fg_color="white", text="Update Password", command=change_password,
                     image_path=self._icon_path("user.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(6, 0))

        self.update_list_scroll()

    def create_reservation_list_item(self, res):
        style = self.get_reservation_status_style(res.get('status', 'Pending'))
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=700, height=146, corner_radius=12, bg_color=style['card'])
        frame.pack(fill="x", pady=6)

        row = tk.Frame(frame.inner_frame, bg=style['card'])
        row.pack(fill="both", expand=True, padx=12, pady=10)

        img_path = self.get_image_path(res)
        img = ImageHelper.load_image(img_path, size=(132, 88))
        if img:
            lbl = tk.Label(row, image=img, bg=style['card'])
            lbl.image = img
            lbl.pack(side="left", padx=(0, 12))

        body = tk.Frame(row, bg=style['card'])
        body.pack(side="left", fill="both", expand=True)

        top = tk.Frame(body, bg=style['card'])
        top.pack(fill="x")
        tk.Label(top, text=f"{res['brand']} {res['model']}", font=("Segoe UI", 13, "bold"), bg=style['card'], fg="#2c3e50").pack(side="left")
        tk.Label(top, text=res.get('status', 'Pending'), bg=style['bg'], fg=style['fg'], font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="right")

        tk.Label(body, text=f"Reservation #{res['reservation_id']}  •  {res['start_date']} to {res['end_date']}", font=("Segoe UI", 10), bg=style['card'], fg="#5d6d7e").pack(anchor="w", pady=(5, 4))

        bottom = tk.Frame(body, bg=style['card'])
        bottom.pack(fill="x", pady=(4, 0))
        total_label = tk.Label(bottom, text=f"Total: ₱{float(res['total_cost']):,.0f}", bg="#d1f2eb", fg="#117864", font=("Segoe UI", 9, "bold"), padx=10, pady=3)
        if res.get('status') in ['Cancelled', 'Rejected']:
            strike_font = tkfont.Font(font=("Segoe UI", 9, "bold"))
            strike_font.configure(overstrike=1)
            total_label.configure(bg="#fdecea", fg="#c0392b", font=strike_font)
        total_label.pack(side="left")
        tk.Label(bottom, text=f"Plate: {res['license_plate']}", bg="#f2f3f4", fg="#566573", font=("Segoe UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(8, 0))

        def on_click(e):
            self.show_reservation_details(res)

        self.bind_click_recursive(frame, on_click)

    def show_reservation_details(self, res):
        self.clear_detail()
        
        tk.Label(self.detail_container, text=f"Reservation #{res['reservation_id']}", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 10))

        img_path = self.get_image_path(res)
        img = ImageHelper.load_image(img_path, size=(400, 250))
        if img:
            lbl = tk.Label(self.detail_container, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)

        # Status Message
        status_messages = {
            'Pending': 'Your reservation is waiting for receptionist approval.',
            'Active': '',
            'Completed': 'This reservation has been completed. Thank you!',
            'Cancelled': 'This reservation was cancelled.',
            'Rejected': 'This reservation was rejected.'
        }
        msg = status_messages.get(res['status'], "")
        if msg:
            tk.Label(self.detail_container, text=msg, font=("Segoe UI", 11, "italic"), fg="#7f8c8d", bg="white").pack(pady=5)

        if res['status'] == 'Active':
            tk.Label(
                self.detail_container,
                text="Please return the vehicle to our shop once your rental period ends. After a condition check, our receptionist will mark this reservation as completed.",
                font=("Segoe UI", 10, "bold"),
                fg="#7d6608",
                bg="#fcf3cf",
                padx=12,
                pady=8,
                wraplength=460,
                justify="left"
            ).pack(fill="x", pady=(8, 10))

        # Info
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=20)

        labels = [
            ("Vehicle:", f"{res['brand']} {res['model']}"),
            ("Start Date:", res['start_date']),
            ("End Date:", res['end_date']),
            ("Total Cost:", f"₱{res['total_cost']}"),
            ("Status:", res['status'])
        ]
        
        for i, (l, v) in enumerate(labels):
            tk.Label(info_frame, text=l, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=3)
            value_label = tk.Label(info_frame, text=str(v), font=("Segoe UI", 10), bg="white")
            if l == "Total Cost:" and res.get('status') in ['Cancelled', 'Rejected']:
                strike_font = tkfont.Font(font=("Segoe UI", 10))
                strike_font.configure(overstrike=1)
                value_label.configure(font=strike_font, fg="#c0392b")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=3)

        if res['status'] == 'Cancelled' and res.get('cancel_reason'):
            tk.Label(
                self.detail_container,
                text=f"Cancellation Reason: {res.get('cancel_reason')}",
                font=("Segoe UI", 10, "bold"),
                fg="#922b21",
                bg="#fdecea",
                padx=12,
                pady=8,
                wraplength=460,
                justify="left"
            ).pack(fill="x", pady=(0, 10))

        if res['status'] == 'Rejected' and res.get('reject_reason'):
            tk.Label(
                self.detail_container,
                text=f"Rejection Reason: {res.get('reject_reason')}",
                font=("Segoe UI", 10, "bold"),
                fg="#2e4053",
                bg="#f0f3f4",
                padx=12,
                pady=8,
                wraplength=460,
                justify="left"
            ).pack(fill="x", pady=(0, 10))

        # Actions
        action_row = tk.Frame(self.detail_container, bg="white")
        action_row.pack(anchor="w", pady=24)

        if res['status'] == 'Pending':
            def cancel():
                if messagebox.askyesno("Confirm", "Are you sure you want to cancel this reservation?"):
                    reason = self._prompt_reason_dialog("Cancel Reservation", "Please enter your cancellation reason for this reservation.")
                    if reason is None:
                        return
                    if self.rental_controller.cancel_reservation(res['reservation_id'], res['vehicle_id'], reason):
                        messagebox.showinfo("Success", "Reservation cancelled")
                        self.show_history_view()
                        self.show_placeholder_detail()
                    else:
                        messagebox.showerror("Error", "Unable to cancel reservation")

            RoundedButton(action_row, width=200, height=45, corner_radius=10,
                         bg_color="#e74c3c", fg_color="white", text="Cancel Reservation", command=cancel,
                         image_path=self._icon_path("delete.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))

        RoundedButton(action_row, width=140, height=45, corner_radius=10,
                     bg_color="#16a085", fg_color="white", text="Back", command=self.show_history_view,
                     image_path=self._icon_path("return.png"), icon_size=(16, 16), font=("Segoe UI", 9, "bold")).pack(side="left")
