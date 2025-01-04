# Base class Node
class Node:
    def __init__(self, node_id, coordinates):
        self.node_id = node_id
        self.coordinates = coordinates

# Subclass Consumer
class Consumer(Node):
    def __init__(self, node_id, coordinates, consumption, capacity):
        super().__init__(node_id, coordinates)
        self.consumption = consumption
        self.capacity = capacity

# Subclass Producer
class Producer(Node):
    def __init__(self, node_id, coordinates, production, capacity):
        super().__init__(node_id, coordinates)
        self.production = production
        self.capacity = capacity
