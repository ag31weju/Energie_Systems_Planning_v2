from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class Technology(ABC):


   @property
   def name(self):
      return self.get_name()
   
   @abstractmethod
   def get_name(self):
      pass

   pass


class ProducerType(Enum):
   # Just a few examples. Using enumerations because we might want to translate the name to other languages
   PV = 'PV'
   WIND = 'WIND'
   GASPP = 'GASPP'

   #def parse_name(self, language):
      # This is just a stub. We would have to implement a translation system
   #   return "The name in the language"

class Producer(Technology):

   def __init__(self, producer_type,  capacity_cost=0, operation_cost=0, operational_lifetime=0):
      
      self.producer_type = producer_type
      self.is_producer = True


      self.capacity_cost = capacity_cost
      self.operation_cost = operation_cost
      self.operational_lifetime = operational_lifetime   
      #renuable producer: availability profile name
      #time step data^
   
   def get_name(self):
      return self.producer_type.value

   @classmethod
   def make(cls, producer_type:ProducerType, **kwargs):
      standard_values = cls.get_standard_values(producer_type)
      standard_values.update(kwargs)
      return cls(producer_type, **standard_values)

   @staticmethod
   def get_standard_values(producer_type:ProducerType):
      match producer_type:
         case ProducerType.PV:
            return {"capacity_cost": 1000, "operation_cost": 10, "operational_lifetime": 20}
         case ProducerType.WIND:
            return {"capacity_cost": 2000, "operation_cost": 20, "operational_lifetime": 20}
         case ProducerType.GASPP:
            return {"capacity_cost": 3000, "operation_cost": 30, "operational_lifetime": 20}
         case _:
            raise ValueError("Producer type not found")


class ConsumerType(Enum):
   CITY = 'CITY'
   HOUSE = 'HOUSE'
   COMMERCIAL = 'COMMERCIAL'

class Consumer(Technology):
   
   def __init__(self):

      self.is_consumer = True
      self.yearly_demand = 0
      self.demand_profile_name = None # This is a string that will be used to identify the demand profile. It will be used to get the demand profile from the database
      #volume data
      pass

   @staticmethod
   def get_standard_values(consumer_type:ConsumerType):
      match consumer_type:
         case ConsumerType.CITY:
            return {"yearly_demand": 10000}
         case ConsumerType.HOUSE:
            return {"yearly_demand": 1000}
         case ConsumerType.COMMERCIAL:
            return {"yearly_demand": 1000}
         case _:
            raise ValueError("Consumer type not found")
   
   @classmethod
   def make(cls, consumer_type:ConsumerType, **kwargs):
      standard_values = cls.get_standard_values(consumer_type)
      standard_values.update(kwargs)
      return cls(consumer_type, **standard_values)
   pass



class Node:
   pass

class Network:

   def __init__(self, nodes:List[Node]):
      self.nodes = nodes
   pass

class Unit:
   def __init__(self, technology:Technology, node:Node):
      self.technology = technology
      self.node = node
      pass
   pass

class TimeStep:
   pass

class Scenario:
   
   def __init__(self, times:List[TimeStep], network:Network, units:List[Unit]):

      self.times: List[TimeStep] = times
      self.network: Network = network
      self.nodes: List[Node] = self.network.nodes
      self.units: List[Unit] = units

      self.technologies: List[Technology] = list(set([unit.technology for unit in units])) # This is a set to avoid duplicates
      
      # consistency checks
      

      pass
   pass