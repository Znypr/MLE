import math
import random

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Point(object):
    x = 0.0
    y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y


def csv_to_dict(csv):
    # reading CSV file
    points = {"blue": [], "red": []}
    data = pd.read_csv(csv, sep=";", header=None)

    for point in data.values:

        if point[2] < 0:
            points["blue"].append((Point(point[0], point[1])))
        else:
            points["red"].append((Point(point[0], point[1])))

    return points


def random_prototype(prototypes):
    rand_category = "blue" if random.randrange(2) == 1 else "red"
    rand_idx = random.randrange(len(prototypes["red"]))
    return prototypes[rand_category][rand_idx], rand_category


def create_spiral(offset=0.0):
    numTurns = 2
    stepover = 0.1
    distanceBetweenTurns = stepover * (1 / 2 * np.pi)

    theta = 0.1

    pointsPerTurn = 30

    points = []
    for i in range(pointsPerTurn * numTurns):
        r = offset + (distanceBetweenTurns * theta)
        points.append(Point(r * np.cos(theta), r * np.sin(theta)))
        theta += 2 * np.pi / pointsPerTurn

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
    for i in prototypes:
        x, y = [], []
        for point in prototypes[i]:
            x.append(point.x)
            y.append(point.y)
        plt.scatter(x, y)

        x, y = [], []
        for point in prototypes[i]:
            x.append(point.x)
            y.append(point.y)
        plt.scatter(x, y)

    plt.show()


def compare_category(input_vector_category, estimated_category):
    return input_vector_category == estimated_category


def main():
    k = 5
    RUNTIME = 10
    amount = 50

    # prototypes = {"blue" : create_spiral(0.3), "red" : create_spiral()}
    prototypes = csv_to_dict("spiral.txt")
    #visualize(prototypes)
    print("classification rate")
    cr = 0

    for i in range(RUNTIME):

        count_true = 0

        for j in range(1, amount):
            # lazy learning
            input_vector, input_vector_category = random_prototype(prototypes)
            estimated_category = classify_input_vector(input_vector, prototypes, k)

            if compare_category(input_vector_category, estimated_category):
                count_true += 1
            #print("Category of Input Vector ({}, {}): {}".format(input_vector.x, input_vector.y, category))

        ccr = count_true/amount
        cr += ccr
        print("  {}: {}".format(i+1, ccr))

    print("avg classification rate in {} runs: {}".format(RUNTIME, cr/RUNTIME))

if __name__ == '__main__':
    main()
