# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:30:48 2020

@author: weldm
"""

# Find a solution to the Eight Queens Problem using Gurobi for any n

from gurobipy import *
import gurobipy as grb
from gurobipy import GRB
import time

def build_eight_queens(n):
    # create model
    Q = Model("Queens")
    N = range(n)
    
    # create variables
    x = Q.addVars(N,N,vtype = GRB.BINARY, name = "x")
    
    # contrain such that no queen attacks another
    Q.addConstrs(grb.quicksum(x[i,j] for j in N) == 1 for i in N)
    Q.addConstrs(grb.quicksum(x[i,j] for i in N) == 1 for j in N)
    Q.addConstr(grb.quicksum(x[i,j] for i in N for j in N) == n)
    Q.addConstrs(grb.quicksum(x[i+k,i] for i in range(n-k)) <= 1 for k in N)
    Q.addConstrs(grb.quicksum(x[i,i+k] for i in range(n-k)) <= 1 for k in N)
    Q.addConstrs(grb.quicksum(x[i+k,n-i-1] for i in range(n-k)) <= 1 for k in range(n))
    Q.addConstrs(grb.quicksum(x[i,n-i-k-1] for i in range(n-k)) <= 1 for k in range(n))
    
    # obtimize model
    Q.setObjective(0)
    Q.optimize()
    
    return Q, x
   
def print_solution(x,N):
    for i in N:
        line = ""
        for j in N:
            if x[i,j].x > 0.1:
                line = line + "Q "
            else:
                line = line + ". "
        print(line)
            
if __name__ == '__main__':
    # Build the model
    n = 8
    start_time = time.time()
    model, variables = build_eight_queens(n)
    model.optimize()
    status = model.status
    # Solve the model
    t = time.time() - start_time
    print("Solution Found in " + str(t) + " seconds.")
    print_solution(variables,range(n))
    