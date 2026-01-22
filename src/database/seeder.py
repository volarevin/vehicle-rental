import mysql.connector
import bcrypt

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vehicle_rental'
}

def seed_database():
    # Connect to MySQL Server (without database first to create it)
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.database = DB_CONFIG['database']
        
        print("Database created/selected.")

        # Read and execute schema
        with open('src/database/schema.sql', 'r') as f:
            schema = f.read()
            statements = schema.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
        
        print("Schema applied.")

        # Helper to hash passwords
        def hash_password(password):
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        password_hash = hash_password("password")

        # Seed Users
        users = [
            ("admin", password_hash, "System", "Admin", "Admin"),
            ("sherwin", password_hash, "Sherwin", "Arizobal", "Receptionist"),
            ("james", password_hash, "James", "Banaag", "Receptionist"),
            ("bien", password_hash, "Bien", "Hipolito", "Member")
        ]

        cursor.executemany(
            "INSERT IGNORE INTO Users (username, password_hash, first_name, last_name, role) VALUES (%s, %s, %s, %s, %s)",
            users
        )
        print("Users seeded.")

        # Seed Vehicles (Common PH Vehicles)
        vehicles = [
            ("Toyota", "Vios", 2024, "ABC 1234", "Car", 1500.00),
            ("Toyota", "Innova", 2023, "DEF 5678", "Van", 2500.00),
            ("Toyota", "Fortuner", 2024, "GHI 9012", "SUV", 3500.00),
            ("Mitsubishi", "L300", 2022, "JKL 3456", "Truck", 2000.00),
            ("Honda", "Click 125i", 2023, "MNO 7890", "Motorcycle", 500.00),
            ("Nissan", "Urvan", 2023, "PQR 1122", "Van", 2800.00),
            ("Ford", "Ranger", 2023, "STU 3344", "Truck", 3000.00),
            ("Toyota", "Wigo", 2024, "VWX 5566", "Car", 1200.00)
        ]

        cursor.executemany(
            "INSERT IGNORE INTO Vehicles (brand, model, year, license_plate, type, daily_rate) VALUES (%s, %s, %s, %s, %s, %s)",
            vehicles
        )
        print("Vehicles seeded.")

        # Seed Equipment
        equipment = [
            ("GPS Navigation", 200.00),
            ("Child Safety Seat", 150.00),
            ("Ski Rack", 300.00), # Maybe less common in PH but requested
            ("Dash Cam", 100.00)
        ]

        cursor.executemany(
            "INSERT IGNORE INTO Equipment (name, daily_rate) VALUES (%s, %s)",
            equipment
        )
        print("Equipment seeded.")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database seeding completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    seed_database()
