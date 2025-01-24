from pathlib import Path
from node_types import Producer, Consumer, Battery
import Utils


class Scenario:
    def __init__(self, graph_data, excel_file_path):
        self.nodes = []  # contains nodes parsed from json sent from frontend
        self.edges = []  # contains edges parsed from json sent from frontend
        self.final_nodes = []  # contains nodes with default values
        self.timestep_chosen = None  # the timestep from the excel file
        self.graph_data = graph_data  # the graph json from frontend
        self.excel_file_path = excel_file_path
        self.defaults = self.get_default_node_values()
        self.get_time_steps()
        self.get_edges()
        
        

    def process_graph_data(self):
        """
        Processes the raw graph data to initialize nodes and assign default values.

        This method iterates over the nodes in the graph data, validates their types, and creates
        corresponding Producer, Consumer, or Battery instances with default values and positions.
        """
        # Define the valid node types
        VALID_TYPES = {"producer", "consumer", "battery"}

        try:
            # Loop through each node in the graph data
            for node in self.graph_data.get("nodes", []):
                # Check that each node contains the required keys
                if not all(key in node for key in ["id", "type", "label"]):
                    raise ValueError(f"Missing keys in node: {node}")

                # Extract and validate the node type
                node_type = node["type"].lower()
                if node_type not in VALID_TYPES:
                    raise ValueError(f"Invalid type in node: {node['type']}")
                

                # Retrieve technology defaults
                technology = node["label"].lower()
                tech_defaults = self.defaults.get(technology)
                if not tech_defaults:
                    raise ValueError(f"No defaults found for technology: {technology}")

                # Create the appropriate node based on type
                if node_type == "producer":
                    self.nodes.append(
                        Producer(
                            node_id=node["id"],
                            technology=node["label"],
                            capacity_cost=tech_defaults.get("capacity_cost"),
                            operation_cost=tech_defaults.get("operation_cost"),
                            operation_lifetime=tech_defaults.get("operation_lifetime"),
                            availability_profile=tech_defaults.get(
                                "availability_profile_name"
                            ),
                        )
                    )
                elif node_type == "consumer":
                    self.nodes.append(
                        Consumer(
                            node_id=node["id"],
                            technology=node["label"],
                            yearly_demand=tech_defaults.get("yearly_demand"),
                            demand_profile_name=tech_defaults.get(
                                "demand_profile_name"
                            ),
                        )
                    )
                elif node_type == "battery":
                    self.nodes.append(
                        Battery(
                            node_id=node["id"],
                            technology=node["label"],
                            capacity=tech_defaults.get("capacity"),
                        )
                    )
        except Exception as e:
            print(f"Error processing graph data: {e}")

    def get_default_node_values(self):
        """Gets the default values for the nodes from the excel file
        and stores as a dictionary in self.defaults"""
        return Utils.load_default_technology_data(self.excel_file_path)

    def get_time_steps(self, scenario_name="default"):
        """
        Gets the timestep for a specific scenario name from excel file and saves it to self.timestep_chosen.

        Parameters:
            scenario_name (str): The name of the scenario to fetch the timestep for (default is "default").
        """
        self.timestep_chosen = Utils.get_timestep(self.excel_file_path, scenario_name)
        print("Timestep chosen:", self.timestep_chosen)

    def get_edges(self):
        """
        Gets the edges from the graph data and stores them in self.edges.
        """
        self.edges = self.graph_data.get("edges", [])
        print("Edges in the scenario:")
        for edge in self.edges:
            print(edge)





def main():
    current_dir = Path(__file__).parent
    scenario_json_file = current_dir.parent / "scenario_data" / "scenario_data.json"
    excel_file_path = current_dir / "volume_data" / "Technology_defaults.xlsx"
    graph_data = Utils.load_json(scenario_json_file)
    # Initialize the Scenario class
    scenario = Scenario(graph_data, excel_file_path=excel_file_path)

    # Process the graph data to create nodes
    scenario.process_graph_data()
    # Print the nodes list
    print("Nodes in the scenario:")
    for node in scenario.nodes:
        print(node)


if __name__ == "__main__":
    main()
