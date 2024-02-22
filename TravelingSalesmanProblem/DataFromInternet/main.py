import numpy as np
import PrepareData as pd
import Run as run
import PlotResults

""" Initials """
#Weights of the objective functions & potential KPI
weights = np.arange(1, 1001, 50)
methods = ['potential_idea3', 'potential_idea4', 'potential_idea5']

""" Create results """
data = pd.prepare_data()
results_w, time_w, results_ww, time_ww, results_www, time_www = [], [], [], [], [], []
for i in range(len(methods)):
    n1, n2, n3, n4, n5, n6 = run.run_algorithms(data, methods[i], weights)
    results_w.append(n1)
    time_w.append(n2)
    results_ww.append(n3)
    time_ww.append(n4)
    results_www.append(n5)
    time_www.append(n6)

""" Plot results """
for m in methods:
    print(PlotResults.simple_plot(m))
    print(PlotResults.histogram(m))
    print(PlotResults.boxplot(m))