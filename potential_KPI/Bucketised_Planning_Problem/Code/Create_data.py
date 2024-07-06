import random
import json
import numpy as np
import math
import ILP

def startposition(tasks, B, T):
    S0 = []
    for i in range(len(tasks)):
        S0.append(random.randint(0, int((B-1)*T)))
    return S0

def create_instances(T, num_tasks, p_max, d_max, name, B=None):
    w = [1, 1000]
    f = open("Bucketised_Planning_Problem/Data/"+name+".txt", 'w')
    for i in range(len(num_tasks)):
        tasks = []

        # Set time limit for ILP solver
        if num_tasks[i] <= 20:
            limit = 180
        elif num_tasks[i] <= 30:
            limit = 300
        elif num_tasks[i] <= 40:
            limit = 800
        elif num_tasks[i] <= 50:
            limit = 1800
        else:
            limit = 3000
            
        # Determine information for instance    
        B_temp = 0
        for j in range(num_tasks[i]):
            p = random.randint(1, p_max) #Process time
            d = random.randint(0, d_max) #Due date
            num_tasks.append([d, p]) 
            B_temp += p

        if B == None:
            B = math.ceil(B_temp/T)
            
        instance = ILP.problem(T, B, tasks)
        model = ILP.create_ILP(instance, w, limit)

        S0 = startposition(tasks, B, T)

        f.write(str(tasks)+'\n')
        f.write(str(B)+'\n')
        f.write(str(S0)+'\n')
        f.write(str(model.objVal)+'\n')

    f.close()
    return 'succeed'

def interpret_data(file):
    f = open(file, "r")
    j = 0
    data = []
    for line in f.readlines():
        l = eval(line)
        if j == 0:
            tasks = l
            j += 1
        elif j == 1:
            B = l
            j += 1
        elif j == 2:
            S0 = l
            j += 1
        elif j ==3:
            data.append([tasks, B, S0, l])
            j = 0
    f.close()
    return data

def greedy_start(data):
    results = []
    for i in range(len(data)):
        time, load = 0, 0
        start, due = [], []
        for j in range(len(data[i][0])):
            due.append([data[i][0][j][0], j])
        due.sort()

        for tasks in due:
            task = tasks[1]
            if time >= 15*(data[i][1]-1):
                start.append(0)
            elif load + data[i][0][task][1] <= 15:
                start.append(time)
                load += data[i][0][task][1]
            else:
                start_task = time + load
                time += 15
                load = data[i][0][task][1] - 15 + load
                start.append(start_task)
        results.append(start)
        
    f = open("Bucketised_Planning_Problem/data/Greedy_initial_solution.txt", "w", encoding="utf-8")
    json.dump(results, f)
    f.close()
    return 'succeed'

def weights_random_fct(data):
    weights_rand = []
    for i in range(len(data)):
        weights_rand.append([])
        for task in range(len(data[i][0])):
            weights_rand[i].append(random.randint(-5, 5))
    f = open('Bucketised_Planning_Problem/data/weights_random_fct.txt', "w", encoding="utf-8")
    json.dump(weights_rand, f)
    f.close()
    return 'Succeed'