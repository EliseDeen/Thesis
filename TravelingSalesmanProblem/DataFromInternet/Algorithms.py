import numpy as np
import random
import PotentialKPIfcts as pot
import time

#Perform a 2-opt swap
def do2Opt(path, i, j):
    new_path = path[0:i+1]
    # for point in range(0, i+1):
    #     new_path.append(path[point])
    for point in np.arange(j, i, -1):
        new_path.append(path[point])
    # for point in range(j+1, len(path)):
    #     new_path.append(path[point])
    new_path += path[j+1:]
    return new_path

#perform local search with start path
def local_search(problem, path_start, c, pot_fct, closest_nodes):
    path = path_start
    n = len(path)
    curLength, closest = eval(pot_fct)(problem, path, c, closest_nodes)
    times = []
    foundImprovement = True
    number_of_iterations = 0
    while foundImprovement:
        a, b = pot.no_potential(problem, path, c, closest)
        print(number_of_iterations, curLength, a)
        time_start = time.time()
        foundImprovement = False
        path2 = path
        length2 = curLength
        closest2 = closest
        for i in range(0, n-1):
            for j in range(i+1, n):
                # print(i,j)
                if j == i:
                    continue
                new_path = do2Opt(path, i, j)
                new_length, new_closest = eval(pot_fct)(problem, new_path, c, closest_nodes)
                # new_length, new_closest = eval(str(pot_fct)+'_change')(problem, path, curLength, i, j, c, closest)
                if new_length < length2:
                    # print(i,j, new_length)
                    path2 = new_path
                    # path2 = do2Opt(path, i, j)
                    length2 = new_length
                    closest2 = new_closest
                    foundImprovement = True
        if foundImprovement:
            path = path2
            curLength = length2
            closest = closest2
        number_of_iterations += 1
        time_end = time.time()
        times.append(time_end-time_start)
    return path, curLength, number_of_iterations+1, sum(times)/len(times)