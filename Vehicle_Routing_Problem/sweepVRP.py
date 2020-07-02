# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:34:31 2020

@author: weldm
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import time

'''
script takes instances berlin52.tsp, bier127.tsp, and ch150.tsp and solves
the vechile routing problem with first node as home city (depot) using the
sweep hueristic.
Assumes K = b = ciel(sqrt(Num Nodes))
'''

# function that takes cartesian coords and returns polar coords
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

# function that takes cartesian coords and returns distance btwn two
def distance(x,y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

# sweep huerisitc for VRP
def sweepVRP(instance):
    # start time and read in .tsp file of instance provided
    start_time = time.time()
    infile = open(instance, 'r')
    infile.readline()
    if instance == "bier127.tsp":
        N = int(infile.readline().strip().split()[2])
        for i in range(4):
            infile.readline()
    elif instance == "berlin52.tsp" or instance == "ch150.tsp":
        infile.readline()
        N = int(infile.readline().strip().split()[1])
        for i in range(3):
            infile.readline()
    
    # create lists to store nodes, locations, and if visited
    nodelist = [infile.readline().strip().split() for i in range(N)]
    nodelist = [[int(nodelist[i][0])-1,float(nodelist[i][1]),float(nodelist[i][2])] for i in range(len(nodelist))]
    location = [(float(nodelist[i][1]),float(nodelist[i][2])) for i in range(N)]
    visited = [False for i in range(N)]
    visited[0] = True
    
    # displace coordinates with v0 as origin
    home_cart = location[0]
    new_location = [(location[i][0]-home_cart[0], location[i][1]-home_cart[1]) for i in range(len(location))]
    
    # convert coords to polar
    polar = []
    for i in range(len(new_location)):
        polar.append(cart2pol(new_location[i][0],new_location[i][1]))
    
    # def k' and b as defined in assignment
    k_prime = math.ceil(math.sqrt(N-1))
    b = k_prime
    k = 1
    
    # start loop by visiting visiting next node based off smallest clockwise angle to current node
    trucks = []
    d = 0
    # loop for each truck and for when we have unvisited nodes
    while all(visited) == False and k < k_prime:
        # find nodes and polar coords that are unvisited to consider
        indices = [i for i, x in enumerate(visited) if x == False]
        unvisit_polar = [polar[i] for i in indices]
        combined = [(indices[i],unvisit_polar[i][1]) for i in range(len(indices))]
        angles = [polar[i][1] for i in indices]
        closest = min(angles, key=lambda x:abs(x-(math.pi*2)))
        s = angles.index(closest)
        cur = combined[s][0]
        cur_angle = combined[s][1]
        count = 1
        visited[cur] = True
        route = [cur]
        # calc distance from home city to first node
        d += distance(location[0],location[cur])
        
        # loop for single truck while under b limit and have unvisited
        while count < b and all(visited) == False:
            # find node closest to cur by smallest angle change clockwise
            # move to this node and calc distance
            old_cur = cur
            indices = [i for i, x in enumerate(visited) if x == False]
            unvisit_polar = [polar[i] for i in indices]
            combined = [(indices[i],unvisit_polar[i][1]) for i in range(len(indices))]
            angles = [polar[i][1] for i in indices]
            displaced_angles = [cur_angle - angles[i] for i in range(len(angles))]
            for i in range(len(displaced_angles)):
                if displaced_angles[i] < 0:
                    displaced_angles[i] = 10
            closest = min(angles, key=lambda x:abs(x-(cur_angle)))
            s = angles.index(closest)
            cur = combined[s][0]
            cur_angle = combined[s][1]
            count += 1
            visited[cur] = True
            route.append(cur)
            d += distance(location[old_cur],location[cur])

        # add distance from end node for truck back to home city
        d += distance(location[cur],location[0])
        k += 1
        trucks.append(route)

    # plot
    for j in range(len(trucks)):
        x = [new_location[i][0] for i in trucks[j]]
        y = [new_location[i][1] for i in trucks[j]]
        plt.scatter(x, y)
    plt.scatter(0,0,marker = '^',color = "black", label = "home")
    plt.title(instance + " sweep hueristic")
    plt.show()
    #plt.savefig('sol.png')
    t = time.time() - start_time
    return(trucks,t,d)
  
# results   
b52, t52, d52 = sweepVRP("berlin52.tsp")
print("-- berlin52.tsp sweep solution --")
print("berlin52 solution found in %f seconds with distance %f" % (t52,d52))
for i in range(len(b52)):
    print("Truck %g visits customers:" %(i) )
    print(b52[i])
        
b127, t127, d127 = sweepVRP("bier127.tsp")
print("-- bier127.tsp sweep solution --")
print("bier127 solution found in %f seconds with distance %f" % (t127,d127))
for i in range(len(b127)):
    print("Truck %g visits customers:" %(i) )
    print(b127[i])
    
ch150, t150, d150 = sweepVRP("ch150.tsp")
print("-- ch150.tsp sweep solution --")
print("ch150 solution found in %f seconds with distance %f" % (t150,d150))
for i in range(len(ch150)):
    print("Truck %g visits customers:" %(i) )
    print(ch150[i])


