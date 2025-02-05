# --------------------------------------------------
#  Optimization Model for School Demostrator
#  Barbosa, J. (2025)
#  mail@juliabarbosa.net
# --------------------------------------------------  

# Importing Libraries
import pyomo.environ as pyo
from pyomo.dataportal import DataPortal
from pathlib import Path

OPT_DEBUG = False  # Debugging flag

def get_abstract_pyomo_model():

   model = pyo.AbstractModel()

   ## Sets
   model.T = pyo.Set(ordered=True) # Times
   model.N = pyo.Set() # Nodes


   model.H = pyo.Set() # Technologies
   
   model.U = pyo.Set(within=model.H*model.N) # Technologies at nodes

   ## Parameters ##
   model.is_consumer = pyo.Param(model.H, default=0) # Is Consumer
   model.is_producer = pyo.Param(model.H, default=0) # Is Generator

   model.capacity_cost = pyo.Param(model.H, default =0) # Capacity Cost
   model.operational_cost = pyo.Param(model.H, default =0) # Operational Cost
   model.operational_lifetime = pyo.Param(model.H, default = 100) # Operational Lifetime

   model.demand_profile = pyo.Param(model.H, model.T) # Demand Profile
   model.yearly_demand = pyo.Param(model.H, default=0) # Yearly Demand

   model.availability_profile = pyo.Param(model.H, model.T, default=1) # Availability Profile

   ## Dynamic Sets 
   model.Ug = pyo.Set(within=model.U, initialize=lambda model: [(h,n) for (h,n)  in model.U if model.is_producer[h]]) # Generators
   model.Uc = pyo.Set(within=model.U, initialize=lambda model: [(h,n) for (h,n) in model.U if model.is_consumer[h]]) # Consumers


   ## Variables ##

   # Cost Variables
   model.OPEX = pyo.Var() # Operational Expenditure
   model.CAPEX = pyo.Var() # Capital Expenditure
   model.TOTEX = pyo.Var() # Total Expenditure #send to frontend

   # Power Variables
   model.Pg = pyo.Var(model.Ug, model.T, within=pyo.NonNegativeReals) # Generation #send to frontend
   model.Pd = pyo.Var(model.Uc, model.T, within=pyo.NonNegativeReals) # Demand      #send to frontend

   model.Pi = pyo.Var(model.N, model.T) 

   model.Cg = pyo.Var(model.Ug, within=pyo.NonNegativeReals) # Generation Capacity
   #e.g x^2 function, around 0 being best

   ## Equations ##

   # Objective Function
   model.obf = pyo.Objective(expr=model.TOTEX, sense=pyo.minimize)

   # Cost Equations
   def totex_rule(model):
      return model.TOTEX == model.CAPEX + model.OPEX
   model.totex_eq = pyo.Constraint(rule=totex_rule)

   def capex_rule(model):
      # Capex already normalized by lifetime
      return model.CAPEX == sum(model.Cg[h,n]*model.capacity_cost[h]/model.operational_lifetime[h] for h in model.H for n in model.N if (h,n) in model.Ug)
   model.capex_eq = pyo.Constraint(rule=capex_rule)

   def opex_rule(model):
      # Cost on the modelled time period
      period_cost = sum(model.Pg[h,n,t]*model.operational_cost[h] for h in model.H for n in model.N if (h,n) in model.Ug for t in model.T)
      # Extrapolated for full year
      factor = 24*365/len(model.T)
      return model.OPEX == period_cost*factor
   model.opex_eq = pyo.Constraint(rule=opex_rule)


   # Power Balance Equations
   def global_power_balance_rule(model, t):
      return sum(model.Pi[n,t] for n in model.N) == 0
   model.global_power_balance_eq = pyo.Constraint(model.T, rule=global_power_balance_rule)

   
   def local_power_balance_rule(model, n, t):
      production = sum(model.Pg[h,n,t] for h in model.H if (h,n) in model.Ug)
      consumption = sum(model.Pd[h,n,t] for h in model.H if (h,n) in model.Uc)
      return production - consumption == model.Pi[n,t]
   model.local_power_balance_eq = pyo.Constraint(model.N, model.T, rule=local_power_balance_rule)


   # Capacity Equations
   # Constraint capacity from given data ( OR NOT if we want to know the final solution)
   def capacity_rule(model, h,n,t):
      return model.Pg[h,n,t] <= model.Cg[h,n]
   model.capacity_eq = pyo.Constraint(model.Ug, model.T, rule=capacity_rule)

   # Load Profiles
   def demand_profile_rule(model, h,n,t):
      year_factor = 24*365/len(model.T)
      try:
         return model.Pd[h,n,t] == (model.yearly_demand[h]/year_factor)*model.demand_profile[h,t]
      except ValueError:
         if OPT_DEBUG:
            print("No demand profile for technology ", h, " Skipping constraint")
         return pyo.Constraint.Skip
   model.demand_profile_eq = pyo.Constraint(model.Uc, model.T, rule=demand_profile_rule) 

   def demand_yearly_rule(model, h,n):
      year_factor = 24*365/len(model.T)
      return sum(model.Pd[h,n,t] for t in model.T) == model.yearly_demand[h]/year_factor
   model.demand_yearly_eq = pyo.Constraint(model.Uc, rule=demand_yearly_rule)
     

   def availability_profile_rule(model, h,n,t):
      return model.Pg[h,n,t] <= model.Cg[h,n]*model.availability_profile[h,t]
   model.availability_profile_eq = pyo.Constraint(model.Ug, model.T, rule=availability_profile_rule)

   return model

def load_input(model, dat_file='test.dat'):
    # Get the absolute path of the .dat file in the current folder
    dat_file_path = Path(__file__).parent / dat_file

    if not dat_file_path.exists():
        raise FileNotFoundError(f"Data file '{dat_file_path}' not found.")

    data = pyo.DataPortal()
    data.load(filename=str(dat_file_path))

    instance = model.create_instance(data)
    return instance

def solve_instance(model_instance):
   solver = pyo.SolverFactory('glpk')
   results = solver.solve(model_instance, tee=True)

   return model_instance

def get_variable_value(instance, var_name):
    """Returns a list with the values of a variable"""
    var = getattr(instance, var_name)
    ret = [pyo.value(x) for x in var.values()]
    return ret

if __name__ == "__main__":
   model = get_abstract_pyomo_model()
   instance = load_input(model)
   instance = solve_instance(instance)   


   print("Total Expenditure: ", pyo.value(instance.TOTEX))
   print("CapEx: ", pyo.value(instance.CAPEX))
   print("OpEx: ", pyo.value(instance.OPEX))
   print("Demand: ", get_variable_value(instance, 'Pd'))
   print("Generation: ", get_variable_value(instance, 'Pg'))
   pass