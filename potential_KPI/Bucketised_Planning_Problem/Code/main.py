import json
import numpy as np
import Create_data
import Without
import Withwithout as ww
import Withoutwithwithout as www
import Extra_phase

# Comment out what you dont want to run
""" Load information """
T = 15
delta = 2*T

""" Create data """
# Simple data
num_tasks = 100*[20] 
B = 7
p_max, d_max = np.ceil(B*T/20), B*T
print(Create_data.create_data(T, num_tasks, p_max, d_max, 'Simple_data', B), flush=True)

# Simple data with twice the amount of buckets
B = 7*2
p_max, d_max = np.ceil(B*T/20), B*T
print(Create_data.create_data(T, num_tasks, p_max, d_max, 'Simple_data_2', B), flush=True)

# Complex data
num_tasks = 10*[10] + 45*[20] + 25*[30] + 15*[40] + 5*[50] 
p_max, d_max = 15, 75
print(Create_data.create_data(T, num_tasks, p_max, d_max, 'Complex_data'), flush=True)

""" Methods run for complex data: load complex data """
""" To run with different data: change which data to load """
path = 'Bucketised_Planning_Problem/Data/'
data = Create_data.interpret_data(path+"Complex_data.txt")
# Add weights for random fct to the information of tasks
f = open(path+"weights_random_fct.txt", 'r', encoding="utf-8")
random_weights = json.load(f)
f.close()
data2 = data.copy()
for i in range(len(data)):
    for j in range(len(data[i][0])):
        data2[i][0][j].append(random_weights[i][j])

# Create Greedy initial solution for complex data
print(Create_data.greedy_start(data), flush=True)

# Create some random weights for the random function
print(Create_data.weights_random_fct(data))

""" Random initial solution """
initial_solution = []
for i in range(len(data)):
    initial_solution.append(data[i][2])

print(Without.run(data, T, delta, [1,1000], initial_solution, 'Random'), flush=True)

# Large weight range (instance-independent weight)
weights = [[1,1000,1], [1,1000,11], [1,1000,21], [1,1000,31], [1,1000,41], [1,1000,51], [1,1000,61], [1,1000,71], [1,1000,81], [1,1000,91], [1,1000,101]]

# SquaredLoad
print(ww.run(data, T, delta, weights, initial_solution, ['SquaredLoad', 'Random']), flush=True)
print(www.run(data, T, delta, weights, ['SquaredLoad','Random']), flush=True)
print(Extra_phase.run(data, T, delta, weights, ['SquaredLoad', 'Random']), flush=True)

# Random function
print(ww.run(data2, T, delta, weights, initial_solution, ['Random', 'Random']), flush=True)
print(www.run(data2, T, delta, weights, ['Random', 'Random']), flush=True)
print(Extra_phase.run(data2, T, delta, weights, ['Random', 'Random']), flush=True)

# Small weight range (instance-dependent weight)
weights = [[1,1000,0.5], [1,1000,1.5], [1,1000,3], [1,1000,4.5], [1,1000,6], [1,1000,7.5], [1,1000,9], [1,1000,10.5], [1,1000,12], [1,1000,13.5], [1,1000,15]]

print(Without.run(data, T, delta, [1,1000], initial_solution, 'Random_small'), flush=True)
# SquaredLoad
print(ww.run(data, T, delta, weights, initial_solution, ['SquaredLoad', 'Random_small']), flush=True)
print(www.run(data, T, delta, weights, ['SquaredLoad', 'Random_small']), flush=True)
print(Extra_phase.run(data, T, delta, weights, ['SquaredLoad', 'Random_small']), flush=True)

""" Greedy initial solution """
f = open(path+"Greedy_initial_solution.txt", "r", encoding="utf-8")
initial_solution = json.load(f)
f.close()

print(Without.run(data, T, delta, [1,1000], initial_solution, 'Greedy'), flush=True)

# Large weight range (instance-independent weight)
weights = [[1,1000,1], [1,1000,11], [1,1000,21], [1,1000,31], [1,1000,41], [1,1000,51], [1,1000,61], [1,1000,71], [1,1000,81], [1,1000,91], [1,1000,101]]

# SquaredLoad
print(ww.run(data, T, delta, weights, initial_solution, ['SquaredLoad', 'Greedy']), flush=True)
print(www.run(data, T, delta, weights, ['SquaredLoad','Greedy']), flush=True)
print(Extra_phase.run(data, T, delta, weights, ['SquaredLoad', 'Greedy']), flush=True)

# Random function
print(ww.run(data2, T, delta, weights, initial_solution, ['Random', 'Greedy']), flush=True)
print(www.run(data2, T, delta, weights, ['Random', 'Greedy']), flush=True)
print(Extra_phase.run(data2, T, delta, weights, ['Random', 'Greedy']), flush=True)