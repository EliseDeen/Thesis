import ILP
import random
import math

def startposition(steps, B, T):
    S0 = []
    for i in range(len(steps)):
        S0.append(random.randint(0, int((B-1)*T)))
    return S0

def create_data(T):
    w = [1, 1000]
    limit = 100
    #open("data_BP.txt", "w")
    f_simple = open("data_BP.txt", "a")
    num_steps = 10*[10] + 45*[20] + 25*[30] + 15*[40] + 5*[50] #+ 10*[60] + 8*[70] + 6*[80] + 4*[90] + 2*[100]
    for i in range(len(num_steps)):
        #print(i, 'simple')
        steps = []
        if num_steps[i] == 20:
            limit = 180
        if num_steps[i] == 30:
            limit = 300
        if num_steps[i] == 40:
            limit = 800
        if num_steps[i] == 50:
            limit = 1800
        #num_steps = 20 #random.randint(0, 100)
        B = 0
        for j in range(num_steps[i]):
            p = random.randint(1, T)
            steps.append([random.randint(0, 5*T), p]) #add [random due date (max end of timeframe), random process time (max end of timeframe / 20)]
            B += p

        B = math.ceil(B/T)
        print(B, i)
        instance = ILP.problem(T, B, steps)
        model = ILP.create_ILP(instance, w, limit)

        S0 = startposition(steps, B, T)

        f_simple.write(str(steps)+'\n')
        f_simple.write(str(B)+'\n')
        f_simple.write(str(S0)+'\n')
        f_simple.write(str(model.objVal)+'\n')

    f_simple.close()
    return 'succeed'

def interpret_data(file):
    f = open(file, "r")
    j = 0
    data = []
    for line in f.readlines():
        l = eval(line)
        if j == 0:
            steps = l
            j += 1
        elif j == 1:
            B = l
            j += 1
        elif j == 2:
            S0 = l
            j += 1
        elif j ==3:
            data.append([steps, B, S0, l])
            #print(len(S0), len(steps))
            j = 0
        #print(j, data)
    f.close()
    # print(len(data[0], data[2]))
    return data

# print(create_data(15))
# print(interpret_data("data_BP.txt"))

# d = interpret_data("data_BP100_simple"+str(15)+str(7)+".txt")
# average = 0
# for i in range(len(d)):
#     average += d[i][1]
# print(average/len(d))