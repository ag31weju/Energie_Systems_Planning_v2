from scenario_processing import parse_json
import os

class GraphProcessor:
    def __init__(self, graph: None):
        """
        Initializes the GraphProcessor with a NetworkX graph.
        """
        self.graph = graph if graph else {"nodes": {}, "edges": {}} 
    
    def parse_and_load_graph(self, json_input):
        """
        Parses the JSON input (string or file-like object) and loads the graph.
        """
        self.graph = parse_json(json_input)

    def get_all_nodes(self):
        """
        Returns a list of all nodes with their attributes.
        """
        return list(self.graph.nodes(data=True))

    def get_all_edges(self):
        """
        Returns a list of all edges with their attributes.
        """
        return list(self.graph.edges(data=True))

    def get_node_details(self, node_id):
        """
        Returns the details of a specific node by its ID.
        """
        if node_id in self.graph:
            return self.graph.nodes[node_id]
        else:
            raise ValueError(f"Node with ID {node_id} does not exist.")

    def print_summary(self):
        """
        Prints a summary of nodes and edges in the graph.
        """
        print(f"Number of nodes: {self.graph.number_of_nodes()}")
        print(f"Number of edges: {self.graph.number_of_edges()}")
        print("Nodes:", self.get_all_nodes())
        print("Edges:", self.get_all_edges())

    def get_node_by_id(self, node_id):
        """
        Returns the details of a node given its ID.
        """
        node = self.get_node_details(node_id)
        print(f"Details of Node ID {node_id}: {node}")
        return node

    def get_nodes_by_type(self, node_type):
        """
        Returns a list of all nodes of a specific type.
        """
        nodes_by_type = [(node_id, data) for node_id, data in self.graph.nodes(data=True) if data.get('type') == node_type]
        if nodes_by_type:
            print(f"Nodes of type '{node_type}':")
            for node_id, attributes in nodes_by_type:
                print(f"  ID: {node_id}, Attributes: {attributes}")
        else:
            print(f"No nodes of type '{node_type}' found.")
        return nodes_by_type

    def get_connected_nodes(self, node_id):
        """
        Returns a list of all nodes that are connected to the given node ID.
        Both incoming and outgoing connections are included.
        """
        if node_id not in self.graph:
            raise ValueError(f"Node with ID {node_id} does not exist.")

        # Get outgoing neighbors (edges going out of the node)
        outgoing = list(self.graph.successors(node_id))

        # Get incoming neighbors (edges coming into the node)
        incoming = list(self.graph.predecessors(node_id))

        # Combine incoming and outgoing neighbors
        connected_nodes = set(outgoing + incoming)

        print(f"Nodes connected to Node ID {node_id}: {connected_nodes}")
        return connected_nodes

def main():
    processor = GraphProcessor()
    json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'graph_data.json')
    processor.parse_json(json_file_path)
    processor.print_summary()

    node_id = 'node_1'
    processor.get_node_by_id(node_id)
    processor.get_nodes_by_type('producer')
    processor.get_connected_nodes(node_id)

if __name__ == "__main__":
    main()   