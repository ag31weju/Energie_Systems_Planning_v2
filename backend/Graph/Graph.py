class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes by their IDs
        self.edges = []  # List to store edges

    def add_node(self, node_id, position, node_type, label):
        """Add a node to the graph."""
        if node_id in self.nodes:
            raise ValueError(f"Node with ID '{node_id}' already exists.")
        self.nodes[node_id] = {
            "position": position,
            "type": node_type,
            "label": label,
        }

    def add_edge(self, edge_id, source, target, color, style):
        """Add an edge to the graph."""
        if any(edge['id'] == edge_id for edge in self.edges):
            raise ValueError(f"Edge with ID '{edge_id}' already exists.")
        self.edges.append({
            "id": edge_id,
            "source": source,
            "target": target,
            "color": color,
            "style": style,
        })

    def display(self):
        """Display the graph details."""
        print("Nodes:")
        for node_id, node_info in self.nodes.items():
            print(f"ID: {node_id}, Position: {node_info['position']}, "
                  f"Type: {node_info['type']}, Label: {node_info['label']}")

        print("\nEdges:")
        for edge in self.edges:
            print(f"ID: {edge['id']}, Source: {edge['source']}, "
                  f"Target: {edge['target']}, Color: {edge['color']}, Style: {edge['style']}")
