import Run as run
import numpy as np
import json
import tsplib95

#Comment out what you dont what to run
""" Load information """ 
f = open("Data/Data_TSP.txt", "r", encoding="utf-8")
data = json.load(f)
f.close()
# The instances you want to use in the local search algorithms
# Choises are: a280, ali535, att48, att532, bayg29, bays29, berlin52, bier127, brazil58, brd14051, brg180, burma14,
# ch130, ch150, d198, d493, d657, d1291, d1655, d2103, d15112, d18512, dantzig42, dsj1000, eil51, eil76, eil101, fl417,
# fl1400, fl1577, fl3795, fnl4461, fri26, gil262, gr17, gr21, gr24, gr48, gr96, gr120, gr137, gr202, gr229, gr431, gr666,
# hk48, kroA100, kroB100, kroC100, kroD100, kroE100, kroA150, kroB150, kroA200, kroB200, lin105, lin318, linhp318, nrw1379,
# p654, pa561, pcb442, pcb1173, pcb3038, pla7397, pla33810, pla85900, pr76, pr107, pr124, pr136, pr144, pr152, pr226, 
# pr264, pr299, pr439, pr1002, pr2392, rat99, rat195, rat575, rat783, rd100, rd400, rl1304, rl1323, rl1889, rl5915, rl5934,
# rl11849, si175, si535, si1032, st70, swiss42, ts225, tsp225, u159, u574, u724, u1060, u1432, u1817, u2152, u2319, ulysses16,
# ulysses22, usa13509, vm1084, vm1748
instances = ['att48', 'bayg29', 'bays29', 'burma14', 'dantzig42', 'fri26', 'gr17', 'gr21', 'gr24', 'gr48', 'hk48', 'swiss42', 'ulysses16', 'ulysses22', 'berlin52', 'eil51', 'brazil58', 'eil76', 'st70', 'pr76', 'gr96', 'kroE100', 'kroD100', 'kroC100', 'kroB100', 'kroA100', 'eil101', 'pr107', 'rat99', 'rd100', 'lin105', 'pr124', 'bier127']

""" Random initial solution, instance independent weights"""
methods = ['ClosestEdge', 'ConnectingNodesvsClosestNodes', 'ConnectingNodesvsClosestEdge', 'random_fct']
weights = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101]

for m in range(len(methods)):
    print(methods[m], m, flush=True)
    close = [] 
    if methods[m] == 'random_fct':
        for file in instances:
            random_weight = np.random.random_integers(-5, 5, (len(data[file][0]), 2))
            close.append(random_weight) #close = weights for in the random function
    else: 
        for i in range(len(instances)):
            close.append(data[instances[i]][2]) #close = the closest nodes
    obj_value_w, num_iterations_w, time_w, obj_value_ww, num_iterations_ww, time_ww, obj_value_www, num_iterations_www, time_www = run.run_algorithms('small_', data, instances, methods[m], weights, close)
    
""" Random initial solution, instance dependent weights"""
method = 'ClosestEdge'
maxcost, mincost = {}, {}
weights = len(instances)*[np.arange(0, 2.2, 0.2)]
close = []
for inst in range(len(instances)):
    problem = tsplib95.load_problem("Data/"+str(instances[inst])+".tsp")
    path = data[instances[inst]][0]
    maxcost[inst], mincost[inst] = 0, np.infty
    for i in path:
        for j in path:
            if i == j:
                continue
            weight = problem.get_weight(i, j)
            if weight > maxcost[inst]:
                maxcost[inst] = weight
            if weight < mincost[inst]:
                mincost[inst] = weight
    weights[inst] = weights[inst] * 2*(maxcost[inst]-mincost[inst])
    close.append(data[instances[i]][2]) #close = the closest nodes
obj_value_w, num_iterations_w, time_w, obj_value_ww, num_iterations_ww, time_ww, obj_value_www, num_iterations_www, time_www = run.run_algorithms('small_', data, instances, method, weights, close)


""" Greedy initial solution, instance independent weights """
methods = ['ClosestEdge', 'random_fct']
weights = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101]

for m in range(len(methods)):
    print(methods[m], m, flush=True)
    close = [] 
    if methods[m] == 'random_fct':
        for file in instances:
            random_weight = np.random.random_integers(-5, 5, (len(data[file][0]), 2))
            close.append(random_weight) #close = weights for in the random function
    else: 
        for i in range(len(instances)):
            close.append(data[instances[i]][2]) #close = the closest nodes
    obj_value_w, num_iterations_w, time_w, obj_value_ww, num_iterations_ww, time_ww, obj_value_www, num_iterations_www, time_www = run.run_algorithms('small_', data, instances, methods[m], weights, close)
