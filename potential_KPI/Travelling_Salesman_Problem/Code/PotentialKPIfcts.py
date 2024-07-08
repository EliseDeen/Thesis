import numpy as np
import Algorithms as alg

def no_potential(problem, path, weight, closest):
    curLength = 0
    for i in range(len(path)):
        if i == len(path)-1:
            curLength += problem.get_weight(path[i], path[0])
        else:
            curLength += problem.get_weight(path[i], path[i+1])
    return curLength, closest

def no_potential_change(problem, path, curr_length, x, y, weight, closest):
    x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    length = curr_length - problem.get_weight(path[x], path[x2]) - problem.get_weight(path[y], path[y2])
    length += problem.get_weight(path[x], path[y]) + problem.get_weight(path[x2], path[y2])
    return length, closest

def random_fct(problem, path, weight, closest):
    result = 0
    for i in range(len(path)):
        if i == len(path)-1:
            result += problem.get_weight(path[i], path[0])
            result += weight*(closest[i][0]*closest[0][0]*problem.get_weight(path[i], path[0])+closest[i][1]*closest[0][1])
        else:
            result += problem.get_weight(path[i], path[i+1])
            result += weight*(closest[i][0]*closest[i+1][0]*problem.get_weight(path[i], path[i+1])+closest[i][1]*closest[i+1][1])
    return result, closest

def random_fct_change(problem, path, curr_length, x, y, weight, values):
    new_path = alg.do2Opt(path, x, y)
    length, closest = random_fct(problem, new_path, weight, values)
    return length, closest  

def min_dist_inserted_in_edge(problem, path, i, exclude=[]):
    closest = [0, np.infty, 0, np.infty]
    for j in range(len(path)):
        if j == i or j == i-1 or (i == 0 and j == len(path)-1) or j in exclude: 
            continue
        if j == len(path)-1:
            dist1 = problem.get_weight(path[i], path[j])
            dist2 = problem.get_weight(path[i], path[0])
            if closest[1]+closest[3] > dist1+dist2:
                closest = [path[j], dist1, path[0], dist2]
        else:
            dist1 = problem.get_weight(path[i], path[j])
            dist2 = problem.get_weight(path[i], path[j+1])
            if closest[1]+closest[3] > dist1+dist2:
                closest = [path[j], dist1, path[j+1], dist2]
    return closest

def potential_idea5(problem, path, weight, closest):
    result = 0
    closest_edge = {}
    for i in range(len(path)):
        closest_edge[path[i]] = min_dist_inserted_in_edge(problem, path, i)
        min_distance = closest_edge[path[i]][1]+closest_edge[path[i]][3]

        if i == 0:
            result += problem.get_weight(path[i], path[i+1])
            result += weight*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/min_distance
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0])
            result += weight*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/min_distance
        else:
            result += problem.get_weight(path[i], path[i+1])
            result += weight*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/min_distance
    return result, closest_edge

def potential_idea5_change(problem, path, curr_length, x, y, weight, closest):
    length, closest = no_potential_change(problem, path, curr_length, x, y, weight, closest)
    closest_edges = closest.copy()
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

        length -= weight*d_min/min_distance_old
        length += weight*d_plus/(closest_edges[path[i]][1]+closest_edges[path[i]][3])
    return length, closest_edges

def potential_idea4(problem, path, weight, closest):
    result = 0
    for i in range(len(path)):
        if i == 0:
            result += problem.get_weight(path[i], path[i+1]) #original objective
            result += weight*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[len(path)-1], path[i]))/(closest[str(path[i])][1]+closest[str(path[i])][3]) #Potential KPI
        elif i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) #original objective
            result += weight*(problem.get_weight(path[i], path[0])+problem.get_weight(path[i-1], path[i]))/(closest[str(path[i])][1]+closest[str(path[i])][3]) #Potential KPI   
        else:
            result += problem.get_weight(path[i], path[i+1]) #original objective
            result += weight*(problem.get_weight(path[i], path[i+1])+problem.get_weight(path[i-1], path[i]))/(closest[str(path[i])][1]+closest[str(path[i])][3]) #Potential KPI
    return result, closest

def potential_idea4_change(problem, path, curr_length, x, y, weight, closest):
    length, closest = no_potential_change(problem, path, curr_length, x, y, weight, closest)
    if x == len(path)-1:
        x2 = 0
    else:
        x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    length = length - weight*(problem.get_weight(path[x], path[x2])/(closest[str(path[x])][1]+closest[str(path[x])][3]) 
                         + problem.get_weight(path[y], path[y2])/(closest[str(path[y])][1]+closest[str(path[y])][3]) 
                         + problem.get_weight(path[x], path[x2])/(closest[str(path[x2])][1]+closest[str(path[x2])][3]) 
                         + problem.get_weight(path[y], path[y2])/(closest[str(path[y2])][1]+closest[str(path[y2])][3]))
    length = length + weight*(problem.get_weight(path[x], path[y])/(closest[str(path[x])][1]+closest[str(path[x])][3]) 
                         + problem.get_weight(path[x2], path[y2])/(closest[str(path[x2])][1]+closest[str(path[x2])][3]) 
                         + problem.get_weight(path[x], path[y])/(closest[str(path[y])][1]+closest[str(path[y])][3]) 
                         + problem.get_weight(path[x2], path[y2])/(closest[str(path[y2])][1]+closest[str(path[y2])][3]))
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

def potential_idea3(problem, path, weight, closest):
    result = 0
    closest_edge = {}
    for i in range(len(path)):
        closest_edge[path[i]] = det_min_dist_to_edge(problem, path, i)
        if i == len(path)-1:
            result += problem.get_weight(path[i], path[0]) + weight*closest_edge[path[i]][2]
        else:
            result += problem.get_weight(path[i], path[i+1]) + weight*closest_edge[path[i]][2]
    return result, closest_edge

def potential_idea3_change(problem, path, curr_length, x, y, weight, closest):
    length, closest = no_potential_change(problem, path, curr_length, x, y, weight, closest)
    closest_edge = closest.copy()
    x2 = x+1
    if y == len(path)-1:
        y2 = 0
    else:
        y2 = y+1
    for i in range(len(path)):
        if ((closest_edge[path[i]][0] == path[x] or closest_edge[path[i]][1] == path[x]) and (closest_edge[path[i]][0] == path[x2] or closest_edge[path[i]][1] == path[x2])) or ((closest_edge[path[i]][0] == path[y] or closest_edge[path[i]][1] == path[y]) and (closest_edge[path[i]][0] == path[y2] or closest_edge[path[i]][1] == path[y2])):
            length -= weight*closest_edge[path[i]][2]
            closest_edge[path[i]] = det_min_dist_to_edge(problem, path, i, [x,y])
            length += weight*closest_edge[path[i]][2]
        dist = 0.5*(problem.get_weight(path[i], path[x]) + problem.get_weight(path[i], path[y]))
        if closest_edge[path[i]][2] > dist and path[i] != path[x] and path[i] != path[y]:
            length -= weight*closest_edge[path[i]][2]
            closest_edge[path[i]] = [path[x], path[y], dist]
            length += weight*closest_edge[path[i]][2]
        dist = 0.5*(problem.get_weight(path[i], path[x2]) + problem.get_weight(path[i], path[y2]))
        if closest_edge[path[i]][2] > dist and path[i] != path[x2] and path[i] != path[y2]:
            length -= weight*closest_edge[path[i]][2]
            closest_edge[path[i]] = [path[x2], path[y2], dist]
            length += weight*closest_edge[path[i]][2]
    return length, closest_edge