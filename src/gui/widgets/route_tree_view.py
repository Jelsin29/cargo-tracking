from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView

class RouteTreeView(QTreeWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setHeaderLabels(['City', 'Distance'])
        self.setColumnCount(2)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def add_nodes_recursively(self, parent_item, node):
        item = QTreeWidgetItem(parent_item if parent_item else self)
        item.setText(0, node.city_name)
        item.setText(1, f"{node.distance} km")
        
        for child in node.children:
            self.add_nodes_recursively(item, child)

    def refresh_data(self, route_tree):
        self.clear()
        if route_tree.root:
            self.add_nodes_recursively(None, route_tree.root)
            self.expandAll()
