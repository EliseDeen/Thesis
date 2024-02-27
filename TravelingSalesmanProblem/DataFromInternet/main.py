import numpy as np
import PrepareData as pd
import Run as run
import PlotResults
import PotentialKPIfcts as pot
import random
import Algorithms as alg
import time

""" Initials """
#Weights of the objective functions & potential KPI
weights = [10] #np.arange(1, 1001, 50)
methods = ['potential_idea3'] #['potential_idea3', 'potential_idea4', 'potential_idea5']

""" Create results """
data = pd.prepare_data(['ulysses16'])
# results_w, time_w, results_ww, time_ww, results_www, time_www = [], [], [], [], [], []
for i in range(len(methods)):
    n1, n2, n3, n4, n5, n6, t7, t8, t9 = run.run_algorithms(data, methods[i], weights)
#     # results_w.append(n1)
#     # time_w.append(n2)
#     # results_ww.append(n3)
#     # time_ww.append(n4)
#     # results_www.append(n5)
#     # time_www.append(n6)
print('Average time per iteration: ', t7, t8, t9)
print('Found optimum: ', n1, n3, n5, data[0][2])

''' Test '''
# path = data[0][1]
# curr_len, closest2 = pot.potential_idea3(data[0][0], path, 10, data[0][3])
# change_result = curr_len
# closest3 = closest2
# for i in range(15):
#     x = random.randint(0, len(data[0][1])-3)
#     y = random.randint(x+2, len(data[0][1])-1)
#     print(x, y)
#     # curr_len, closest = pot.potential_idea3(data[0][0], path, 10, data[0][3])
#     time1 = time.time()
#     change_result, closest2 = pot.potential_idea3_change(data[0][0], path, change_result, x, y, 10, closest3)
#     time2 = time.time()
#     path = alg.do2Opt(path, x, y)
#     norm_result, closest3 = pot.potential_idea3(data[0][0], path, 10, closest3)
#     time3 = time.time()
#     print(curr_len, change_result, norm_result)
#     print(time2-time1, time3-time2)


""" Plot results """
# for m in methods:
#     print(PlotResults.simple_plot(m))
#     print(PlotResults.histogram(m))
#     print(PlotResults.boxplot(m))