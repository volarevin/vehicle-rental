from src.database.db_manager import DBManager
import bcrypt

class AdminController:
    def __init__(self):
        self.db = DBManager()

    def get_dashboard_stats(self):
        stats = {}
        
        # Total Earnings (Completed or Active, excluding Cancelled)
        query_earnings = "SELECT SUM(total_cost) as total FROM Reservations WHERE status != 'Cancelled'"
        res_earnings = self.db.fetch_one(query_earnings)
        stats['total_earnings'] = res_earnings['total'] if res_earnings and res_earnings['total'] else 0.0

        # Active Rentals
        query_active = "SELECT COUNT(*) as count FROM Reservations WHERE status = 'Active'"
        res_active = self.db.fetch_one(query_active)
        stats['active_rentals'] = res_active['count'] if res_active else 0

        # Total Users
        query_users = "SELECT COUNT(*) as count FROM Users"
        res_users = self.db.fetch_one(query_users)
        stats['total_users'] = res_users['count'] if res_users else 0

        # Total Vehicles
        query_vehicles = "SELECT COUNT(*) as count FROM Vehicles"
        res_vehicles = self.db.fetch_one(query_vehicles)
        stats['total_vehicles'] = res_vehicles['count'] if res_vehicles else 0

        return stats

    def get_all_reservations(self):
        query = """
            SELECT r.reservation_id, u.username, v.brand, v.model, r.start_date, r.end_date, r.total_cost, r.status
            FROM Reservations r
            JOIN Users u ON r.user_id = u.user_id
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(query)

    def get_earnings_by_type(self):
        query = """
            SELECT v.type, SUM(r.total_cost) as earnings
            FROM Reservations r
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.status != 'Cancelled'
            GROUP BY v.type
        """
        return self.db.fetch_all(query)

    def get_all_users(self):
        return self.db.fetch_all("SELECT user_id, username, first_name, last_name, role FROM Users")

    def add_user(self, username, password, first_name, last_name, role):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = """
            INSERT INTO Users (username, password_hash, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute_query(query, (username, hashed, first_name, last_name, role))
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE user_id = %s"
        self.db.execute_query(query, (user_id,))
        return True
