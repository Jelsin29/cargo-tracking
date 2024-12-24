"""
Test package for Cargo Tracking System.
This package contains all test modules for testing the functionality
of the cargo tracking system.
"""

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

__all__ = [
    'test_customer',
    'test_shipment',
    'test_cargo_priority',
    'test_route_tree',
    'test_integration'
]