# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 19:05:27 2020

@author: weldm
"""

from gurobipy import *
import gurobipy as grb
from gurobipy import GRB
import numpy as np

def cuttingstock(patterns, demands, raw, finals):
    # Solves cutting stock problem (prints solution)
    # Inputs:
    #   patterns: list of lists containing initial patterns
    #   demands: list of demands
    #   raw: length of raw
    #   finals: list of lengths of finals
    
    # initialize pi_val to be more than 1
    pi_val = 10 
    
    # initialize iteration count
    iterations = 0
    
    # while pricing problem has obj value > 1
    while pi_val > 1:
        # create restricted master problem
        m_RMP = Model("Restricted Master Problem")
        m_RMP.Params.outputFlag = 0
        num_cols = len(patterns[0])
        cols = range(num_cols)
        num_rows = len(patterns)
        rows = range(num_rows)
        
        # create variables x
        x = m_RMP.addVars(cols, name = "x", lb = 0)
        
        # create constraints in Ax >= b form
        for i in rows:
            expr = grb.LinExpr()
            for j in cols:
                expr += patterns[i][j]*x[j]
            m_RMP.addConstr(expr, GRB.GREATER_EQUAL, demands[i])
            
        # update and write for sanity check
        m_RMP.update()
        m_RMP.write("cuttingstock.lp")
        
        # create objective function
        m_RMP.setObjective(grb.quicksum(x[j] for j in cols))
        
        # solve
        m_RMP.optimize()
        
        # gurobi finds dual values
        y = m_RMP.getAttr("Pi", m_RMP.getConstrs())
        
        # create pricing problem
        m_knap = Model("Knapsack Pricing Problem")
        
        m = len(y)
        M = range(m)
        
        # create pricing variables
        pi = m_knap.addVars(M, vtype = GRB.INTEGER, name = "pi", lb = 0)
        
        # create objective function
        m_knap.setObjective(grb.quicksum(y[i]*pi[i] for i in M), GRB.MAXIMIZE)
        
        # add knapsack constraint
        m_knap.addConstr(grb.quicksum(finals[i]*pi[i] for i in M) <= raw)
        
        # update and write for sanity check
        m_knap.update()
        m_knap.write("knap.lp")
        
        m_knap.Params.outputFlag = 0
        
        # solve
        m_knap.optimize()
        
        # obtain objective value
        pi_obj = m_knap.getObjective()
        pi_val = pi_obj.getValue()
        
        # iteration count
        iterations += 1
        
        # add new best pattern to pattern array
        for i in rows:
            patterns[i].append(pi[i].x)
    
    # now optimal, print solution to cutting stock
    optimal = m_RMP.getObjective()
    optimal_value = optimal.getValue()
    pattern_array = np.array(patterns)
    for i in cols:
        if x[i].x > 0:
            print("Cut %f raws with pattern:" % (x[i].x))
            print(pattern_array[:,i])
    print("For a total of %f raws used and %d iterations" % (optimal_value, iterations))
    
initial_patterns = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
demands = [97,610,395,211]
raw = 104
finals = [45, 36, 31, 14]
cuttingstock(initial_patterns, demands, raw, finals)