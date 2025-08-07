import sqlite3
from datetime import datetime, timedelta
import random

def seed_database():
    """Populate the database with sample data"""
    
    conn = sqlite3.connect('data/dealership.db')
    cursor = conn.cursor()
    
    # Sample vehicles data
    vehicles_data = [
        ('Toyota', 'Corolla', 2022, 'White', 85000.00, 15000, 'Gasoline', 'Automatic', 'Available'),
        ('Honda', 'Civic', 2021, 'Black', 78000.00, 25000, 'Gasoline', 'Manual', 'Available'),
        ('Ford', 'Focus', 2020, 'Blue', 65000.00, 35000, 'Gasoline', 'Automatic', 'Available'),
        ('Volkswagen', 'Golf', 2023, 'Red', 95000.00, 8000, 'Gasoline', 'Manual', 'Available'),
        ('Chevrolet', 'Onix', 2022, 'Silver', 72000.00, 18000, 'Flex', 'Manual', 'Available'),
        ('Nissan', 'Sentra', 2021, 'Gray', 82000.00, 22000, 'Gasoline', 'Automatic', 'Sold'),
        ('Hyundai', 'HB20', 2023, 'White', 68000.00, 5000, 'Flex', 'Manual', 'Available'),
        ('Fiat', 'Argo', 2022, 'Blue', 63000.00, 12000, 'Flex', 'Manual', 'Available'),
    ]
    
    cursor.executemany('''
        INSERT INTO vehicles (brand, model, year, color, price, mileage, fuel_type, transmission, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vehicles_data)
    
    # Sample customers data
    customers_data = [
        ('João Silva', 'joao.silva@email.com', '(11) 99999-1111', 'Rua das Flores, 123', '123.456.789-01'),
        ('Maria Santos', 'maria.santos@email.com', '(11) 99999-2222', 'Av. Paulista, 456', '987.654.321-02'),
        ('Pedro Oliveira', 'pedro.oliveira@email.com', '(11) 99999-3333', 'Rua da Paz, 789', '456.789.123-03'),
        ('Ana Costa', 'ana.costa@email.com', '(11) 99999-4444', 'Rua do Sol, 321', '789.123.456-04'),
        ('Carlos Ferreira', 'carlos.ferreira@email.com', '(11) 99999-5555', 'Av. Brasil, 654', '321.654.987-05'),
    ]
    
    cursor.executemany('''
        INSERT INTO customers (name, email, phone, address, cpf)
        VALUES (?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Sample employees data
    employees_data = [
        ('Roberto Manager', 'roberto@dealership.com', 'Manager', 8000.00),
        ('Lucia Vendas', 'lucia@dealership.com', 'Sales Representative', 4500.00),
        ('Fernando Vendas', 'fernando@dealership.com', 'Sales Representative', 4200.00),
        ('Patricia Financeiro', 'patricia@dealership.com', 'Financial Analyst', 5500.00),
    ]
    
    cursor.executemany('''
        INSERT INTO employees (name, email, position, salary)
        VALUES (?, ?, ?, ?)
    ''', employees_data)
    
    # Sample sales data
    sales_data = [
        (2, 6, 80000.00, 'Credit Card', 'Customer was very satisfied with the purchase'),
    ]
    
    cursor.executemany('''
        INSERT INTO sales (customer_id, vehicle_id, sale_price, payment_method, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', sales_data)
    
    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
