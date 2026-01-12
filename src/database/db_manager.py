import mysql.connector
from src.config import DB_CONFIG

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor
        except mysql.connector.Error as err:
            print(f"Query Error: {err}")
            return None
        finally:
            # We don't close here to allow fetching results, 
            # but for simple updates it might be better to close.
            # For this simple app, we'll manage connection per controller action or keep it open.
            pass

    def fetch_one(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params or ())
        result = self.cursor.fetchone()
        self.disconnect()
        return result

    def fetch_all(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params or ())
        result = self.cursor.fetchall()
        self.disconnect()
        return result
