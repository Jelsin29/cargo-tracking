# tests/test_shipment.py
import pytest
from datetime import datetime
from src.models.shipment import ShipmentRecord, ShipmentStack

def test_shipment_record_creation():
    """Test shipment record creation"""
    now = datetime.now()
    shipment = ShipmentRecord(
        shipment_id="TEST001",
        customer_id=1,
        post_date=now,
        status="Processing",
        delivery_time=3
    )
    assert shipment.shipment_id == "TEST001"
    assert shipment.customer_id == 1
    assert shipment.post_date == now
    assert shipment.status == "Processing"
    assert shipment.delivery_time == 3

def test_empty_stack():
    """Test operations on empty stack"""
    stack = ShipmentStack()
    assert stack.is_empty()
    assert stack.peek() is None
    assert stack.pop() is None
    assert stack.get_last_n_shipments(5) == []

def test_stack_push_pop():
    """Test push and pop operations"""
    stack = ShipmentStack()
    shipment = ShipmentRecord(
        shipment_id="TEST001",
        customer_id=1,
        post_date=datetime.now(),
        status="Processing",
        delivery_time=3
    )
    
    stack.push(shipment)
    assert not stack.is_empty()
    assert stack.peek() == shipment
    
    popped = stack.pop()
    assert popped == shipment
    assert stack.is_empty()

def test_last_n_shipments():
    """Test retrieving last N shipments"""
    stack = ShipmentStack()
    
    # Add multiple shipments
    for i in range(10):
        shipment = ShipmentRecord(
            shipment_id=f"TEST{i:03d}",
            customer_id=1,
            post_date=datetime.now(),
            status="Processing",
            delivery_time=3
        )
        stack.push(shipment)
    
    # Test getting last 5 shipments
    last_five = stack.get_last_n_shipments(5)
    assert len(last_five) == 5
    assert last_five[0].shipment_id == "TEST009"
    assert last_five[-1].shipment_id == "TEST005"

def test_customer_shipments():
    """Test getting shipments for specific customer"""
    stack = ShipmentStack()
    
    # Add shipments for different customers
    for i in range(5):
        shipment = ShipmentRecord(
            shipment_id=f"TEST{i:03d}",
            customer_id=1,
            post_date=datetime.now(),
            status="Processing",
            delivery_time=3
        )
        stack.push(shipment)
        
        # Add shipment for another customer
        other_shipment = ShipmentRecord(
            shipment_id=f"OTHER{i:03d}",
            customer_id=2,
            post_date=datetime.now(),
            status="Processing",
            delivery_time=3
        )
        stack.push(other_shipment)
    
    # Test getting customer shipments
    customer1_shipments = stack.get_customer_shipments(1)
    assert len(customer1_shipments) == 5
    for shipment in customer1_shipments:
        assert shipment.customer_id == 1