from pathlib import Path
import math, json
from . node_types import Producer, Consumer, Battery, Timesteps
from . import Utils
from . import model_input
from . import model
import pyomo.environ as pyo


class Scenario:
    def __init__(self, graph_data):
        self.nodes = []  # contains nodes parsed from json sent from frontend
        self.edges = []  # contains edges parsed from json sent from frontend
        self.timestepfile_chosen = None  # the timestep from the excel file
        self.timesteps = []
        self.graph_data = graph_data  # the scenario+slider json from frontend
        self.reset_flag = False
        self.auto_simulate_flag = False
        self.prodCapacities = []
        self.modified_slider_values = []
        # folder paths
        self.current_dir = Path(__file__).parent
        self.excel_file_path = (
            self.current_dir / "volume_data" / "Technology_defaults.xlsx"
        )
        self.volume_data_folder = self.current_dir / "volume_data"
        self.initialize()

    def initialize(self):
        """
        Initializes the Scenario class by processing the graph data and getting the default node values.
        """
        self.get_time_steps()
        self.get_default_node_values()
        self.get_slider_data()
        self.process_graph_data()
        self.get_edges()
        # self.print_nodes()

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
                        tech_defaults["availability_profile_name"],
                        profile_type="availability",
                    )

                if (
                    "demand_profile_name" in tech_defaults
                    and tech_defaults["demand_profile_name"] != None
                ):
                    processed_demand_profile = self.process_profile(
                        tech_defaults["demand_profile_name"], profile_type="demand"
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
                            installed_capacity=self.get_installed_capacity(node["id"]),  # gets slider value for a node 
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
                            installed_capacity=self.get_installed_capacity(node["id"]),  # gets slider value for a node 
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

    def get_slider_data(self):
        """Gets slider data from json and saves it to respective"""
        slider_data = self.graph_data.get("sliderData")
        self.reset_flag = slider_data.get("reset")
        self.autoSimulate_flag = slider_data.get("autoSimulate")
        self.prodCapacities = [
            (id, value) for id, value in slider_data.get("prodCapacities")
        ]
        self.modified_slider_values = [
            [f"node_{item[0]}", item[1]] for item in self.prodCapacities
        ]  # adds node Id to slider data

    def print_nodes(self):
        """
        Gets the nodes from the graph data and stores them in self.nodes.
        """
        print("Nodes in the scenario:")
        for node in self.nodes:
            print(node)


    def get_installed_capacity(self, nodeId: str):
        '''Returns the installed capacity corresponding to a node ID'''
        for node in self.modified_slider_values:
            if node[0] == nodeId:
                return node[1]
        return 0  # Return 0 if nodeId is not found

    def process_profile(self, profile_name, profile_type):
        """
        Processes the profile file based on the given profile name and selected timesteps. Availability profiles are processed differently from demand profiles. Demand profiles must be normalized to sum 1, otherwise model renders infeasible.

        Args:
            profile_name (str): The name of the profile file to process.
            profile_type (str): The type of profile to process (availability or demand).

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

            # Normalize the demand profile if necessary
            if profile_type.lower() == "demand":
                # Normalize the demand profile to sum to 1
                sum_values = sum(selected_data)
                if sum_values == 0:
                    raise ValueError("Sum of demand profile values is zero.")
                selected_data = [value / sum_values for value in selected_data]
            elif profile_type.lower() == "availability":
                # Availability profiles are not normalized
                pass
            else:
                raise ValueError(
                    f"Invalid profile type: {profile_type}. Must be 'demand' or 'availability'."
                )

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

    @staticmethod
    def parse_json(json_file: json):
        """
        Get the json file from frontend and using create_scenario.py, parse the json file for optimizer
        """
        scenario = Scenario(json_file)
        scenario.optimize()



    def optimize(self):
        m = model_input.OptNetworkInput()
        m.populate_from_scenario_list(self.nodes, self.timesteps)
        #temp_file_path = m.save_to_temp_file() #saves file temporarily for multiple users
        m.write("somefile.dat") #save file to folder

        '''
        optimizer = model.get_abstract_pyomo_model(fix_capacities=False)
        instance = model.load_input(optimizer)
        instance = model.load_input_from_temp_file(optimizer, temp_file_path)
        instance = model.solve_instance(instance)
        
        print("Total Expenditure: ", pyo.value(instance.TOTEX))
        print("CapEx: ", pyo.value(instance.CAPEX))
        print("OpEx: ", pyo.value(instance.OPEX))
        print("Demand: ", model.get_variable_value(instance, "Pd"))
        print("Generation: ", model.get_variable_value(instance, "Pg"))
        print("Unmet Demand: ", model.get_variable_value(instance, "nSPd"))
        print("Generation Capacity: ", model.get_variable_value(instance, "Cg"))
        print("Power Injection: ", model.get_variable_value(instance, "Pi"))
        '''


def main():
    current_dir = Path(__file__).parent
    scenario_json_file = current_dir.parent / "scenario_data" / "scenario_data.json"
    graph_data = Utils.load_json(scenario_json_file)
    # Initialize the Scenario class
    scenario = Scenario(graph_data)
    scenario.optimize()


if __name__ == "__main__":
    main()
