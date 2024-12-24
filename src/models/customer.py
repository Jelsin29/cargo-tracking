from datetime import datetime
from typing import Optional, List

class CustomerNode:
    def __init__(self, customer_id: int, name: str):
        self.customer_id = customer_id
        self.name = str(name)
        self.shipment_history = []
        self.next = None

class CustomerList:
    def __init__(self):
        self.head = None

    def add_customer(self, customer_id: int, name: str) -> int:
        """Add a new customer and return their ID"""
        new_node = CustomerNode(customer_id, name)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        return customer_id

    def find_customer(self, customer_id: int) -> Optional[CustomerNode]:
        """Find a customer by their ID"""
        current = self.head
        while current:
            if current.customer_id == customer_id:
                return current
            current = current.next
        return None

    def get_all_customers(self) -> List[CustomerNode]:
        """Get all customers as a list"""
        customers = []
        current = self.head
        while current:
            customers.append(current)
            current = current.next
        return customers

    def add_shipment_to_customer(self, customer_id: int, shipment) -> bool:
        """Add a shipment to a customer's history"""
        customer = self.find_customer(customer_id)
        if customer:
            customer.shipment_history.append(shipment)
            return True
        return False