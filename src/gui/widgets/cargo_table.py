from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class CargoTable(QTableWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            'Tracking ID', 'Customer', 'Status', 
            'Post Date', 'Delivery Time'
        ])
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def refresh_data(self):
        self.setRowCount(0)
        shipments = self.db.get_all_shipments()
        
        self.setRowCount(len(shipments))
        for row, shipment in enumerate(shipments):
            customer = self.db.find_customer(shipment[1])
            customer_name = customer[1] if customer else "Unknown"
            
            items = [
                QTableWidgetItem(shipment[0]),  # Tracking ID
                QTableWidgetItem(customer_name),
                QTableWidgetItem(shipment[3]),  # Status
                QTableWidgetItem(datetime.fromisoformat(shipment[2]).strftime('%Y-%m-%d %H:%M')),
                QTableWidgetItem(f"{shipment[4]} days")
            ]
            
            for col, item in enumerate(items):
                self.setItem(row, col, item)