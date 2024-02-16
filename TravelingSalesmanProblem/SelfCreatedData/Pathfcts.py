import numpy as np
import random
import matplotlib.pyplot as plt

class Point:
    def __init__(self, id='', x=0, y=0):
        self.x = x
        self.y = y
        self.id = id

	#Distance between two points 
    def dist2(self, other):
        return np.sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))
    
    #Find middle of an edge (two neighbours)
    def mid_point(self, other):
        x = 0.5*self.x + 0.5*other.x
        y = 0.5*self.y + 0.5*other.y
        return Point(str(self.id)+'half', x, y)
    
    #plot point
    def plot(self):
        plt.plot(self.x, self.y, marker='o')

#Calculate the distance of the whole path (Squared Distances between points)
def pathLengthSq(path):
    length = 0
    for i in range(len(path)):
        if i == len(path)-1:
            length += path[i].dist2(path[0])
        else:    
            length += path[i].dist2(path[i+1])
    return length

#Create paths
def createRandomPath(n):
    path =[]
    #points = {}
    tabu = []
    for i in range(n):
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        if [x, y] in tabu:
            continue
        else:
            path.append(Point(i, x, y))
            tabu.append([x, y])
            #points[i] = Point(i, x, y)
    # path.append(path[0])
    return path#, points

def createStartPath():
    #return [Point(), Point(0,1), Point(3,1), Point(3,3), Point(0,3), Point(0,4), Point(3,4), Point(5,3), Point(5,1), Point(3,0), Point()]
    path = [Point(0), Point(1,0,1), Point(2,3,3), Point(3,3,1), Point(4,0,3), Point(5,0,4), Point(6,3,4), Point(7,5,3), Point(8,5,1), Point(9,3,0), Point(0)]
    #points = {0: Point(0), 1: Point(1,0,1), 2: Point(2,3,3), 3: Point(3,3,1), 4: Point(4,0,3), 5: Point(5,0,4), 6: Point(6,3,4), 7: Point(7,5,3), 8 : Point(8,5,1), 9: Point(9,3,0)}
    return path#, points

def createSecondPath():
    return [Point(0), Point(1,0,1), Point(3,5,1), Point(2,5,3), Point(4,0,3), Point(5,0,4), Point(6,5,4), Point(7,7,3), Point(8,7,1), Point(9,5,0), Point(0)]

def createOptimalPath():
    path = [Point(0), Point(1,0,1), Point(4,0,3), Point(5,0,4), Point(6,5,4), Point(2,5,3), Point(7,7,3), Point(8,7,1), Point(3,5,1), Point(9,5,0), Point(0)]
    return path

#Check if paths are equal
def pathsequal(path1, path2):
    if len(path1) != len(path2):
        return False
    for i in range(len(path1)):
        if path1[i].x != path2[i].x:
            return False
        elif path2[i].y != path1[i].y:
            return False
    return True

#Visualize path
def printPath(pathname, path):
    print(pathname, ' =')
    for i in range(len(path)):
        print(path[i].x, path[i].y)
    return 0

def plotPath(path):
    x = []
    y = []
    for point in path:
        x.append(point.x)
        y.append(point.y)
    plt.plot(x, y, 'ob')
    plt.plot(x, y, '-k')
    plt.show()
    return