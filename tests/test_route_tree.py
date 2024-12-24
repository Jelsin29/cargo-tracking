import pytest
from src.models.route import RouteTree

def test_route_tree_structure():
    """Test route tree construction and navigation"""
    tree = RouteTree()
    
    # Add headquarters
    hq_id = tree.add_city(None, "Headquarters", 0)
    assert tree.root.city_name == "Headquarters"
    
    # Add main hub
    hub_id = tree.add_city(hq_id, "North Hub", 2)
    assert len(tree.root.children) == 1
    assert tree.root.children[0].city_name == "North Hub"
    
    # Add city to hub
    city_id = tree.add_city(hub_id, "North City 1", 1)
    
    # Test route calculation
    route = tree.get_route_to_city(city_id)
    assert len(route) == 3  # HQ -> Hub -> City
    assert route[0].city_name == "Headquarters"
    assert route[-1].city_name == "North City 1"
