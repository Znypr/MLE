import math
import random
import copy

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi


class Point(object):
    x = 0.
    y = 0.

    def __init__(self, x=0., y=0.):
        self.x, self.y = x, y


def random_int(n):
    return random.randrange(0, n)


def random_prototype(prototypes):
    rand_category = "blue" if random.randrange(2) == 1 else "red"
    rand_idx = random.randrange(len(prototypes["red"]))
    return prototypes[rand_category][rand_idx]


def create_spiral(offset = 0.0):
    numTurns = 2
    stepover = 0.1
    distanceBetweenTurns = stepover * (1/2*pi)

    theta = 0.1

    pointsPerTurn = 30

    points = []
    for i in range(pointsPerTurn*numTurns):
        r = offset + (distanceBetweenTurns*theta)
        points.append(Point(r*np.cos(theta), r*np.sin(theta)))
        theta += 2*pi / pointsPerTurn


    return points


def get_euklidean_distance(p1, p2):
    d1 = p1.x - p2.x
    d2 = p1.y - p1.y

    return math.sqrt(d1 ** 2 + d2 ** 2)


def check_neighborhood(neighborhood):
    amount_blue, amount_red = 0, 0
    for neighbor in neighborhood:
        if neighbor[1] == "blue":
            amount_blue += 1
        elif neighbor[1] == "red":
            amount_red += 1

    return "blue" if amount_blue > amount_red else "red"


def classify_input_vector(input_vector, prototypes, k):
    distances = []
    for category in prototypes:
        for prototype in prototypes[category]:
            d = get_euklidean_distance(input_vector, prototype)
            distances.append((d, category))

    neighborhood = sorted(distances)[:k]

    return check_neighborhood(neighborhood)


def visualize(prototypes):
    x, y = [], []
    for point in prototypes["red"]:
        x.append(point.x)
        y.append(point.y)
    plt.scatter(x, y)

    x, y = [], []
    for point in prototypes["blue"]:
        x.append(point.x)
        y.append(point.y)
    plt.scatter(x, y)

    plt.show()


def main():
    k = 3
    prototypes = {"blue": create_spiral(0.3), "red": create_spiral()}
    #visualize(prototypes)

    for i in range(10):
        # lazy learning
        input_vector = random_prototype(prototypes)
        category = classify_input_vector(input_vector, prototypes, k)

        print("Category of Input Vector ({}, {}): {}".format(input_vector.x, input_vector.y, category))


if __name__ == '__main__':
    main()


