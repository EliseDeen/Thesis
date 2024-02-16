import numpy as np
import random

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

def path_change(curr_length, path, i, j):
    length = curr_length + np.abs(path[i].x - path[j].x) + np.abs(path[i].y - path[j].y) + np.abs(path[i+1].x - path[j+1].x) + np.abs(path[i+1].y - path[j+1].y)
    return length

#perform local search with start path
def local_search(problem, path_start, c, pot_fct):
    path = path_start
    n = len(path)
    curLength = pot_fct(problem, path, c)
    
    foundImprovement = True
    number_of_iterations = 0
    while foundImprovement:
        print(number_of_iterations, curLength)
        foundImprovement = False
        path2 = path
        length2 = curLength
        for i in range(0, n-1):
            for j in range(i+1, n):
                # print(i,j)
                if j == i:
                    continue
                new_path = do2Opt(path, i, j)
                new_length = pot_fct(problem, new_path, c)
                #verandering ipv volledig opnieuw berekenen: lengthDelta += c*(np.abs(path[i].x - path[j].x) + np.abs(path[i].y - path[j].y) + np.abs(path[i+1].x - path[j+1].x) + np.abs(path[i+1].y - path[j+1].y))
                if new_length < length2:
                    path2 = new_path
                    length2 = new_length
                    foundImprovement = True
        if foundImprovement:
            path = path2
            curLength = length2
        number_of_iterations += 1
    return path, curLength, number_of_iterations+1