import os
import json
import Graph as graph

# Path to the JSON file
scenario_json_folder = "backend\scenario_data"
scenario_json_file = "scenario_data.json"
file_path = os.path.join(scenario_json_folder, scenario_json_file)

def create_graph():
    # Load JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    graph_data = data.get("data", {})

    # Create the graph
    playfield_graph = graph.Graph()

    # Add nodes
    for node in graph_data.get("nodes", []):
        playfield_graph.add_node(node["id"], node["position"], node["type"], node["label"])

    # Add edges
    for edge in graph_data.get("edges", []):
        playfield_graph.add_edge(edge["id"], edge["source"], edge["target"], edge["color"], edge["style"])

    return playfield_graph

if __name__ == "__main__":
    # Create and display the graph when running this script
    graph_instance = create_graph()
    graph_instance.display()
