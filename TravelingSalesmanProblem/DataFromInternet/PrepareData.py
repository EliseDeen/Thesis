import pandas as pd
import tsplib95
import random
import numpy as np

def read_opt_values():
    opt = {}
    mydata  = pd.read_table("Thesis/TravelingSalesmanProblem/DataFromInternet/Data/Opt_values.txt", sep=' : ') #sep='\s+'

    lst = mydata.values
    for value in lst:
        opt[value[0]] = value[1]

    return opt

def prepare_data(files=[]):
    data = []
    opt = read_opt_values()
    i = 0

    if files == []:
        files = opt

    for file in files:
        problem = tsplib95.load_problem("Thesis/TravelingSalesmanProblem/DataFromInternet/Data/"+str(file)+".tsp")
        # solution = tsplib95.load_solution("TSP/Data/"+str(file)+".opt.tour")

        # path = (list(problem.get_nodes()).copy())
        # random.shuffle(path)
        path = [5, 13, 8, 3, 6, 7, 15, 14, 9, 11, 10, 16, 4, 1, 2, 12]
        # print(path)
        
        closest_nodes = {} #len(path)*[[0, np.infty]]
        for i in path:
            closest_nodes[i] = [0, np.infty, 0, np.infty]
            for j in path:
                weight = problem.get_weight(i, j)
                if weight < closest_nodes[i][1]:
                    closest_nodes[i][0] = j
                    closest_nodes[i][1] = weight
                elif weight < closest_nodes[i][3]:
                    closest_nodes[i][2] = j
                    closest_nodes[i][3] = weight
        
        data.append([problem, path, opt[file], closest_nodes])
        i += 1

    print('Data succesful loaded')
    return data