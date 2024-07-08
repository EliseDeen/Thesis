import numpy as np
import PotentialKPIfcts as pot
import time

def do2Opt(path, i, j):
    new_path = path[0:i+1]
    for point in np.arange(j, i, -1):
        new_path.append(path[point])
    new_path += path[j+1:]
    return new_path

def local_search(problem, path_start, weight, pot_fct, closest_nodes):
    t0 = time.time()
    cur_path = path_start
    cur_length, cur_closest = eval(pot_fct)(problem, cur_path, weight, closest_nodes)
    best_path = path_start.copy()
    best_length, best_closest = pot.no_potential(problem, best_path, weight, closest_nodes)
    number_of_iterations = 0
    foundImprovement = 0
    while foundImprovement < len(path_start):
        path, length, closest = cur_path, cur_length, cur_closest
        noImprovement = True

        for i in range(0, len(cur_path)-2):
            for j in range(i+2, len(cur_path)):
                if i == 0 and j == len(cur_path)-1:
                    continue
                new_length, new_closest = eval(str(pot_fct)+'_change')(problem, cur_path, cur_length, i, j, weight, cur_closest)
                path_test = do2Opt(cur_path, i, j)

                if new_length <= length:
                    path = path_test
                    length, closest = new_length, new_closest
                    noImprovement = False
                    
                f_normal, clos = pot.no_potential(problem, path_test, 0, cur_closest)
                if f_normal <= best_length:
                    best_path = path_test
                    best_length, best_closest = f_normal, clos
        if noImprovement:
            break
        if length < cur_length:
            cur_path, cur_length, cur_closest = path, length, closest
            foundImprovement = 0
            # if number_of_iterations in [20,50,100,150,200,250,300,350,400,450,500]:
            print(number_of_iterations, cur_length, cur_path, closest, flush=True)
        elif length == cur_length:
            cur_path, cur_length, cur_closest = path, length, closest
            foundImprovement += 1
            # if number_of_iterations in [20,50,100,150,200,250,300,350,400,450,500]:
            print(number_of_iterations, cur_length, cur_path, closest, flush=True)
        else:
            foundImprovement += 1
        
        number_of_iterations += 1
    return cur_path, cur_length, number_of_iterations+1, time.time()-t0, best_path, best_length 