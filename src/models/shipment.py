from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ShipmentRecord:
    shipment_id: str
    customer_id: int
    post_date: datetime
    status: str
    delivery_time: int
    destination_city: Optional[str] = None

class ShipmentStack:
    def __init__(self):
        self._stack = []

    def push(self, shipment: ShipmentRecord):
        """Add a new shipment to the stack"""
        self._stack.append(shipment)

    def pop(self) -> Optional[ShipmentRecord]:
        """Remove and return the most recent shipment"""
        if self._stack:
            return self._stack.pop()
        return None

    def peek(self) -> Optional[ShipmentRecord]:
        """View the most recent shipment without removing it"""
        if self._stack:
            return self._stack[-1]
        return None

    def get_last_n_shipments(self, n: int) -> List[ShipmentRecord]:
        """Get the last n shipments from the stack"""
        return self._stack[-n:][::-1] if self._stack else []

    def get_customer_shipments(self, customer_id: int, n: Optional[int] = None) -> List[ShipmentRecord]:
        """Get all or last n shipments for a specific customer"""
        customer_shipments = [s for s in self._stack if s.customer_id == customer_id]
        if n is not None:
            return customer_shipments[-n:]
        return customer_shipments

    def is_empty(self) -> bool:
        """Check if the stack is empty"""
        return len(self._stack) == 0