#import libraries
import matplotlib.pyplot as plt
import numpy as np
import two_opt as opt
import Pathfcts as fcts
import Potential_KPI as pot
# import ILP
import Test_data
import Prepare_data

# Creating dataset
def run_algorithms(data, method, weights):
    normal_results = np.zeros(len(data))
    pot_with_results = np.zeros([len(weights), len(data)])
    pot_without_results = np.zeros([len(weights), len(data)])
    normal_time = np.zeros(len(data))
    pot_with_time = np.zeros([len(weights), len(data)])
    pot_without_time = np.zeros([len(weights), len(data)])
    for i in range(len(data)):
        # print('c')
        path_normal, num_iterations_normal = opt.local_search(data[i][0], 0, eval('pot.no_pot'))
        normal_results[i] = fcts.pathLengthSq(path_normal)
        normal_time[i] = num_iterations_normal
        # print('check1')

        for w in range(len(weights)):
            path_pot_with, num_iterations_pot1_1 = opt.local_search(data[i][0], weights[w], eval('pot.'+method))
            path_pot_with, num_iterations_pot1_2 = opt.local_search(path_pot_with, 0, eval('pot.no_pot'))
            pot_with_results[w][i] = fcts.pathLengthSq(path_pot_with)
            pot_with_time[w][i] = num_iterations_normal + num_iterations_pot1_1 + num_iterations_pot1_2
            # print('check2')
            path_pot_without, num_iterations_pot2_1 = opt.local_search(path_normal, weights[w], eval('pot.'+method))
            path_pot_without, num_iterations_pot2_2 = opt.local_search(path_pot_without, 0, eval('pot.no_pot'))
            pot_without_results[w][i] = fcts.pathLengthSq(path_pot_without)
            pot_without_time[w][i] = num_iterations_normal + num_iterations_pot2_1 + num_iterations_pot2_2
            # print(w)
    print(normal_results, pot_with_results, pot_without_results)
    return normal_results, normal_time, pot_with_results, pot_with_time, pot_without_results, pot_without_time

# Creating plot
def create_boxplot(data, normal, pot_with, pot_without, w):
    plotdata1, plotdata2, plotdata3 = [], [], []
    for i in range(len(data)):
        plotdata1.append(data[i][1]/normal[i])
        plotdata2.append(data[i][1]/pot_with[w][i])
        plotdata3.append(data[i][1]/pot_without[w][i])
    plotdata = [np.array(plotdata1), np.array(plotdata2), np.array(plotdata3)]
    plt.boxplot(plotdata)
    plt.ylim(0.95, 1.25)
    plt.show()

def create_barplot(normal, pot_with, pot_without, weights):
    x = np.arange(len(weights))
    width = 0.25

    data0 = len(weights) * [sum(normal)/len(normal)]
    data1, data2 = [], []
    for w in range(len(weights)):
        data1.append(sum(pot_with[w])/len(pot_with[w]))
        data2.append(sum(pot_without[w])/len(pot_without[w]))
        
    fig, ax = plt.subplots()

    bar1 = ax.bar(x, data0, width=width, label='Without', color='b')
    bar2 = ax.bar(x+width, data1, width=width, label='With-without', color='g')
    bar3 = ax.bar(x+2*width, data2, width=width, label='Without-with-without', color='r')

    ax.legend(loc='upper left')
    plt.show()
 
weights = [0.1, 1, 10, 100] 
data = [(Prepare_data.prepare_data('burma14.tsp'), 3323)] #Test_data.interpret_data("data_simple100.txt")
methods = ['potential_idea3', 'potential_idea4', 'potential_idea5']
normal_results, normal_time, pot_with_results, pot_with_time, pot_without_results, pot_without_time = [], [], [], [], [], []
for i in range(len(methods)):
    # open("results.txt", "w")
    # f = open("results.txt", "a")
    n1, n2, n3, n4, n5, n6 = run_algorithms(data, methods[i], weights) 
    normal_results.append(n1)
    normal_time.append(n2) 
    pot_with_results.append(n3)
    pot_with_time.append(n4)
    pot_without_results.append(n5)
    pot_without_time.append(n6)

#     f.write(str(n1)+'\n')
#     f.write(str(n2)+'\n')
#     f.write(str(n3)+'\n')
#     f.write(str(n4)+'\n')
#     f.write(str(n5)+'\n')
#     f.write(str(n6)+'\n')
#     f.write('\n')
# #check = 'y'
# #while check == 'y':
# f.close()

# f = open(file, "r")
# j = 0
# for line in f.readlines():
#     if j == 0:
#         normal_results.append(n1)
#     normal_time.append(n2) 
#     pot_with_results.append(n3)
#     pot_with_time.append(n4)
#     pot_without_results.append(n5)
    # pot_without_time.append(n6)
    #     j += 1
    # elif j == 1:
    #     j += 1
    # elif j == 2:
    #     j += 1
    # elif j == 3:
    #     j += 1
    # elif j == 4:
    #     j += 1
    # elif j == 5:
    #     j = 0
for i in range(len(methods)):
    create_barplot(normal_results[i], pot_with_results[i], pot_without_results[i], weights)
    # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 0)
    # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 1)
    # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 2)
    # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 3)
    #check = input('continue? [y/n] ')