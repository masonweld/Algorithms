# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 20:24:18 2020

@author: weldm
"""

# Finds solution to the change problem for any cent given with Gurobi

from gurobipy import *
import gurobipy as grb
from gurobipy import GRB
import time

start_time = time.time()

# create model
m = Model("Change")

# create coin vec and list
coins = [1,5,10,25]
N = range(len(coins))
c = 99
M = range(c)

# variables x being number of each coin in collection
# s being the 'coin slack' for each constraint
x = m.addVars(N, vtype = GRB.INTEGER, name = "x")
sp = m.addVars(M, vtype = GRB.INTEGER, name = "s_p")
sn = m.addVars(M, vtype = GRB.INTEGER, name = "s_n")
sd = m.addVars(M, vtype = GRB.INTEGER, name = "s_d")
sq = m.addVars(M, vtype = GRB.INTEGER, name = "s_q")

# for each 1-99 need to be able to make exact change
# slack cannont be larger than amount of coins we have
for i in M:
    m.addConstr( (x[0]-sp[i])+5*(x[1]-sn[i])+10*(x[2]-sd[i])+25*(x[3]-sq[i]) == i )
    m.addConstr( sp[i] <= x[0] )
    m.addConstr( sn[i] <= x[1] )
    m.addConstr( sd[i] <= x[2] )
    m.addConstr( sq[i] <= x[3] )
  
# minimize the amount of coins we have
m.setObjective(grb.quicksum(x[i] for i in N))

m.Params.outputFlag=0
m.update()
m.optimize()

t = time.time() - start_time
print("Solution found in " + str(t) + " seconds.")
coin_list = ["pennies","nickles","dimes","quarters"]
print("Minimum number of coins needed for making change for any value up to %d cents = %d" %(c, m.objVal))
for i in N:
    print("Number of %s = %d" % (coin_list[i], x[i].x))