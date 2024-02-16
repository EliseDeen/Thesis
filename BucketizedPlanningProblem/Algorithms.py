import Bucketized_problem as BP
import time
import numpy as np
# import visual
import random

""" PickBest algorithm """            #stopping criteria and when a change in weight toevoegen
def PickBest(steps, S0, T, B, delta, objective, c, stop):
    # start_time0 = time.time()
    # w = c
    S_best = S0.copy()
    o = eval('BP.Objective_'+ objective)
    o_change = eval('BP.Change_'+ objective)
    f_best, L_best = o(steps, S_best, T, B, c)
    num_iterations = [0, 0]

    while num_iterations[stop[0]] <= stop[1]:
        # start_time = time.time()
        # print(f_best, f_best_norm)
        # visual.graph([steps, T, B], L_best)
        # if per == 1:
        #     w[2] = c[2] * f_best
        S = None
        f_subopt = np.infty
        L = None
        i_range = list(range(len(steps)))

        for buur in range(len(steps)):
            d_range = list(np.arange(-delta, delta+1, 1))
            i = random.choice(i_range)
            i_range.remove(i)

            for dit in np.arange(-delta, delta+1, 1):
                d = random.choice(d_range)
                d_range.remove(d)

                if d == 0:
                    continue
                t = S_best[i] + d
                if t < 0 or t + steps[i][1] >= B*T:
                    continue

                f, L2, J1, J2 = o_change(steps, S_best, L_best, i, t, T, f_best, c)
                if f_subopt >= f:
                    #print(i, d, k, t)
                    S = S_best.copy()
                    S[i] = t
                    f_subopt = f   
                    L = L2.copy()
            #print(time.time()-start_time) 
        if f_subopt >= f_best:
            num_iterations[1] += 1
        else:
            num_iterations[1] = 0
        if f_subopt <= f_best:
            S_best = S.copy()
            f_best = f_subopt  
            L_best = L.copy()
        num_iterations[0] += 1
    return S_best, f_best, L_best, num_iterations[0] #time.time()-start_time0

         
def Hill_Climbing(steps, S0, K, P, T, B, delta, objective, c):
    start_time0 = time.time()
    S_best = S0.copy()
    o = eval('BP.Objective_'+ objective)
    o_change = eval('BP.Change_'+ objective)
    f_best, L_best = o(steps, S_best, T, B, c)
    count = 0
    for k in range(K):
        if count >= 10:
            return S_best, f_best, L_best, time.time()-start_time0
        f_best_norm, L_norm = BP.Objective_normal(steps, S_best, T, B, c)
        print(f_best, f_best_norm)
        i = 0
        y = True
        while y:
            for d in np.arange(-delta, delta, 1):
                if d == 0:
                    continue
                t = S_best[i] + d
                #print(i, t)
                if t < 0 or t + steps[i][1] >= B*T:
                    continue
                f, L2, J1, J2 = o_change(steps, S_best, L_best, i, t, T, f_best, c)
                if f_best >= f:
                    S_best[i] = t
                    f_best = f   
                    L_best = L2.copy()
                    y = False
                    break
            i += 1
            if i >= len(steps):
                y = False
                count += 1
    return S_best, f_best, L_best, time.time()-start_time0

def Hard_cut_no_change(steps, S0, K, P, T, B, delta, w, m):
    start_time0 = time.time()
    count = 0
    c = w.copy()
    S_best = S0.copy()
    f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
    for k in range(K):
        if count >= m:
            return S_best, f_best, time.time()-start_time0
        S_subopt = None
        f_subopt = np.infty
        L_subopt = None
        for p in range(P):
            i = np.random.randint(0,len(steps))
            t = S_best[i] + np.random.randint(-delta, delta)
            if t < 0 or t + steps[i][1] >= B*T:
                continue
            f, L, J1, J2 = BP.Change_Potential(steps, S_best, L_best, i, t, T, f_best, c)
            if f_subopt >= f:
                S_subopt = S_best.copy()
                S_subopt[i] = t
                f_subopt = f   
                L_subopt = L
        #print(count, f_best, f_subopt)  
        if f_subopt == f_best or f_subopt > f_best:
            count += 1
        else:
            count = 0
        if f_subopt <= f_best:
            S_best = S_subopt.copy()
            f_best = f_subopt
            L_best = L_subopt
    return S_best, f_best, time.time()-start_time0

def Soft_cut_no_change(steps, S0, K, P, T, B, delta, w, n, m):
    start_time0 = time.time()
    count = 0
    c = w.copy()
    S_best = S0.copy()
    f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
    for k in range(K):
        if count >= m:
            c[2] = c[2] * n
            f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
            count = 0
        #print(k)    
        #start_time = time.time()
        S_subopt = None
        f_subopt = np.infty
        for p in range(P):
            #start_time = time.time()
            i = np.random.randint(0,len(steps))
            t = S_best[i] + np.random.randint(-delta, delta)
            if t < 0 or t + steps[i][1] >= B*T:
                continue
            S = S_best.copy()
            S[i] = t
            f, L2 = BP.Objective_Potential(steps, S, T, B, c)
            if f_subopt >= f:
                S_subopt = S.copy()
                f_subopt = f   
        #print(count, f_best, f_subopt)  
        if f_subopt == f_best or f_subopt > f_best:
            count += 1
        else:
            count = 0
        if f_subopt <= f_best:
            S_best = S_subopt.copy()
            f_best = f_subopt
    #print(c[2])
    return S_best, f_best, time.time()-start_time0, c[2]

def Soft_cut_per_iteration(steps, S0, K, P, T, B, delta, w, n, m):
    start_time0 = time.time()
    S_best = S0.copy()
    c = w.copy()
    f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
    count = 0
    for k in range(K):
        count += 1
        S_subopt = None
        f_subopt = np.infty
        for p in range(P):
            i = np.random.randint(0,len(steps))
            t = S_best[i] + np.random.randint(-delta, delta)
            if t < 0 or t + steps[i][1] >= B*T:
                continue
            S = S_best.copy()
            S[i] = t
            f, L2 = BP.Objective_Potential(steps, S, T, B, c)
            if f_subopt >= f:
                S_subopt = S.copy()
                f_subopt = f   
        if f_subopt <= f_best:
            S_best = S_subopt.copy()
            f_best = f_subopt  
        if count >= m:    
            c[2] = c[2] * n
            f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
            count = 0
    #print(c[2])
    return S_best, f_best, time.time()-start_time0, c[2]

def Soft_cut_no_change_plus(steps, S0, K, P, T, B, delta, w, n, m):
    start_time0 = time.time()
    count = 0
    c = w.copy()
    S_best = S0.copy()
    f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
    for k in range(K):
        if count >= m and c[2] + n >= 0:
            c[2] = c[2] + n
            f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
            count = 0
        #print(k)    
        #start_time = time.time()
        S_subopt = None
        f_subopt = np.infty
        for p in range(P):
            #start_time = time.time()
            i = np.random.randint(0,len(steps))
            t = S_best[i] + np.random.randint(-delta, delta)
            if t < 0 or t + steps[i][1] >= B*T:
                continue
            S = S_best.copy()
            S[i] = t
            f, L2 = BP.Objective_Potential(steps, S, T, B, c)
            if f_subopt >= f:
                S_subopt = S.copy()
                f_subopt = f   
        #print(count, f_best, f_subopt)  
        if f_subopt == f_best or f_subopt > f_best:
            count += 1
        else:
            count = 0
        if f_subopt <= f_best:
            S_best = S_subopt.copy()
            f_best = f_subopt
    #print(c[2])
    return S_best, f_best, time.time()-start_time0, c[2]

def Soft_cut_per_iteration_plus(steps, S0, K, P, T, B, delta, w, n, m):
    start_time0 = time.time()
    S_best = S0.copy()
    c = w.copy()
    f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
    count = 0
    for k in range(K):
        count += 1
        S_subopt = None
        f_subopt = np.infty
        for p in range(P):
            i = np.random.randint(0,len(steps))
            t = S_best[i] + np.random.randint(-delta, delta)
            if t < 0 or t + steps[i][1] >= B*T:
                continue
            S = S_best.copy()
            S[i] = t
            f, L2 = BP.Objective_Potential(steps, S, T, B, c)
            if f_subopt >= f:
                S_subopt = S.copy()
                f_subopt = f   
        if f_subopt <= f_best:
            S_best = S_subopt.copy()
            f_best = f_subopt  
        if count >= m and c[2] + n >= 0:    
            c[2] = c[2] + n
            f_best, L_best = BP.Objective_Potential(steps, S_best, T, B, c)
            count = 0
    #print(c[2])
    return S_best, f_best, time.time()-start_time0, c[2]