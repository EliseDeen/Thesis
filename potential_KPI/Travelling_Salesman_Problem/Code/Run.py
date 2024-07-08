import Algorithms as opt
import json
import numpy as np
import tsplib95

def run_algorithms(dataname, data, instances, method, weights, close):
    path = 'Travelling_Salesman_Problem/Data/TSPLIB95/'
    # Create lists to save results
    results_w, results_ww, results_www = np.zeros(len(instances)), np.zeros([len(instances), len(weights)]), np.zeros([len(instances), len(weights)])
    num_iterations_w, num_iterations_ww, num_iterations_www = np.zeros(len(instances)), np.zeros([len(instances), len(weights), 2]), np.zeros([len(instances), len(weights), 3])
    time_w, time_ww, time_www = np.zeros(len(instances)), np.zeros([len(instances), len(weights), 2]), np.zeros([len(instances), len(weights), 3])

    # Run the different LS algorithms with potential KPI
    for i in range(len(instances)): 
        print(instances[i], flush=True)   

        # Basic Local Search algorithm
        problem = tsplib95.load_problem(path+str(instances[i])+".tsp")
        path_w, result_end, num_iterations_w[i], time_w[i], path_best_w, results_w[i] = opt.local_search(problem, data[instances[i]][0], 0, 'pot.no_potential', close[i])

        for w in range(len(weights)):
            """ ww-method """
            print('ww', w, flush=True)
            path_ww, length_ww, num_iterations_ww_1, time_ww_1, path_best_ww1, length_best_ww1 = opt.local_search(problem, data[instances[i]][0], weights[w], 'pot.'+str(method), close[i])
            path_ww, length_ww, num_iterations_ww_2, time_ww_2, path_best_ww2, length_best_ww2 = opt.local_search(problem, path_ww, 0, 'pot.no_potential', close[i])
            # Determine which found solution is the best, in first phase (with potential KPI) or second (without)
            if length_best_ww1 < length_best_ww2:
                results_ww[i][w] = length_best_ww1
            else:
                results_ww[i][w] = length_best_ww2
            # Save results
            num_iterations_ww[i][w][0], num_iterations_ww[i][w][1] = num_iterations_ww_1, num_iterations_ww_2
            time_ww[i][w][0], time_ww[i][w][1] = time_ww_1, time_ww_2

            """ www-method """
            print('www', w, flush=True)
            path_www, length_www, num_iterations_www_1, time_www_1, path_best_www1, length_best_www1 = opt.local_search(problem, path_w, weights[w], 'pot.'+str(method), close[i])
            path_www, length_www, num_iterations_www_2, time_www_2, path_best_www2, length_best_www2 = opt.local_search(problem, path_www, 0, 'pot.no_potential', close[i])
            # Determine which found solution is the best, in first phase (without potential KPI), second (with) or last (without)
            if length_best_www1 < length_best_www2 and length_best_www1 < results_w[i]:
                results_www[i][w] = length_best_www1
            elif length_best_www2 < length_best_www1 and length_best_www2 < results_w[i]:
                results_www[i][w] = length_best_www2
            else:
                results_www[i][w] = results_w[i]
            # Save results
            num_iterations_www[i][w][0], num_iterations_www[i][w][1], num_iterations_www[i][w][2] = num_iterations_w[i], num_iterations_www_1, num_iterations_www_2
            time_www[i][w][0], time_www[i][w][1], time_www[i][w][2] = time_w[i], time_www_1, time_www_2

    f = open("Results_TSP_"+str(dataname)+str(method)+".txt", "w", encoding="utf-8")
    json.dump([results_w.tolist(), num_iterations_w.tolist(), time_w.tolist(), results_ww.tolist(), num_iterations_ww.tolist(), time_ww.tolist(),results_www.tolist(), num_iterations_www.tolist(), time_www.tolist(), weights], f)
    f.close()

    return results_w, num_iterations_w, time_w, results_ww, num_iterations_ww, time_ww, results_www, num_iterations_www, time_www