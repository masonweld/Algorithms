# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:39:14 2020

@author: weldm
"""
# Sudoku Solver with CPLEX

from docplex.mp.model import Model
from docplex.util.environment import get_environment
import numpy as np
from numpy import genfromtxt
import pandas as pd


# ----------------------------------------------------------------------------
# Initialize Sudoku Grid
# ----------------------------------------------------------------------------

# read csv sudoku grid
GRID = genfromtxt("sudoku_grid1.csv", delimiter=',')

# ----------------------------------------------------------------------------
# Build Optimization Model
# ----------------------------------------------------------------------------
def build_sudoku_model(grid, **kwargs):
    # create model
    m = Model(name='Sudoku', **kwargs)
    # create variables
    # x(i,j,k) = 1 if number k is in row i col j
    v  = {(i,j,k): m.binary_var(name="x_{0}_{1}_{2}".format(i,j,k)) for i in range(9) for j in range(9) for k in range(9)}
    
    # constrain given numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                c = m.add_constraint(v[i,j,grid[i][j]-1] == 1)
    
    # constrain each cell to have one number 
    for i in range(9):
        for j in range(9):
            m.add_constraint(m.sum(v[i,j,k] for k in range(9)) == 1)
    
    # constrain each column to have one of each number
    for j in range(9):
        for k in range(9):
            m.add_constraint(m.sum(v[i,j,k] for i in range(9)) == 1)
    
    # constrain each row to have one of each number
    for i in range(9):
        for k in range(9):
            m.add_constraint(m.sum(v[i,j,k] for j in range(9)) == 1)
     
    # constrain each 3x3 box to have one of each number
    for a in range(3):
        for b in range(3):
            for k in range(9):
                box_row = [3*a, 3*a+1, 3*a+2]
                box_col = [3*b, 3*b+1, 3*b+2]
                m.add_constraint(m.sum(v[i,j,k] for i in box_row
                                       for j in box_col) == 1)
    
    m.minimize(1)
    return m, v

def print_solution(variables):
    # create pandas df to store solution and print solution
    opt_df = pd.DataFrame.from_dict(variables, orient="index", columns = ["variable_object"])
    opt_df.index = pd.MultiIndex.from_tuples(opt_df.index, names=["i", "j", "k"])
    opt_df.reset_index(inplace=True)
    opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
    solution = np.zeros((9,9))
    for i, row in opt_df.iterrows():
        if row["solution_value"] == 1:
            solution[int(row["i"])][int(row["j"])] = int(row["k"]) + 1
    print(solution)
    
# ----------------------------------------------------------------------------
# Solve the Model
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    # Build the model
    model, variables = build_sudoku_model(GRID)
    model.print_information()
    # Solve the model.
    if model.solve():
        print("Solution Found")
        print_solution(variables)
    else:
        print("Sudoku grid given has no solution")