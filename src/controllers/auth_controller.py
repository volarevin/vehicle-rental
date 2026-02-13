import bcrypt
from src.database.db_manager import DBManager
from src.models.user import Receptionist, Member, Admin

class AuthController:
    def __init__(self):
        self.db = DBManager()

    def login(self, username, password):
        query = "SELECT * FROM Users WHERE username = %s"
        user_data = self.db.fetch_one(query, (username,))

        if not user_data:
            return None

        password_ok = bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8'))
        if password_ok:
            return self._create_user_object(user_data)
        return None

    def register(self, username, password, first_name, last_name):
        existing_user = self.db.fetch_one("SELECT user_id FROM Users WHERE username = %s", (username,))
        if existing_user:
            return False, "Username already exists"

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = """
            INSERT INTO Users (username, password_hash, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, 'Member')
        """
        result = self.db.execute_query(query, (username, hashed, first_name, last_name))
        if result:
            return True, "Registration successful"
        return False, "Registration failed"

    def get_user_by_id(self, user_id):
        query = "SELECT user_id, username, first_name, last_name, role FROM Users WHERE user_id = %s"
        return self.db.fetch_one(query, (user_id,))

    def update_user_profile(self, user_id, username, first_name, last_name):
        if not username or not first_name or not last_name:
            return False, "All profile fields are required"

        existing = self.db.fetch_one("SELECT user_id FROM Users WHERE username = %s AND user_id != %s", (username, user_id))
        if existing:
            return False, "Username is already taken"

        query = """
            UPDATE Users
            SET username = %s, first_name = %s, last_name = %s
            WHERE user_id = %s
        """
        result = self.db.execute_query(query, (username, first_name, last_name, user_id))
        if result is None:
            return False, "Failed to update profile"
        return True, "Profile updated successfully"

    def change_user_password(self, user_id, current_password, new_password):
        if not current_password or not new_password:
            return False, "Current and new password are required"

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"

        user_data = self.db.fetch_one("SELECT password_hash FROM Users WHERE user_id = %s", (user_id,))
        if not user_data:
            return False, "User not found"

        if not bcrypt.checkpw(current_password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
            return False, "Current password is incorrect"

        new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        result = self.db.execute_query("UPDATE Users SET password_hash = %s WHERE user_id = %s", (new_hashed, user_id))
        if result is None:
            return False, "Failed to update password"

        return True, "Password updated successfully"

    def _create_user_object(self, data):
        role = data['role']
        if role == 'Receptionist':
            return Receptionist(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        if role == 'Member':
            return Member(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        if role == 'Admin':
            return Admin(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        return None
