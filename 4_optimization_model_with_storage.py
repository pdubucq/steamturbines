# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 19:33:15 2018

Erweitertes Modell einer Kraftwerkseinsatzoptimierung bestehend aus drei Blöcken,
die ein Wärmelast decken sollen. Die Blöcke sind ein Gaskessel, eine Gegedruckturbine,
ein Wärmespeicher. Anhand einer Prognose für den Strompreis soll das optimale 
Einsatzprofil für den Folgetag gefunden werden.

@author: Pascal Dubucq
"""
#%% Imports
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpStatus, value,LpAffineExpression

from tools import update_excel

def read_config(filename='4_optimization_model_with_storage_input.xlsx'):
    full_params=pd.read_excel(filename, sheet_name='params', index_col=0)
    params=full_params['Wert'].transpose()
    ts=pd.read_excel(filename, sheet_name='timeseries', index_col=0)

    return params, ts    
# Funktion baut Optimierungsproblem auf, löst es und speichert die Ergebnisse
def build_and_solve(params, ts):
    
    #%% Einlesen und Verarbeiten der Parameter aus der Excel Datei
    tsindex=ts.index
    ts.reset_index(inplace=True)    
    
    # Scale timeseries
    ts['Heatload']=ts['Heatload']*params['Qlmax']
    ts['EEX']=ts['EEX'] / ts['EEX'].mean() * params['k_sp']
    #%% Definition des Problems als Lineare Minimierungsproblem
    
    prob = LpProblem("Advanced Unit Commitment Problem",LpMinimize)
    
    nts=ts.shape[0]
    
    # Inititalize variables with boundaries and store them in a list (one per timestep)
    
    # These variables are normalized to nominal capacity so range [0,1]
    q1 = [LpVariable(f"q1{t}", 0, 1) for t in range(nts)]
    q2 = [LpVariable(f"q2{t}", 0, 1/params['SKZ2']) for t in range(nts)]
    p2 = [LpVariable(f"p2{t}", 0, 1) for t in range(nts)]
    q3 = [LpVariable(f"q3{t}", -1, 1) for t in range(nts)]
    
    # This is the one binary variable for the turbine operating state
    z2 = [LpVariable(f"z2{t}", 0, 1, LpInteger) for t in range(nts)]
    
    # Storage capacity is stored in hours of full heat load coverage
    e3 = [LpVariable(f"e3{t}", 0, params['e3max']) for t in range(nts)]
    
    
    ''' Definition of target function which will be minimised (cost formulation) '''
    
    objective={}
    
    # Production cost of unit 1 (heat only boiler)
    objective.update({q1[t]:params['Q1max']*params['k_1'] for t in range(nts)})
    
    # Production cost of unit 2 (increase cost)
    objective.update({p2[t]:params['P2max']*(params['k_21']-ts.loc[t, 'EEX']) for t in range(nts)})
    
    # Production cost of unit 2 (constant operating cost)
    objective.update({z2[t]:params['P2max']*params['k_20'] for t in range(nts)})
    
    # Add objectives to problem
    prob += LpAffineExpression(objective), "Objective function, Linear Production Cost"
    
    # These are the conditions per timestep
    for t in range(nts):
        
        # Load constraint
        prob += q1[t]*params['Q1max'] \
        + p2[t]*params['P2max']/params['SKZ2']  \
        + q3[t]*params['Qlmax'] == ts.loc[t, 'Heatload'], f"Load constraint t={t}"
        
        # Heat storage level
        prob += e3[t] == params['estart'] + sum(q3[i] for i in range(0,t+1)), f"Heat storage contraint t={t}"
        
        # Steam turbine characteristic
        prob += p2[t] == q2[t] * params['SKZ2']
        
        # Minimum Power
        prob += p2[t]*params['P2max'] >= z2[t]*params['P2min']
        
        # Maximum Power
        prob += p2[t] <= z2[t]
        
    # Storage level at last step
    prob += e3[-1] == params['estart']    
        
    # Löse das Problem
    prob.solve()
    
    print("Status:", LpStatus[prob.status])
    
    # Each of the variables is printed with it's resolved optimum value
    raw_result={}
    for v in prob.variables():
        raw_result[v.name]=v.varValue
        
    # The optimised objective function value is printed to the screen
    print(f"Total cost of production is {value(prob.objective)} EUR.")
    
    #%% Construct result frame
    
    # Gets the variable values back as timeseries in correct order of timesteps given the variable name (key)
    get_series = lambda key: pd.Series({int(k.replace(key,'')):raw_result[k] for k in raw_result.keys() if k.startswith(key)}, name=key)
    
    # selection of variables to be exported to excel file
    result_vars=['q1', 'q2', 'q3', 'p2', 'e3', 'z2']
    
    # save as dataframe
    df = pd.concat([get_series(k) for k in result_vars], axis=1, keys=result_vars)
    
    df.index = tsindex
    
#%%    
    return (LpStatus[prob.status],value(prob.objective), df)
    
def postprocess(filename, result, params, ts):
    update_excel(result[2], filename, 'schedule')
    result[2][['q1','q2','q3','e3']].plot()
    ts.plot(x='Time', y='EEX')
    result[2]['p2'].plot()

def build_and_run(filename):
    params, ts = read_config(filename)
    result = build_and_solve(params, ts)
    postprocess(filename, result, params, ts)
    plt.show()

#%% Eintrittspunkt, der ausgeführt wird, wenn man das Skript als Programm startet
if __name__ == '__main__':
    if len(sys.argv)>1:
        build_and_run(sys.argv[1])
    else:
         build_and_run('4_optimization_model_with_storage_input.xlsx')   
         
#%% Vergleiche Speichergrößen         
def simulate_storage_sizes(filename, n=10):
    base_config, ts = read_config(filename)
    rel_storage_sizes=np.linspace(0, base_config['e3max'], n)
    results=[]
    for i in range(0,n):
        this_config = base_config.copy()
        this_config['e3max'] = rel_storage_sizes[i]
        this_config['estart'] = this_config['e3max']*0.5        
        results.append(build_and_solve(this_config, ts.copy()))
        
    return pd.concat([r[2][['q1','q2','q3','p2']].sum() for r in results],
                      axis=1,
                      keys=[f"Storage {x:.0f}h" for x in rel_storage_sizes])        
#%%
if False:
#%%
    filename='4_optimization_model_with_storage_input.xlsx'
    results=simulate_storage_sizes(filename)    
    
#%%
    filename='4_optimization_model_with_storage_input.xlsx'
    
