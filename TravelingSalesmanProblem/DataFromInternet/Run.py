import Algorithms as opt
import json
import numpy as np

# Run algorithm for all data for different weights
def run_algorithms(data, method, weights):
    results_w, results_ww, results_www = np.zeros(len(data)), np.zeros([len(weights), len(data)]), np.zeros([len(weights), len(data)])
    num_iterations_w, num_iterations_ww, num_iterations_www = np.zeros(len(data)), np.zeros([len(weights), len(data)]), np.zeros([len(weights), len(data)])
    time_w, time_ww, time_www = np.zeros(len(data)), np.zeros([len(weights), len(data)]), np.zeros([len(weights), len(data)])

    for i in range(len(data)):    
        print(data[i][4])    
        path_w, results_w[i], num_iterations_w[i], time_w[i] = opt.local_search(data[i][0], data[i][1], 0, 'pot.no_potential', data[i][3])

        for w in range(len(weights)):
            print('ww', w)
            path_ww, length_ww, num_iterations_ww_1, time_ww_1 = opt.local_search(data[i][0], data[i][1], weights[w], 'pot.'+str(method), data[i][3])
            path_ww, length_ww, num_iterations_ww_2, time_ww_2 = opt.local_search(data[i][0], path_ww, 0, 'pot.no_potential', data[i][3])
            results_ww[w][i] = length_ww
            num_iterations_ww[w][i] = num_iterations_ww_1 + num_iterations_ww_2
            time_ww[i] = time_ww_1 + time_ww_2
            print('www', w)
            path_www, length_www, num_iterations_www_1, time_www_1 = opt.local_search(data[i][0], path_w, weights[w], 'pot.'+str(method), data[i][3])
            path_www, length_www, num_iterations_www_2, time_www_2 = opt.local_search(data[i][0], path_www, 0, 'pot.no_potential', data[i][3])
            results_www[w][i] = length_www
            num_iterations_www[w][i] = num_iterations_w[i] + num_iterations_www_1 + num_iterations_www_2
            time_www[i] = time_www_1 + time_www_2 + time_w[i]

    f = open("Results_TSP_"+str(method)+".txt", "w", encoding="utf-8")
    json.dump([results_w, num_iterations_w, time_w, results_ww, num_iterations_ww, time_ww, results_www, num_iterations_www, time_www, weights], f)
    f.close()

    return results_w, num_iterations_w, time_w, results_ww, num_iterations_ww, time_ww, results_www, num_iterations_www, time_www