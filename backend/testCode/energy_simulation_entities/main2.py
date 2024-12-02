from graph import Graph
import json

def main():
    # Create a new graph
    graph = Graph()

    # Add nodes to the graph
    print("Adding nodes...")
    graph.add_node(1, "type_a", "Node1", 0, 0)
    graph.add_node(2, "type_b", "Node2", 3, 4)
    graph.add_node(3, "type_c", "Node3", 1, 1)
    graph.add_node(4, "type_d", "Node4", 5, 2)

    # Display nodes
    print("\nNodes in the graph:")
    for node in graph.nodes.values():
        print(node)

    # Add edges to the graph
    print("\nAdding edges...")
    graph.add_edge(1, 2, weight=5)
    graph.add_edge(1, 3, weight=2)
    graph.add_edge(2, 4, weight=3)

    # Display edges
    print("\nEdges in the graph:")
    for edge in graph.edges:
        print(edge)

    # Display the complete graph
    print("\nComplete graph representation:")
    print(graph)

    # Test distance calculation between nodes
    print("\nTesting distance calculation...")
    node1 = graph.nodes[1]
    node2 = graph.nodes[2]
    distance = node1.distance_to(node2)
    print(f"Distance between {node1.name} and {node2.name}: {distance:.2f}")

     # Convert graph to dictionary
    graph_dict = graph.to_dict()

    # Save to JSON file
    with open("graph.json", "w") as json_file:
        json.dump(graph_dict, json_file, indent=4)

    print("Graph saved to 'graph.json'.")

if __name__ == "__main__":
    main()
