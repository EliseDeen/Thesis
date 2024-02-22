import matplotlib.pyplot as plt
import numpy as np
import PrepareData as pd
import json

def histogram(method):  
    ''' Read results '''  
    f = open("Results_TSP_"+str(method)+".txt", "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    
    optimum = pd.prepare_data()

    ''' Initialize lists to store results in useful format '''
    average_ww = np.zeros(len(data[6])+1)
    average_www = np.zeros(len(data[6])+1)
    # average_time = np.zeros(len(weights)+1)
    average_ww[0] = sum(data[0])/len(data[0])
    average_www[0] = sum(data[0])/len(data[0])
    weight_plus_zero = [0]
    # average_time[0] = sum(without[1])/len(without[1])
    for w in range(len(data[6])):
        for i in range(len(data[2])):
            average_ww[w+1] += data[2][i][w]/len(data[2])
            average_www[w+1] += data[4][i][w]/len(data[4])
            # average_time[w+1] += data[1][i][w]/len(data[1])
        weight_plus_zero.append(data[6][w])
    opt = 0
    for i in range(len(optimum)):
        opt += optimum[i][2]/len(optimum)
    opt = (len(weight_plus_zero))*[opt]
    
    ''' Plot '''
    width = 0.5*(weight_plus_zero[2] - weight_plus_zero[1])

    plt.bar(weight_plus_zero, average_ww, width=width)
    plt.plot(weight_plus_zero, opt, 'k-')
    plt.xlabel('Weight')
    plt.ylabel('Average objective value')
    #plt.ylim(-0.1, 5000)
    plt.show()   
    
    plt.bar(weight_plus_zero, average_www, width=width)
    plt.plot(weight_plus_zero, opt, 'k-')
    plt.xlabel('Weight')
    plt.ylabel('Average objective value')
    #plt.ylim(-0.1, 5000)
    plt.show()   

    return 'Succeed'

# Creating plots
def simple_plot(method):
    ''' Read results '''  
    f = open("Results_TSP_"+str(method)+".txt", "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    
    optimum = pd.prepare_data()

    ''' Plot '''  
    n = 0.1
    for i in range(len(data[0])):
        y = [data[0][i]] + list(data[2][i]) #+ [optimum[i][3]]
        if n > 1:
            n = 0.1
        plt.plot([0]+data[6], y, '-o', color=(0.2, 0.5, 0.7, n))
        n += 0.1
    opt = [optimum[i][2]]*(len(data[6])+1)
    plt.plot([0]+data[6], opt, '-', color=(0.8, 0.5, 0.3, 0.4))
    plt.xlabel('Weight')
    plt.ylabel('Objective value')
    plt.show()
    
    n = 0.1
    for i in range(len(data[0])):
        y = [data[0][i]] + list(data[4][i]) #+ [optimum[i][3]]
        if n > 1:
            n = 0.1
        plt.plot([0]+data[6], y, '-o', color=(0.2, 0.5, 0.7, n))
        n += 0.1
    opt = [optimum[i][2]]*(len(data[6])+1)
    plt.plot([0]+data[6], opt, '-', color=(0.8, 0.5, 0.3, 0.4))
    plt.xlabel('Weight')
    plt.ylabel('Objective value')
    plt.show()

    return 'Succeed'

def boxplot(method):
    ''' Read results '''  
    f = open("Results_TSP_"+str(method)+".txt", "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    
    optimum = pd.prepare_data()

    plotdata1, plotdata2, plotdata3 = [], [], []
    for w in range(0, len(data[6]), 2):
        for i in range(len(data)):
            plotdata1.append(optimum[i][2]/data[0][i])
            plotdata2.append(optimum[i][2]/data[2][w][i])
            plotdata3.append(optimum[i][2]/data[4][w][i])
    plotdata = [np.array(plotdata1), np.array(plotdata2), np.array(plotdata3)]
    plt.boxplot(plotdata)
    plt.ylim(0.95, 1.25)
    plt.show()
    
    return 'Succeed'

 
# weights = [0.1, 1, 10, 100] 
# data = [(Prepare_data.prepare_data('att48'), 10628)]
# # data = [(Prepare_data.prepare_data('burma14'), 3323), (Prepare_data.prepare_data('bays29'), 2020)] #Test_data.interpret_data("data_simple100.txt")
# for i in range(len(data)):
#     path = (list(data[i][0].get_nodes()).copy())
#     random.shuffle(path)
# methods = ['potential_idea3', 'potential_idea4', 'potential_idea5']
# normal_results, normal_time, pot_with_results, pot_with_time, pot_without_results, pot_without_time = [], [], [], [], [], []
# for i in range(len(methods)):
#     # open("results.txt", "w")
#     # f = open("results.txt", "a")
#     n1, n2, n3, n4, n5, n6 = run_algorithms(data, path, methods[i], weights) 
#     normal_results.append(n1)
#     normal_time.append(n2) 
#     pot_with_results.append(n3)
#     pot_with_time.append(n4)
#     pot_without_results.append(n5)
#     pot_without_time.append(n6)

# #     f.write(str(n1)+'\n')
# #     f.write(str(n2)+'\n')
# #     f.write(str(n3)+'\n')
# #     f.write(str(n4)+'\n')
# #     f.write(str(n5)+'\n')
# #     f.write(str(n6)+'\n')
# #     f.write('\n')
# # #check = 'y'
# # #while check == 'y':
# # f.close()

# # f = open(file, "r")
# # j = 0
# # for line in f.readlines():
# #     if j == 0:
# #         normal_results.append(n1)
# #     normal_time.append(n2) 
# #     pot_with_results.append(n3)
# #     pot_with_time.append(n4)
# #     pot_without_results.append(n5)
#     # pot_without_time.append(n6)
#     #     j += 1
#     # elif j == 1:
#     #     j += 1
#     # elif j == 2:
#     #     j += 1
#     # elif j == 3:
#     #     j += 1
#     # elif j == 4:
#     #     j += 1
#     # elif j == 5:
#     #     j = 0
# for i in range(len(methods)):
#     create_barplot(normal_results[i], pot_with_results[i], pot_without_results[i], weights)
#     # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 0)
#     # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 1)
#     # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 2)
#     # create_boxplot(data, normal_results[i], pot_with_results[i], pot_without_results[i], 3)
#     #check = input('continue? [y/n] ')