import Algorithms as alg
import json

def run(data, T, delta, weights, initial_solution, setting):
    objectives, times, num_iterations, sol = [], [], [], []
    obj_vs_opt = []

    for i in range(len(data)):
        sol_normal, obj_normal, L_normal, num_iterations_normal, time_w, sol_best, obj_best = alg.LocalSearch(data[i][0], initial_solution[i], T, data[i][1], delta, 'normal', weights, [1, len(data[i][0])])
        objectives.append(float(obj_best))
        num_iterations.append(float(num_iterations_normal))
        sol.append([float(x) for x in sol_normal])
        times.append(float(time_w))

        if obj_normal == 0:
            obj_vs_opt.append(1.0)
        else:
            obj_vs_opt.append(float(data[i][3] / obj_normal))
        print(i, obj_normal, flush=True)

    f = open("Results_BPP_w_"+setting+".txt", "w", encoding="utf-8")
    json.dump([objectives, times, num_iterations, sol, obj_vs_opt], f)
    f.close()

    return objectives, times, num_iterations, sol, obj_vs_opt