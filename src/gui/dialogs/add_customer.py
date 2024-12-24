from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)

class AddCustomerDialog(QDialog):
    customerAdded = pyqtSignal()

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add New Customer')
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Name input
        layout.addWidget(QLabel('Customer Name:'))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        add_btn = QPushButton('Add Customer')
        add_btn.clicked.connect(self.add_customer)
        layout.addWidget(add_btn)

    def add_customer(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Error', 'Name cannot be empty')
            return

        try:
            customer_id = self.db.add_customer(name)
            QMessageBox.information(self, 'Success', 
                                f'Customer added successfully!\nID: {customer_id}')
            self.customerAdded.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add customer: {str(e)}')
