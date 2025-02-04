class Producer:
    def __init__(
        self,
        node_id,
        technology,
        capacity_cost,
        operation_cost,
        operation_lifetime,
        availability_profile,
    ):
        self.node_id = node_id
        self.technology = technology
        self.capacity_cost = capacity_cost
        self.operation_cost = operation_cost
        self.operation_lifetime = operation_lifetime
        self.availability_profile = availability_profile

    def __repr__(self):
        return (
            f"Producer(node_id={self.node_id}, technology={self.technology}, "
            f"capacity_cost={self.capacity_cost}, "
            f"operation_cost={self.operation_cost}, operation_lifetime={self.operation_lifetime}, "
            f"availability_profile={self.availability_profile})"
        )


class Consumer:
    def __init__(self, node_id, technology, yearly_demand, demand_profile):
        self.node_id = node_id
        self.technology = technology
        self.yearly_demand = yearly_demand
        self.demand_profile = demand_profile

    def __repr__(self):
        return (
            f"Consumer(node_id={self.node_id}, technology={self.technology}, "
            f"yearly_demand={self.yearly_demand}, "
            f"demand_profile={self.demand_profile})"
        )


class Battery:
    def __init__(self, node_id, technology, capacity):
        self.node_id = node_id
        self.technology = technology
        self.capacity = capacity

    def __repr__(self):
        return (
            f"Battery(node_id={self.node_id}, technology={self.technology}, "
            f"capacity={self.capacity})"
        )


class Timesteps:
    def __init__(self, timesteplist):
        self.timesteps = timesteplist

    def __repr__(self):
        return(f"Timesteps({self.timesteps})")
