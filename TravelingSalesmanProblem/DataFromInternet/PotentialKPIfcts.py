import numpy as np
import random
import matplotlib.pyplot as plt

def no_potential(problem, path, c):
    curLength = 0
    for i in range(len(path)):
        if i == len(path)-1:
            curLength += problem.get_weight(path[i], path[0])
        else:
            curLength += problem.get_weight(path[i], path[i+1])
    return curLength

def potential_idea5(problem, path, c): #lijkt te werken, heel erg vergelijkbaar met 4
    result = 0
    for i in range(len(path)):
        min_distance = np.infty
        for j in range(len(path)):
            if j == i or j == i-1 or (i == 0 and j == len(path)-1):
                continue
            if j == len(path)-1:
                distance = problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[0])
            else:
                distance = problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[j+1])
            if min_distance > distance:
                min_distance = distance

        if i == 0:
            result += problem.get_weight(path[i], path[i+1]) + c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) + c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance
        else:
            result += problem.get_weight(path[i], path[i+1]) + c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance
    return result

def potential_idea4(problem, path, c): #Lijkt te werken
    result = 0
    for i in range(len(path)):
        min_distance1 = np.infty
        min_distance2 = np.infty
        for j in range(len(path)):
            if j == i:
                continue
            distance = problem.get_weight(path[i], path[j])
            if min_distance1 > distance:
                min_distance1 = distance
            elif distance < min_distance2 and distance >= min_distance1:
                min_distance2 = distance
        if i == 0:
            result += problem.get_weight(path[i], path[i+1]) + c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/(min_distance1+min_distance2)
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) + c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/(min_distance1+min_distance2)      
        else:
            result += problem.get_weight(path[i], path[i+1]) + c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/(min_distance1+min_distance2)    
    return result

def potential_idea3(problem, path, c): # lijkt te werken, geen logische uitleg (- ook goed??)
    result = 0
    for i in range(len(path)):
        min_distance = np.infty
        for j in range(len(path)):
            if j == i or j == i-1 or (j == len(path)+1 and i == 0):
                continue
            if j == len(path)-1:
                distance = 0.5*(problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[0]))
            else:
                distance = 0.5*(problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[j+1]))
            if distance < min_distance:
                min_distance = distance
        if i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) + c*min_distance
        else:
            result += problem.get_weight(path[i], path[i+1]) + c*min_distance
    return result


def potential_idea2(path): #Werkt niet
    result = 0
    for i in range(len(path)):
        for j in range(len(path)):
            if j == i-1 or j == i+1 or (i == 0 and j == len(path) -1):
                result += np.abs(path[i].x - path[j].x) + np.abs(path[i].y - path[j].y)
    return result

def potential_idea1(path, points): #werkt niet
    n = len(path)
    pot1 = 0
    pot2 = 0
    I = np.zeros([n,n])
    for i in range(n-1):
        for j in range(n-1):
            if path[i+1].id == j:
                pot1 += path[i].dist2(points[j])
            elif i != 0 and path[i-1].id == j:
                pot1 += path[i].dist2(points[j])
            elif i == 0 and path[n-2].id == j:
                pot1 += path[i].dist2(points[j])
            else:
                pot2 -= path[i].dist2(points[j])
    #print(pot1, pot2)
    return pot1 + pot2