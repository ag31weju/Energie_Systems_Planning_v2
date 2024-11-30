# energy_graph/services.py
from .models import Node, Edge

class EnergyGraph:
    def __init__(self):
        self.nodes = list(Node.objects.all())
        self.edges = list(Edge.objects.all())

    def add_node(self, node):
        """Add a node to the database."""
        node.save()
        self.nodes.append(node)

    def add_edge(self, start_node_id, end_node_id, weight=1.0, properties=None):
        """Add an edge to the database."""
        start_node = Node.objects.get(node_id=start_node_id)
        end_node = Node.objects.get(node_id=end_node_id)
        edge = Edge(start_node=start_node, end_node=end_node, weight=weight, properties=properties or {})
        edge.save()
        self.edges.append(edge)

    def get_neighbors(self, node_id):
        """Get neighbors of a node."""
        return [edge.end_node for edge in Edge.objects.filter(start_node__node_id=node_id)]
