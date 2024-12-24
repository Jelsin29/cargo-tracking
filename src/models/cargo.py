import heapq
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CargoItem:
    post_id: str
    delivery_time: int
    status: str  # Processing / In Delivery / Delivered
    customer_id: int
    
    def __lt__(self, other):
        return self.delivery_time < other.delivery_time

class CargoPriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
        self._cargo_map = {}  # To store cargo items by post_id

    def add_cargo(self, cargo: CargoItem):
        # Add to priority queue
        heapq.heappush(self._queue, (cargo.delivery_time, self._index, cargo))
        # Store in map for quick lookup
        self._cargo_map[cargo.post_id] = cargo
        self._index += 1

    def get_next_cargo(self) -> Optional[CargoItem]:
        if self._queue:
            return heapq.heappop(self._queue)[2]
        return None
    
    def find_cargo(self, post_id: str) -> Optional[CargoItem]:
        return self._cargo_map.get(post_id)
    
    def update_status(self, post_id: str, new_status: str) -> bool:
        cargo = self._cargo_map.get(post_id)
        if cargo:
            cargo.status = new_status
            return True
        return False

    def get_all_cargo(self) -> List[CargoItem]:
        return list(self._cargo_map.values())