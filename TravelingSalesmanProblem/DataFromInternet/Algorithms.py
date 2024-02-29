import numpy as np
import PotentialKPIfcts as pot
import time

#Perform a 2-opt swap
def do2Opt(path, i, j):
    new_path = path[0:i+1]
    for point in np.arange(j, i, -1):
        new_path.append(path[point])
    new_path += path[j+1:]
    return new_path

#perform local search with given start path
def local_search(problem, path_start, weight, pot_fct, closest_nodes):
    t0 = time.time()
    cur_path = path_start
    cur_length, cur_closest = eval(pot_fct)(problem, cur_path, weight, closest_nodes)
    number_of_iterations = 0
    foundImprovement = True
    while foundImprovement:
        foundImprovement = False
        path, length, closest = cur_path, cur_length, cur_closest

        for i in range(0, len(cur_path)-2):
            for j in range(i+2, len(cur_path)):
                if i == 0 and j == len(cur_path)-1:
                    continue
                new_length, new_closest = eval(str(pot_fct)+'_change')(problem, cur_path, cur_length, i, j, weight, cur_closest)
                if new_length < length:
                    path = do2Opt(cur_path, i, j)
                    length, closest = new_length, new_closest
                    foundImprovement = True
        
        if foundImprovement:
            cur_path, cur_length, cur_closest = path, length, closest
            print(number_of_iterations, cur_length, cur_path)
        
        number_of_iterations += 1
    return cur_path, cur_length, number_of_iterations+1, time.time()-t0 