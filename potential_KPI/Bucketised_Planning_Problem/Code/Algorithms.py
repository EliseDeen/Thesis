import potentialKPI_fcts as fcts
import time
import numpy as np
import random

def LocalSearch(tasks, S_initial, T, B, delta, objective_name, weight, stop):
    # Initial settings
    time_start = time.time()
    S_current, S_best = S_initial.copy(), S_initial.copy()
    objective = eval('fcts.Objective_'+ objective_name)
    objective_change = eval('fcts.Change_'+ objective_name)
    f_current, L_current = objective(tasks, S_current, T, B, weight)
    f_best, L_best = fcts.Objective_normal(tasks, S_best, T, B, weight)
    num_iterations = [0, 0]

    # Start algorithm
    while num_iterations[stop[0]] <= stop[1]:
        S_best_neighbour, f_best_neighbour, L_best_neighbour = None, np.infty, None
        i_range = list(range(len(tasks)))

        for neighbour_task in range(len(tasks)):
            # Choose task to move randomly
            i = random.choice(i_range)
            i_range.remove(i)

            d_range = list(np.arange(-delta, delta+1, 1))
            for neighbour_time in np.arange(-delta, delta+1, 1):
                # Choose new start time of the task randomly
                d = random.choice(d_range)
                d_range.remove(d)
                t = S_current[i] + d

                # Check if start & end time within time interval
                if d == 0 or t < 0 or t + tasks[i][1] >= B*T:
                    continue

                # Calculate (adapted) objective value of neighbour & check if it is the best neighbour
                f_neighbour, L_neighbour, bucket1, bucket2 = objective_change(tasks, S_current, L_current, i, t, T, f_current, weight)
                S_neighbour = S_current.copy()
                S_neighbour[i] = t
                if f_best_neighbour >= f_neighbour:
                    S_best_neighbour = S_neighbour
                    f_best_neighbour = f_neighbour   
                    L_best_neighbour = L_neighbour.copy()

                # Check if neighbour better than best solution for original objective
                f_normal, L_normal = fcts.Objective_normal(tasks, S_neighbour, T, B, weight)
                if f_normal <= f_best:
                    S_best = S_neighbour
                    f_best = f_normal
                    L_best = L_normal

        # Check if best neighbour better than current solution
        if f_best_neighbour <= f_current:
            S_current = S_best_neighbour.copy()
            f_current = f_best_neighbour  
            L_current = L_best_neighbour.copy()
        # Update the number of iterations with no improvement and complete number of iterations
        if f_best_neighbour >= f_current:
            num_iterations[1] += 1
        else:
            num_iterations[1] = 0
        num_iterations[0] += 1

    return S_current, f_current, L_current, num_iterations[0], time.time()-time_start, S_best, f_best