import Algorithms as opt
import json
import numpy as np
import PotentialKPIfcts as pot

# Run algorithm for all data for different weights
def run_algorithms(data, method, weights):
    results_w = np.zeros(len(data))
    results_ww = np.zeros([len(weights), len(data)])
    results_www = np.zeros([len(weights), len(data)])
    time_w = np.zeros(len(data))
    time_ww = np.zeros([len(weights), len(data)])
    time_www = np.zeros([len(weights), len(data)])

    for i in range(len(data)):    
        print('problem ', i)    
        path_w, length_w, num_iterations_w, time_w_0 = opt.local_search(data[i][0], data[i][1], 0, 'pot.no_potential', data[i][3])
        results_w[i] = length_w
        time_w[i] = num_iterations_w

        for w in range(len(weights)):
            path_ww, length_ww, num_iterations_ww_1, time_ww_1 = opt.local_search(data[i][0], data[i][1], weights[w], 'pot.'+str(method), data[i][3])
            path_ww, length_ww, num_iterations_ww_2, time_ww_2 = opt.local_search(data[i][0], path_ww, 0, 'pot.no_potential', data[i][3])
            results_ww[w][i] = length_ww
            time_ww[w][i] = num_iterations_ww_1 + num_iterations_ww_2
            # time_ww_0 = time_ww_1+time_ww_2

            path_www, length_www, num_iterations_www_1, time_www_1 = opt.local_search(data[i][0], path_w, weights[w], 'pot.'+str(method), data[i][3])
            path_www, length_www, num_iterations_www_2, time_www_2 = opt.local_search(data[i][0], path_www, 0, 'pot.no_potential', data[i][3])
            results_www[w][i] = length_www
            time_www[w][i] = num_iterations_w + num_iterations_www_1 + num_iterations_www_2
            # time_www_0 = time_www_1 + time_www_2

    # f = open("Results_TSP_"+str(method)+".txt", "w", encoding="utf-8")
    # json.dump([results_w, time_w, results_ww, time_ww, results_www, time_www, weights], f)
    # f.close()

    return results_w, time_w, results_ww, time_ww, results_www, time_www, time_w_0, [time_ww_1, time_ww_2], [time_www_1, time_www_2]
