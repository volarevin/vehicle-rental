import os

content = r'''import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.controllers.rental_controller import RentalController
from datetime import datetime, date
from src.utils.image_helper import ImageHelper
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame
import os

class MemberDashboard(tk.Frame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        self.rental_controller = RentalController()
        # Pack to fill window
        self.pack(fill="both", expand=True)
        
        self.create_layout()
        self.show_rent_view()

    def create_layout(self):
        # Top Bar
        self.top_bar = tk.Frame(self, bg="#2c3e50", height=60)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)

        tk.Label(self.top_bar, text="Vehicle Rental System", bg="#2c3e50", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        
        user_info = tk.Frame(self.top_bar, bg="#2c3e50")
        user_info.pack(side="right", padx=20)
        
        tk.Label(user_info, text=f"Welcome, {self.user.full_name}", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 12)).pack(side="left", padx=10)
        RoundedButton(user_info, width=80, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # 1. Left Sidebar (280px)
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=280)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.create_sidebar_button("Rent a Vehicle", "car.png", self.show_rent_view)
        self.create_sidebar_button("My Reservations", "rental.png", self.show_history_view)

        # 2. Middle List Pane (600px)
        self.list_pane = tk.Frame(self.main_container, bg="#f8f9fa", width=600)
        self.list_pane.pack(side="left", fill="y")
        self.list_pane.pack_propagate(False)

        # List Header / Filter Area
        self.list_header_frame = tk.Frame(self.list_pane, bg="#f8f9fa")
        self.list_header_frame.pack(fill="x", padx=20, pady=15)
        
        self.list_title = tk.Label(self.list_header_frame, text="Select Item", bg="#f8f9fa", font=("Segoe UI", 14, "bold"), anchor="w")
        self.list_title.pack(side="left", fill="x", expand=True)

        self.list_scroll = ScrollableFrame(self.list_pane, bg="#f8f9fa")
        self.list_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # 3. Right Detail Pane
        self.detail_pane = tk.Frame(self.main_container, bg="white")
        self.detail_pane.pack(side="left", fill="both", expand=True)
        
        self.detail_container = tk.Frame(self.detail_pane, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=40, pady=40)

        self.show_placeholder_detail()

    def create_sidebar_button(self, text, icon_name, command):
        # Fix path: go up from src/views/ to src/img/icons
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "src", "img", "icons", icon_name)
        if not os.path.exists(icon_path):
             # Try simpler path if running from root
             icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)
             
        btn = RoundedButton(self.side_bar, width=260, height=50, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command, image_path=icon_path)
        btn.pack(pady=5)

    def clear_list(self):
        # Clear filters if any (except title)
        for widget in self.list_header_frame.winfo_children():
            if widget != self.list_title:
                widget.destroy()
        # Clear scrolling list
        for widget in self.list_scroll.scrollable_frame.winfo_children():
            widget.destroy()

    def clear_detail(self):
        for widget in self.detail_container.winfo_children():
            widget.destroy()

    def show_placeholder_detail(self):
        self.clear_detail()
        tk.Label(self.detail_container, text="Select an item from the list to view details", 
                font=("Segoe UI", 14), fg="#bdc3c7", bg="white").pack(expand=True)

    def get_image_path(self, vehicle_or_res):
        return ImageHelper.get_vehicle_image_path(vehicle_or_res.get('model', ''))

    # --- RENT VIEW ---
    def show_rent_view(self):
        self.clear_list()
        self.show_placeholder_detail()
        self.list_title.config(text="Available Vehicles")
        
        # Filters in list header
        filter_frame = tk.Frame(self.list_header_frame, bg="#f8f9fa")
        filter_frame.pack(side="right")
        
        self.type_var = tk.StringVar(value="All")
        type_cb = ttk.Combobox(filter_frame, textvariable=self.type_var, values=["All", "Car", "Truck", "SUV", "Van", "Motorcycle"], width=10)
        type_cb.pack(side="left", padx=5)
        
        RoundedButton(filter_frame, width=70, height=30, corner_radius=8, bg_color="#3498db", fg_color="white", text="Filter", command=self.load_vehicles_list).pack(side="left", padx=5)

        self.load_vehicles_list()

    def load_vehicles_list(self):
        # Clear items only
        for widget in self.list_scroll.scrollable_frame.winfo_children():
            widget.destroy()
            
        vehicles = self.rental_controller.get_available_vehicles(self.type_var.get())
        for v in vehicles:
            self.create_vehicle_list_item(v)

    def create_vehicle_list_item(self, vehicle):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=540, height=120, corner_radius=10, bg_color="white")
        frame.pack(pady=5)
        
        img_path = self.get_image_path(vehicle)
        img = ImageHelper.load_image(img_path, size=(120, 80))
        
        if img:
            lbl = tk.Label(frame.inner_frame, image=img, bg="white")
            lbl.image = img
            lbl.pack(side="left", padx=15)
            
        text_frame = tk.Frame(frame.inner_frame, bg="white")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(text_frame, text=f"{vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(text_frame, text=f"{vehicle['year']} - {vehicle['type']}", font=("Segoe UI", 10), fg="#7f8c8d", bg="white").pack(anchor="w")
        tk.Label(text_frame, text=f"P{vehicle['daily_rate']}/day", font=("Segoe UI", 10, "bold"), fg="#27ae60", bg="white").pack(anchor="w")

        def on_click(e): self.show_rent_details(vehicle)
        frame.bind("<Button-1>", on_click)
        frame.inner_frame.bind("<Button-1>", on_click)
        text_frame.bind("<Button-1>", on_click)
        for child in text_frame.winfo_children():
            child.bind("<Button-1>", on_click)

    def show_rent_details(self, vehicle):
        self.clear_detail()
        
        tk.Label(self.detail_container, text=f"Rent {vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 10))

        img_path = self.get_image_path(vehicle)
        img = ImageHelper.load_image(img_path, size=(400, 250))
        if img:
            lbl = tk.Label(self.detail_container, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)

        # Details Grid
        details_frame = tk.Frame(self.detail_container, bg="white")
        details_frame.pack(fill="x", pady=10)
        
        tk.Label(details_frame, text="Daily Rate:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(details_frame, text=f"P{vehicle['daily_rate']}", font=("Segoe UI", 10), bg="white").grid(row=0, column=1, sticky="w", padx=10)
        
        tk.Label(details_frame, text="Type:", font=("Segoe UI", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w")
        tk.Label(details_frame, text=vehicle['type'], font=("Segoe UI", 10), bg="white").grid(row=1, column=1, sticky="w", padx=10)

        separator = ttk.Separator(self.detail_container, orient='horizontal')
        separator.pack(fill='x', pady=15)

        # Form
        form_frame = tk.Frame(self.detail_container, bg="white")
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
        tk.Checkbutton(form_frame, text="Add Insurance (+500/day)", variable=insurance_var, bg="white", font=("Segoe UI", 10)).pack(anchor="w", pady=10)

        tk.Label(form_frame, text="Equipment:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", pady=(10, 5))
        
        equipment_vars = {}
        equipments = self.rental_controller.get_equipment()
        for eq in equipments:
            var = tk.BooleanVar()
            equipment_vars[eq['equipment_id']] = var
            tk.Checkbutton(form_frame, text=f"{eq['name']} (+{eq['daily_rate']})", variable=var, bg="white").pack(anchor="w")

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
                
            eq_ids = [eid for eid, var in equipment_vars.items() if var.get()]
            
            if self.rental_controller.create_reservation(self.user.user_id, vehicle['vehicle_id'], s_date, e_date, insurance_var.get(), eq_ids):
                messagebox.showinfo("Success", "Reservation requested! Waiting for approval.")
                self.show_placeholder_detail()
                self.load_vehicles_list()
            else:
                messagebox.showerror("Error", "Failed to create reservation")

        RoundedButton(self.detail_container, width=200, height=45, corner_radius=10, 
                     bg_color="#27ae60", fg_color="white", text="Confirm Reservation", command=confirm_rent).pack(pady=30)


    # --- HISTORY VIEW ---
    def show_history_view(self):
        self.clear_list()
        self.show_placeholder_detail()
        self.list_title.config(text="My Reservations")
        
        reservations = self.rental_controller.get_user_reservations(self.user.user_id)
        for res in reservations:
            self.create_reservation_list_item(res)

    def create_reservation_list_item(self, res):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=540, height=120, corner_radius=10, bg_color="white")
        frame.pack(pady=5)
        
        img_path = self.get_image_path(res)
        img = ImageHelper.load_image(img_path, size=(120, 80))
        
        if img:
            lbl = tk.Label(frame.inner_frame, image=img, bg="white")
            lbl.image = img
            lbl.pack(side="left", padx=15)
            
        text_frame = tk.Frame(frame.inner_frame, bg="white")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(text_frame, text=f"{res['brand']} {res['model']}", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        
        status_colors = {'Pending': '#f39c12', 'Active': '#27ae60', 'Completed': '#3498db', 'Cancelled': '#e74c3c', 'Rejected': '#e74c3c'}
        color = status_colors.get(res['status'], 'black')
        
        tk.Label(text_frame, text=res['status'], font=("Segoe UI", 9, "bold"), fg=color, bg="white").pack(anchor="w")
        tk.Label(text_frame, text=f"{res['start_date']} - {res['end_date']}", font=("Segoe UI", 9), fg="#7f8c8d", bg="white").pack(anchor="w")

        def on_click(e): self.show_reservation_details(res)
        frame.bind("<Button-1>", on_click)
        frame.inner_frame.bind("<Button-1>", on_click)
        text_frame.bind("<Button-1>", on_click)
        for child in text_frame.winfo_children():
            child.bind("<Button-1>", on_click)

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
            'Active': 'Your reservation is active. Drive safely!',
            'Completed': 'This reservation has been completed. Thank you!',
            'Cancelled': 'This reservation was cancelled.',
            'Rejected': 'This reservation was rejected.'
        }
        msg = status_messages.get(res['status'], "")
        if msg:
            tk.Label(self.detail_container, text=msg, font=("Segoe UI", 11, "italic"), fg="#7f8c8d", bg="white").pack(pady=5)

        # Info
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=20)

        labels = [
            ("Vehicle:", f"{res['brand']} {res['model']}"),
            ("Start Date:", res['start_date']),
            ("End Date:", res['end_date']),
            ("Total Cost:", f"P{res['total_cost']}"),
            ("Status:", res['status'])
        ]
        
        for i, (l, v) in enumerate(labels):
            tk.Label(info_frame, text=l, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(info_frame, text=str(v), font=("Segoe UI", 10), bg="white").grid(row=i, column=1, sticky="w", padx=10, pady=3)

        # Actions
        if res['status'] in ['Pending', 'Active']:
             def cancel():
                 if messagebox.askyesno("Confirm", "Are you sure you want to cancel this reservation?"):
                     self.rental_controller.cancel_reservation(res['reservation_id'], res['vehicle_id'])
                     messagebox.showinfo("Success", "Reservation cancelled")
                     self.show_history_view() # reload list
                     self.show_placeholder_detail() # clear detail which is now invalid

             RoundedButton(self.detail_container, width=200, height=45, corner_radius=10, 
                          bg_color="#e74c3c", fg_color="white", text="Cancel Reservation", command=cancel).pack(pady=30)
'''

with open('src/views/member_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated member_dashboard.py")
