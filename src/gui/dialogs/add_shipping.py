import sqlite3
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox, QComboBox)
class AddShippingDialog(QDialog):
    shipmentAdded = pyqtSignal()

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.load_customers()

    def init_ui(self):
        self.setWindowTitle('Add New Shipment')
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Customer selection
        layout.addWidget(QLabel('Select Customer:'))
        self.customer_combo = QComboBox()
        layout.addWidget(self.customer_combo)

        # Delivery time input
        layout.addWidget(QLabel('Delivery Time (days):'))
        self.delivery_time = QSpinBox()
        self.delivery_time.setMinimum(1)
        self.delivery_time.setMaximum(365)
        layout.addWidget(self.delivery_time)

        # Add button
        add_btn = QPushButton('Add Shipment')
        add_btn.clicked.connect(self.add_shipment)
        layout.addWidget(add_btn)

    def load_customers(self):
        self.customer_combo.clear()
        with sqlite3.connect(self.db.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT customer_id, name FROM customers')
            customers = cursor.fetchall()
            for customer_id, name in customers:
                self.customer_combo.addItem(f"{name} (ID: {customer_id})", customer_id)

    def add_shipment(self):
        if self.customer_combo.count() == 0:
            QMessageBox.warning(self, 'Error', 'No customers available')
            return

        customer_id = self.customer_combo.currentData()
        delivery_time = self.delivery_time.value()
        shipment_id = f"CARGO{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            self.db.add_shipment(
                shipment_id=shipment_id,
                customer_id=customer_id,
                post_date=datetime.now(),
                status="Processing",
                delivery_time=delivery_time
            )
            QMessageBox.information(self, 'Success', 
                                    f'Shipment added successfully!\nTracking ID: {shipment_id}')
            self.shipmentAdded.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add shipment: {str(e)}')
