#author: Candra Mulyadhi (1920996)
#date: 11/10/2021

## the path between cities is abbreviated as "p"
## the total distance of a path is abbreviated as "d"

import random
import numpy as np
import copy
import math



TEMPERATURE = 100
EPSILON = 0.01



def generateRandomProbability():
    return random.random()

def generateRandomDistance():
    return random.randrange(1, 1000)

def initiateMap(amountCities):

    # 2D Array of map
    map = np.array([[0 for x in range(amountCities)] for y in range(amountCities)])

    for i in range(0,amountCities):
        for j in range(0,amountCities):
            if i == j:
                map[i][j] = 0
            elif i < j:
                distance = generateRandomDistance()
                map[i][j] = distance
                map[j][i] = distance

    return map

def createRandomPath(map):
    path = np.array([i for i in range(0, len(map))])
    return shuffle(path)



def exp(exponent):
    return math.pow(math.e, exponent)

def shuffle(path):
    np.random.shuffle(path)
    return path

def calculateDistance(map, path):

    distance = 0

    for i in range(0,len(path)):
        if i < len(path)-1:
            distance += map[path[i]][path[i + 1]]

    return distance

def swapRandomNeighbors(path):

    p = copy.copy(path)
    idx = random.randrange(0, len(p)-1)

    p[idx], p[idx+1] = p[idx+1], p[idx]

    return p



def findOptimalPath(map):

    global TEMPERATURE
    global EPSILON

    p = createRandomPath(map)
    d = calculateDistance(map, p)

    while TEMPERATURE > EPSILON:

        randomProbability = generateRandomProbability()
        p2 = swapRandomNeighbors(p)
        d2 = calculateDistance(map, p2)

        if d2 < d:
            p = p2
            d = d2

        elif randomProbability > exp(-(d2-d)/TEMPERATURE):
            p = p2
            d = d2

        TEMPERATURE = TEMPERATURE - EPSILON

    return p

def findMinimum(map, reruns):

    p = findOptimalPath(map)
    d = calculateDistance(map, p)

    print("\nDistance: ", d)
    print("Path: ", p, "\n")

    for i in range(0, reruns):
        p2 = findOptimalPath(map)
        d2 = calculateDistance(map, p2)
        if d2 < d:
            print("\nRerun: ", i + 1)
            d = d2
            p = p2

            print("\n Distance: ", d, "\n", "Path: ", p)

    print("\n\n\nFinal result: \n\n Distance: ", d, "\n Path: ", p)



if __name__ == '__main__':
    map = initiateMap(100)
    findMinimum(map,100)
