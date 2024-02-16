import Algorithms as alg
import json

# Run algorithm for all data without potential KPI
def run(data, T, delta, weights):
    objectives = []
    time = []
    sol = []
    obj_vs_opt = []
    for i in range(len(data)):
        sol_normal, obj_normal, L_normal, num_iterations_normal = alg.PickBest(data[i][0], data[i][2], T, data[i][1], delta, 'normal', weights, [1, 2])
        objectives.append(obj_normal)
        time.append(num_iterations_normal)
        sol.append([float(x) for x in sol_normal])
        if obj_normal == 0:
            obj_vs_opt.append(1.0)
        else:
            obj_vs_opt.append(float(data[i][3] / obj_normal))
        print(i)
    f = open("Results_BP_w.txt", "w", encoding="utf-8")
    json.dump([objectives, time, sol, obj_vs_opt], f)
    f.close()
    return objectives, time, sol, obj_vs_opt