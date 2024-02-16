import numpy as np

#inst = (steps, T, B)
def create_ILP(inst, w, limit):
    try:
        from gurobipy import Model, GRB
    except:
        raise RuntimeError('Gurobi not found')
    
    model = Model('')

    #Variables
    x = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)
    y = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)
    z00 = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)
    z10 = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)
    z01 = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)
    z11 = model.addVars(len(inst.steps), inst.B, vtype = GRB.BINARY)

    s = model.addVars(len(inst.steps), lb = 0, ub = inst.B*inst.T, vtype = GRB.CONTINUOUS)
    c1 = model.addVars(len(inst.steps), inst.B, vtype = GRB.CONTINUOUS)
    c2 = model.addVars(len(inst.steps), inst.B, vtype = GRB.CONTINUOUS)
    
    b1 = model.addVars(len(inst.steps), inst.B, vtype = GRB.CONTINUOUS)
    b2 = model.addVars(len(inst.steps), inst.B, vtype = GRB.CONTINUOUS)

    r1 = model.addVars(len(inst.steps), vtype = GRB.CONTINUOUS)
    r2 = model.addVars(inst.B, vtype = GRB.CONTINUOUS)

    #Constant
    M = 100*inst.B*inst.T

    #Constraints
    
    for i in range(len(inst.steps)):
        xsum = 0
        ysum = 0
        for j in range(inst.B):
            
            model.addConstr(s[i] >= inst.T*j - M*(1-x[i,j]))
            model.addConstr(s[i] <= inst.T*(j+1) + M*(1-x[i,j]))
            model.addConstr(s[i]+inst.steps[i][1] >= inst.T*j - M*(1-y[i,j]))
            model.addConstr(s[i]+inst.steps[i][1] <= inst.T*(j+1) + M*(1-y[i,j]))
            
            model.addConstr(z11[i,j] >= x[i,j]+y[i,j]-1)
            model.addConstr(z11[i,j] <= x[i,j])
            model.addConstr(z11[i,j] <= y[i,j])
            model.addConstr(z10[i,j] >= x[i,j]-y[i,j])
            model.addConstr(z10[i,j] <= x[i,j])
            model.addConstr(z10[i,j] <= 1-y[i,j])
            model.addConstr(z01[i,j] >= y[i,j]-x[i,j])
            model.addConstr(z01[i,j] <= 1-x[i,j])
            model.addConstr(z01[i,j] <= y[i,j])
            
            jcount1 = 0
            jcount2 = 0
            for j2 in range(inst.B):
                if j2 < j:
                    jcount1 += x[i,j2]
                elif j2 > j:
                    jcount2 += y[i,j2] 
            model.addConstr(z00[i,j] >= jcount1+jcount2-1)
            model.addConstr(z00[i,j] <= jcount1)
            model.addConstr(z00[i,j] <= jcount2) 
            
            model.addConstr(c1[i,j] <= inst.T*inst.B * z10[i,j])
            model.addConstr(c1[i,j] <= b1[i,j])
            model.addConstr(c1[i,j] >= b1[i,j] - (1-z10[i,j])*inst.T*inst.B)
            model.addConstr(c2[i,j] <= inst.T*inst.B * z01[i,j])
            model.addConstr(c2[i,j] <= b2[i,j])
            model.addConstr(c2[i,j] >= b2[i,j] - (1-z01[i,j])*inst.T*inst.B)
            
            model.addConstr(b1[i,j] >= 0)
            model.addConstr(b1[i,j] >= inst.T*(j+1) - s[i])
            model.addConstr(b2[i,j] >= 0)
            model.addConstr(b2[i,j] >= s[i] + inst.steps[i][1] - inst.T*j)
            
            xsum += x[i,j]
            ysum += y[i,j]

        model.addConstr(xsum == 1)
        model.addConstr(ysum == 1)

        model.addConstr(r1[i] >= 0)
        model.addConstr(r1[i] >= s[i]+inst.steps[i][1]- inst.steps[i][0])

    for j in range(inst.B):
        L = 0
        for i in range(len(inst.steps)):
            L += inst.steps[i][1]*z11[i,j] + c1[i,j] + c2[i,j] + inst.T*z00[i,j]
        model.addConstr(r2[j] >= 0)
        model.addConstr(r2[j] >= L - inst.T)
    
    #Objective
    model.setObjective(w[0]*sum(r1[i] for i in range(len(inst.steps))) + w[1]*sum(r2[j] for j in range(inst.B)), GRB.MINIMIZE)
    
    model.setParam('TimeLimit', limit)
    model.optimize() #verbose=0

    # for v in model.getVars():
    #     v.Start = v.X

    # model.setObjective(w[0]*sum(r1[i] for i in range(len(inst.steps))) + w[1]*sum(r2[j] for j in range(inst.B)), GRB.MINIMIZE)
    
    # model.update()
    # model.optimize()

    return model

class problem():
    def __init__(self, T, B, steps) -> None:
        self.T = T
        self.B = B
        self.steps = steps


# w = [0.1, 1000] #Weights of the objective functions
# T = 15 
# B = 7 #Number of bucketsstart_time0
# steps = 20 * [[0, 5]]
# instance = problem(T, B, steps)
# create_ILP(instance, w)