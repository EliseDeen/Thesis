import matplotlib.pyplot as plt
import numpy as np
import Local_min_tests as test
import Bucketized_problem as BP
   
def graph(problem, load):
    buckets = range(problem[2])
    loads = {}
    for i in range(len(problem[0])):
        loads[i] = np.zeros(problem[2])
        for j in buckets:
            loads[i][j] = load[i,j]
    width = 0.9  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()
    bottom = np.zeros(problem[2])
    plt.ylim(0,30)
    color = []
    n = 0.1
    for c in range(len(problem[0])):
        if n > 1:
            n = 0.1
        color.append((0.2, n, 0.7, 0.1))
        n += 0.1

    for step, load in loads.items():
        p = ax.bar(buckets, load, width, label=step, bottom=bottom, color=color, edgecolor='black')
        bottom += load
        for i in range(len(color)):
            n = color[i][3]+0.1
            if n > 1:
                n = 0.1
            color[i] = (color[i][0], color[i][1], color[i][2], n)

        ax.bar_label(p, label_type='center')

    ax2 = ax.twinx()
    capacity = np.ones(problem[2]) * problem[1]
    ax2.plot(buckets, capacity, color='darkblue')
    ax2.set_ylim(0,30)

    ax.set_xlabel('Buckets')
    ax.set_ylabel('Time')

    plt.show()

""" Initials """
c = [0.1, 1000, 100] #Weights of the objective functions
K = 1000 #Number of iterations
P = 10 #Number of trials
n = 1/2 #Change of weight

ans = input('Plot basics? [y] ')
if ans == 'y':
    problem, start = test.create_example()
    normal, potential, GLS = test.run_basics(problem, start, K, P, c)
while ans == 'y':
    choice = input('Which method do you want to plot? [normal, potential, GLS, start] ')
    if choice == 'normal':
        load = normal[3]
    elif choice == 'potential':
        load = potential[3]
    elif choice == 'GLS':
        load = GLS[3]
    elif choice == 'start':
        load = BP.Load_per_bucket(problem[0], start, problem[1], problem[2])
    else:
        print('Method does not exist.')
        continue
    graph(problem, load)
    ans = input('Do you want to continue? [y] ')
 