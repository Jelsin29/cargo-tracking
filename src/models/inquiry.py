from typing import List, Optional
from models.cargo import CargoItem
from utils.searching import binary_search
from utils.sorting import merge_sort, quick_sort

class CargoInquiryManager:
    def __init__(self, db):
        self.db = db
        self._sorted_cargo = []
        self._needs_resort = True

    def _ensure_sorted(self, sort_method='quick'):
        """Ensure cargo list is sorted by ID for binary search"""
        if self._needs_resort:
            all_shipments = self.db.get_all_shipments()
            cargo_items = [
                CargoItem(
                    post_id=s[0],
                    delivery_time=s[4],
                    status=s[3],
                    customer_id=s[1]
                ) for s in all_shipments
            ]
            
            # Sort using specified method
            if sort_method == 'merge':
                self._sorted_cargo = merge_sort(cargo_items, key=lambda x: x.post_id)
            else:  # Default to quick sort
                self._sorted_cargo = quick_sort(cargo_items, key=lambda x: x.post_id)
            
            self._needs_resort = False
        
        return self._sorted_cargo

    def find_cargo_by_id(self, cargo_id: str) -> Optional[CargoItem]:
        """Find cargo using binary search by ID"""
        sorted_cargo = self._ensure_sorted()
        idx = binary_search(sorted_cargo, cargo_id, key=lambda x: x.post_id)
        if idx is not None:
            return sorted_cargo[idx]
        return None

    def get_sorted_by_delivery_time(self, sort_method='quick') -> List[CargoItem]:
        """Get all cargo sorted by delivery time"""
        all_shipments = self.db.get_all_shipments()
        cargo_items = [
            CargoItem(
                post_id=s[0],
                delivery_time=s[4],
                status=s[3],
                customer_id=s[1]
            ) for s in all_shipments
        ]

        if sort_method == 'merge':
            return merge_sort(cargo_items, key=lambda x: x.delivery_time)
        return quick_sort(cargo_items, key=lambda x: x.delivery_time)

    def get_undelivered_shipments(self) -> List[CargoItem]:
        """Get all undelivered shipments"""
        sorted_cargo = self._ensure_sorted()
        return [cargo for cargo in sorted_cargo if cargo.status != "Delivered"]

    def get_delivered_shipments(self) -> List[CargoItem]:
        """Get all delivered shipments"""
        sorted_cargo = self._ensure_sorted()
        return [cargo for cargo in sorted_cargo if cargo.status == "Delivered"]

    def invalidate_cache(self):
        """Mark the sorted cache as needing resort"""
        self._needs_resort = True