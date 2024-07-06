import json
import Algorithms as alg

def run(data, T, delta, weights, setting):
    f = open("Results_BPP_ww_"+setting[0]+"_"+setting[1]+".txt", "r", encoding="utf-8")
    ww = json.load(f)
    f.close()
    
    f = open("Results_BP_www_"+setting[0]+"_"+setting[1]+".txt", "r", encoding="utf-8")
    www = json.load(f)
    f.close()

    objectives_final_ww, objectives_final_www = [], [] 
    time_final_ww, time_final_www = [], []
    num_iterations_final_ww, num_iterations_final_www = [], []
    obj_vs_opt_final_ww, obj_vs_opt_final_www = [], []

    for i in range(len(data)):
        objectives_ww, objectives_www = [], []
        time_ww, time_www = [], []
        num_iterations_ww, num_iterations_www = [], []
        obj_vs_opt_ww, obj_vs_opt_www = [], []
        for w in range(len(weights)):
            # ww-method with extra phase, i.e., wwww
            start = ww[3][w+i*11]
            solution_end, obj_end, L_pot_with, num_iterations1, time1, sol_best1, obj_best1 = alg.LocalSearch(data[i][0], start, T, data[i][1], delta, setting[0], weights[w], [1, len(data[i][0])])
            solution, obj_end, L_pot_with, num_iterations2, time2, sol_best2, obj_best2 = alg.LocalSearch(data[i][0], solution_end, T, data[i][1], delta, 'normal', weights[w], [1, len(data[i][0])])
            if obj_best1 < obj_best2 and obj_best1 < ww[0][i][w]:
                obj = obj_best1
            elif obj_best2 < obj_best1 and obj_best2 < ww[0][i][w]:
                obj = obj_best2
            else:
                obj = ww[0][i][w]
            objectives_ww.append(float(obj))
            num_iterations_ww.append([ww[2][i][w][0], ww[2][i][w][1], float(num_iterations1), float(num_iterations2)]) 
            time_ww.append([ww[1][i][w][0], ww[1][i][w][1], float(time1), float(time2)])
            if obj == 0:
                obj_vs_opt_ww.append(1.0)
            else:
                obj_vs_opt_ww.append(float(data[i][3] / obj))

            # www-method with extra phase, i.e., wwwww
            start = www[3][w+i*11]
            solution_end, obj_end, L_pot_with, num_iterations1, time1, sol_best1, obj_best1 = alg.LocalSearch(data[i][0], start, T, data[i][1], delta, setting[0], weights[w], [1, len(data[i][0])])
            solution, obj_end, L_pot_with, num_iterations2, time2, sol_best2, obj_best2 = alg.LocalSearch(data[i][0], solution_end, T, data[i][1], delta, 'normal', weights[w], [1, len(data[i][0])])
            if obj_best1 < obj_best2 and obj_best1 < www[0][i][w]:
                obj = obj_best1
            elif obj_best2 < obj_best1 and obj_best2 < www[0][i][w]:
                obj = obj_best2
            else:
                obj = www[0][i][w]
            objectives_www.append(float(obj))
            num_iterations_www.append([www[2][i][w][0], www[2][i][w][1], www[2][i][w][2], float(num_iterations1), float(num_iterations2)]) 
            time_www.append([www[1][i][w][0], www[1][i][w][1], www[1][i][w][2], float(time1), float(time2)])
            if obj == 0:
                obj_vs_opt_www.append(1.0)
            else:
                obj_vs_opt_www.append(float(data[i][3] / obj))
        objectives_final_ww.append(objectives_ww)
        time_final_ww.append(time_ww)
        num_iterations_final_ww.append(num_iterations_ww)
        obj_vs_opt_final_ww.append(obj_vs_opt_ww)
        print(i, objectives_ww, flush=True)

        objectives_final_www.append(objectives_www)
        time_final_www.append(time_www)
        num_iterations_final_www.append(num_iterations_www)
        obj_vs_opt_final_www.append(obj_vs_opt_www)
        print(i, objectives_www, flush=True)
    
    f = open("Results_BP_wwww_"+setting[0]+"_"+setting[1]+".txt", "w", encoding="utf-8")
    json.dump([objectives_final_ww, time_final_ww, num_iterations_final_ww, [], obj_vs_opt_final_ww], f)
    f.close()

    f = open("Results_BP_wwwww_"+setting[0]+"_"+setting[1]+".txt", "w", encoding="utf-8")
    json.dump([objectives_final_www, time_final_www, num_iterations_final_www, [], obj_vs_opt_final_www], f)
    f.close()
    return objectives_final_www, time_final_www, num_iterations_final_www, obj_vs_opt_final_www