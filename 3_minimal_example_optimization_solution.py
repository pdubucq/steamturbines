# -*- coding: utf-8 -*-
"""

Minimalbeispiel einer Kraftwerkseinsatzoptimierung bestehend aus drei Blöcken,
die eine Last decken sollen. Es wird nur ein Zeitschritt betrachtet. Die Blöcke
sind durch eine Mindestlast und eine Maximallast charakterisiert und haben 
lineare Erzeugungskosten.

Dies hier ist die Musterlösung.

Einzelne Zellen können mit Strg + Enter ausgeführt werden.

@author: Pascal Dubucq
"""

#%%

from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpStatus, value

initial_state_to_teach=True

prob = LpProblem("The Sandbox Problem",LpMinimize)
P1=LpVariable("P1", 0, 600)
P2=LpVariable("P2", 0, 400)
P3=LpVariable("P3", 0, 500)

z1=LpVariable("z1", 0, 1, LpInteger)
z2=LpVariable("z2", 0, 1, LpInteger)
z3=LpVariable("z3", 0, 1, LpInteger)

prob += 510*z1 + 310*z2 + 78*z3 + 7.9*P1 + 7.85*P2 + 9.56*P3, "Linear Production Cost"

if initial_state_to_teach:
    
    prob += P1 >= z1*250, "Min Power Block 1"
    prob += P2 >= z2*200, "Min Power Block 2"
    prob += P3 >= z3*150, "Min Power Block 3"
    
    prob += P1 <= z1*600, "Max Power Block 1"
    prob += P2 <= z2*400, "Max Power Block 2"
    prob += P3 <= z3*500, "Max Power Block 3"

prob += P1 + P2 + P3 == 650, "Load constraint"

prob.writeLP("sandbox.lp")

prob.solve()

print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
# The optimised objective function value is printed to the screen
print("Total Cost = ", value(prob.objective))
