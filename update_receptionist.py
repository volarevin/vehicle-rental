I've created the `update_receptionist.py` script and executed it to update `src/views/receptionist_dashboard.py` with the new content.

Here is the full content of `update_receptionist.py`:

```python
import os

content = r'''import tkinter as tk
from tkinter import ttk, messagebox
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
        RoundedButton(user_info, width=80, height=30, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Logout", command=self.logout_callback).pack(side="left")

        # Main Container
        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        # 1. Left Sidebar
        self.side_bar = tk.Frame(self.main_container, bg="#34495e", width=280)
        self.side_bar.pack(side="left", fill="y")
        self.side_bar.pack_propagate(False)

        self.create_sidebar_button("Process Returns", "return.png", self.show_returns_view)
        self.create_sidebar_button("Approve Requests", "list.png", self.show_approvals_view)
        self.create_sidebar_button("Manage Fleet", "car.png", self.show_fleet_view)

        # 2. Middle List Pane
        self.list_pane = tk.Frame(self.main_container, bg="#f8f9fa", width=400)
        self.list_pane.pack(side="left", fill="y")
        self.list_pane.pack_propagate(False)
        
        # Header for List Pane
        self.list_header = tk.Label(self.list_pane, text="Select Item", bg="#f8f9fa", font=("Segoe UI", 14, "bold"), anchor="w", padx=20, pady=15)
        self.list_header.pack(fill="x")
        
        self.list_scroll = ScrollableFrame(self.list_pane, bg="#f8f9fa")
        self.list_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # 3. Right Detail Pane
        self.detail_pane = tk.Frame(self.main_container, bg="white")
        self.detail_pane.pack(side="left", fill="both", expand=True)
        
        # Container inside detail pane so we can clear it easily
        self.detail_container = tk.Frame(self.detail_pane, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=40, pady=40)

        self.show_placeholder_detail()

    def create_sidebar_button(self, text, icon_name, command):
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "src", "img", "icons", icon_name)
        # Fix path logic if needed, but relative to this file: ../img/icons
        icon_path = os.path.join(os.path.dirname(__file__), "..", "img", "icons", icon_name)
        
        btn = RoundedButton(self.side_bar, width=260, height=50, corner_radius=10, bg_color="#34495e", fg_color="white", text=text, command=command, image_path=icon_path)
        btn.pack(pady=5)

    def clear_list(self):
        for widget in self.list_scroll.scrollable_frame.winfo_children():
            widget.destroy()

    def clear_detail(self):
        for widget in self.detail_container.winfo_children():
            widget.destroy()

    def show_placeholder_detail(self):
        self.clear_detail()
        tk.Label(self.detail_container, text="Select an item from the list to view details", 
                font=("Segoe UI", 14), fg="#bdc3c7", bg="white").pack(expand=True)

    # --- View Switchers ---

    def show_returns_view(self):
        self.list_header.config(text="Active Rentals")
        self.clear_list()
        self.show_placeholder_detail()
        
        rentals = self.rental_controller.get_all_active_rentals()
        for r in rentals:
            self.create_rental_list_item(r)

    def show_approvals_view(self):
        self.list_header.config(text="Pending Requests")
        self.clear_list()
        self.show_placeholder_detail()
        
        pending = self.rental_controller.get_pending_reservations()
        for p in pending:
            self.create_approval_list_item(p)

    def show_fleet_view(self):
        self.list_header.config(text="Vehicle Fleet")
        self.clear_list()
        self.show_placeholder_detail()
        
        # Add New Vehicle Button at top of list
        add_btn = RoundedButton(self.list_scroll.scrollable_frame, width=340, height=40, corner_radius=10, 
                               bg_color="#27ae60", fg_color="white", text="+ Add New Vehicle", 
                               command=self.show_add_vehicle_form)
        add_btn.pack(pady=(0, 15))
        
        vehicles = self.rental_controller.get_all_vehicles()
        for v in vehicles:
            self.create_fleet_list_item(v)

    # --- List Items Creation ---

    def create_rental_list_item(self, rental):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=350, height=100, corner_radius=10, bg_color="white")
        frame.pack(pady=5)
        
        # Content
        tk.Label(frame.inner_frame, text=f"{rental['brand']} {rental['model']}", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame.inner_frame, text=f"Customer: {rental['username']}", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        tk.Label(frame.inner_frame, text=f"Due: {rental['end_date']}", font=("Segoe UI", 9, "bold"), fg="#e74c3c", bg="white").pack(anchor="w", pady=(5,0))
        
        # Click handler
        frame.bind("<Button-1>", lambda e: self.show_return_details(rental))
        frame.inner_frame.bind("<Button-1>", lambda e: self.show_return_details(rental))
        for child in frame.inner_frame.winfo_children():
            child.bind("<Button-1>", lambda e: self.show_return_details(rental))

    def create_approval_list_item(self, reservation):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=350, height=100, corner_radius=10, bg_color="white")
        frame.pack(pady=5)
        
        tk.Label(frame.inner_frame, text=f"{reservation['brand']} {reservation['model']}", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame.inner_frame, text=f"User: {reservation['username']}", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        tk.Label(frame.inner_frame, text=f"Total: â‚±{reservation['total_cost']}", font=("Segoe UI", 9, "bold"), fg="#27ae60", bg="white").pack(anchor="w", pady=(5,0))
        
        frame.bind("<Button-1>", lambda e: self.show_approval_details(reservation))
        frame.inner_frame.bind("<Button-1>", lambda e: self.show_approval_details(reservation))
        for child in frame.inner_frame.winfo_children():
            child.bind("<Button-1>", lambda e: self.show_approval_details(reservation))

    def create_fleet_list_item(self, vehicle):
        frame = RoundedFrame(self.list_scroll.scrollable_frame, width=350, height=100, corner_radius=10, bg_color="white")
        frame.pack(pady=5)
        
        status_color = "#27ae60" if vehicle['status'] == 'Available' else "#e74c3c"
        
        tk.Label(frame.inner_frame, text=f"{vehicle['brand']} {vehicle['model']}", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame.inner_frame, text=f"{vehicle['license_plate']}", font=("Segoe UI", 9), bg="white", fg="#7f8c8d").pack(anchor="w")
        tk.Label(frame.inner_frame, text=vehicle['status'], font=("Segoe UI", 9, "bold"), fg=status_color, bg="white").pack(anchor="w", pady=(5,0))
        
        frame.bind("<Button-1>", lambda e: self.show_fleet_details(vehicle))
        frame.inner_frame.bind("<Button-1>", lambda e: self.show_fleet_details(vehicle))
        for child in frame.inner_frame.winfo_children():
            child.bind("<Button-1>", lambda e: self.show_fleet_details(vehicle))

    # --- Detail Views ---

    def show_return_details(self, rental):
        self.clear_detail()
        
        # Header
        tk.Label(self.detail_container, text="Return Vehicle", font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        # Info Grid
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        # Image
        img_path = self.get_image_path(rental)
        img = ImageHelper.load_image(img_path, size=(300, 200))
        if img:
            lbl = tk.Label(info_frame, image=img, bg="white")
            lbl.image = img
            lbl.grid(row=0, column=0, rowspan=5, padx=(0, 30))

        # Details
        labels = [
            ("Reservation ID:", rental['reservation_id']),
            ("Customer:", rental['username']),
            ("Vehicle:", f"{rental['brand']} {rental['model']}"),
            ("License Plate:", rental['license_plate']),
            ("Due Date:", rental['end_date'])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(info_frame, text=label, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=1, sticky="w", pady=5)
            tk.Label(info_frame, text=str(value), font=("Segoe UI", 10), bg="white").grid(row=i, column=2, sticky="w", padx=10, pady=5)

        # Action Area
        tk.Label(self.detail_container, text="Return Processing", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(30, 10))
        
        tk.Label(self.detail_container, text="Condition Notes:", bg="white", font=("Segoe UI", 10)).pack(anchor="w")
        notes_entry = tk.Entry(self.detail_container, font=("Segoe UI", 11), width=50)
        notes_entry.pack(anchor="w", pady=5)
        
        def confirm():
            notes = notes_entry.get() or "Standard return"
            if self.rental_controller.return_vehicle(rental['reservation_id'], rental['vehicle_id'], notes, self.user.user_id):
                messagebox.showinfo("Success", "Vehicle returned successfully")
                self.show_returns_view() # Refresh list
            else:
                messagebox.showerror("Error", "Failed to return vehicle")

        RoundedButton(self.detail_container, width=200, height=45, corner_radius=10, 
                     bg_color="#f39c12", fg_color="white", text="Confirm Return", command=confirm).pack(anchor="w", pady=20)


    def show_approval_details(self, reservation):
        self.clear_detail()
        
        tk.Label(self.detail_container, text="Review Rental Request", font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        img_path = self.get_image_path(reservation)
        img = ImageHelper.load_image(img_path, size=(300, 200))
        if img:
            lbl = tk.Label(info_frame, image=img, bg="white")
            lbl.image = img
            lbl.grid(row=0, column=0, rowspan=6, padx=(0, 30))

        labels = [
            ("Vehicle:", f"{reservation['brand']} {reservation['model']}"),
            ("Customer:", f"{reservation['first_name']} {reservation['last_name']} ({reservation['username']})"),
            ("Dates:", f"{reservation['start_date']} to {reservation['end_date']}"),
            ("Total Cost:", f"â‚±{reservation['total_cost']}"),
            ("Insurance:", "Yes" if reservation['insurance_added'] else "No"),
            ("Status:", reservation['status'])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(info_frame, text=label, font=("Segoe UI", 10, "bold"), bg="white").grid(row=i, column=1, sticky="w", pady=5)
            tk.Label(info_frame, text=str(value), font=("Segoe UI", 10), bg="white").grid(row=i, column=2, sticky="w", padx=10, pady=5)

        tk.Label(self.detail_container, text="Actions", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", pady=(30, 10))
        
        btn_frame = tk.Frame(self.detail_container, bg="white")
        btn_frame.pack(anchor="w")
        
        def approve():
            if self.rental_controller.approve_reservation(reservation['reservation_id']):
                messagebox.showinfo("Success", "Rental approved")
                self.show_approvals_view()
            else:
                messagebox.showerror("Error", "Failed to approve")

        def reject():
            if self.rental_controller.reject_reservation(reservation['reservation_id']):
                messagebox.showinfo("Success", "Rental rejected")
                self.show_approvals_view()
            else:
                 messagebox.showerror("Error", "Failed to reject")

        RoundedButton(btn_frame, width=150, height=45, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Approve", command=approve).pack(side="left", padx=(0, 10))
        RoundedButton(btn_frame, width=150, height=45, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Reject", command=reject).pack(side="left")


    def show_fleet_details(self, vehicle):
        self.clear_detail()
        self._create_fleet_form(is_edit=True, vehicle=vehicle)

    def show_add_vehicle_form(self):
        self.clear_detail()
        self._create_fleet_form(is_edit=False)

    def _create_fleet_form(self, is_edit, vehicle=None):
        title = f"Edit {vehicle['brand']} {vehicle['model']}" if is_edit else "Add New Vehicle"
        tk.Label(self.detail_container, text=title, font=("Segoe UI", 24, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        current_image_path = None
        if is_edit and vehicle:
            # Show current image
            img_path = self.get_image_path(vehicle)
            img = ImageHelper.load_image(img_path, size=(300, 200))
            if img:
                lbl = tk.Label(self.detail_container, image=img, bg="white")
                lbl.image = img
                lbl.pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self.detail_container, bg="white")
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

        # Image Selection
        tk.Label(form, text="Image", font=("Segoe UI", 10, "bold"), bg="white").grid(row=len(fields), column=0, sticky="w", pady=10)
        img_entry_frame = tk.Frame(form, bg="white")
        img_entry_frame.grid(row=len(fields), column=1, sticky="w", padx=20, pady=10)
        
        self.img_path_var = tk.StringVar()
        tk.Entry(img_entry_frame, textvariable=self.img_path_var, width=20).pack(side="left")
        tk.Button(img_entry_frame, text="Browse", command=self.browse_image).pack(side="left", padx=5)

        # Buttons
        btn_frame = tk.Frame(self.detail_container, bg="white")
        btn_frame.pack(anchor="w", pady=30)

        def save():
            data = {k: entries[k].get() for k in keys}
            new_image_path = self.img_path_var.get()
            
            if not all(data.values()): # Basic validation
                 messagebox.showerror("Error", "All text fields are required")
                 return

            final_image_filename = vehicle['image'] if (is_edit and vehicle) else None
            
            if new_image_path:
                try:
                    ext = os.path.splitext(new_image_path)[1]
                    clean_model = data['model'].replace(" ", "").lower()
                    final_image_filename = f"{clean_model}{ext}"
                    dest_path = os.path.join(os.path.dirname(__file__), "..", "img", "vehicles", final_image_filename)
                    # Create dir if not exists
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
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

        RoundedButton(btn_frame, width=150, height=45, corner_radius=10, bg_color="#27ae60", fg_color="white", text="Save Vehicle", command=save).pack(side="left", padx=(0, 20))

        if is_edit:
            def delete():
                if messagebox.askyesno("Confirm", "Delete this vehicle?"):
                    try:
                        self.rental_controller.delete_vehicle(vehicle['vehicle_id'])
                        messagebox.showinfo("Success", "Vehicle deleted")
                        self.show_fleet_view()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            
            RoundedButton(btn_frame, width=150, height=45, corner_radius=10, bg_color="#e74c3c", fg_color="white", text="Delete", command=delete).pack(side="left")

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.img_path_var.set(file_path)

    def get_image_path(self, item):
        # Delegate to ImageHelper logic or recreate needed logic
        return ImageHelper.get_vehicle_image(item.get('model', '')) # Simple lookup
'''

with open(r'c:\Users\blond\Desktop\rental\src\views\receptionist_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated receptionist_dashboard.py successfully")
```
