import numpy as np
import random
import matplotlib.pyplot as plt

def no_potential(problem, path, c, closest):
    curLength = 0
    for i in range(len(path)):
        if i == len(path)-1:
            curLength += problem.get_weight(path[i], path[0])
        else:
            curLength += problem.get_weight(path[i], path[i+1])
    return curLength, closest

def no_potential_change(problem, path, curr_length, x, y, c, closest):
    if x == len(path)-1:
        x2 = 0
    else:
        x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    length = curr_length - problem.get_weight(path[x], path[x2]) - problem.get_weight(path[y], path[y2])
    length += problem.get_weight(path[x], path[y]) + problem.get_weight(path[x2], path[y2])
    return length, closest

def min_dist_inserted_in_edge(problem, path, i, exclude=[]):
    min_distance = np.infty
    closest = [0, np.infty, 0, np.infty]
    for j in range(len(path)):
        if j == i or j == i-1 or (i == 0 and j == len(path)-1) or j in exclude: 
            continue
        if j == len(path)-1:
            dist1 = problem.get_weight(path[i], path[j])
            dist2 = problem.get_weight(path[i], path[0])
            if min_distance > dist1+dist2:
                min_distance = dist1+dist2
                closest = [path[j], dist1, path[0], dist2]
        else:
            dist1 = problem.get_weight(path[i], path[j])
            dist2 = problem.get_weight(path[i], path[j+1])
            if min_distance > dist1+dist2:
                min_distance = dist1+dist2
                closest = [path[j], dist1, path[j+1], dist2]
    return closest

def potential_idea5(problem, path, c, closest): #lijkt te werken, heel erg vergelijkbaar met 4
    result = 0
    closest_edge = {}
    for i in range(len(path)):
        closest_edge[path[i]] = min_dist_inserted_in_edge(problem, path, i)
        min_distance = closest_edge[path[i]][1]+closest_edge[path[i]][3]

        if i == 0:
            result += problem.get_weight(path[i], path[i+1]) #Original objective
            result += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance #Potential KPI
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) #Original objective
            result += c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance #Potential KPI
        else:
            result += problem.get_weight(path[i], path[i+1]) #Original objective
            result += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance #Potential KPI
    return result, closest_edge

def potential_idea5_change(problem, path, curr_length, x, y, c, closest):
    length, closest_edges = no_potential_change(problem, path, curr_length, x, y, c, closest)
    x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1

    for i in range(len(path)):
        if i == x:
            d_plus = problem.get_weight(path[i], path[y])
            d_min = problem.get_weight(path[i], path[i+1])
            if i == 0:
                d_plus += problem.get_weight(path[len(path)-1], path[i])
                d_min += problem.get_weight(path[len(path)-1], path[i])
            else:
                d_plus += problem.get_weight(path[i-1], path[i])
                d_min += problem.get_weight(path[i-1], path[i])
        elif i == x2:
            d_plus = problem.get_weight(path[i], path[y2]) + problem.get_weight(path[i], path[i+1])
            d_min = problem.get_weight(path[i-1], path[i]) + problem.get_weight(path[i], path[i+1])
        elif i == y:
            d_plus = problem.get_weight(path[x], path[i]) + problem.get_weight(path[i-1], path[i])
            d_min = problem.get_weight(path[i-1], path[i])
            if i == len(path)-1:
                d_min += problem.get_weight(path[i], path[0])
            else:
                d_min += problem.get_weight(path[i], path[i+1])
        elif i == y2:
            d_plus = problem.get_weight(path[x2], path[i])
            if i == 0:
                d_plus += problem.get_weight(path[i], path[i+1])
                d_min = problem.get_weight(path[len(path)-1], path[i]) + problem.get_weight(path[i], path[i+1])
            elif i == len(path)-1:
                d_plus += problem.get_weight(path[i], path[0])
                d_min = problem.get_weight(path[i-1], path[i]) + problem.get_weight(path[i], path[0])
            else:
                d_plus += problem.get_weight(path[i], path[i+1])
                d_min = problem.get_weight(path[i-1], path[i]) + problem.get_weight(path[i], path[i+1])
        else:
            if i == 0:
                d_min = problem.get_weight(path[len(path)-1], path[i]) + problem.get_weight(path[i], path[i+1])
                d_plus = d_min
            elif i == len(path)-1:
                d_min = problem.get_weight(path[i-1], path[i]) + problem.get_weight(path[i], path[0])
                d_plus = d_min
            else:
                d_min = problem.get_weight(path[i-1], path[i]) + problem.get_weight(path[i], path[i+1])
                d_plus = d_min
        
        min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
        if ((closest_edges[path[i]][0] == path[x] or closest_edges[path[i]][2] == path[x]) and (closest_edges[path[i]][0] == path[x2] or closest_edges[path[i]][2] == path[x2])) or ((closest_edges[path[i]][0] == path[y] or closest_edges[path[i]][2] == path[y]) and (closest_edges[path[i]][0] == path[y2] or closest_edges[path[i]][2] == path[y2])):
            closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
        dist1 = problem.get_weight(path[i], path[x])
        dist2 = problem.get_weight(path[i], path[y])
        if closest_edges[path[i]][1]+closest_edges[path[i]][3] > dist1+dist2 and path[i] != path[x] and path[i] != path[y]:
            closest_edges[path[i]] = [path[x], dist1, path[y], dist2]
        dist1 = problem.get_weight(path[i], path[x2])
        dist2 = problem.get_weight(path[i], path[y2])
        if closest_edges[path[i]][1]+closest_edges[path[i]][3] > dist1+dist2 and path[i] != path[x2] and path[i] != path[y2]:
            closest_edges[path[i]] = [path[x2], dist1, path[y2], dist2]

        length -= c*d_min/min_distance_old
        length += c*d_plus/(closest_edges[path[i]][1]+closest_edges[path[i]][3])










        '''
        if i == x:
            min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
            if (closest_edges[path[i]][0] == path[y] or closest_edges[path[i]][2] == path[y]) and (closest_edges[path[i]][2] == path[y2] or closest_edges[path[i]][0] == path[y2]):
                min_distance, closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
                dist1 = problem.get_weight(path[i], path[x2])
                dist2 = problem.get_weight(path[i], path[y2])
                if min_distance > dist1+dist2:
                    min_distance = dist1+dist2
                    closest_edges[path[i]] = [path[x2], dist1, path[y2], dist2]
            else:
                min_distance = min_distance_old
            if i == 0:
                length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance_old
                length += c*(problem.get_weight(path[i], path[y])+problem.get_weight(path[len(path)-1], path[i]))/min_distance 
            else:
                length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance_old 
                length += c*(problem.get_weight(path[i], path[y])+problem.get_weight(path[i-1], path[i]))/min_distance 

        elif i == x2:
            min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
            if (closest_edges[path[i]][0] == path[y] or closest_edges[path[i]][2] == path[y]) and (closest_edges[path[i]][2] == path[y2] or closest_edges[path[i]][0] == path[y2]):
                min_distance, closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
                dist1 = problem.get_weight(path[i], path[x])
                dist2 = problem.get_weight(path[i], path[y])
                if min_distance > dist1+dist2:
                    min_distance = dist1+dist2
                    closest_edges[path[i]] = [path[x], dist1, path[y], dist2]
            else:
                min_distance = min_distance_old
            length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance_old 
            length += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[y2], path[i]))/min_distance 

        elif i == y:
            min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
            if (closest_edges[path[i]][0] == path[x] or closest_edges[path[i]][2] == path[x]) and (closest_edges[path[i]][2] == path[x2] or closest_edges[path[i]][0] == path[x2]):
                min_distance, closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
                dist1 = problem.get_weight(path[i], path[x2])
                dist2 = problem.get_weight(path[i], path[y2])
                if min_distance > dist1+dist2:
                    min_distance = dist1+dist2
                    closest_edges[path[i]] = [path[x2], dist1, path[y2], dist2]
            else:
                min_distance = min_distance_old
            if i == len(path)-1:
                length -= c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance_old
                length += c*(problem.get_weight(path[i], path[x])+problem.get_weight(path[i-1], path[i]))/min_distance 
            else:
                length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance_old 
                length += c*(problem.get_weight(path[i], path[x])+problem.get_weight(path[i-1], path[i]))/min_distance 

        elif i == y2:
            min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
            if (closest_edges[path[i]][0] == path[x] or closest_edges[path[i]][2] == path[x]) and (closest_edges[path[i]][2] == path[x2] or closest_edges[path[i]][0] == path[x2]):
                min_distance, closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
                dist1 = problem.get_weight(path[i], path[x])
                dist2 = problem.get_weight(path[i], path[y])
                if min_distance > dist1+dist2:
                    min_distance = dist1+dist2
                    closest_edges[path[i]] = [path[x], dist1, path[y], dist2]
            else:
                min_distance = min_distance_old
            if i == len(path)-1:
                length -= c*(problem.get_weight(path[i-1], path[i])+problem.get_weight(path[i], path[0]))/min_distance_old
                length += c*(problem.get_weight(path[x2], path[i])+problem.get_weight(path[i], path[0]))/min_distance 
            elif i == 0:
                length -= c*(problem.get_weight(path[len(path)-1], path[i])+problem.get_weight(path[i], path[i+1]))/min_distance_old
                length += c*(problem.get_weight(path[x2], path[i])+problem.get_weight(path[i], path[i+1]))/min_distance 
            else:
                length -= c*(problem.get_weight(path[i-1], path[i])+problem.get_weight(path[i], path[i+1]))/min_distance_old 
                length += c*(problem.get_weight(path[x2], path[i])+problem.get_weight(path[i], path[i+1]))/min_distance 

        else:
            min_distance_old = closest_edges[path[i]][1]+closest_edges[path[i]][3]
            change = False
            if ((closest_edges[path[i]][0] == path[x] or closest_edges[path[i]][2] == path[x]) and (closest_edges[path[i]][2] == path[x2] or closest_edges[path[i]][0] == path[x2])) or ((closest_edges[path[i]][0] == path[y] or closest_edges[path[i]][2] == path[y]) and (closest_edges[path[i]][2] == path[y2] or closest_edges[path[i]][0] == path[y2])):
                min_distance, closest_edges[path[i]] = min_dist_inserted_in_edge(problem, path, i, [x,y])
                change = True
            dist1 = problem.get_weight(path[i], path[x])
            dist2 = problem.get_weight(path[i], path[y])
            if closest_edges[path[i]][1]+closest_edges[path[i]][3] > dist1+dist2:
                closest_edges[path[i]] = [path[x], dist1, path[y], dist2]
                change = True
            dist1 = problem.get_weight(path[i], path[x2])
            dist2 = problem.get_weight(path[i], path[y2])
            if closest_edges[path[i]][1]+closest_edges[path[i]][3] > dist1+dist2:
                closest_edges[path[i]] = [path[x2], dist1, path[y2], dist2]
                change = True
            
            if not change:
                continue
            elif i == 0:
                length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance_old
                length += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance 
            elif i == len(path)-1:
                length -= c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance_old 
                length += c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance 
            else:
                length -= c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance_old
                length += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance
    '''
    return length, closest_edges

def potential_idea4(problem, path, c, closest): #Lijkt te werken
    result = 0
    for i in range(len(path)):
        if i == 0:
            result += problem.get_weight(path[i], path[i+1]) #original objective
            result += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/(closest[path[i]][1]+closest[path[i]][3]) #Potential KPI
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) #original objective
            result += c*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/(closest[path[i]][1]+closest[path[i]][3]) #Potential KPI   
        else:
            result += problem.get_weight(path[i], path[i+1]) #original objective
            result += c*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/(closest[path[i]][1]+closest[path[i]][3]) #Potential KPI
    return result, closest

def potential_idea4_change(problem, path, curr_length, x, y, c, closest):
    length, closest = no_potential_change(problem, path, curr_length, x, y, c, closest)
    if x == len(path)-1:
        x2 = 0
    else:
        x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    length = length - c*(problem.get_weight(path[x], path[x2])/(closest[path[x]][1]+closest[path[x]][3]) 
                         + problem.get_weight(path[y], path[y2])/(closest[path[y]][1]+closest[path[y]][3]) 
                         + problem.get_weight(path[x], path[x2])/(closest[path[x2]][1]+closest[path[x2]][3]) 
                         + problem.get_weight(path[y], path[y2])/(closest[path[y2]][1]+closest[path[y2]][3]))
    length = length + c*(problem.get_weight(path[x], path[y])/(closest[path[x]][1]+closest[path[x]][3]) 
                         + problem.get_weight(path[x2], path[y2])/(closest[path[x2]][1]+closest[path[x2]][3]) 
                         + problem.get_weight(path[x], path[y])/(closest[path[y]][1]+closest[path[y]][3]) 
                         + problem.get_weight(path[x2], path[y2])/(closest[path[y2]][1]+closest[path[y2]][3]))
    return length, closest

def det_min_dist_to_edge(problem, path, i, exclude=[]):
    closest_edge = [0, 0, np.infty]
    for j in range(len(path)):
        if j == i or j == i-1 or (j == len(path)-1 and i == 0) or j in exclude:
            continue
        if j == len(path)-1:
            distance = 0.5*(problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[0]))            
            if distance < closest_edge[2]:
                closest_edge = [path[j], path[0], distance]
        else:
            distance = 0.5*(problem.get_weight(path[i], path[j]) + problem.get_weight(path[i], path[j+1]))            
            if distance < closest_edge[2]:
                closest_edge = [path[j], path[j+1], distance]
    return closest_edge

def potential_idea3(problem, path, c, closest): # lijkt te werken, geen logische uitleg (- ook goed??)
    result = 0
    closest_edge = {}
    for i in range(len(path)):
        closest_edge[path[i]] = det_min_dist_to_edge(problem, path, i)
        if i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) + c*closest_edge[path[i]][2]
        else:
            result += problem.get_weight(path[i], path[i+1]) + c*closest_edge[path[i]][2]
    return result, closest_edge

def potential_idea3_change(problem, path, curr_length, x, y, c, closest):
    length, closest_edge = no_potential_change(problem, path, curr_length, x, y, c, closest)
    x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    for i in range(len(path)):
        if ((closest_edge[path[i]][0] == path[x] or closest_edge[path[i]][1] == path[x]) and (closest_edge[path[i]][0] == path[x2] or closest_edge[path[i]][1] == path[x2])) or ((closest_edge[path[i]][0] == path[y] or closest_edge[path[i]][1] == path[y]) and (closest_edge[path[i]][0] == path[y2] or closest_edge[path[i]][1] == path[y2])):
            length -= c*closest_edge[path[i]][2]
            closest_edge[path[i]] = det_min_dist_to_edge(problem, path, i, [x,y])
            length += c*closest_edge[path[i]][2]
        dist = 0.5*(problem.get_weight(path[i], path[x]) + problem.get_weight(path[i], path[y]))
        if closest_edge[path[i]][2] > dist and path[i] != path[x] and path[i] != path[y]:
            length -= c*closest_edge[path[i]][2]
            closest_edge[path[i]] = [path[x], path[y], dist]
            length += c*closest_edge[path[i]][2]
        dist = 0.5*(problem.get_weight(path[i], path[x2]) + problem.get_weight(path[i], path[y2]))
        if closest_edge[path[i]][2] > dist and path[i] != path[x2] and path[i] != path[y2]:
            length -= c*closest_edge[path[i]][2]
            closest_edge[path[i]] = [path[x2], path[y2], dist]
            length += c*closest_edge[path[i]][2]
    return length, closest_edge

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