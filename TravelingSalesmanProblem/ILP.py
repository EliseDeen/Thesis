import numpy as np
import Pathfcts as fcts

#inst = (cities, costs)
def create_ILP(inst):
    try:
        from gurobipy import Model, GRB
    except:
        raise RuntimeError('Gurobi not found')
    
    model = Model('')

    x = model.addVars(len(inst.cities), len(inst.cities), vtype = GRB.BINARY)
    u = model.addVars(len(inst.cities), lb=2, ub=len(inst.cities), vtype = GRB.CONTINUOUS)

    for i in range(len(inst.cities)):
        model.addConstr(x[i,i] == 0)
        model.addConstr(sum(x[j,i] for j in range(len(inst.cities))) == 1)
        model.addConstr(sum(x[i,j] for j in range(len(inst.cities))) == 1)
        for j in range(len(inst.cities)):
            if i != j and i != 0 and j != 0:
                model.addConstr(u[i] - u[j] + 1 <= (len(inst.cities)-1)*(1-x[i,j]))
    c = inst.costs
    model.setObjective(sum(c[i,j]*x[i,j] for i in range(len(inst.cities)) for j in range(len(inst.cities))), GRB.MINIMIZE)

    model.optimize()
    #print(model.objVal)
    
    # for v in model.getVars():
    #     v.Start = v.X

    # model.setObjective(sum(c[i,j]*x[i,j] for i in range(len(inst.cities)) for j in range(len(inst.cities))), GRB.MINIMIZE)
   
    # model.update()
    # model.optimize()
    return model

class problem():
    def __init__(self, cities, costs = None) -> None:
        self.cities = cities
        if costs == None:
            costs = np.zeros([len(cities), len(cities)])
            for i in range(len(cities)):
                for j in range(len(cities)):
                    costs[i,j] = cities[i].dist2(cities[j])
        self.costs = costs

#cities = [(3,10), (8,5), (9,1), (5,1), (5,2), (3,3), (1,0), (2,3), (3,4), (3,10)]
#instance = problem(cities)
#create_ILP(instance)