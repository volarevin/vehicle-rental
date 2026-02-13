from src.database.db_manager import DBManager
import bcrypt

class AdminController:
    def __init__(self):
        self.db = DBManager()

    def get_dashboard_stats(self):
        stats = {}
        
        # Total Earnings 
        query_earnings = "SELECT SUM(total_cost) as total FROM Reservations WHERE status NOT IN ('Cancelled', 'Rejected')"
        res_earnings = self.db.fetch_one(query_earnings)
        if res_earnings and res_earnings['total']:
            stats['total_earnings'] = res_earnings['total']
        else:
            stats['total_earnings'] = 0.0

        # Active Rentals
        query_active = "SELECT COUNT(*) as count FROM Reservations WHERE status = 'Active'"
        res_active = self.db.fetch_one(query_active)
        if res_active:
            stats['active_rentals'] = res_active['count']
        else:
            stats['active_rentals'] = 0

        # Total Users
        query_users = "SELECT COUNT(*) as count FROM Users"
        res_users = self.db.fetch_one(query_users)
        if res_users:
            stats['total_users'] = res_users['count']
        else:
            stats['total_users'] = 0

        # Total Vehicles
        query_vehicles = "SELECT COUNT(*) as count FROM Vehicles"
        res_vehicles = self.db.fetch_one(query_vehicles)
        if res_vehicles:
            stats['total_vehicles'] = res_vehicles['count']
        else:
            stats['total_vehicles'] = 0

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
            WHERE r.status NOT IN ('Cancelled', 'Rejected')
            GROUP BY v.type
        """
        return self.db.fetch_all(query)

    def get_available_analytics_months(self):
        query = """
            SELECT DISTINCT
                DATE_FORMAT(start_date, '%Y-%m') AS month_key,
                DATE_FORMAT(start_date, '%b %Y') AS month_label
            FROM Reservations
            ORDER BY month_key DESC
        """
        return self.db.fetch_all(query)

    def get_filtered_analytics_summary(self, month_key='All', status='All'):
        conditions = []
        params = []

        if month_key and month_key != 'All':
            conditions.append("DATE_FORMAT(r.start_date, '%Y-%m') = %s")
            params.append(month_key)
        if status and status != 'All':
            conditions.append("r.status = %s")
            params.append(status)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT
                COUNT(*) AS reservation_count,
                COALESCE(SUM(CASE WHEN r.status NOT IN ('Cancelled', 'Rejected') THEN r.total_cost ELSE 0 END), 0) AS total_revenue,
                COALESCE(AVG(CASE WHEN r.status NOT IN ('Cancelled', 'Rejected') THEN r.total_cost END), 0) AS avg_revenue,
                COUNT(DISTINCT r.user_id) AS customer_count,
                COUNT(DISTINCT r.vehicle_id) AS vehicle_count
            FROM Reservations r
            {where_clause}
        """
        result = self.db.fetch_one(query, tuple(params))
        if not result:
            result = {}
        return {
            'reservation_count': int(result.get('reservation_count') or 0),
            'total_revenue': float(result.get('total_revenue') or 0),
            'avg_revenue': float(result.get('avg_revenue') or 0),
            'customer_count': int(result.get('customer_count') or 0),
            'vehicle_count': int(result.get('vehicle_count') or 0)
        }

    def get_filtered_earnings_by_type(self, month_key='All', status='All'):
        conditions = ["r.status NOT IN ('Cancelled', 'Rejected')"]
        params = []

        if month_key and month_key != 'All':
            conditions.append("DATE_FORMAT(r.start_date, '%Y-%m') = %s")
            params.append(month_key)
        if status and status != 'All':
            conditions.append("r.status = %s")
            params.append(status)

        where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT v.type, COALESCE(SUM(r.total_cost), 0) AS earnings
            FROM Reservations r
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            {where_clause}
            GROUP BY v.type
            ORDER BY earnings DESC
        """
        return self.db.fetch_all(query, tuple(params))

    def get_filtered_reservation_status_breakdown(self, month_key='All'):
        conditions = []
        params = []

        if month_key and month_key != 'All':
            conditions.append("DATE_FORMAT(start_date, '%Y-%m') = %s")
            params.append(month_key)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT status, COUNT(*) AS total
            FROM Reservations
            {where_clause}
            GROUP BY status
            ORDER BY total DESC
        """
        return self.db.fetch_all(query, tuple(params))

    def get_monthly_earnings_data(self):
        query = "SELECT DATE_FORMAT(start_date, '%d') as day, SUM(total_cost) as total FROM Reservations WHERE DATE_FORMAT(start_date, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m') AND status NOT IN ('Cancelled', 'Rejected') GROUP BY day ORDER BY day"
        return self.db.fetch_all(query)

    def get_monthly_overview_stats(self):
        query = """
            SELECT
                COALESCE(SUM(CASE WHEN status NOT IN ('Cancelled', 'Rejected') THEN total_cost ELSE 0 END), 0) AS month_revenue,
                COUNT(*) AS total_reservations,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,
                SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
                COALESCE(AVG(CASE WHEN status NOT IN ('Cancelled', 'Rejected') THEN total_cost END), 0) AS avg_ticket
            FROM Reservations
            WHERE DATE_FORMAT(start_date, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')
        """
        result = self.db.fetch_one(query)
        if not result:
            result = {}
        return {
            'month_revenue': float(result.get('month_revenue') or 0),
            'total_reservations': int(result.get('total_reservations') or 0),
            'completed_count': int(result.get('completed_count') or 0),
            'cancelled_count': int(result.get('cancelled_count') or 0),
            'avg_ticket': float(result.get('avg_ticket') or 0)
        }

    def get_reservation_status_counts(self):
        query = """
            SELECT status, COUNT(*) AS total
            FROM Reservations
            GROUP BY status
        """
        data = self.db.fetch_all(query)
        counts = {}
        for item in data:
            counts[item['status']] = int(item['total'])
        return counts

    def get_vehicle_status_counts(self):
        query = """
            SELECT status, COUNT(*) AS total
            FROM Vehicles
            GROUP BY status
        """
        data = self.db.fetch_all(query)
        counts = {}
        for item in data:
            counts[item['status']] = int(item['total'])
        return counts

    def get_upcoming_returns(self, limit=5):
        query = """
            SELECT r.reservation_id, u.username, v.brand, v.model, r.end_date
            FROM Reservations r
            JOIN Users u ON r.user_id = u.user_id
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE r.status = 'Active' AND r.end_date >= CURDATE()
            ORDER BY r.end_date ASC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    def get_top_vehicle_type_this_month(self):
        query = """
            SELECT v.type, COALESCE(SUM(r.total_cost), 0) AS revenue
            FROM Reservations r
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            WHERE DATE_FORMAT(r.start_date, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')
                            AND r.status NOT IN ('Cancelled', 'Rejected')
            GROUP BY v.type
            ORDER BY revenue DESC
            LIMIT 1
        """
        top = self.db.fetch_one(query)
        if not top:
            return {'type': 'N/A', 'revenue': 0.0}
        return {'type': top['type'], 'revenue': float(top['revenue'] or 0)}

    def get_recent_reservations(self, limit=5):
        query = """
            SELECT r.reservation_id, u.username, v.brand, v.model, r.created_at, r.total_cost
            FROM Reservations r
            JOIN Users u ON r.user_id = u.user_id
            JOIN Vehicles v ON r.vehicle_id = v.vehicle_id
            ORDER BY r.created_at DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

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

    def promote_user(self, user_id):
        current = self.db.fetch_one("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        if not current:
            return False, "User not found"

        role = current['role']
        next_role_map = {
            'Member': 'Receptionist',
            'Receptionist': 'Admin',
            'Admin': 'Admin'
        }
        next_role = next_role_map.get(role, role)

        if next_role == role:
            return False, "User is already Admin"

        result = self.db.execute_query("UPDATE Users SET role = %s WHERE user_id = %s", (next_role, user_id))
        if result is None:
            return False, "Failed to promote user"

        return True, f"User promoted to {next_role}"

    def demote_user(self, user_id):
        current = self.db.fetch_one("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        if not current:
            return False, "User not found"

        role = current['role']
        next_role_map = {
            'Admin': 'Receptionist',
            'Receptionist': 'Member',
            'Member': 'Member'
        }
        next_role = next_role_map.get(role, role)

        if next_role == role:
            return False, "User is already at the lowest role"

        result = self.db.execute_query("UPDATE Users SET role = %s WHERE user_id = %s", (next_role, user_id))
        if result is None:
            return False, "Failed to demote user"

        return True, f"User demoted to {next_role}"
