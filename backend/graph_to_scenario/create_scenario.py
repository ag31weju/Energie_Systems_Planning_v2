import json
import os
from pathlib import Path

class Scenario:
    '''
    Class to create a scenario object from the graph data and default values.
    '''
    def __init__(self, graph_data, slider_data, default_node_values):
        self.nodes = []  # contains nodes parsed from json sent from frontend
        self.final_nodes = []  # contains the final nodes with default values
        self.edges = []  # Optional
        self.graph_data = graph_data # the graph json from frontend 
        self.default_node_values = default_node_values  # the default values json
        self.slider_data = slider_data  # the slider data from frontend
        self.process_graph_data()
        self.display()

    def process_graph_data(self):
        """Processes the raw graph data to initialize nodes and assign default values."""
        try:
            # Extract nodes from graph data
            for node in self.graph_data.get("nodes", []):
                if not all(key in node for key in ["id", "type", "label"]):
                    raise ValueError(f"Missing keys in node: {node}")
                self.nodes.append(
                    {"id": node["id"], "type": node["type"], "label": node["label"]}
                )

            # Assign default values to nodes
            self.assign_default_values()

        except Exception as e:
            print(f"Error processing graph data: {e}")

    def assign_default_values(self):
        """Assigns default values from default_node_values to create the final_nodes list."""
        try:
            for node in self.nodes:
                label = node.get("label")
                if label in self.default_node_values.get("label", {}):
                    updated_node = {
                        **node,
                        **self.default_node_values["label"][label],
                    }
                    self.final_nodes.append(updated_node)
                else:
                    # If no matching default values, append the node as is
                    self.final_nodes.append(node)
        except Exception as e:
            print(f"Error assigning default values: {e}")

    def return_final_nodes(self):
        """Returns the final nodes with default values."""
        return self.final_nodes

    def display(self):
        """Displays the final nodes in a JSON format."""
        try:
            print(json.dumps(self.final_nodes, indent=4))
        except Exception as e:
            print(f"Error displaying final nodes: {e}")

    @staticmethod
    def load_json(file_path):
        """Loads a JSON file from the given path."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file at {file_path}")
        except Exception as e:
            print(f"Unexpected error loading JSON file: {e}")
        return {}

    @staticmethod
    def save_json(data, file_path):
        """Saves data to a JSON file at the given path."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving JSON to {file_path}: {e}")



# Solar,Wind,Gas,Coal,House,City,Industry,Battery    names of all nodes
# testing, loading node json and default values json files

# Get the directory of the current script
current_dir = Path(__file__).parent #parent aka root aka backend folder

# Move up one level (cd..) and then navigate into the sibling folder
scenario_json_file = current_dir.parent / "scenario_data" / "scenario_data.json"
default_value_file = current_dir.parent/ "graph_to_scenario" / "default_node_values.json"


graph_data = Scenario.load_json(scenario_json_file)
default_data = Scenario.load_json(default_value_file)


x = Scenario(graph_data, None, default_data)

