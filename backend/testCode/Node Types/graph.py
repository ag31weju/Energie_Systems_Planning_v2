import edge
import nodes

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        if node.node_id not in self.nodes:
            self.nodes[node.node_id] = node

    def add_edge(self, edge):
        self.edges.append(edge)