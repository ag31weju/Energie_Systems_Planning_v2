# main.py
from features import BackdropFeature, Position
from producers import CoalPlant, WindTurbine, SolarPlant
from consumers import ResidentialArea, IndustrialComplex, CommercialBuilding

# Create some backdrop features
backdrop = BackdropFeature.GRASSLAND
print(f"Backdrop feature: {backdrop.name}")

# Create some energy producers
coal_plant = CoalPlant(Position(1, 1))
wind_turbine = WindTurbine(Position(3, 4))
solar_plant = SolarPlant(Position(5, 5))

# Create some energy consumers
residential = ResidentialArea(Position(2, 2))
industrial = IndustrialComplex(Position(6, 7))
commercial = CommercialBuilding(Position(8, 3))

# Simulate energy production and consumption
producers = [coal_plant, wind_turbine, solar_plant]
consumers = [residential, industrial, commercial]

total_energy_produced = sum(producer.produce_energy() for producer in producers)
total_energy_consumed = sum(consumer.consume_energy() for consumer in consumers)

print("\nEnergy Producers:")
for producer in producers:
    print(producer)

print("\nEnergy Consumers:")
for consumer in consumers:
    print(consumer)

print(f"\nTotal Energy Produced: {total_energy_produced} MW")
print(f"Total Energy Consumed: {total_energy_consumed} MW")

if total_energy_produced >= total_energy_consumed:
    print("Energy supply is sufficient.")
else:
    print("Energy supply is insufficient.")
