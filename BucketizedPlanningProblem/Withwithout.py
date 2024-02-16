import json
import Algorithms as alg

# Run LS for all data first with potential KPI and then without for multiple weights
def run(data, T, delta, weights):
    objectives_final = [] #len(weights)*[len(data)*[0]]
    time_final = [] #len(weights)*[len(data)*[0]]
    sol = []
    obj_vs_opt_final = [] #len(weights)*[len(data)*[0]]

    for i in range(len(data)):
        objectives = []
        time = []
        obj_vs_opt = []
        for w in range(0, len(weights)):
            solution, obj, L_pot_with, num_iterations1 = alg.PickBest(data[i][0], data[i][2], T, data[i][1], delta, 'Potential', weights[w], [1, 2])
            solution, obj, L_pot_with, num_iterations2 = alg.PickBest(data[i][0], solution, T, data[i][1], delta, 'normal', weights[w], [1, 2])
            objectives.append(float(obj)) # objectives[w][i] = float(obj)
            # print(obj)
            time.append(float(num_iterations1 + num_iterations2)) #time[w][i] = float(num_iterations1 + num_iterations2)
            sol.append([float(x) for x in solution])
            if obj == 0:
                obj_vs_opt.append(1.0) #obj_vs_opt[w][i] = 1.0
            else:
                obj_vs_opt.append(float(data[i][3] / obj)) #obj_vs_opt[w][i] = float(data[i][3] / obj)
        objectives_final.append(objectives)
        time_final.append(time)
        obj_vs_opt_final.append(obj_vs_opt)
        print(i)
    f = open("Results_BP_ww_smaller.txt", "w", encoding="utf-8")
    json.dump([objectives_final, time_final, sol, obj_vs_opt_final], f)
    f.close()
    return objectives_final, time_final, sol, obj_vs_opt_final