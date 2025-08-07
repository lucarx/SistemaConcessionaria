import sqlite3
import os

def create_database():
    """Create the SQLite database and tables for the car dealership system"""
    
    # Create database directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect('data/dealership.db')
    cursor = conn.cursor()
    
    # Create vehicles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            color TEXT NOT NULL,
            price REAL NOT NULL,
            mileage INTEGER DEFAULT 0,
            fuel_type TEXT DEFAULT 'Gasoline',
            transmission TEXT DEFAULT 'Manual',
            status TEXT DEFAULT 'Available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            cpf TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            vehicle_id INTEGER NOT NULL,
            sale_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            payment_method TEXT DEFAULT 'Cash',
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
        )
    ''')
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            position TEXT NOT NULL,
            salary REAL,
            hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
