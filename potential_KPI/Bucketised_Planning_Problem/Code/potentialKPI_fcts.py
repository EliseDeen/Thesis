import numpy as np
import json

""" Information to help understand the functions: """
# S = solution for BPP, i.e., start times
# tasks[i][0] = due date of task i
# tasks[i][1] = process time of task i
# tasks[i][2] = weight for random fct
# L = load
# T = capacity of a bucket
# B = number of buckets

""" Objective functions """
def Lateness(tasks, S):
    result = 0
    for i in range((len(tasks))):
        result += max(0, S[i]+tasks[i][1]-tasks[i][0]) 
    return result

def Load_per_bucket(tasks, S, T, B):
    L = np.zeros([len(tasks),B])
    for i in range(len(tasks)):
        # Determine in which buckets taks i is processed
        start_bucket = int(S[i]/T)
        end_bucket = int((S[i]+tasks[i][1])/T)

        # Determine load
        if start_bucket == end_bucket: #task starts and ends in same bucket
            L[i, start_bucket] = tasks[i][1]
        else: #task doesnot start and end in same bucket
            L[i, start_bucket] = (start_bucket+1)*T - S[i]
            L[i, end_bucket] = S[i] + tasks[i][1] - end_bucket*T
            for j in range(start_bucket+1, end_bucket): #load in buckets between start and end bucket
                L[i, j] = T
    return L

def Overload(T, B, L):
    result = 0
    for j in range(B):
        result += max(0, sum(L[:,j]) - T)
    return result

def Objective_normal(tasks, S, T, B, weight):
    L = Load_per_bucket(tasks, S, T, B)
    result = weight[0]*Lateness(tasks, S) + weight[1]*Overload(T, B, L)
    return result, L

def Change_normal(tasks, S, L, i, t, T, f, weight): #Calculate changed objective value when one task is moved
    L_new = L.copy()
    # Change in Lateness objective
    result = f - weight[0]*(max(0, S[i] + tasks[i][1] - tasks[i][0])) + weight[0]*(max(0, t + tasks[i][1] - tasks[i][0]))
    
    # Determine in which buckets the overload changes
    if S[i] <= t:
        bucket1 = int(S[i]/T)
        bucket2 = int((t + tasks[i][1])/T)
    elif S[i] > t:
        bucket1 = int(t/T)
        bucket2 = int((S[i] + tasks[i][1])/T)
    for j in range(bucket1, bucket2+1):
        if j > len(L[0])-1:
            continue
        result -= weight[1]*max(0, sum(L[:, j])-T)

    L_new[i, int(S[i]/T)] = 0
    if int((S[i]+tasks[i][1])/T) < len(L[0]):
        L_new[i, int((S[i]+tasks[i][1])/T)] = 0

    # Determine new load
    start_bucket = int(t/T)
    end_bucket = int((t+tasks[i][1])/T)
    if start_bucket == end_bucket:
        L_new[i, start_bucket] = tasks[i][1]
    else:
        L_new[i, start_bucket] = (start_bucket+1)*T - t
        if end_bucket < len(L[0]):
            L_new[i, end_bucket] = t + tasks[i][1] - end_bucket*T
        for j in range(start_bucket+1, end_bucket):
            L_new[i, j] = T

    # Determine new overload
    for j in range(bucket1, bucket2+1):
        if j < len(L[0]):
            result += weight[1]*max(0, sum(L_new[:, j])-T)

    return result, L_new, bucket1, bucket2

""" Possible potential KPI functions """
def SquaredLoad(B, L):
    result = 0
    for j in range(B):
        if j < len(L):
            result += (sum(L[:,j]))**2
    return result

def Objective_SquaredLoad(tasks, S, T, B, weight):
    L = Load_per_bucket(tasks, S, T, B)
    return weight[0]*Lateness(tasks, S) + weight[1]*Overload(T, B, L) + weight[2]*SquaredLoad(T, B, L), L

def Change_SquaredLoad(tasks, S, L, i, t, T, f, weight):
    result, L_new, bucket1, bucket2 = Change_normal(tasks, S, L, i, t, T, f, weight)
    for j in range(bucket1, bucket2+1):
        if j < len(L[0]):
            result -= weight[2]* (sum(L[:, j])**2)
        if j < len(L_new[0]):
            result += weight[2]* (sum(L_new[:, j])**2)
    return result, L_new, bucket1, bucket2

def Random_fct(tasks, S):
    result = 0
    for i in range(len(tasks)):
        result += tasks[i][2]*S[i]
    return result

def Objective_Random(tasks, S, T, B, weight):
    L = Load_per_bucket(tasks, S, T, B)
    return weight[0]*Lateness(tasks, S) + weight[1]*Overload(T, B, L) + weight[2]*Random_fct(tasks, S), L

def Change_Random(tasks, S, L, i, t, T, f, weight): 
    result, L_new, bucket1, bucket2 = Change_normal(tasks, S, L, i, t, T, f, weight)
    result += weight[2]*tasks[i][2]*t - weight[2]*tasks[i][2]*S[i]
    return result, L_new, bucket1, bucket2

def GLS(T, B, L):
    I = 0
    for j in range(B):
        if sum(L[:,j]) >= T:
            I += 1
    return I

def Objective_GLS(tasks, S, T, B, weight):
    L = Load_per_bucket(tasks, S, T, B)
    return weight[0]*Lateness(tasks, S) + weight[1]*Overload(T, B, L) + weight[2]*GLS(T, B, L), L

def Change_GLS(tasks, S, L, i, t, T, f, weight):
    result, L_new, bucket1, bucket2 = Change_normal(tasks, S, L, i, t, T, f, weight)
    for j in range(bucket1, bucket2+1):
        s1 = sum(L[:,j])
        s2 = sum(L_new[:,j])
        if s1 >= T and s2 < T:
            result -= weight[2]
        if s1 < T and s2 >= T:
            result += weight[2]
    return result, L_new, bucket1, bucket2