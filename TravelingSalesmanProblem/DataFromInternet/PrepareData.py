import pandas as pd
import tsplib95
import random

def read_opt_values():
    opt = {}
    mydata  = pd.read_table("Thesis/TravelingSalesmanProblem/DataFromInternet/Data/Opt_values.txt", sep=' : ') #sep='\s+'

    lst = mydata.values
    for value in lst:
        opt[value[0]] = value[1]

    return opt

def prepare_data():
    data = []
    opt = read_opt_values()
    i = 0

    for file in opt:
        # print(i)
        problem = tsplib95.load_problem("Thesis/TravelingSalesmanProblem/DataFromInternet/Data/"+str(file)+".tsp")
        # solution = tsplib95.load_solution("TSP/Data/"+str(file)+".opt.tour")
        path = (list(problem.get_nodes()).copy())
        random.shuffle(path)

        data.append([problem, path, opt[file]])
        i += 1

    print('Data succesful loaded')
    return data