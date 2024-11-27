from features import Position


class EnergyConsumer:
    def __init__(self, name, consumption_rate, position):
        """
        Initializes the EnergyConsumer class.

        :param name: Name of the consumer (e.g., "Residential Area")
        :param consumption_rate: Energy consumption rate in MW (megawatts)
        :param position: Position object indicating x, y coordinates on the board
        """
        self.name = name
        self.consumption_rate = consumption_rate
        self.position = position

    def consume_energy(self):
        """
        Simulates energy consumption.

        :return: Amount of energy consumed (in MW).
        """
        return self.consumption_rate

    def __repr__(self):
        return f"{self.name} at {self.position} with consumption rate {self.consumption_rate} MW"


# Examples of specific consumers
class ResidentialArea(EnergyConsumer):
    def __init__(self, position):
        super().__init__(
            name="Residential Area", consumption_rate=100, position=position
        )


class IndustrialComplex(EnergyConsumer):
    def __init__(self, position):
        super().__init__(
            name="Industrial Complex", consumption_rate=300, position=position
        )


class CommercialBuilding(EnergyConsumer):
    def __init__(self, position):
        super().__init__(
            name="Commercial Building", consumption_rate=50, position=position
        )
