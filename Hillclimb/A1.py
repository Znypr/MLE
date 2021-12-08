'''
author: Candra Mulyadhi (1920996)
date: 08/12/2021

the path between cities is abbreviated as "p"
the total distance of a path is abbreviated as "d"

EDIT: swapRandomNeighbors => swapRandomCities
two random, non-equal cities will be swapped in the path
'''
import copy
import random

import numpy as np


def generateRandomDistance ():
    return random.randrange(1, 1000)


def initiateMap (amountCities):
    # 2D Array of map
    map = np.array(
        [[0 for x in range(amountCities)] for y in
         range(amountCities)]
    )

    for i in range(0, amountCities):
        for j in range(0, amountCities):
            if i == j:
                map[i][j] = 0
            elif i < j:
                distance = generateRandomDistance()
                map[i][j] = distance
                map[j][i] = distance

    return map


def createRandomPath (map):
    path = np.array([i for i in range(0, len(map))])
    return shuffle(path)


def shuffle (path):
    np.random.shuffle(path)
    return path


def calculateDistance (map, path):
    distance = 0

    for i in range(0, len(path)):
        if i < len(path) - 1:
            distance += map[path[i]][path[i + 1]]

    return distance


def swapRandomCities (path):
    p = copy.copy(path)

    idx, idx2 = -1, -1
    while idx == idx2:
        idx = random.randrange(0, len(p))
        idx2 = random.randrange(0, len(p))

    p[idx], p[idx2] = p[idx2], p[idx]

    return p


def findOptimalPath (map):
    p = createRandomPath(map)
    d = calculateDistance(map, p)

    for i in range(0, 500):

        p2 = swapRandomCities(p)
        d2 = calculateDistance(map, p2)

        if d2 < d:
            p = p2
            d = d2

    return p


def findMinimum (map, reruns):
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
    findMinimum(map, 100)
