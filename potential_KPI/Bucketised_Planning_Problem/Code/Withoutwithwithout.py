import json
import Algorithms as alg

def run(data, T, delta, weights, setting):
    f = open("Results_BPP_w_"+setting[1]+".txt", "r", encoding="utf-8")
    without = json.load(f)
    f.close()

    objectives_final, time_final, num_iterations_final, sol = [], [], [], []
    obj_vs_opt_final = []

    for i in range(len(data)):
        objectives, time_www, num_iterations_www = [], [], []
        obj_vs_opt = []

        for w in range(len(weights)):
            solution, obj, L_pot_with, num_iterations1, time1, sol_best1, obj_best1 = alg.LocalSearch(data[i][0], without[3][i], T, data[i][1], delta, setting[0], weights[w], [1, len(data[i][0])])
            solution, obj, L_pot_with, num_iterations2, time2, sol_best2, obj_best2 = alg.LocalSearch(data[i][0], solution, T, data[i][1], delta, 'normal',  weights[w], [1, len(data[i][0])])
            
            # Determine which solution is best, the one found with the first, second or third phase of the algorithm
            if obj_best1 < obj_best2 and obj_best1 < without[0][i]:
                objectives.append(float(obj_best1))
            elif obj_best2 < obj_best1 and obj_best2 < without[0][i]:
                objectives.append(float(obj_best2))
            else:
                objectives.append(float(without[0][i]))

            num_iterations_www.append([float(without[2][i]), float(num_iterations1), float(num_iterations2)])
            time_www.append([without[1][i], float(time1), float(time2)])
            sol.append([float(x) for x in solution])

            if obj == 0:
                obj_vs_opt.append(1.0)
            else:
                obj_vs_opt.append(float(data[i][3] / obj))
        objectives_final.append(objectives)
        time_final.append(time_www)
        num_iterations_final.append(num_iterations_www)
        obj_vs_opt_final.append(obj_vs_opt)
        print(i, objectives, flush=True)
    
    f = open("Results_BPP_www_"+setting[0]+"_"+setting[1]+".txt", "w", encoding="utf-8")
    json.dump([objectives_final, time_final, num_iterations_final, sol, obj_vs_opt_final], f)
    f.close()
    return objectives_final, time_final, num_iterations_final, sol, obj_vs_opt_final