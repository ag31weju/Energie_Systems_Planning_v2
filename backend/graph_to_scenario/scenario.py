from pathlib import Path
import math
# from .node_types import Producer, Consumer, Battery
# from . import Utils
from node_types import Producer, Consumer, Battery, Timesteps
import Utils
import model_input
import model
import pyomo.environ as pyo


class Scenario:
    def __init__(self, graph_data):
        self.nodes = []  # contains nodes parsed from json sent from frontend
        self.edges = []  # contains edges parsed from json sent from frontend
        self.timestepfile_chosen = None  # the timestep from the excel file
        self.timesteps = []
        self.graph_data = graph_data  # the graph json from frontend
        # folder paths
        self.current_dir = Path(__file__).parent
        self.excel_file_path = (
            self.current_dir / "volume_data" / "Technology_defaults.xlsx"
        )
        self.volume_data_folder = self.current_dir / "volume_data"

    def initialize(self):
        """
        Initializes the Scenario class by processing the graph data and getting the default node values.
        """
        self.get_time_steps()
        self.get_default_node_values()
        self.process_graph_data()
        self.get_edges()
        self.print_nodes()

    def process_graph_data(self):
        """
        Processes the raw graph data to initialize nodes and assign default values.

        This method iterates over the nodes in the graph data, validates their types, and creates
        corresponding Producer, Consumer, or Battery instances with default values and positions.
        """
        # Define the valid node types
        VALID_TYPES = {"producer", "consumer", "battery", "junction"}

        try:
            # Loop through each node in the graph data
            for node in self.graph_data.get("nodes", []) or self.graph_data.get(
                "data", {}
            ).get("nodes", []):
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

                # Process availability_profile_name or demand_profile
                processed_availability_profile = None
                processed_demand_profile = None

                if (
                    "availability_profile_name" in tech_defaults
                    and tech_defaults["availability_profile_name"] != None
                ):
                    processed_availability_profile = self.process_profile(
                        tech_defaults["availability_profile_name"]
                    )

                if (
                    "demand_profile_name" in tech_defaults
                    and tech_defaults["demand_profile_name"] != None
                ):
                    processed_demand_profile = self.process_profile(
                        tech_defaults["demand_profile_name"]
                    )
                # Create the appropriate node based on type
                if node_type == "producer":
                    self.nodes.append(
                        Producer(
                            node_id=node["id"],
                            technology=node["label"],
                            capacity_cost=tech_defaults.get("capacity_cost"),
                            operation_cost=tech_defaults.get("operation_cost"),
                            operation_lifetime=tech_defaults.get("operation_lifetime"),
                            availability_profile=processed_availability_profile,
                        )
                    )
                elif node_type == "consumer":
                    self.nodes.append(
                        Consumer(
                            node_id=node["id"],
                            technology=node["label"],
                            yearly_demand=tech_defaults.get("yearly_demand"),
                            demand_profile=processed_demand_profile,
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
            self.nodes.append(
                Timesteps(timesteplist=self.timesteps)
            )  # at end append timestep list
        except Exception as e:
            print(f"Error processing graph data: {e}")

    def get_default_node_values(self):
        """Gets the default values for the nodes from the excel file
        and stores as a dictionary in self.defaults"""
        self.defaults = Utils.load_default_technology_data(self.excel_file_path)

    def get_time_steps(self, scenario_name="default"):
        """
        Gets the timestep for a specific scenario name from excel file and saves it to self.timestepfile_chosen.

        Parameters:
            scenario_name (str): The name of the scenario to fetch the timestep for (default is "default").
        """
        self.timestepfile_chosen = Utils.get_timestep(
            self.excel_file_path, scenario_name
        )

    def get_edges(self):
        """
        Gets the edges from the graph data and stores them in self.edges.
        """
        self.edges = self.graph_data.get("edges", []) or self.graph_data.get(
            "data", {}
        ).get("edges", [])

    def print_nodes(self):
        """
        Gets the nodes from the graph data and stores them in self.nodes.
        """
        print("Nodes in the scenario:")
        for node in self.nodes:
            print(node)

    def print_edges(self):
        """
        Gets the nodes from the graph data and stores them in self.nodes.
        """
        print("Nodes in the scenario:")
        for edge in self.edges:
            print(edge)

    def print_time_step(self):
        """
        Prints the timestep chosen for the scenario.
        """
        print(f"Time step chosen: {self.timestepfile_chosen}")

    def process_profile(self, profile_name):
        """
        Processes the profile file based on the given profile name and selected timesteps.

        Args:
            profile_name (str): The name of the profile file to process.

        Returns:
            list: Processed and formatted array or data structure.
        """
        try:
            # Handle empty or NaN profile_name
            if not profile_name or (
                isinstance(profile_name, float) and math.isnan(profile_name)
            ):
                # print(f"Skipping invalid profile_name: {profile_name}")
                return []

            # Construct paths using pathlib
            profile_file_path = self.volume_data_folder / profile_name
            indices_file_path = self.volume_data_folder / self.timestepfile_chosen

            # Read and process the profile data
            with open(profile_file_path, "r") as profile_file:
                profile_data = [float(value) for value in profile_file.read().split()]

            # Read and process the indices data
            with open(indices_file_path, "r") as indices_file:
                indices = [int(index.strip()) for index in indices_file.readlines()]
                self.timesteps = indices  # assign timesteps from file to list

            # Extract the corresponding values
            selected_data = [
                profile_data[i - 1] for i in indices
            ]  # timesteps are not 0 index

            # Format the values to six decimal places
            formatted_data = [f"{value:.6f}" for value in selected_data]

            return formatted_data

        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return []
        except ValueError as e:
            print(f"Value error: {e}")
            return []
        except IndexError as e:
            print(f"Index error: {e}")
            return []
        except Exception as e:
            print(f"Error processing profile {profile_name}: {e}")
            return []

    def optimize(self):
        m = model_input.OptNetworkInput()
        m.populate1(self.nodes)
        m.write("test.dat")
        optimizer = model.get_abstract_pyomo_model()
        instance = model.load_input(optimizer, "test.dat")
        instance = model.solve_instance(instance)
        print("Total Expenditure (TOTEX):", pyo.value(instance.TOTEX))
        print("CapEx:", pyo.value(instance.CAPEX))
        print("OpEx:", pyo.value(instance.OPEX))


def main():
    current_dir = Path(__file__).parent
    scenario_json_file = current_dir.parent / "scenario_data" / "scenario_data.json"
    graph_data = Utils.load_json(scenario_json_file)
    # Initialize the Scenario class
    scenario = Scenario(graph_data)
    scenario.initialize()
    scenario.optimize()



if __name__ == "__main__":
    # pass
    main()
