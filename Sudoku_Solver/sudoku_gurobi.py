# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 18:34:50 2019

@author: weldm
"""

# Sudoku solver with Gurobi

from gurobipy import *
import numpy as np
from numpy import genfromtxt
import pandas as pd
import time

# ----------------------------------------------------------------------------
# Initialize Sudoku Grid
# ----------------------------------------------------------------------------

# read csv sudoku grid
GRID = genfromtxt("sudoku_grid1.csv", delimiter=',')

# ----------------------------------------------------------------------------
# Build Optimization Model
# ----------------------------------------------------------------------------

def build_sudoku_model(grid):
    # Create model
    m = Model("Solve_Sudoku")
    
    # Add Binary Variables
    # x(i,j,k) = 1 if cell in row i column j is number k
    rows = range(9)
    columns = range(9)
    numbers = range(9)
    
    # Create variables
    v = m.addVars(rows, columns, numbers, vtype = GRB.BINARY, name = 'v')
    
    # Assign values for filled in cells
    for i in rows:
        for j in columns:
            if grid[i][j] != 0:
                v[i,j,grid[i][j]-1].lb = 1
    
    # Each cell contains one number
    each_cell = m.addConstrs(v.sum(i,j,'*') == 1 for i in rows for j in columns)
    
    # Each row has one of each number
    each_row = m.addConstrs(quicksum([v[i,j,k] for j in columns]) 
    == 1 for i in rows for k in numbers)
    
    # Each column has one of each number
    each_col = m.addConstrs(quicksum([v[i,j,k] for i in rows]) 
    == 1 for j in columns for k in numbers)
    
    # Each box has one of each number
    for a in range(3):
        for b in range(3):
            box_row = [3*a, 3*a+1, 3*a+2]
            box_col = [3*b, 3*b+1, 3*b+2]
            each_box = m.addConstrs(quicksum([v[i,j,k] for i in box_row
                                              for j in box_col]) == 1 for k in numbers)
    
    # Write model
    m.write("Solve_Sudoku.lp")
    
    # Update model
    m.update()
    m.setParam("OutputFlag", 0)
    return m, v

def print_solution(model, variables):
    # Obtain indices of where x_ijk = 1
    index = []
    solution = np.zeros((9,9))
    for z in model.getVars():
        if z.x == 1:
            index.append(z.varName)      
    for c in range(len(index)):
        new_list = list(str(index[c]))
        i = int(new_list[2])
        j = int(new_list[4])
        k = int(new_list[6])
        solution[i][j] = k + 1
    print(solution)
       

if __name__ == '__main__':
    # Build the model
    start_time = time.time()
    model, variables = build_sudoku_model(GRID)
    model.optimize()
    status = GRB.OPTIMAL
    # Solve the model.
    if status == 2:
        t = time.time() - start_time
        print("Solution Found in " + str(t) + " seconds.")
        print_solution(model, variables)
    else:
        print("Sudoku grid given has no solution")
    
    
    
            

