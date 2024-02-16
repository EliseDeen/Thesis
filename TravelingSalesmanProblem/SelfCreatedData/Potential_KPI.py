import numpy as np
import random
import matplotlib.pyplot as plt
import Pathfcts as fcts
import two_opt as opt

def no_pot(path):
    return 0

def potential_idea5(path): #lijkt te werken, heel erg vergelijkbaar met 4
    result = 0
    min_info = {}
    for i in range(len(path)):
        id = path[i].id
        min_dist = np.infty
        for j in range(len(path)):
            if j == i or j == i-1 or (i == 0 and j == len(path)-1):
                continue
            if j == len(path)-1:
                dist = path[i].dist2(path[j])+path[i].dist2(path[0])
            else:
                dist = path[i].dist2(path[j])+path[i].dist2(path[j+1])
            if min_dist > dist:
                min_dist = dist
                min_info[id] = [j,dist]
        if i == 0:
            result += (path[i].dist2(path[i+1])+path[len(path)-1].dist2(path[i]))/min_dist 
        elif i == len(path)-1:
            result += (path[i].dist2(path[0])+path[i-1].dist2(path[i]))/min_dist         
        else:
            result += (path[i].dist2(path[i+1])+path[i-1].dist2(path[i]))/min_dist
    return result#, min_info

def change_potential_idea5(curr_length, min_info, path, i, j): #klopt niet!!
    length = curr_length
    new_min_info = min_info
    new_path = opt.do2Opt(path, i, j)
    for k in range(len(path)):
        id = path[k].id
        d_1 = path[k].dist2(path[i])+path[k].dist2(path[j])
        d_2 = path[k].dist2(path[i+1])+path[k].dist2(path[j+1])
        if min_info[id][0] == i or min_info[id][0] == j:            
            for l in range(len(new_path)-1):
                if new_path[l].id == id or new_path[l].id == path[k-1].id:
                    continue
                dist = path[k].dist2(new_path[l])+path[k].dist2(new_path[l+1])
                if new_min_info[id][1] > dist:
                    new_min_info[id] = [l,dist]
        elif min_info[id][1] > d_1:
            min_info[id] = [i, d_1]
        elif min_info[id][1] > d_2 and d_1 > d_2:
            min_info[id] = [i+1, d_2]
        if k == 0:
            length -= (path[k].dist2(path[k+1])+path[len(path)-1].dist2(path[k]))/min_info[id][1]
        else:
            length -= (path[k].dist2(path[k+1])+path[len(path)-1].dist2(path[k]))/min_info[id][1]
        if new_path[k] == id:
            length += (new_path[k].dist2(new_path[k+1])+new_path[len(new_path)-1].dist2(new_path[k]))/new_min_info[id][1]
        else:
            length += (new_path[k].dist2(new_path[k+1])+new_path[k-1].dist2(new_path[k]))/new_min_info[id][1]
        return length

def potential_idea4(path): #Lijkt te werken
    result = 0
    for i in range(len(path)):
        min_dist1 = np.infty
        min_dist2 = np.infty
        for j in range(len(path)):
            if j == i:
                continue
            dist = path[i].dist2(path[j])
            if min_dist1 > dist:
                min_dist1 = dist
            elif dist<min_dist2 and dist>=min_dist1:
                min_dist2 = dist
        if i == 0:
            result += (path[i].dist2(path[i+1])+path[len(path)-1].dist2(path[i]))/(min_dist1+min_dist2)
        elif i == len(path)-1:
            result += (path[i].dist2(path[0])+path[i-1].dist2(path[i]))/(min_dist1+min_dist2)            
        else:
            result += (path[i].dist2(path[i+1])+path[i-1].dist2(path[i]))/(min_dist1+min_dist2)
    return result

def potential_idea3(path): # lijkt te werken, geen logische uitleg (- ook goed??)
    result = 0
    for i in range(len(path)):
        min_dis = np.infty
        for j in range(len(path)):
            if j == i or j == i-1 or (j == len(path)-1 and i == 0):
                continue
            if j == len(path)-1:
                mid_point = path[j].mid_point(path[0])
            else:
                mid_point = path[j].mid_point(path[j+1])
            dis = path[i].dist2(mid_point)
            if dis < min_dis:
                min_dis = dis
        result += min_dis
    return result

def change_potential_idea3(curr_length, min_info, path, i, j):
    length = curr_length


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