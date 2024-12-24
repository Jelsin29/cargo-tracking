from typing import Optional, List

class CityNode:
    def __init__(self, city_id: int, city_name: str):
        self.city_id = city_id
        self.city_name = city_name
        self.children = []  # List of child cities
        self.distance = 0   # Distance from parent city

class RouteTree:
    def __init__(self):
        self.root = None
        self._city_count = 0

    def add_city(self, parent_id: Optional[int], city_name: str, distance: int = 0) -> int:
        """Add a new city to the route tree"""
        self._city_count += 1
        new_city = CityNode(self._city_count, city_name)
        new_city.distance = distance

        if not self.root:
            self.root = new_city
            return new_city.city_id

        if parent_id:
            parent = self._find_city(self.root, parent_id)
            if parent:
                parent.children.append(new_city)
                return new_city.city_id

        return -1

    def _find_city(self, node: CityNode, city_id: int) -> Optional[CityNode]:
        """Find a city by ID in the tree"""
        if node.city_id == city_id:
            return node
        
        for child in node.children:
            result = self._find_city(child, city_id)
            if result:
                return result
        return None

    def get_route_to_city(self, city_id: int) -> List[CityNode]:
        """Get the route from root to specified city"""
        def find_path(node: CityNode, target_id: int, path: List[CityNode]) -> bool:
            if not node:
                return False
            
            path.append(node)
            if node.city_id == target_id:
                return True

            for child in node.children:
                if find_path(child, target_id, path):
                    return True
            
            path.pop()
            return False

        path = []
        if self.root:
            find_path(self.root, city_id, path)
        return path

    def calculate_delivery_time(self, city_id: int) -> int:
        """Calculate total delivery time to a city based on path distances"""
        route = self.get_route_to_city(city_id)
        return sum(city.distance for city in route)

    def print_tree(self, node: Optional[CityNode] = None, level: int = 0):
        """Print the tree structure"""
        if node is None:
            if self.root is None:
                return
            node = self.root
        
        print("  " * level + f"└── {node.city_name} (ID: {node.city_id}, Distance: {node.distance})")
        for child in node.children:
            self.print_tree(child, level + 1)