from features import Position


class EnergyProducer:
    def __init__(self, name, production_capacity, position):
        """
        Initializes the EnergyProducer class.

        :param name: Name of the energy producer (e.g., "Solar Plant")
        :param production_capacity: Energy production capacity in MW (megawatts)
        :param position: Position object indicating x, y coordinates on the board
        """
        self.name = name
        self.production_capacity = production_capacity
        self.position = position

    def produce_energy(self):
        """
        Simulates energy production.

        :return: Amount of energy produced (in MW).
        """
        return self.production_capacity

    def __repr__(self):
        return f"{self.name} at {self.position} with capacity {self.production_capacity} MW"


# Examples of specific energy producers
class CoalPlant(EnergyProducer):
    def __init__(self, position):
        super().__init__(name="Coal Plant", production_capacity=10, position=position)


class WindTurbine(EnergyProducer):
    def __init__(self, position):
        super().__init__(name="Wind Turbine", production_capacity=10, position=position)


class SolarPlant(EnergyProducer):
    def __init__(self, position):
        super().__init__(name="Solar Plant", production_capacity=10, position=position)


class NuclearPlant(EnergyProducer):
    def __init__(self, position):
        super().__init__(name="Solar Plant", production_capacity=10, position=position)


class HydroPlant(EnergyProducer):
    def __init__(self, position):
        super().__init__(name="Solar Plant", production_capacity=10, position=position)
