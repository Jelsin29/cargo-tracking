import pytest
from src.models.customer import CustomerNode, CustomerList

def test_customer_creation():
    """Test customer node creation and attributes"""
    customer = CustomerNode(1, "John Doe")
    assert customer.customer_id == 1
    assert customer.name == "John Doe"
    assert customer.next is None
    assert customer.shipment_history == []

def test_customer_list_add():
    """Test adding customers to list"""
    customer_list = CustomerList()
    
    # Add first customer
    customer_id1 = customer_list.add_customer(1, "Umut Gulmez")
    assert customer_list.head is not None
    assert customer_list.head.name == "Umut Gulmez"
    assert customer_list.head.customer_id == 1
    
    # Add second customer
    customer_id2 = customer_list.add_customer(2, "Abdullah Yilmaz")
    assert customer_list.head.next is not None
    assert customer_list.head.next.name == "Abdullah Yilmaz"
    assert customer_list.head.next.customer_id == 2

def test_customer_find():
    """Test finding customers in list"""
    customer_list = CustomerList()
    customer_id = 1  # Define ID explicitly
    customer_list.add_customer(customer_id, "Umut Gulmez")  # Changed to provide ID
    
    # Test finding existing customer
    found = customer_list.find_customer(customer_id)
    assert found is not None
    assert found.name == "Umut Gulmez"
    assert found.customer_id == customer_id
    
    # Test finding non-existent customer
    not_found = customer_list.find_customer(999)
    assert not_found is None