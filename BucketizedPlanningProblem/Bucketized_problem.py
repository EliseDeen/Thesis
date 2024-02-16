# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 15:10:25 2023

@author: elise
"""

import numpy as np
#from datetime import datetime
#import pandas as pd
import time

TimeConverter = {'s': 1, 'm': 60, 'h': 3600}

""" Objective functions """
def Lateness(steps, S):
    result = 0
    for i in range((len(steps))):
        result += max(0, S[i]+steps[i][1]-steps[i][0])
    return result
    
def Load_per_bucket(steps, S, T, B):
    L = np.zeros([len(steps),B])
    for i in range(len(steps)):
        j1 = int(S[i]/T)
        j2 = int((S[i]+steps[i][1])/T)
        if j1 == j2:
            L[i, j1] = steps[i][1]
        else:
            L[i, j1] = (j1+1)*T - S[i]
            L[i, j2] = S[i] + steps[i][1] - j2*T
            for j in range(j1+1, j2):
                L[i, j] = T
    return L

def max_load(T, B, L):
    result = 0
    for j in range(B):
        result += max(0, sum(L[:,j]) - T)
    return result

def Objective_normal(steps, S, T, B, c):
    L = Load_per_bucket(steps, S, T, B)
    result = c[0]*Lateness(steps, S) + c[1]*max_load(T, B, L)
    return result, L

def Change_normal(steps, S, L, i, t, T, f, c): 
    L2 = L.copy()
    result = f - c[0]*(max(0, S[i] + steps[i][1] - steps[i][0])) + c[0]*(max(0, t + steps[i][1] - steps[i][0]))
    if S[i] <= t:
        J1 = int(S[i]/T)
        J2 = int((t + steps[i][1])/T)
    elif S[i] > t:
        J1 = int(t/T)
        J2 = int((S[i] + steps[i][1])/T)
    for j in range(J1, J2+1):
        result -= c[1]*max(0, sum(L[:, j])-T)
    L2[i, int(S[i]/T)] = 0
    L2[i, int((S[i]+steps[i][1])/T)] = 0
    j1 = int(t/T)
    j2 = int((t+steps[i][1])/T)
    if j1 == j2:
        L2[i, j1] = steps[i][1]
    else:
        L2[i, j1] = (j1+1)*T - t
        L2[i, j2] = t + steps[i][1] - j2*T
        for j in range(j1+1, j2):
            L2[i, j] = T
    for j in range(J1, J2+1):
        result += c[1]*max(0, sum(L2[:, j])-T)
    return result, L2, J1, J2
    

""" Possible changes to the objective """
def Potential(T, B, L):
    result = 0
    for j in range(B):
        result += (sum(L[:,j]))**2
    return result

def Objective_only_Potential(steps, S, T, B, c):
    L = Load_per_bucket(steps, S, T, B)
    return Potential(T, B, L), L

def Objective_Potential(steps, S, T, B, c):
    L = Load_per_bucket(steps, S, T, B)
    return c[0]*Lateness(steps, S) + c[1]*max_load(T, B, L) + c[2]*Potential(T, B, L), L

def Change_only_Potential(steps, S, L, i, t, T, f, c): 
    L2 = L.copy()
    result = f
    if S[i] <= t:
        J1 = int(S[i]/T)
        J2 = int((t + steps[i][1])/T)
    elif S[i] > t:
        J1 = int(t/T)
        J2 = int((S[i] + steps[i][1])/T)
    L2[i, int(S[i]/T)] = 0
    L2[i, int((S[i]+steps[i][1])/T)] = 0
    j1 = int(t/T)
    j2 = int((t+steps[i][1])/T)
    if j1 == j2:
        L2[i, j1] = steps[i][1]
    else:
        L2[i, j1] = (j1+1)*T - t
        L2[i, j2] = t + steps[i][1] - j2*T
        for j in range(j1+1, j2):
            L2[i, j] = T
    for j in range(J1, J2+1):
        result -= c[2]* (sum(L[:, j])**2)
        result += c[2]* (sum(L2[:, j])**2)
    return result, L2, J1, J2

def Change_Potential(steps, S, L, i, t, T, f, c):
    result, L2, J1, J2 = Change_normal(steps, S, L, i, t, T, f, c)
    for j in range(J1, J2+1):
        result -= c[2]* (sum(L[:, j])**2)
        result += c[2]* (sum(L2[:, j])**2)
    return result, L2, J1, J2

def GLS(T, B, L):
    I = 0
    for j in range(B):
        if sum(L[:,j]) >= T:
            I += 1
    return I

def Objective_GLS(steps, S, T, B, c):
    L = Load_per_bucket(steps, S, T, B)
    return c[0]*Lateness(steps, S) + c[1]*max_load(T, B, L) + c[2]*GLS(T, B, L), L

def Objective_only_GLS(steps, S, T, B, c):
    L = Load_per_bucket(steps, S, T, B)
    return c[2]*GLS(T, B, L), L

def Change_GLS(steps, S, L, i, t, T, f, c):
    result, L2, J1, J2 = Change_normal(steps, S, L, i, t, T, f, c)
    for j in range(J1, J2+1):
        s1 = sum(L[:,j])
        s2 = sum(L2[:,j])
        if s1 >= T and s2 < T:
            result -= c[2]
        if s1 < T and s2 >= T:
            result += c[2]
    return result, L2, J1, J2

def Change_only_GLS(steps, S, L, i, t, T, f, c):
    result, L2, J1, J2 = Change_normal(steps, S, L, i, t, T, f, c)
    L2 = L.copy()
    result = f
    if S[i] <= t:
        J1 = int(S[i]/T)
        J2 = int((t + steps[i][1])/T)
    elif S[i] > t:
        J1 = int(t/T)
        J2 = int((S[i] + steps[i][1])/T)
    L2[i, int(S[i]/T)] = 0
    L2[i, int((S[i]+steps[i][1])/T)] = 0
    j1 = int(t/T)
    j2 = int((t+steps[i][1])/T)
    if j1 == j2:
        L2[i, j1] = steps[i][1]
    else:
        L2[i, j1] = (j1+1)*T - t
        L2[i, j2] = t + steps[i][1] - j2*T
        for j in range(j1+1, j2):
            L2[i, j] = T
    for j in range(J1, J2+1):
        s1 = sum(L[:,j])
        s2 = sum(L2[:,j])
        if s1 >= T and s2 < T:
            result -= c[2]
        if s1 < T and s2 >= T:
            result += c[2]
    return result, L2, J1, J2