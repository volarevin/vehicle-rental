from src.database.db_manager import DBManager
from datetime import datetime

class RentalController:
    def __init__(self):
        self.db = DBManager()
        self._ensure_reservation_reason_columns()

    def _ensure_reservation_reason_columns(self):
        checks = [
            ("cancel_reason", "ALTER TABLE Reservations ADD COLUMN cancel_reason TEXT NULL"),
            ("reject_reason", "ALTER TABLE Reservations ADD COLUMN reject_reason TEXT NULL")
        ]

        for column_name, alter_sql in checks:
            result = self.db.fetch_one(
                """
                SELECT COUNT(*) AS count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'Reservations'
                  AND COLUMN_NAME = %s
                """,
                (column_name,)
            )
            if int((result or {}).get('count') or 0) == 0:
                self.db.execute_query(alter_sql)
                self.db.disconnect()

    def get_available_vehicles(self, vehicle_type=None):
        query = "SELECT * FROM Vehicles WHERE status = 'Available'"
        params = []
        if vehicle_type and vehicle_type != "All":
            query = query + " AND type = %s"
            params.append(vehicle_type)
        return self.db.fetch_all(query, tuple(params))

    def get_member_vehicle_catalog(self, vehicle_type=None):
        query = "SELECT * FROM Vehicles WHERE status IN ('Available', 'Maintenance')"
        params = []
        if vehicle_type and vehicle_type != "All":
            query = query + " AND type = %s"
            params.append(vehicle_type)
        query = query + " ORDER BY FIELD(status, 'Available', 'Maintenance'), brand, model"
        return self.db.fetch_all(query, tuple(params))

    def get_receptionist_dashboard_stats(self):
        active_rentals = self.db.fetch_one("SELECT COUNT(*) AS count FROM Reservations WHERE status = 'Active'")
        pending_requests = self.db.fetch_one("SELECT COUNT(*) AS count FROM Reservations WHERE status = 'Pending'")
        available_vehicles = self.db.fetch_one("SELECT COUNT(*) AS count FROM Vehicles WHERE status = 'Available'")
        due_today = self.db.fetch_one("SELECT COUNT(*) AS count FROM Reservations WHERE status = 'Active' AND end_date = CURDATE()")

        stats = {}
        stats['active_rentals'] = int((active_rentals or {}).get('count') or 0)
        stats['pending_requests'] = int((pending_requests or {}).get('count') or 0)
        stats['available_vehicles'] = int((available_vehicles or {}).get('count') or 0)
        stats['due_today'] = int((due_today or {}).get('count') or 0)
        return stats

    def create_reservation(self, user_id, vehicle_id, start_date, end_date, insurance):
        # Calculate days
        delta = (end_date - start_date).days
        if delta < 1:
            delta = 1
        
        # Get vehicle info and ensure it is rentable
        v_query = "SELECT daily_rate, status FROM Vehicles WHERE vehicle_id = %s"
        vehicle = self.db.fetch_one(v_query, (vehicle_id,))
        if not vehicle:
            return False

        if vehicle.get('status') != 'Available':
            return False

        base_cost = float(vehicle['daily_rate']) * delta

        total_cost = base_cost
        if insurance:
            total_cost = total_cost + (500 * delta) # Flat 500 per day for insurance

        # Insert Reservation as Pending (requires approval)
        ins_query = """
            INSERT INTO Reservations (user_id, vehicle_id, start_date, end_date, insurance_added, total_cost, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        """
        self.db.execute_query(ins_query, (user_id, vehicle_id, start_date, end_date, insurance, total_cost))
        
        # Vehicle remains Available until approved
        return True

    def get_user_reservations(self, user_id):
        query = """
            SELECT r.*, v.vehicle_id, v.brand, v.model, v.license_plate, v.image, v.type, v.year, v.daily_rate
            FROM Reservations r 
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id 
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(query, (user_id,))

    def get_pending_reservations(self):
        query = """
            SELECT r.*, v.brand, v.model, u.username, u.first_name, u.last_name, v.image 
            FROM Reservations r 
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id 
            JOIN Users u ON r.user_id = u.user_id
            WHERE r.status = 'Pending'
            ORDER BY r.created_at ASC
        """
        return self.db.fetch_all(query)

    def approve_reservation(self, reservation_id, auto_reject_reason=None):
        res_query = """
            SELECT reservation_id, vehicle_id, status
            FROM Reservations
            WHERE reservation_id = %s
        """
        reservation = self.db.fetch_one(res_query, (reservation_id,))
        if not reservation:
            return {'success': False, 'message': 'Reservation not found'}

        if reservation.get('status') != 'Pending':
            return {'success': False, 'message': 'Only pending reservations can be approved'}

        vehicle_id = reservation['vehicle_id']

        active_conflict = self.db.fetch_one(
            """
            SELECT reservation_id
            FROM Reservations
            WHERE vehicle_id = %s AND status = 'Active'
            LIMIT 1
            """,
            (vehicle_id,)
        )
        if active_conflict:
            return {'success': False, 'message': 'This vehicle already has an active rental'}

        conflicting_pending = self.db.fetch_one(
            """
            SELECT COUNT(*) AS count
            FROM Reservations
            WHERE vehicle_id = %s AND status = 'Pending' AND reservation_id <> %s
            """,
            (vehicle_id, reservation_id)
        )
        conflict_count = int((conflicting_pending or {}).get('count') or 0)

        if conflict_count > 0 and not auto_reject_reason:
            return {
                'success': False,
                'requires_reason': True,
                'conflict_count': conflict_count,
                'message': 'Rejection reason is required to auto-reject conflicting reservations'
            }

        approve_cursor = self.db.execute_query(
            "UPDATE Reservations SET status = 'Active' WHERE reservation_id = %s AND status = 'Pending'",
            (reservation_id,)
        )
        if approve_cursor is None or getattr(approve_cursor, 'rowcount', 0) == 0:
            self.db.disconnect()
            return {'success': False, 'message': 'Unable to approve reservation'}

        vehicle_cursor = self.db.execute_query(
            "UPDATE Vehicles SET status = 'Rented' WHERE vehicle_id = %s",
            (vehicle_id,)
        )
        if vehicle_cursor is None:
            self.db.disconnect()
            return {'success': False, 'message': 'Unable to update vehicle status'}

        auto_rejected_count = 0
        if conflict_count > 0:
            reject_cursor = self.db.execute_query(
                """
                UPDATE Reservations
                SET status = 'Rejected', total_cost = 0, reject_reason = %s
                WHERE vehicle_id = %s AND status = 'Pending' AND reservation_id <> %s
                """,
                (auto_reject_reason, vehicle_id, reservation_id)
            )
            if reject_cursor is None:
                self.db.disconnect()
                return {'success': False, 'message': 'Approved but failed to auto-reject conflicting requests'}
            auto_rejected_count = max(getattr(reject_cursor, 'rowcount', 0), 0)

        self.db.disconnect()
        return {
            'success': True,
            'auto_rejected_count': auto_rejected_count,
            'message': 'Reservation approved'
        }

    def reject_reservation(self, reservation_id, reason=None):
        # Update Reservation Status to Rejected
        upd_res = "UPDATE Reservations SET status = 'Rejected', total_cost = 0, reject_reason = %s WHERE reservation_id = %s"
        result = self.db.execute_query(upd_res, (reason, reservation_id))
        if result is None:
            fallback = self.db.execute_query("UPDATE Reservations SET status = 'Rejected', total_cost = 0 WHERE reservation_id = %s", (reservation_id,))
            if fallback is None:
                return False
        
        # Vehicle remains Available
        return True

    def return_vehicle(self, reservation_id, vehicle_id, condition_notes, user_id=None):
        # Update Reservation
        upd_res = "UPDATE Reservations SET status = 'Completed' WHERE reservation_id = %s"
        self.db.execute_query(upd_res, (reservation_id,))

        # Update Vehicle
        upd_veh = "UPDATE Vehicles SET status = 'Available' WHERE vehicle_id = %s"
        self.db.execute_query(upd_veh, (vehicle_id,))

        # Log Return
        log_query = """
            INSERT INTO Vehicle_Logs (vehicle_id, user_id, event_type, description)
            VALUES (%s, %s, 'Return', %s)
        """
        self.db.execute_query(log_query, (vehicle_id, user_id, condition_notes))
        return True

    def get_all_vehicles(self):
        return self.db.fetch_all("SELECT * FROM Vehicles")

    def add_vehicle(self, brand, model, year, license_plate, v_type, rate, image=None):
        query = """
            INSERT INTO Vehicles (brand, model, year, license_plate, type, daily_rate, image, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available')
        """
        self.db.execute_query(query, (brand, model, year, license_plate, v_type, rate, image))
        return True

    def delete_vehicle(self, vehicle_id):
        query = "DELETE FROM Vehicles WHERE vehicle_id = %s"
        self.db.execute_query(query, (vehicle_id,))
        return True

    def cancel_reservation(self, reservation_id, vehicle_id, reason=None):
        # Get current status
        status_query = "SELECT status FROM Reservations WHERE reservation_id = %s"
        res = self.db.fetch_one(status_query, (reservation_id,))
        if not res:
            return False
        
        # Only allow cancellation of pending or active reservations
        if res['status'] not in ['Pending', 'Active']:
            return False
        
        # Update Reservation Status
        upd_res = "UPDATE Reservations SET status = 'Cancelled', total_cost = 0, cancel_reason = %s WHERE reservation_id = %s"
        result = self.db.execute_query(upd_res, (reason, reservation_id))
        if result is None:
            fallback = self.db.execute_query("UPDATE Reservations SET status = 'Cancelled', total_cost = 0 WHERE reservation_id = %s", (reservation_id,))
            if fallback is None:
                return False
        
        # Make vehicle available again for both pending and active reservations
        upd_veh = "UPDATE Vehicles SET status = 'Available' WHERE vehicle_id = %s"
        upd_result = self.db.execute_query(upd_veh, (vehicle_id,))
        if upd_result is None:
            return False
        return True

    def update_vehicle(self, vehicle_id, brand, model, year, license_plate, v_type, rate, image=None):
        if image:
            query = """
                UPDATE Vehicles 
                SET brand=%s, model=%s, year=%s, license_plate=%s, type=%s, daily_rate=%s, image=%s
                WHERE vehicle_id=%s
            """
            self.db.execute_query(query, (brand, model, year, license_plate, v_type, rate, image, vehicle_id))
        else:
            query = """
                UPDATE Vehicles 
                SET brand=%s, model=%s, year=%s, license_plate=%s, type=%s, daily_rate=%s
                WHERE vehicle_id=%s
            """
            self.db.execute_query(query, (brand, model, year, license_plate, v_type, rate, vehicle_id))
        return True

    def set_vehicle_status(self, vehicle_id, status):
        query = "UPDATE Vehicles SET status = %s WHERE vehicle_id = %s"
        self.db.execute_query(query, (status, vehicle_id))
        return True

    def get_all_active_rentals(self):
        query = """
            SELECT r.*, v.brand, v.model, v.license_plate, v.image, u.username 
            FROM Reservations r 
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id 
            JOIN Users u ON r.user_id = u.user_id 
            WHERE r.status = 'Active' 
            ORDER BY r.end_date ASC
        """
        return self.db.fetch_all(query)

    def get_vehicle_rental_history(self, vehicle_id):
        query = """
            SELECT r.*, u.first_name, u.last_name, u.username
            FROM Reservations r
            JOIN Users u ON r.user_id = u.user_id
            WHERE r.vehicle_id = %s
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(query, (vehicle_id,))

    def get_vehicle_return_logs(self, vehicle_id):
        query = """
            SELECT log_date, description
            FROM Vehicle_Logs
            WHERE vehicle_id = %s AND event_type = 'Return'
            ORDER BY log_date DESC
        """
        return self.db.fetch_all(query, (vehicle_id,))

