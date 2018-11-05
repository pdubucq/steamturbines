# -*- coding: utf-8 -*-
"""
Minimal example of a unit commitment problem. The energy system modeled consists
of three units used to cover an electric load. Only one timestep (i.e. load) is
considered. The units are described by a minimal power, a maximum power and 
linear production cost.

Task:
    
Complete the code by taking the following steps:
    
    1. Analyze and try to understand what happens in the code now
       
    2. Define binary variables (integer with boundaries [0,1] to model the
       operating state.
    
    3. Add the constant part of the fuel cost to the objective function 

    4. Define the restriction of minimal power (P > Pmin * z)
    
    5. Compare with the solution file (3_minimal_example_optimization_solution.py)
    
Created on Sun Jul 22 19:33:15 2018

@author: Pascal Dubucq

"""
#%% Import of the library PuLP

from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpStatus, value

#%% Problem definition

prob = LpProblem("Unit Commitment Sandbox Problem",LpMinimize)

''' Definition der Variablen:
 Je Block eine kontinuierliche Variable für die Leistung. Die Unter- und 
 Obergrenze können direkt angegeben werden.
'''

P1=LpVariable("P1", 0, 600)
P2=LpVariable("P2", 0, 400)
P3=LpVariable("P3", 0, 500)

''' TODO: Zur Abbildung der Mindestleistungsbedingung müssen zusätzliche Binär-
 Variablen eingeführt werden
 
 Definition einer Integer Variablen in Pulp:
     
     z1 = LpVariable("z1", 0, 1, LpInteger)
 
 '''

# Definition der Zielfunktion, die minimiert werden soll
prob += 7.9*P1 + 7.85*P2 + 9.56*P3, "Linear Production Cost"

# Nebenbedingung der Lastdeckung
prob += P1 + P2 + P3 == 500, "Load constraint"

# Löse das Problem
prob.solve()

print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
# The optimised objective function value is printed to the screen
print(f"Total cost of production is {value(prob.objective)} EUR.")