from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTabWidget, QMessageBox, QHeaderView, QTableWidgetItem)

from models.route import RouteTree
from .widgets.cargo_table import CargoTable
from database.db_manager import DatabaseManager
from .widgets.route_tree_view import RouteTreeView
from .dialogs.add_customer import AddCustomerDialog
from .dialogs.add_shipping import AddShippingDialog
from .dialogs.view_shipment import ViewShipmentDialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.route_tree = RouteTree()
        self._setup_demo_routes()
        self.init_ui()

    def _setup_demo_routes(self):
        """Setup initial demo routes"""
        hq_id = self.route_tree.add_city(None, "Headquarters", 0)
        
        # Main hubs
        north_id = self.route_tree.add_city(hq_id, "North Hub", 2)
        south_id = self.route_tree.add_city(hq_id, "South Hub", 2)
        east_id = self.route_tree.add_city(hq_id, "East Hub", 2)
        west_id = self.route_tree.add_city(hq_id, "West Hub", 2)

        # Add cities to each hub
        self.route_tree.add_city(north_id, "North City 1", 1)
        self.route_tree.add_city(north_id, "North City 2", 1)
        self.route_tree.add_city(south_id, "South City 1", 1)
        self.route_tree.add_city(south_id, "South City 2", 1)
        self.route_tree.add_city(east_id, "East City 1", 1)
        self.route_tree.add_city(east_id, "East City 2", 1)
        self.route_tree.add_city(west_id, "West City 1", 1)
        self.route_tree.add_city(west_id, "West City 2", 1)


    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Cargo Tracking System')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        tabs = QTabWidget()

        # Dashboard tab
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)

        # Action buttons
        button_layout = QHBoxLayout()
        add_customer_btn = QPushButton('Add Customer')
        add_customer_btn.clicked.connect(self.show_add_customer)
        add_shipping_btn = QPushButton('Add Shipping')
        add_shipping_btn.clicked.connect(self.show_add_shipping)
        
        button_layout.addWidget(add_customer_btn)
        button_layout.addWidget(add_shipping_btn)
        button_layout.addStretch()
        
        dashboard_layout.addLayout(button_layout)

        # Cargo table
        self.cargo_table = CargoTable(self.db)
        self.cargo_table.doubleClicked.connect(self.view_shipment)
        dashboard_layout.addWidget(self.cargo_table)

        tabs.addTab(dashboard, "Dashboard")

        # Routes tab
        routes = QWidget()
        routes_layout = QVBoxLayout(routes)
        self.route_tree_view = RouteTreeView(self.db)
        self.route_tree_view.refresh_data(self.route_tree)
        routes_layout.addWidget(self.route_tree_view)
        tabs.addTab(routes, "Routes")
        
        # Recent Shipments tab
        shipment_history = QWidget()
        history_layout = QVBoxLayout(shipment_history)
        
        # Create table for recent shipments
        history_table = QTableWidget()
        history_table.setColumnCount(4)
        history_table.setHorizontalHeaderLabels(['Tracking ID', 'Status', 'Post Date', 'Delivery Time'])
        header = history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Get last 5 shipments from stack
        shipments = self.db.get_all_shipments()[-5:]
        history_table.setRowCount(len(shipments))
        for i, shipment in enumerate(shipments):
            history_table.setItem(i, 0, QTableWidgetItem(shipment[0]))
            history_table.setItem(i, 1, QTableWidgetItem(shipment[3]))
            history_table.setItem(i, 2, QTableWidgetItem(str(shipment[2])))
            history_table.setItem(i, 3, QTableWidgetItem(f"{shipment[4]} days"))

        history_layout.addWidget(history_table)
        tabs.addTab(shipment_history, "Recent Shipments")

        main_layout.addWidget(tabs)

    def show_add_customer(self):
        dialog = AddCustomerDialog(self.db, self)
        dialog.customerAdded.connect(self.refresh_data)
        dialog.exec_()

    def show_add_shipping(self):
        dialog = AddShippingDialog(self.db, self)
        dialog.shipmentAdded.connect(self.refresh_data)
        dialog.exec_()

    def view_shipment(self):
        current_row = self.cargo_table.currentRow()
        if current_row >= 0:
            tracking_id = self.cargo_table.item(current_row, 0).text()
            dialog = ViewShipmentDialog(self.db, tracking_id, self)
            dialog.statusUpdated.connect(self.refresh_data)
            dialog.exec_()

    def refresh_data(self):
        self.cargo_table.refresh_data()
        self.route_tree_view.refresh_data(self.route_tree)