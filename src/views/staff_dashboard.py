import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.rental_controller import RentalController
from src.utils.image_helper import ImageHelper
from src.utils.gui_helpers import RoundedFrame, RoundedButton, ScrollableFrame
import os

class StaffDashboard(tk.Frame):
    def __init__(self, parent, user, logout_callback):
        super().__init__(parent)
        self.user = user
        self.logout_callback = logout_callback
        self.rental_controller = RentalController()
        self.pack(fill="both", expand=True)
        
        self.create_layout()
        self.show_returns_view()

    def create_layout(self):
        # Top Bar
        self.top_bar = tk.Frame(self, bg="#2c3e50", height=60)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)

        role_title = "Receptionist" if self.user.role == "Receptionist" else "Worker"
        tk.Label(self.top_bar, text=f"{role_title} Dashboard", bg="#2c3e50", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        
        user_info = tk.Frame(self.top_bar, bg="#2c3e50")
        user_info.pack(side="right", padx=20)
        
        tk.Label(user_info, text=f"User: {self.user.full_name}", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 12)).pack(side="left", padx=10)
        RoundedButton(user_info, width=80, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # Side Bar
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=200)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.create_sidebar_button("Process Returns", self.show_returns_view)
        if self.user.role == "Receptionist":
            self.create_sidebar_button("Manage Fleet", self.show_fleet_view)

        # Content Area
        self.content_area = tk.Frame(self.main_container, bg="white")
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def create_sidebar_button(self, text, command):
        btn = RoundedButton(self.side_bar, width=180, height=40, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command)
        btn.pack(pady=5)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_returns_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Process Returns", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.returns_frame = tk.Frame(self.content_area, bg="white")
        self.returns_frame.pack(fill="both", expand=True)
        self.setup_returns_view()

    def show_fleet_view(self):
        self.clear_content()
        tk.Label(self.content_area, text="Manage Fleet", font=("Segoe UI", 20, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        self.fleet_frame = tk.Frame(self.content_area, bg="white")
        self.fleet_frame.pack(fill="both", expand=True)
        self.setup_fleet_view()

    def setup_returns_view(self):
        self.ret_scroll = ScrollableFrame(self.returns_frame)
        self.ret_scroll.pack(fill="both", expand=True, padx=10)
        self.load_rentals()

    def load_rentals(self):
        for widget in self.ret_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        rentals = self.rental_controller.get_all_active_rentals()
        
        columns = 3
        row = 0
        col = 0

        for r in rentals:
            self.create_rental_card(r, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def create_rental_card(self, rental, row, col):
        card = RoundedFrame(self.ret_scroll.scrollable_frame, width=280, height=220, corner_radius=15, bg_color="#f8f9fa")
        card.grid(row=row, column=col, padx=10, pady=10)

        # Image
        img_path = self.get_image_path(rental['model'])
        img = ImageHelper.load_resized_image(img_path, size=(150, 100))
        if img:
            lbl = tk.Label(card.inner_frame, image=img, bg="#f8f9fa")
            lbl.image = img
            lbl.pack(pady=5)

        tk.Label(card.inner_frame, text=f"{rental['brand']} {rental['model']}", font=("Segoe UI", 11, "bold"), bg="#f8f9fa").pack()
        tk.Label(card.inner_frame, text=f"Rented by: {rental['username']}", font=("Segoe UI", 9), bg="#f8f9fa").pack()
        tk.Label(card.inner_frame, text=f"Due: {rental['end_date']}", font=("Segoe UI", 9, "bold"), fg="#e74c3c", bg="#f8f9fa").pack()

        # Click
        card.bind("<Button-1>", lambda e, r=rental: self.show_return_popup(r))
        card.inner_frame.bind("<Button-1>", lambda e, r=rental: self.show_return_popup(r))
        for child in card.inner_frame.winfo_children():
            child.bind("<Button-1>", lambda e, r=rental: self.show_return_popup(r))

    def show_return_popup(self, rental):
        popup = tk.Toplevel(self)
        popup.title(f"Return Vehicle - {rental['brand']} {rental['model']}")
        popup.geometry("400x500")
        popup.configure(bg="white")
        popup.grab_set()

        tk.Label(popup, text="Process Return", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)
        
        info = f"""
        Reservation ID: {rental['reservation_id']}
        Customer: {rental['username']}
        Vehicle: {rental['brand']} {rental['model']}
        Due Date: {rental['end_date']}
        """
        tk.Label(popup, text=info, justify="left", bg="white", font=("Segoe UI", 10)).pack(pady=10)

        tk.Label(popup, text="Condition Notes:", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
        notes_entry = tk.Entry(popup, width=40)
        notes_entry.pack(padx=20, pady=5)

        def confirm():
            notes = notes_entry.get() or "Standard return"
            try:
                self.rental_controller.return_vehicle(rental['reservation_id'], rental['vehicle_id'], notes)
                messagebox.showinfo("Success", "Vehicle returned successfully")
                popup.destroy()
                self.load_rentals()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Confirm Return", command=confirm, bg="#f39c12", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", pady=10).pack(fill="x", padx=20, pady=20)

    def setup_fleet_view(self):
        # Add Vehicle Button (Opens Popup)
        RoundedButton(self.fleet_frame, width=200, height=40, corner_radius=10, bg_color="#27ae60", fg_color="white", 
                      text="+ Add New Vehicle", command=self.show_add_vehicle_popup).pack(fill="x", padx=20, pady=10)

        self.fleet_scroll = ScrollableFrame(self.fleet_frame)
        self.fleet_scroll.pack(fill="both", expand=True, padx=10)
        self.load_fleet()

    def load_fleet(self):
        for widget in self.fleet_scroll.scrollable_frame.winfo_children():
            widget.destroy()
        
        vehicles = self.rental_controller.get_all_vehicles()
        
        columns = 3
        row = 0
        col = 0

        for v in vehicles:
            self.create_fleet_card(v, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def create_fleet_card(self, vehicle, row, col):
        card = RoundedFrame(self.fleet_scroll.scrollable_frame, width=280, height=220, corner_radius=15, bg_color="#f8f9fa")
        card.grid(row=row, column=col, padx=10, pady=10)

        # Image
        img_path = self.get_image_path(vehicle['model'])
        img = ImageHelper.load_resized_image(img_path, size=(150, 100))
        if img:
            lbl = tk.Label(card.inner_frame, image=img, bg="#f8f9fa")
            lbl.image = img
            lbl.pack(pady=5)

        tk.Label(card.inner_frame, text=f"{vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 11, "bold"), bg="#f8f9fa").pack()
        tk.Label(card.inner_frame, text=f"{vehicle['license_plate']}", font=("Segoe UI", 9), bg="#f8f9fa", fg="#7f8c8d").pack()
        tk.Label(card.inner_frame, text=f"Status: {vehicle['status']}", font=("Segoe UI", 9, "bold"), 
                 fg="green" if vehicle['status']=='Available' else "red", bg="#f8f9fa").pack(pady=5)

        # Click
        card.bind("<Button-1>", lambda e, v=vehicle: self.show_edit_vehicle_popup(v))
        card.inner_frame.bind("<Button-1>", lambda e, v=vehicle: self.show_edit_vehicle_popup(v))
        for child in card.inner_frame.winfo_children():
            child.bind("<Button-1>", lambda e, v=vehicle: self.show_edit_vehicle_popup(v))

    def show_add_vehicle_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New Vehicle")
        popup.geometry("400x500")
        popup.configure(bg="white")
        popup.grab_set()

        self._create_vehicle_form(popup, is_edit=False)

    def show_edit_vehicle_popup(self, vehicle):
        popup = tk.Toplevel(self)
        popup.title(f"Edit {vehicle['brand']} {vehicle['model']}")
        popup.geometry("400x500")
        popup.configure(bg="white")
        popup.grab_set()

        self._create_vehicle_form(popup, is_edit=True, vehicle=vehicle)

    def _create_vehicle_form(self, popup, is_edit, vehicle=None):
        tk.Label(popup, text="Vehicle Details", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)
        
        form = tk.Frame(popup, bg="white")
        form.pack(padx=20, pady=10)

        entries = {}
        fields = ["Brand", "Model", "Year", "License Plate", "Type", "Daily Rate"]
        keys = ["brand", "model", "year", "license_plate", "type", "daily_rate"]

        for i, field in enumerate(fields):
            tk.Label(form, text=f"{field}:", bg="white").grid(row=i, column=0, sticky="e", pady=5)
            if field == "Type":
                entry = ttk.Combobox(form, values=["Car", "Truck", "SUV", "Van", "Motorcycle"])
            else:
                entry = tk.Entry(form)
            
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            entries[keys[i]] = entry
            
            if is_edit and vehicle:
                if field == "Type":
                    entry.set(vehicle[keys[i]])
                else:
                    entry.insert(0, str(vehicle[keys[i]]))

        def save():
            data = {k: entries[k].get() for k in keys}
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                if is_edit:
                    self.rental_controller.update_vehicle(vehicle['vehicle_id'], data['brand'], data['model'], 
                                                        data['year'], data['license_plate'], data['type'], data['daily_rate'])
                    messagebox.showinfo("Success", "Vehicle updated")
                else:
                    self.rental_controller.add_vehicle(data['brand'], data['model'], data['year'], 
                                                     data['license_plate'], data['type'], data['daily_rate'])
                    messagebox.showinfo("Success", "Vehicle added")
                popup.destroy()
                self.load_fleet()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Save Vehicle", command=save, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", pady=5).pack(fill="x", padx=20, pady=10)

        if is_edit:
            def delete():
                if messagebox.askyesno("Confirm", "Delete this vehicle?"):
                    self.rental_controller.delete_vehicle(vehicle['vehicle_id'])
                    popup.destroy()
                    self.load_fleet()
            
            tk.Button(popup, text="Delete Vehicle", command=delete, bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", pady=5).pack(fill="x", padx=20, pady=(0, 20))

    def get_image_path(self, model):
        base_path = os.path.join(os.path.dirname(__file__), "..", "img", "vehicles")
        clean_model = model.replace(" ", "")
        candidates = [
            f"{model}.jpg", f"{model}.png",
            f"{model.lower()}.jpg", f"{model.lower()}.png",
            f"{clean_model}.jpg", f"{clean_model}.png",
            f"{clean_model.lower()}.jpg", f"{clean_model.lower()}.png"
        ]
        for c in candidates:
            p = os.path.join(base_path, c)
            if os.path.exists(p):
                return p
        return ""

    def process_return(self):
        pass # Replaced by popup logic

    def add_vehicle(self):
        pass # Replaced by popup logic






