# -*- coding: utf-8 -*-
"""

This script gives a short introduction on python for Mechanical Engineers.

Inspiration came from: https://github.com/rpmuller/PythonCrashCourse/

It is recommended to open this in Spyder and execute the individual cells
(code blocks seperated by #%%) to see what happens.

@author: Pascal Dubucq
"""

#%% Add two numbers

3+4

#%% Division (note that need to use float is automatically detected!)

9/2

#%% Defining variables

width = 20
length = 30

area = width * length

area

#%% Help and documentation to objects and functions

help(area)

''' Within the Ipython console you can furthermore do: 
        
    area? 
    
    and

    area?? 

    on both classes and instances!'''
    
#%% Simple strings

s = 'Hello World'

s

print(s)

#%% Format Strings (F-Strings)

s=f'The area is {area}'

print(s)

print(f"A week consists of {7*24} hours")
#%% Lists

weekdays = ['Mon', 'Tue', 'Wed','Thu', 'Fri', 'Sat', 'Sun']

weekdays[2]

ideas=[]

ideas

#%% Looping over elements of a list

for day in weekdays:
    print(day)


#%% Looping using numeric indices
    
for i in range(0,3):
    print(weekdays[i])

#%% Boolean algebra
    
if weekdays:
    print('This list is not empty')
    
if ideas:
    print(ideas)    
    
for day in weekdays:
    if "M" in day:
        print(day)
    if "Sun" == day:
        print(day)        
        
#%% Tuple

physical_value = (230, 'MW')        

numerical_value = physical_value[0]
unit = physical_value[1]

print(f"The installed capacity is {numerical_value} {unit}")

#%% Dictionary

parameter={
        'P_nom': (230, 'MW'),
        'p_min_pu': 0.3
        }

P_min = parameter['P_nom'][0] * parameter['p_min_pu']

print(f"Minimal Power: {P_min} {parameter['P_nom'][1]}")

#%% Definition of a simple function
        
def calc_stuff(a,b):
    return (a+b)/a**2

x = calc_stuff(3,2)

print(x)

print(f"The result of calc_stuff with two decimal places is: {x:.2f}")

#%% Definition of a function with lambda keyword

calc_stuff_2 = lambda a,b: (a+b)/a**2

print(calc_stuff_2(3,2))

#%% Defining a class

class PowerPlant:
    def __init__(self, P_nom, unit):
        self.P_nom = (P_nom, unit)
        
    def P_max(self):
        return self.P_nom
    
tiefstack = PowerPlant(270, 'MW')

print(tiefstack.P_max())

#%% Importing libraries like pandas (great library for tables and timeseries)
import pandas as pd

#%% Defining and plotting a timeseries with pandas
series=pd.Series([0,2,4,1,4])

series.plot()

#%% Creating a dataframe from timeseries

series2 = series * 2.3

series3 = series.multiply([1.1, .9, 1.1, .9, 1.2])

dataframe=pd.concat([series, series2, series3], axis=1, keys=['series', 'series2', 'series3'])

#%% A dataframe behaves like a dictionary

dataframe['series3']

dataframe['series4']=1

print(dataframe)

#%% Eine Menge nütliche Funktionen sind integriert, zum Beispiel Statistiken

dataframe.describe()