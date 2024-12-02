class Node:
    def __init__(self, node_id, node_type, name, x, y):
        """
        Initialize a Node object.
        """
        self.id = node_id
        self.type = node_type
        self.name = name
        self.x = x
        self.y = y
    
    def distance_to(self, other_node):
        """
        Calculate the Euclidean distance to another node.
        """
        return ((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2) ** 0.5

    def __repr__(self):
        """
        Return a string representation of the Node object for debugging.
        """
        return f"Node(id={self.id}, type='{self.type}', name='{self.name}', x={self.x}, y={self.y})"


class Edge:
    def __init__(self, start_node, end_node, weight=1):
        """
        Initialize an Edge object.
        
        :param start_node: The starting node of the edge
        :param end_node: The ending node of the edge
        :param weight: Weight of the edge (default is 1)
        """
        self.start = start_node
        self.end = end_node
        self.weight = weight #powerline type

    def __repr__(self):
        """
        Return a string representation of the Edge object for debugging.
        """
        return f"Edge(start={self.start.id}, end={self.end.id}, weight={self.weight})"


class Graph:
    def __init__(self):
        """
        Initialize a Graph object.
        """
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, node_type, name, x, y):
        """
        Add a node to the graph.
        """
        if node_id in self.nodes:
            raise ValueError(f"Node with id {node_id} already exists.")
        self.nodes[node_id] = Node(node_id, node_type, name, x, y)

    def add_edge(self, start_node_id, end_node_id, weight=1):
        """
        Add an edge to the graph.
        """
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph before adding an edge.")
        start_node = self.nodes[start_node_id]
        end_node = self.nodes[end_node_id]
        edge = Edge(start_node, end_node, weight)
        self.edges.append(edge)

    def __repr__(self):
        """
        Return a string representation of the Graph object.
        """
        nodes_repr = ", ".join(str(node) for node in self.nodes.values())
        edges_repr = ", ".join(str(edge) for edge in self.edges)
        return f"Graph(Nodes=[{nodes_repr}], Edges=[{edges_repr}])"
    
    def to_dict(self):
        """
        Convert the graph to a dictionary representation.
        """
        return {
            "nodes": [
                {
                    "id": node.id,
                    "type": node.type,
                    "name": node.name,
                    "x": node.x,
                    "y": node.y
                }
                for node in self.nodes.values()
            ],
            "edges": [
                {
                    "start": edge.start.id,
                    "end": edge.end.id,
                    "weight": edge.weight
                }
                for edge in self.edges
            ]
        }

