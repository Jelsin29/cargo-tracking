import heapq
import sqlite3
from datetime import datetime
from typing import List, Tuple, Any
from models.customer import CustomerList
from models.inquiry import CargoInquiryManager
from models.shipment import ShipmentRecord, ShipmentStack
class DatabaseManager:
    def __init__(self, db_file: str = "cargo_tracking.db"):
        self.db_file = db_file
        self.shipment_stack = ShipmentStack()
        self.customer_list = CustomerList()
        self.conn = None
        if db_file == ":memory:":
            # For in-memory database, keep the connection
            self.conn = sqlite3.connect(":memory:")
        self._create_tables()
        
    def __del__(self):
        if self.conn:
            self.conn.close()

    def _get_connection(self):
        """Get database connection"""
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_file)

    def _create_tables(self):
        """Create database tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
            
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
            
            # Create shipments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipments (
                shipment_id TEXT PRIMARY KEY,
                customer_id INTEGER,
                post_date TEXT NOT NULL,
                status TEXT NOT NULL,
                delivery_time INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
            
        # Create routes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                city_id INTEGER PRIMARY KEY,
                city_name TEXT NOT NULL,
                parent_id INTEGER,
                distance INTEGER NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES cities (city_id)
            )
        ''')
            
        conn.commit()
        if not self.conn:
            conn.close()

    def add_customer(self, name: str) -> int:
        """Add a new customer and return their ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO customers (name) VALUES (?)',
            (name,)
        )
        customer_id = cursor.lastrowid
        conn.commit()
        if not self.conn:
            conn.close()
            
        # Add to linked list
        self.customer_list.add_customer(customer_id, name)
        return customer_id
    
    def add_shipment(self, shipment_id: str, customer_id: int, post_date: datetime, status: str, delivery_time: int):
        """Add a new shipment"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO shipments 
                (shipment_id, customer_id, post_date, status, delivery_time)
                VALUES (?, ?, ?, ?, ?)''',
            (shipment_id, customer_id, post_date.isoformat(), status, delivery_time)
        )
        conn.commit()
        if not self.conn:
            conn.close()
    
    # Add to shipment stack
        self.shipment_stack.push(ShipmentRecord(
            shipment_id=shipment_id,
            customer_id=customer_id,
            post_date=post_date,
            status=status,
            delivery_time=delivery_time
        ))
        
    
    def get_inquiry_manager(self):
        """Get a cargo inquiry manager instance"""
        return CargoInquiryManager(self)

    def get_customer_shipments(self, customer_id: int) -> List[Tuple[Any, ...]]:
        """Get all shipments for a customer"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM shipments 
                WHERE customer_id = ? 
                ORDER BY post_date DESC''',
            (customer_id,)
        )
        result = cursor.fetchall()
        if not self.conn:
            conn.close()
        return result

    def update_shipment_status(self, shipment_id: str, new_status: str) -> bool:
        """Update the status of a shipment"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE shipments SET status = ? WHERE shipment_id = ?',
            (new_status, shipment_id)
        )
        conn.commit()
        rows_affected = cursor.rowcount
        if not self.conn:
            conn.close()
        return rows_affected > 0

    def get_all_shipments(self) -> List[Tuple[Any, ...]]:
        """Get all shipments"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM shipments ORDER BY delivery_time'
        )
        result = cursor.fetchall()
        if not self.conn:
            conn.close()
        return result

    def find_customer(self, customer_id: int) -> Tuple[Any, ...]:
        """Find a customer by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
                'SELECT * FROM customers WHERE customer_id = ?',
                (customer_id,)
        )
        result = cursor.fetchone()
        if not self.conn:
                conn.close()
        return result