import json
import os
from .graph import Graph
from nodes import Node
from edge import Edge

# MainClass to process the JSON and build the graph
class MainClass:
    def __init__(self, json_file):
        self.json_file = json_file
        self.graph = Graph()

    def process_json(self):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, '../scenario/scenario1/graph.json')

        with open(json_path, "r") as json_file:
            data = json.load(json_file)

        # Process nodes
        for node_data in data['nodes']:
            node_id = node_data['id']
            name = node_data['name']
            coordinates = (node_data['x'], node_data['y'])
            node_type = node_data['type']

            node = Node(node_id, coordinates, node_type, name)
            self.graph.add_node(node)

        # Process edges
        for edge_data in data['edges']:
            start_node = self.graph.nodes[edge_data['start']]
            end_node = self.graph.nodes[edge_data['end']]
            voltage_type = edge_data['weight']

            edge = Edge(start_node, end_node, voltage_type)
            self.graph.add_edge(edge)

    def get_graph(self):
        return self.graph

# Example usage
if __name__ == "__main__":
    main_class = MainClass('../scenario/scenario1/graph.json')
    main_class.process_json()
    graph = main_class.get_graph()

    # Print nodes
    for node_id, node in graph.nodes.items():
        print(f"Node ID: {node.node_id}, Name: {node.name}, Coordinates: {node.coordinates}, Type: {node.node_type}")

    # Print edges
    for edge in graph.edges:
        print(f"Edge from {edge.start_node.node_id} to {edge.end_node.node_id} with voltage type {edge.voltage_type}")
