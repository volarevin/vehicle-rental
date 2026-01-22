import bcrypt
from src.database.db_manager import DBManager
from src.models.user import Receptionist, Member, Admin

class AuthController:
    def __init__(self):
        self.db = DBManager()

    def login(self, username, password):
        query = "SELECT * FROM Users WHERE username = %s"
        user_data = self.db.fetch_one(query, (username,))

        if user_data:
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
                return self._create_user_object(user_data)
        return None

    def register(self, username, password, first_name, last_name):
        # Check if username exists
        if self.db.fetch_one("SELECT user_id FROM Users WHERE username = %s", (username,)):
            return False, "Username already exists"

        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert user
        query = """
            INSERT INTO Users (username, password_hash, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, 'Member')
        """
        if self.db.execute_query(query, (username, hashed, first_name, last_name)):
            return True, "Registration successful"
        return False, "Registration failed"

    def _create_user_object(self, data):
        role = data['role']
        if role == 'Receptionist':
            return Receptionist(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        elif role == 'Member':
            return Member(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        elif role == 'Admin':
            return Admin(data['user_id'], data['username'], data['first_name'], data['last_name'], role)
        return None
