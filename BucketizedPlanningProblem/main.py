# import Local_min_tests as test
# import Algorithms as alg
# import numpy as np
# import Bucketized_problem as BP
# import visual
import Test_data
import Without
import plot_results
import json
import Withwithout as ww
import Withoutwithwithout as www

""" Initials """
# c = [0.1, 1000] #Weights of the objective functions
# K = 100000 #Number of iterations
# P = 10 #Number of trials
# n = 1/2 #Change of weight

weight = [1, 1000] #Standard weight for objective
T, B = 15, 7 #Timeframe
delta = 2*T #maximal change

#Weights of the objective functions & potential KPI
weights = [] 
for i in range(1, 21):
    weights.append([1, 1000, i*50])
    # weights.append([1, 1000, i*0.1])

""" Create data --> problem instances and found minima """
# problem, start = test.create_example()
# create_data(15)

# data = Test_data.interpret_data("data_BP.txt")
# objectives_without, time_without, sol_without, obj_vs_opt = Without.run(data, T, delta, weight)

# objectives, time, sol, obj_vs_opt, weights_ww = plot_results.test_prepare(T, weights, delta, ww)

# objectives, time, sol, obj_vs_opt, weights_www = plot_results.test_prepare(T, weights, delta, www)

""" Plot results """
# print(plot_results.plot(weights, 'ww_smaller'))
# print(plot_results.plot(weights, 'www_smaller'))
plot_results.count_better(weights, 'ww')
plot_results.count_better(weights, 'www')

'''
S1 = 4*[0] + 3*[15] + 3*[30] + 3*[45] + [45+problem[3]] + 3*[60] + 3*[75]
#S2 = 4*[0] + 3*[15] + 3*[30] + 3*[45] + [45+problem[3]] + 3*[60] + 3*[75]
f, L = BP.Objective_Potential(problem[0], start, problem[1], problem[2], c+[1])
f1, L1 = BP.Objective_Potential(problem[0], S1, problem[1], problem[2], c+[1])
#f2, L2 = BP.Objective_Potential(problem[0], S2, problem[1], problem[2], c+[])
print(f, f1)
visual.graph(problem, L)
visual.graph(problem, L1)
'''
# count = 0
# for i in range(100):
#     #S_hardcut_1, f_hardcut_1, L, time_hardcut_1_1 = alg.PickBest(problem[0], start, K, P, problem[1], problem[2], problem[3], 'Potential', c+[1]) 
#     S_hardcut_1, f_hardcut_1, L, time_hardcut_1_1 = alg.PickBest(problem[0], start, K, P, problem[1], problem[2], problem[3], 'Potential', c+[10]) #weight higher than 0.6 (357 if <delta) to escape local min by LS, by HC >300 but worse
#     f, L = BP.Objective_normal(problem[0], S_hardcut_1, problem[1], problem[2], c)
#     print(i, f)
#     #visual.graph(problem, L)
#     if f < 1000:
#         count += 1
# print(count)
#'''
#print(f)
#print('break')
#visual.graph(problem, L)

#S_hardcut_2, f_hardcut_2, L, time_hardcut_1_2 = alg.PickBest(problem[0], S_hardcut_1, K, P, problem[1], problem[2], problem[3], 'normal', c)
#visual.graph(problem, L)

#print(f_hardcut_2, time_hardcut_1_1+time_hardcut_1_2)
#print(S_hardcut_2)

'''
I = 100
count = {}
for n in np.arange(2, 15, 1):
    count[n] = [0, 0]
for i in range(I):
    print(i)
    for n in np.arange(2, 15, 1):
        S_hardcut_1, f_hardcut_1, L, time_hardcut_1_1 = alg.PickBest(problem[0], start, K, P, problem[1], problem[2], problem[3], 'Potential', c+[1000])

        S_softcut_1, f_softcut_1, time_hardcut_1_2, c2 = alg.Soft_cut_per_iteration(problem[0], S_hardcut_1, K, P, problem[1], problem[2], problem[3], c+[1000], 1/n, 10)
        #S_softcut_1, f_softcut_1, time_hardcut_1_2, c2 = alg.Soft_cut_no_change(problem[0], start, K, P, problem[1], problem[2], problem[3], c+[0.001], n, 10)
        
        S_softcut_1, f_softcut_1, L, time_hardcut_1_3 = alg.PickBest(problem[0], S_softcut_1, K, P, problem[1], problem[2], problem[3], 'normal', c)
        if f_softcut_1 < 1000:
            count[n][0] += 1
        count[n][1] += (time_hardcut_1_2+time_hardcut_1_3)/I
    
print(count)
        
count, gem_time = test.test_increasing(problem, start, K, P, c, n)    
print('Percentages of escaping local minima:', n)
print('Hard cut iterations: ', count[0], ' in on average ', gem_time[0], 'seconds')
print('Hard cut 10: ', count[1], ' in on average ', gem_time[1], 'seconds')
print('Hard cut 100: ', count[2], ' in on average ', gem_time[2], 'seconds')
print('Soft cut 1 10: ', count[3], ' in on average ', gem_time[3], 'seconds')
print('Soft cut 1 100: ', count[4], ' in on average ', gem_time[4], 'seconds')
print('Soft cut no change 10: ', count[5], ' in on average ', gem_time[5], 'seconds')
print('Soft cut 2 100: ', count[6], ' in on average ', gem_time[6], 'seconds')
'''