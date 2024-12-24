import pytest
from src.models.cargo import CargoItem, CargoPriorityQueue

def test_cargo_priority():
    """Test cargo prioritization"""
    queue = CargoPriorityQueue()
    
    # Add cargos with different priorities
    cargo1 = CargoItem("TEST001", 5, "Processing", 1)  # 5 days delivery
    cargo2 = CargoItem("TEST002", 2, "Processing", 1)  # 2 days delivery
    cargo3 = CargoItem("TEST003", 3, "Processing", 1)  # 3 days delivery
    
    queue.add_cargo(cargo1)
    queue.add_cargo(cargo2)
    queue.add_cargo(cargo3)
    
    # Test priority order
    next_cargo = queue.get_next_cargo()
    assert next_cargo.post_id == "TEST002"
    
    next_cargo = queue.get_next_cargo()
    assert next_cargo.post_id == "TEST003"