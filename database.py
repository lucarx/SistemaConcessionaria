import sqlite3
from typing import List, Dict, Optional, Tuple
import os

class DatabaseManager:
    def __init__(self, db_path: str = 'data/dealership.db'):
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Ensure the database and tables exist"""
        if not os.path.exists(self.db_path):
            from scripts.create_database import create_database
            create_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    # Vehicle operations
    def add_vehicle(self, brand: str, model: str, year: int, color: str, 
                   price: float, mileage: int = 0, fuel_type: str = 'Gasoline',
                   transmission: str = 'Manual') -> int:
        """Add a new vehicle to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vehicles (brand, model, year, color, price, mileage, fuel_type, transmission)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (brand, model, year, color, price, mileage, fuel_type, transmission))
            return cursor.lastrowid
    
    def get_vehicles(self, status: str = None) -> List[Dict]:
        """Get all vehicles, optionally filtered by status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('SELECT * FROM vehicles WHERE status = ? ORDER BY created_at DESC', (status,))
            else:
                cursor.execute('SELECT * FROM vehicles ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Dict]:
        """Get a vehicle by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_vehicle(self, vehicle_id: int, **kwargs) -> bool:
        """Update vehicle information"""
        if not kwargs:
            return False
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [vehicle_id]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE vehicles SET {set_clause} WHERE id = ?', values)
            return cursor.rowcount > 0
    
    def delete_vehicle(self, vehicle_id: int) -> bool:
        """Delete a vehicle"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM vehicles WHERE id = ?', (vehicle_id,))
            return cursor.rowcount > 0
    
    # Customer operations
    def add_customer(self, name: str, email: str, phone: str, 
                    address: str = '', cpf: str = '') -> int:
        """Add a new customer"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (name, email, phone, address, cpf)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, address, cpf))
            return cursor.lastrowid
    
    def get_customers(self) -> List[Dict]:
        """Get all customers"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        """Get a customer by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_customer(self, customer_id: int, **kwargs) -> bool:
        """Update customer information"""
        if not kwargs:
            return False
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [customer_id]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE customers SET {set_clause} WHERE id = ?', values)
            return cursor.rowcount > 0
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
            return cursor.rowcount > 0
    
    # Sales operations
    def add_sale(self, customer_id: int, vehicle_id: int, sale_price: float,
                payment_method: str = 'Cash', notes: str = '') -> int:
        """Add a new sale"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Add the sale
            cursor.execute('''
                INSERT INTO sales (customer_id, vehicle_id, sale_price, payment_method, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, vehicle_id, sale_price, payment_method, notes))
            
            # Update vehicle status to sold
            cursor.execute('UPDATE vehicles SET status = ? WHERE id = ?', ('Sold', vehicle_id))
            
            return cursor.lastrowid
    
    def get_sales(self) -> List[Dict]:
        """Get all sales with customer and vehicle information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, c.name as customer_name, c.email as customer_email,
                       v.brand, v.model, v.year, v.color
                FROM sales s
                JOIN customers c ON s.customer_id = c.id
                JOIN vehicles v ON s.vehicle_id = v.id
                ORDER BY s.sale_date DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_sales_summary(self) -> Dict:
        """Get sales summary statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total sales
            cursor.execute('SELECT COUNT(*) as total_sales, SUM(sale_price) as total_revenue FROM sales')
            summary = dict(cursor.fetchone())
            
            # Available vehicles
            cursor.execute('SELECT COUNT(*) as available_vehicles FROM vehicles WHERE status = "Available"')
            summary.update(dict(cursor.fetchone()))
            
            # Total customers
            cursor.execute('SELECT COUNT(*) as total_customers FROM customers')
            summary.update(dict(cursor.fetchone()))
            
            return summary
    
    # Employee operations
    def add_employee(self, name: str, email: str, position: str, salary: float = 0.0) -> int:
        """Add a new employee"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (name, email, position, salary)
                VALUES (?, ?, ?, ?)
            ''', (name, email, position, salary))
            return cursor.lastrowid
    
    def get_employees(self) -> List[Dict]:
        """Get all employees"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]
    
    def search_vehicles(self, query: str) -> List[Dict]:
        """Search vehicles by brand, model, or color"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_query = f"%{query}%"
            cursor.execute('''
                SELECT * FROM vehicles 
                WHERE brand LIKE ? OR model LIKE ? OR color LIKE ?
                ORDER BY created_at DESC
            ''', (search_query, search_query, search_query))
            return [dict(row) for row in cursor.fetchall()]
