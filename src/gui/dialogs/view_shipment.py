from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QGroupBox)

class ViewShipmentDialog(QDialog):
    statusUpdated = pyqtSignal(str, str)  # shipment_id, new_status

    def __init__(self, db, shipment_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.shipment_id = shipment_id
        self.init_ui()
        self.load_shipment_data()

    def init_ui(self):
        self.setWindowTitle('View Shipment Details')
        self.setModal(True)
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        # Details group
        details_group = QGroupBox("Shipment Details")
        details_layout = QVBoxLayout()
        
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(2)
        self.details_table.setHorizontalHeaderLabels(['Field', 'Value'])
        self.details_table.horizontalHeader().setStretchLastSection(True)
        details_layout.addWidget(self.details_table)
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        # Status update group
        status_group = QGroupBox("Update Status")
        status_layout = QHBoxLayout()
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Processing', 'In Delivery', 'Delivered'])
        status_layout.addWidget(self.status_combo)
        
        update_btn = QPushButton('Update Status')
        update_btn.clicked.connect(self.update_status)
        status_layout.addWidget(update_btn)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Delivery route group
        route_group = QGroupBox("Delivery Route")
        route_layout = QVBoxLayout()
        self.route_label = QLabel()
        route_layout.addWidget(self.route_label)
        route_group.setLayout(route_layout)
        layout.addWidget(route_group)

        # Buttons
        button_layout = QHBoxLayout()
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def load_shipment_data(self):
        with self.db.db_file as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, c.name 
                FROM shipments s 
                JOIN customers c ON s.customer_id = c.customer_id 
                WHERE shipment_id = ?
            ''', (self.shipment_id,))
            result = cursor.fetchone()

        if result:
            fields = [
                ('Tracking ID', result[0]),
                ('Customer', result[5]),
                ('Status', result[3]),
                ('Post Date', datetime.fromisoformat(result[2]).strftime('%Y-%m-%d %H:%M:%S')),
                ('Delivery Time', f"{result[4]} days")
            ]
            
            self.details_table.setRowCount(len(fields))
            for i, (field, value) in enumerate(fields):
                self.details_table.setItem(i, 0, QTableWidgetItem(field))
                self.details_table.setItem(i, 1, QTableWidgetItem(str(value)))
                
            # Set current status in combo box
            index = self.status_combo.findText(result[3])
            if index >= 0:
                self.status_combo.setCurrentIndex(index)

            # Show delivery route if available
            self.update_route_display(result[1])  # customer_id

    def update_status(self):
        new_status = self.status_combo.currentText()
        try:
            self.db.update_shipment_status(self.shipment_id, new_status)
            self.statusUpdated.emit(self.shipment_id, new_status)
            self.load_shipment_data()  # Refresh data
            QMessageBox.information(self, 'Success', 'Status updated successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update status: {str(e)}')

    def update_route_display(self, customer_id):
        # Get delivery route from database
        with self.db.db_file as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT city_name 
                FROM cities 
                WHERE customer_id = ?
                ORDER BY distance
            ''', (customer_id,))
            cities = cursor.fetchall()
            
            if cities:
                route = " → ".join([city[0] for city in cities])
                self.route_label.setText(f"Route: {route}")
            else:
                self.route_label.setText("No route information available")