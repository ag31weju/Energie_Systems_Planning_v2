# --------------------------------------------------
#  .DAT File Parser
#  Barbosa, J. (2024)
#  mail@juliabarbosa.net
# --------------------------------------------------

import math
from typing import Any
import numpy as np
import node_types
from pathlib import Path


from abc import ABC, abstractmethod
import random


## -- Abstract Parser Class, can be used to parse .dat files --##
class ModelSet:
    def __init__(self, name: str, dim: int):
        self.name: str = name
        self.dim: int = dim
        self.val = []

    def write(self, f):
        f.write(f"set {self.name} := \n")
        for v in self.val:
            if self.dim > 1:
                f.write(" ".join(str(vv) for vv in v) + "\n")
            else:
                f.write(f"{v} \n")
        f.write("; \n\n")

    def __repr__(self) -> str:
        return f"SET:{self.name}"


class ModelParam:
    """
    Parameter Class
    """

    def __init__(self, name, set_list: list[ModelSet], scaling_factor=1, model=None):
        self.name = name
        self.set_list = set_list
        self.dim: int = 0
        self.set_names = []
        self.model = model

        for s in set_list:
            self.dim = self.dim + s.dim
            self.set_names.append(s.name)
        self.vals = dict()
        self.sf = scaling_factor

    def add_value(self, value, key=None):
        # Add new value
        if self.dim == 0:
            self.vals = value * self.sf
        else:
            key = self.is_key_valid(key)
            nkey = " ".join([str(x) for x in key])
            self.vals[str(nkey)] = value * self.sf

    def is_key_valid(self, key):
        # Verify if key is a valid key
        # verify if the is a list/tuple
        if not isinstance(key, (list, tuple)):
            # assume it is a single value
            key = [key]

        if len(key) != self.dim:
            raise ValueError(
                "%s is invalid  for parameter %s -  Invalid Key size!"
                % (key, self.name)
            )

        return key

    def write(self, f):
        if not self.vals:
            return

        if self.name in ["demand_profile", "availability_profile"]:
            if not self.model:
                raise ValueError(f"Model reference is missing in ModelParam {self.name}.")

            # Get timesteps from `T` set
            T_set = self.model.get_set("T")
            if not T_set or not T_set.val:
                raise ValueError(f"Set T is missing or empty in the model for {self.name}.")

            time_indices = sorted(T_set.val)  # Get actual T values (e.g., [1, 2, 3])
            num_timesteps = len(time_indices)  # Keep count of timesteps

            # Get the unique entities (e.g., City, Industry, Solar)
            entities = sorted(set(k.split()[0] for k in self.vals.keys()))

            # Write the header using `T` values instead of 0-based indices
            f.write(f'param {self.name}:   ' + "   ".join(map(str, time_indices)) + " :=\n")

            # Write each entity's values **in the original order** but with `T` as headers
            for entity in entities:
                values = [f"{self.vals.get(f'{entity} {t_index}', 0):.6f}" for t_index in range(num_timesteps)]
                f.write(f"{entity:<15} " + "   ".join(values) + "\n")

            f.write(";\n\n")  # Ensure correct semicolon placement

        else:
            f.write(f'param {self.name} := \n')

            if self.dim == 0:
                f.write(f'{self.vals}\n')
            else:
                for key, value in self.vals.items():
                    if not math.isnan(value):
                        f.write(f'{key} {value}\n')

            f.write(";\n\n")  # Ensure a semicolon at the end of normal parameters



class AbstractModelInput(ABC):
    def __init__(self) -> None:
        self._sets = []
        self._params = []

        self._init_structure()

    @property
    def sets(self):
        return self._sets

    @property
    def _set_names(self):
        return [s.name for s in self.sets]

    @property
    def params(self):
        return self._params

    @property
    def _param_names(self):
        return [p.name for p in self.params]

    @abstractmethod
    def _init_structure(self):
        """
        In this method, the user should define the structure of the model. Clearly definning
        which sets and parameters are needed. Note that parameters and sets must not be initially populated
        """
        pass

    def get_set(self, name: str):
        for s in self._sets:
            if s.name == name:
                return s
        return None

    def get_param(self, name: str):
        for p in self._params:
            if p.name == name:
                return p
        return None

    def __getitem__(self, key: str):
        if key in self._set_names:
            return self.get_set(key)
        if key in self._param_names:
            return self.get_param(key)
        else:
            raise ValueError(
                f"Key {key} not found in the model. Are you sure it is a valid set or parameter?"
            )

    def add_set(self, name: str, dim: int):
        s = ModelSet(name, dim)
        self._sets.append(s)
        return s

    def add_param(self, name: str, set_list: list[ModelSet], scaling_factor=1):
        p = ModelParam(name, set_list, scaling_factor, model=self)
        self._params.append(p)
        return p

    def write(self, file: str):
        script_dir = (
            Path(__file__).resolve().parent
        )  # Get the directory where the script is located
        file_path = script_dir / file  # Construct the full file path

        with file_path.open("w") as f:  # Use Path's open() method
            for s in self._sets:
                s.write(f)
            for p in self._params:
                p.write(f)  # This calls the updated ModelParam.write method

    pass


class OptNetworkInput(AbstractModelInput):

    def _init_structure(self):
        # Dictoionary of sets:dimension
        # H: tech, T: timesteps, U:(NodeId,Tech),N NodeId,
        sets = dict(T=1, N=1, H=1, U=2)

        for k, v in sets.items():
            self.add_set(k, v)

        # Dictoionary of parameters: pname:set_list
        params = dict(
            capacity_cost=[self["H"]],
            operational_cost=[self["H"]],
            operational_lifetime=[self["H"]],
            demand_profile=[self["H"], self["T"]],
            yearly_demand=[self["H"]],
            availability_profile=[self["H"], self["T"]],
            is_consumer=[self["H"]],
            is_producer=[self["H"]],
        )

        for k, v in params.items():
            self.add_param(k, v)
        pass

    # Takes the list generated from scenario and prepares it for conversion to .dat
 
    def populate1(self, scenario_list: list):
        nodes = set()
        technologies = set()

        for item in scenario_list:
            # Handle Timesteps first to avoid AttributeError
            if isinstance(item, node_types.Timesteps):
                if hasattr(item, "timesteps"):
                    self["T"].val = item.timesteps  # Use the correct attribute name
                continue  # Skip the rest of the loop for Timesteps

            node_id = item.node_id
            tech = item.technology
            nodes.add(node_id)
            technologies.add(tech)

            if isinstance(item, node_types.Producer):
                self["is_producer"].add_value(1, tech)
                if hasattr(item, "capacity_cost"):  # Fixed typo
                    self["capacity_cost"].add_value(item.capacity_cost, tech)
                if hasattr(item, "operation_cost"):
                    self["operational_cost"].add_value(item.operation_cost, tech)
                if hasattr(item, "operation_lifetime"):
                    self["operational_lifetime"].add_value(item.operation_lifetime, tech)
                if hasattr(item, "availability_profile"):
                    for t, value in enumerate(item.availability_profile):
                        self["availability_profile"].add_value(float(value), (tech, t))

            elif isinstance(item, node_types.Consumer):
                self["is_consumer"].add_value(1, tech)
                if hasattr(item, "yearly_demand"):
                    self["yearly_demand"].add_value(item.yearly_demand, tech)
                if hasattr(item, "demand_profile"):
                    for t, value in enumerate(item.demand_profile):
                        self["demand_profile"].add_value(float(value), (tech, t))

            elif isinstance(item, node_types.Battery):
                pass  # No specific action for Battery

        # Populate sets
        self["N"].val = list(nodes)
        self["H"].val = list(technologies)

        # Generate connections (U set)
        self["U"].val = [(tech, node) for node in nodes for tech in technologies]


    def populate(self):
        # This is a simple example. The input probably should come ffrom a scenario class
        n_ts = 24  # timesteps
        dt = 1  # per hour
        # Populate the sets
        self["T"].val = list(range(0, n_ts))

        self["N"].val = ["Node1", "Node2", "Node3"]

        self["H"].val = ["City", "PV"]

        self["U"].val = [("City", "Node1"), ("PV", "Node2")]

        # Populate the parameters
        self["is_consumer"].add_value(1, "City")
        self["is_producer"].add_value(1, "PV")

        self["capacity_cost"].add_value(100, "PV")
        self["operational_lifetime"].add_value(8, "PV")
        self["operational_cost"].add_value(10, "PV")

        self["yearly_demand"].add_value(10000, "City")
        pass


if __name__ == "__main__":
    # for testing
    entity_list = [
        node_types.Producer(
            node_id="node_1",
            technology="Solar",
            capacity_cost=1000,
            operation_cost=36526,
            operation_lifetime=25.0,
            availability_profile=["0.000000", "0.000000"],
        ),
        node_types.Consumer(
            node_id="node_2",
            technology="City",
            yearly_demand=50000000.0,
            demand_profile=["0.000076", "0.000072"],
        ),
        node_types.Battery(node_id="node_3", technology="Battery", capacity=10000.0),
        node_types.Consumer(
            node_id="node_5",
            technology="Industry",
            yearly_demand=100000000.0,
            demand_profile=["0.000076", "0.000072"],
        ),
        node_types.Producer(
            node_id="node_6",
            technology="Coal",
            capacity_cost=2000,
            operation_cost=0.08,
            operation_lifetime=40.0,
            availability_profile=[],
        ),
        node_types.Timesteps([1, 2]),
    ]
    h = OptNetworkInput()
    # h.populate1(entity_list)
    h.populate()

    h.write("test2.dat")

    pass
