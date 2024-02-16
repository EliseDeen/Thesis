import Pathfcts as fcts
import ILP
import random

def createRandomPath(n):
    path =[]
    tabu = []
    for i in range(n):
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        if [x, y] in tabu:
            continue
        else:
            path.append([i, x, y])
            tabu.append([x, y])
    # path.append(path[0])
    return path

def create_data():
    open("data_simple100.txt", "w")
    f_simple = open("data_simple100.txt", "a")
    for i in range(100):
        #print(i, 'simple')
        path_start = createRandomPath(25)
        path = create_path(path_start)

        instance = ILP.problem(path)
        model = ILP.create_ILP(instance)

        f_simple.write(str(path_start)+'\n')
        f_simple.write(str(model.objVal)+'\n')

    f_simple.close()
    
    # open("data_complex.txt", "w")
    # f_complex = open("data_complex.txt", "a")
    # for i in range(1):
    #     #print(i, 'complex')
    #     path_start = createRandomPath(100)
    #     path = create_path(path_start)

    #     instance = ILP.problem(path)
    #     model = ILP.create_ILP(instance)

    #     f_complex.write(str(path_start)+'\n')
    #     f_complex.write(str(model.objVal)+'\n')

    # f_complex.close()

    return 'succeed'

def create_path(path_start):
    path = path_start.copy()
    for i in range(len(path)):
        point = fcts.Point(path[i][0], path[i][1], path[i][2])
        path[i] = point
    return path

def interpret_data(file):
    f = open(file, "r")
    j = 0
    data = []
    for line in f.readlines():
        l = eval(line)
        if j == 0:
            path = create_path(l)
            # path = []
            j += 1
            # for d in l:
            #     point = fcts.Point(d[0], d[1], d[2])
            #     path.append(point)
        elif j == 1:
            data.append((path, l))
            j = 0
        #print(j, data)
    f.close()
    return data

# print(create_data())
# print(interpret_data("data_simple.txt"))