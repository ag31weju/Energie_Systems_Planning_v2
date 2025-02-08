
# --------------------------------------------------
#  .DAT File Parser
#  Barbosa, J. (2024)
#  mail@juliabarbosa.net
# -------------------------------------------------- 

import math
from typing import Any
import numpy as np


from abc import ABC, abstractmethod
import random


## -- Abstract Parser Class, can be used to parse .dat files --##
class ModelSet:
   def __init__(self, name:str, dim:int):
        self.name:str = name
        self.dim:int = dim
        self.val = []
        
   def write(self,f):
        f.write(f'set {self.name} := \n')
        for v in self.val:
            if self.dim >1:
               f.write(" ".join(str(vv) for vv in v) + "\n")
            else:
               f.write(f'{v} \n')
        f.write('; \n\n')

      
   def __repr__(self) -> str:
       return f'SET:{self.name}'
        
class ModelParam:
    """
    Parameter Class
    """
    def __init__(self, name, set_list:list[ModelSet], scaling_factor = 1):
        self.name = name
        self.set_list = set_list
        self.dim:int = 0
        self.set_names = []

        for s in set_list:
            self.dim= self.dim + s.dim
            self.set_names.append(s.name)
        self.vals = dict()
        self.sf = scaling_factor
        
    def add_value(self, value, key=None):
        #Add new value
        if self.dim == 0:
            self.vals = value*self.sf
        else:
            key =  self.is_key_valid(key)
            nkey = " ".join([str(x) for x in key])
            self.vals[str(nkey)] = value*self.sf
         
        
    def is_key_valid(self, key):
        #Verify if key is a valid key
         # verify if the is a list/tuple
         if not isinstance(key, (list, tuple)):
            # assume it is a single value
            key = [key]

         if len(key) != self.dim:
            raise ValueError ("%s is invalid  for parameter %s -  Invalid Key size!" %(key, self.name))
           
         return key
    
    def write(self, f):
      if not self.vals:
         return
      f.write(f'param {self.name} := \n')
      if self.dim == 0:
         f.write(f'{self.vals}\n')
      else:
         for key, value in self.vals.items():
               if not math.isnan(value):
                  f.write(f'{key} {value}\n')
      f.write(';\n\n')

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
   
   def get_set(self, name:str):
      for s in self._sets:
          if s.name == name:
              return s
      return None
   
   def get_param(self, name:str):
      for p in self._params:
          if p.name == name:
              return p
      return None
   
   def __getitem__(self, key:str):
      if key in self._set_names:
         return self.get_set(key)
      if key in self._param_names:
         return self.get_param(key)
      else:
         raise ValueError(f'Key {key} not found in the model. Are you sure it is a valid set or parameter?')


   def add_set(self, name:str, dim:int):
        s = ModelSet(name, dim)
        self._sets.append(s)
        return s
   def add_param(self, name:str, set_list:list[ModelSet], scaling_factor = 1):
        p = ModelParam(name, set_list, scaling_factor)
        self._params.append(p)
        return p
   
   def write(self, file:str):
         f = open(file, "w")
         for s in self._sets:
            s.write(f)
         for p in self._params:
            p.write(f)
         f.close()
         pass
   pass


class OptNetworkInput(AbstractModelInput):

   def _init_structure(self):
      # Dictoionary of sets:dimension
      sets = dict(T=1, N=1, H=1, U=2)


      for k,v in sets.items():
         self.add_set(k,v)

      # Dictoionary of parameters: pname:set_list
      params = dict(capacity_cost = [self['H']],
                  operational_cost = [self['H']],
                  operational_lifetime = [self['H']],
                  demand_profile = [self['H'], self['T']],
                  yearly_demand = [self['H']],
                  availability_profile = [self['H'], self['T']],
                  is_consumer = [self['H']], 
                  is_producer = [self['H']] ,
                  )
      
      for k,v in params.items():
         self.add_param(k,v)
      pass       

   def populate(self, scenario):
       # TODO: Parse a scenario class to the input. 
       
       pass
   def populate(self):
      # This is a simple example. The input probably should come ffrom a scenario class
      n_ts = 24 #timesteps
      dt=1      #per hour
      #Populate the sets
      self['T'].val = list(range(0, n_ts))

      self['N'].val = ["Node1", "Node2", "Node3"]

      self['H'].val = ["City", "PV"]
  
      self['U'].val = [("City", "Node1"), ("PV", "Node2")]      


      # Populate the parameters
      self['is_consumer'].add_value(1, "City")
      self['is_producer'].add_value(1, "PV")

      self['capacity_cost'].add_value(100, "PV")
      self['operational_lifetime'].add_value(8, "PV")
      self['operational_cost'].add_value(10, "PV")

      self['yearly_demand'].add_value(10000, "City")
      pass

if __name__ == "__main__":
   h = OptNetworkInput()
   h.populate()

   h.write('test.dat')

   pass



      


      
          
             


