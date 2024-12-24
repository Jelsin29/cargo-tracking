# tests/test_integration.py
import pytest
from datetime import datetime
from src.database.db_manager import DatabaseManager

@pytest.fixture
def db():
    """Fixture to provide a test database"""
    database = DatabaseManager(":memory:")
    return database

def test_end_to_end_shipment(db):
    """Test complete shipment workflow"""
    # Add customer
    customer_id = db.add_customer("John Doe")
    assert customer_id is not None
    
    # Add shipment
    shipment_id = "TEST001"
    db.add_shipment(
        shipment_id=shipment_id,
        customer_id=customer_id,
        post_date=datetime.now(),
        status="Processing",
        delivery_time=3
    )
    
    # Check customer shipments
    shipments = db.get_customer_shipments(customer_id)
    assert len(shipments) == 1
    assert shipments[0][0] == shipment_id
    
    # Update status
    success = db.update_shipment_status(shipment_id, "Delivered")
    assert success
    
    # Verify status update
    inquiry = db.get_inquiry_manager()
    cargo = inquiry.find_cargo_by_id(shipment_id)
    assert cargo is not None
    assert cargo.status == "Delivered"