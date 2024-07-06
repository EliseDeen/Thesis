import matplotlib.pyplot as plt
import numpy as np
import potentialKPI_fcts as fct
      
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

    for task, load in loads.items():
        p = ax.bar(buckets, load, width, label=task, bottom=bottom, color=color, edgecolor='black')
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

""" Program to visualise a instance for BPP, given by the user """
ans = 'y'
while ans == 'y':
    print('Give the instance you want to plot/visualise.')
    num_tasks = int(input('Number of tasks (integer): '))
    tasks, S = [], []
    for n in range(len(num_tasks)):
        d = int(input('Due date '+n+'th task (integer): '))
        p = int(input('Process time '+n+'th task (integer): '))
        tasks.append([d,p])
        start = int(input('Start time '+n+'th task (integer): '))
        S.append(start)
    T = int(input('Capacity of a bucket (integer): '))
    B = int(input('Number of buckets (integer): '))

    problem = [tasks, T, B, None]
    load = fct.Load_per_bucket(tasks, S, T, B)

    graph(problem, load)
    ans = input('Do you want to continue? [y] ')