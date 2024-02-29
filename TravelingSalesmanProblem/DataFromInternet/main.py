import PrepareData as pd
import Run as run

""" Initials """
#Weights of the objective functions & potential KPI
weights = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101] #np.arange(1, 1001, 50)
methods = ['potential_idea4', 'potential_idea3', 'potential_idea5']

""" Create results """
data = pd.prepare_data(['a280'])
for i in range(len(methods)):
    print(methods[i])
    obj_value_w, num_iterations_w, time_w, obj_value_ww, num_iterations_ww, time_ww, obj_value_www, num_iterations_www, time_www = run.run_algorithms(data, methods[i], weights)
    print('Time of the method: ', time_w, time_ww, time_www)
    print('Found optimum: ', obj_value_w, obj_value_ww, obj_value_www, data[0][2])
    print('Number of iterations: ', num_iterations_w, num_iterations_ww, num_iterations_www)