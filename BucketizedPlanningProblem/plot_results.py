import matplotlib.pyplot as plt
import numpy as np
import Test_data
import Withwithout as ww
import Withoutwithwithout as www
import json

#create results for a weight range of 50 to 1000
def test_prepare(T, weights, delta, method):
    data = Test_data.interpret_data("data_BP.txt")
    objectives, time, sol, obj_vs_opt = method.run(data, T, delta, weights)
    return objectives, time, sol, obj_vs_opt, weights

#Plot the results
def plot(weights, method):
    print('ontvangen') 
    ''' Get data '''
    f = open("Results_BP_w.txt", "r", encoding="utf-8")
    without = json.load(f)
    f.close()

    f = open("Results_BP_"+method+".txt", "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    
    optimum = Test_data.interpret_data("data_BP.txt")

    ''' Initialize lists to store results in useful format '''
    average = np.zeros(len(weights)+1)
    # average_time = np.zeros(len(weights)+1)
    average[0] = sum(without[0])/len(without[0])
    weight_plus_zero = [0]
    # average_time[0] = sum(without[1])/len(without[1])
    for w in range(len(weights)):
        for i in range(len(data[0])):
            average[w+1] += data[0][i][w]/len(data[0])
            # average_time[w+1] += data[1][i][w]/len(data[1])
        weight_plus_zero.append(weights[w][2])
    opt = 0
    for i in range(len(optimum)):
        opt += optimum[i][3]/len(optimum)
    opt = (len(weights)+1)*[opt]
    
    ''' Simple plot to see difference '''
    n = 0.1
    for i in range(len(data[0])):
        y = [without[0][i]] + list(data[0][i]) #+ [optimum[i][3]]
        if n > 1:
            n = 0.1
        plt.plot(weight_plus_zero, y, '-o', color=(0.2, 0.5, 0.7, n))
    plt.xlabel('Weight')
    plt.ylabel('Objective value')
    plt.show()

    ''' Create plots '''
    #Plot of objectives
    plt.bar(weight_plus_zero, average, width=0.05)
    plt.plot(weight_plus_zero, opt, 'k-')
    plt.xlabel('Weight')
    plt.ylabel('Average objective value')
    #plt.ylim(-0.1, 5000)
    plt.show()   

    # #Plot of number of iterations i.e. time
    # plt.bar(weight_plus_zero, average_time, width=25)
    # plt.xlabel('Weight')
    # plt.ylabel('Average number of iterations')
    # plt.show()   
    
    #Boxplot of the optimum in comparison with the calculated objective
    plotdata = [np.array(without[3])]
    for w in range(0, len(weights), 2):
        y = []
        for i in range(len(data[3])):
            y.append(data[3][i][w])
        plotdata.append(np.array(y))
    plt.boxplot(plotdata)
    plt.ylim(-0.1, 1.1)
    plt.xlabel('Weights')
    plt.ylabel('Objective value of optimum / method')
    plt.show()

    return 'succeed'

def count_better(weights, method):
    print('ontvangen') 
    ''' Get data '''
    f = open("Results_BP_w.txt", "r", encoding="utf-8")
    without = json.load(f)
    f.close()

    f = open("Results_BP_"+method+".txt", "r", encoding="utf-8")
    data = json.load(f)
    f.close()

    better_10 = np.zeros(len(data[0][0]))
    better = np.zeros(len(data[0][0]))
    worse_10 = np.zeros(len(data[0][0]))
    worse = np.zeros(len(data[0][0]))
    equal = np.zeros(len(data[0][0]))
    for i in range(len(data[0])):
        for w in range(len(weights)):
            if without[0][i] == data[0][i][w]:
                equal[w] += 1
            elif 1.1 * without[0][i] < data[0][i][w]:
                worse[w] += 1
            elif without[0][i] < data[0][i][w]:
                worse_10[w] += 1
            elif 0.9 * without[0][i] > data[0][i][w]:
                better[w] += 1
            elif without[0][i] > data[0][i][w]:
                better_10[w] += 1
    print('better: ', sum(better), better)
    print('worse: ', sum(worse), worse)
    print('better_10: ', sum(better_10), better_10)
    print('worse_10: ', sum(worse_10), worse_10)
    print('equal: ', sum(equal), equal)

    counts = {'More than 10% worse': worse, 'Less than 10% worse': worse_10, 'Equal': equal, 'At most 10% better': better_10, 'More than 10% better': better}
    weight_label = []
    for i in range(len(weights)):
        weight_label.append(str(weights[i][2]))
    width = 0.5

    fig, ax = plt.subplots()
    bottom = np.zeros(len(weights))

    for name, count in counts.items():
        # print(len(count), count)
        # print(len(weight_label), weight_label)
        p = ax.bar(weight_label, count, width, label=name, bottom=bottom)
        bottom += count

    # ax.set_title("Number of penguins with above average body mass")
    ax.legend(loc="upper right")

    plt.show()
    return better, worse, equal