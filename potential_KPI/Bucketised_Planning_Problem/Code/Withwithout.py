import json
import Algorithms as alg

def run(data, T, delta, weights, initial_solution, setting):
    objectives_final, time_final, num_iterations_final, sol = [], [], [], []
    obj_vs_opt_final = [] 

    for i in range(len(data)):
        objectives, times, num_iterations = [], [], []
        obj_vs_opt = []
        for w in range(len(weights)):
            solution, obj, L_pot_with, num_iterations1, time1, sol_best1, obj_best1 = alg.LocalSearch(data[i][0], initial_solution, T, data[i][1], delta, setting[0], weights[w], [1, len(data[i][0])])
            solution, obj, L_pot_with, num_iterations2, time2, sol_best2, obj_best2 = alg.LocalSearch(data[i][0], solution, T, data[i][1], delta, 'normal',  weights[w], [1, len(data[i][0])])
            if obj_best1 < obj_best2:
                objectives.append(float(obj_best1))
            else:
                objectives.append(float(obj_best2)) 
            num_iterations.append([float(num_iterations1), float(num_iterations2)]) 
            times.append([float(time1), float(time2)])
            sol.append([float(x) for x in solution])
            if obj == 0:
                obj_vs_opt.append(1.0)
            else:
                obj_vs_opt.append(float(data[i][3] / obj)) 
        objectives_final.append(objectives)
        time_final.append(times)
        num_iterations_final.append(num_iterations)
        obj_vs_opt_final.append(obj_vs_opt)
        print(i, objectives, flush=True)
    f = open("Results_BPP_ww_"+setting[0]+"_"+setting[1]+".txt", "w", encoding="utf-8")
    json.dump([objectives_final, time_final, num_iterations_final, sol, obj_vs_opt_final], f)
    f.close()
    return objectives_final, time_final, num_iterations_final, sol, obj_vs_opt_final