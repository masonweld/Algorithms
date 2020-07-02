# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:10:11 2020

@author: weldm
"""

# Find a solution to magic square using Gurobi of size n

from gurobipy import *
import gurobipy as grb
from gurobipy import GRB
import numpy as np
import time

def build_magic_square(inp):
    n = range(inp)
    N = range(inp**2)
    
    # Create model
    m = Model("magic_square")
    
    m.Params.outputFlag = 0
    
    # Create variables
    x = m.addVars(n, n, N, vtype = GRB.BINARY, name = 'x')
    S = m.addVar(vtype = GRB.CONTINUOUS, name = 'S')
    
    # Each integer can only be assigned once
    m.addConstrs(x.sum('*','*',k) == 1 for k in N)
    
    # Each cell can only have one number
    m.addConstrs(x.sum(i,j,'*') == 1 for i in n for j in n)

    # Each row must sum to S
    m.addConstrs(grb.quicksum(k*x[i,j,k] for j in n for k in N) == S for i in n)
    
    # Each column must sum to S
    m.addConstrs(grb.quicksum(k*x[i,j,k] for i in n for k in N) == S for j in n)
    
    # Main diagonal must sum to S
    m.addConstr(grb.quicksum(k*x[i,i,k] for i in n for k in N) == S)
    
    # Other diagonal must sum to S
    m.addConstr(grb.quicksum(k*x[i,inp-1-i,k] for i in n for k in N) == S)
    
    m.update()
    m.write("magicsquare.lp")
    
    return m, x

def print_solution(x, inp):
    grid = np.zeros((inp,inp))
    for i in range(inp):
        for j in range(inp):
            for k in range(inp**2):
                if x[i,j,k].x > 0.1:
                    grid[i][j] = int(k+1)                  
    print(grid)

if __name__ == '__main__':
    # Build the model
    n = 6
    start_time = time.time()
    model, variables = build_magic_square(n)
    # Solve the model.
    model.optimize()
    status = model.status
    if status == 2:
        t = time.time() - start_time
        print("Solution Found in " + str(t) + " seconds.")
        print_solution(variables, n)
    else:
        print("Sudoku grid given has no solution")
                    
    

        
    