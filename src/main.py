import os
import sys
import sqlite3
from typing import Optional
from datetime import datetime

from models.route import RouteTree
from models.customer import CustomerList
from database.db_manager import DatabaseManager
from models.cargo import CargoItem, CargoPriorityQueue
from models.shipment import ShipmentRecord, ShipmentStack
from utils.sorting import merge_sort, quick_sort, measure_sorting_time
class CargoTrackingSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.customers = CustomerList()
        self.cargo_queue = CargoPriorityQueue()
        self.route_tree = RouteTree()
        self.shipment_stack = ShipmentStack()
        self._setup_demo_routes()

    def _setup_demo_routes(self):
        """Setup some initial demo routes"""
        # Add headquarters
        hq_id = self.route_tree.add_city(None, "Headquarters", 0)
        
        # Add main hubs
        north_id = self.route_tree.add_city(hq_id, "North Hub", 2)
        south_id = self.route_tree.add_city(hq_id, "South Hub", 2)
        east_id = self.route_tree.add_city(hq_id, "East Hub", 2)
        west_id = self.route_tree.add_city(hq_id, "West Hub", 2)

        # Add some cities to each hub
        self.route_tree.add_city(north_id, "North City 1", 1)
        self.route_tree.add_city(north_id, "North City 2", 1)
        self.route_tree.add_city(south_id, "South City 1", 1)
        self.route_tree.add_city(south_id, "South City 2", 1)
        self.route_tree.add_city(east_id, "East City 1", 1)
        self.route_tree.add_city(east_id, "East City 2", 1)
        self.route_tree.add_city(west_id, "West City 1", 1)
        self.route_tree.add_city(west_id, "West City 2", 1)

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the main menu and get user choice"""
        self.clear_screen()
        print("\n=== Cargo Tracking System ===")
        print("1. Add new customer")
        print("2. Add shipping")
        print("3. Check cargo status")
        print("4. View post history")
        print("5. List all cargo (sorted)")
        print("6. Show delivery routes")
        print("0. Exit")
        return input("\nSelect an option: ")

    def wait_for_enter(self):
        """Wait for user to press enter"""
        input("\nPress Enter to continue...")

    def add_customer(self):
        """Add a new customer to the system"""
        self.clear_screen()
        print("\n=== Add New Customer ===")
        
        while True:
            name = input("Enter customer name (or 'cancel' to go back): ").strip()
            if name.lower() == 'cancel':
                return
            if name:
                break
            print("Name cannot be empty. Please try again.")
            
        # Add to database and get ID
        customer_id = self.db.add_customer(name)

        print(f"\nCustomer added successfully!")
        print(f"Customer ID: {customer_id}")
        print(f"Name: {name}")
        self.wait_for_enter()

    def add_shipping(self):
        """Add a new shipment to the system"""
        self.clear_screen()
        print("\n=== Add New Shipment ===")

        # Get customer ID
        while True:
            try:
                customer_id = int(input("Enter customer ID (or 0 to cancel): "))
                if customer_id == 0:
                    return
                
                # Check in database
                customer = self.db.find_customer(customer_id)
                if customer:
                    break
                print("Customer not found. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        # Get delivery time
        while True:
            try:
                delivery_time = int(input("Enter delivery time (in days): "))
                if delivery_time > 0:
                    break
                print("Delivery time must be positive.")
            except ValueError:
                print("Please enter a valid number.")

        # Generate shipment ID
        shipment_id = f"CARGO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Add to database
        self.db.add_shipment(
            shipment_id=shipment_id,
            customer_id=customer_id,
            post_date=datetime.now(),
            status="Processing",
            delivery_time=delivery_time
        )
        
        # Create and store ShipmentRecord
        shipment = ShipmentRecord(
            shipment_id=shipment_id,
            customer_id=customer_id,
            post_date=datetime.now(),
            status="Processing",
            delivery_time=delivery_time
        )
        self.shipment_stack.push(shipment)
        
        # Create cargo and shipment
        cargo = CargoItem(
            post_id=shipment_id,
            delivery_time=delivery_time,
            status="Processing",
            customer_id=customer_id
        )

        # Add to tracking systems
        self.cargo_queue.add_cargo(cargo)

        print(f"\nShipment added successfully!")
        print(f"Tracking ID: {shipment_id}")
        self.wait_for_enter()

    def check_cargo_status(self):
        """Check the status of a specific cargo"""
        self.clear_screen()
        print("\n=== Check Cargo Status ===")

        tracking_id = input("Enter tracking ID (or 'cancel' to go back): ").strip()
        if tracking_id.lower() == 'cancel':
            return

        inquiry_manager = self.db.get_inquiry_manager()
        cargo = inquiry_manager.find_cargo_by_id(tracking_id)
    
        if cargo:
            customer = self.db.find_customer(cargo.customer_id)
            print(f"\nCargo Status:")
            print(f"Tracking ID: {cargo.post_id}")
            print(f"Status: {cargo.status}")
            print(f"Delivery Time: {cargo.delivery_time} days")
            print(f"Customer: {customer[1] if customer else 'Unknown'}")
        else:
            print("\nCargo not found.")
    
        self.wait_for_enter()

    def view_post_history(self):
        """View shipment history for a specific customer"""
        self.clear_screen()
        print("\n=== View Shipment History ===")

        while True:
            try:
                customer_id = int(input("Enter customer ID (or 0 to cancel): "))
                if customer_id == 0:
                    return
                
                customer = self.db.find_customer(customer_id)
                if customer:
                    break
                print("Customer not found. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        # Get shipments from database
        shipments = self.db.get_customer_shipments(customer_id)
    
        if not shipments:
            print(f"\nNo shipment history found for customer {customer[1]}")
        else:
            print(f"\nShipment history for customer {customer[1]}:")
            print("\nLast 5 shipments:")
            for shipment in shipments[-5:]:
                print(f"\nTracking ID: {shipment[0]}")
                print(f"Status: {shipment[3]}")
                print(f"Post Date: {datetime.fromisoformat(shipment[2]).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Delivery Time: {shipment[4]} days")
        
        self.wait_for_enter()

    def list_all_cargo(self):
        """List all cargo with sorting options"""
        self.clear_screen()
        print("\n=== List All Cargo ===")

        # Get all shipments from database
        shipments = self.db.get_all_shipments()
    
        if not shipments:
            print("No cargo in the system.")
            self.wait_for_enter()
            return

        print("\nSort using:")
        print("1. Merge Sort")
        print("2. Quick Sort")
        choice = input("Select sorting algorithm (1/2): ").strip()

        # Convert to CargoItem objects for sorting
        cargo_items = [
            CargoItem(
                post_id=s[0],
                delivery_time=s[4],
                status=s[3],
                customer_id=s[1]
            ) for s in shipments
        ]

        sort_func = merge_sort if choice == "1" else quick_sort
        sorting_time = measure_sorting_time(sort_func, cargo_items, key=lambda x: x.delivery_time)
        sorted_cargo = sort_func(cargo_items, key=lambda x: x.delivery_time)

        print(f"\nAll cargo (sorted by delivery time):")
        print(f"Sorting time: {sorting_time:.6f} seconds")
        print("\nFormat: ID | Status | Delivery Time | Customer")
        print("-" * 60)
    
        for cargo in sorted_cargo:
            customer = self.db.find_customer(cargo.customer_id)
            customer_name = customer[1] if customer else "Unknown"
            print(f"{cargo.post_id} | {cargo.status} | {cargo.delivery_time} days | {customer_name}")

        self.wait_for_enter()

    def show_delivery_routes(self):
        """Display the delivery route tree"""
        self.clear_screen()
        print("\n=== Delivery Routes ===")

        if not self.route_tree.root:
            print("No routes configured.")
        else:
            print("\nDelivery route structure:")
            self.route_tree.print_tree()

        self.wait_for_enter()

    def run(self):
        """Main application loop"""
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.add_customer()
            elif choice == "2":
                self.add_shipping()
            elif choice == "3":
                self.check_cargo_status()
            elif choice == "4":
                self.view_post_history()
            elif choice == "5":
                self.list_all_cargo()
            elif choice == "6":
                self.show_delivery_routes()
            elif choice == "0":
                self.clear_screen()
                print("\nThank you for using the Cargo Tracking System!")
                sys.exit(0)
            else:
                print("\nInvalid option. Please try again.")
                self.wait_for_enter()

if __name__ == "__main__":
    db = DatabaseManager()  # This creates tables
    system = CargoTrackingSystem()
    system.run()