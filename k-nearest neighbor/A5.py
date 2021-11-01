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
    points = {"orange": [], "red": []}
    data = pd.read_csv(csv, sep=";", header=None)

    for point in data.values:

        if point[2] < 0:
            points["orange"].append((Point(point[0], point[1])))
        else:
            points["red"].append((Point(point[0], point[1])))

    return points


def get_random_prototype(prototypes):
    rand_category = "orange" if random.randrange(2) == 1 else "red"
    rand_idx = random.randrange(len(prototypes["red"]))
    return prototypes[rand_category][rand_idx], rand_category


def create_v_input(xMin, yMin, xMax, yMax, precision):
    x = round(random.uniform(xMin, xMax),precision)
    y = round(random.uniform(yMin, yMax),precision)
    return Point(x,y)


def get_euklidean_distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    return math.sqrt(dx ** 2 + dy ** 2)


def check_neighborhood(neighborhood):
    amount_orange, amount_red = 0, 0
    for neighbor in neighborhood:
        if neighbor[1] == "orange":
            amount_orange += 1
        elif neighbor[1] == "red":
            amount_red += 1

    return "orange" if amount_orange > amount_red else "red"


def classify_v_input(v_input, prototypes, k):
    distances = []
    for category in prototypes:
        for prototype in prototypes[category]:
            d = get_euklidean_distance(v_input, prototype)
            distances.append((d, category))

    neighborhood = sorted(distances)[:k]


    return check_neighborhood(neighborhood)


def visualize(prototypes, v_input=False):
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

    if v_input != False:
        plt.scatter(v_input.x, v_input.y)

    plt.show()


def compare_category(v_input_category, estimated_category):
    return v_input_category == estimated_category


def print_setup(k, runcount, amount, prototypes ):
    print("\n\n === LAZY LEARNING === ")
    print()
    print("=> {} classes".format(len(prototypes)))
    print("=> {} input vectors classified".format(amount))
    print("=> {} neighbors compared".format(k))
    print()
    print("SCP := successful classification probability")
    print()
    print("SCP per run:")


def run_lazy(prototypes, k, amount, runcount):


    print_setup(k, runcount, amount, prototypes)
    cp = 0  # classification probability

    for i in range(runcount):

        count_true = 0

        for j in range(1, amount):

            v_input, v_input_category = get_random_prototype(prototypes)
            estimated_category = classify_v_input(v_input, prototypes, k)

            if compare_category(v_input_category, estimated_category):
                count_true += 1

        ccp = count_true/amount # current classification probability
        cp += ccp
        print("   run-{}: {}".format(i+1, ccp))

    print()
    print("average SCP: {}".format(round(cp/runcount, 2)))


def run(prototypes, k, xMin, yMin, xMax, yMax, precision):

    v_input = create_v_input(xMin, yMin, xMax, yMax, precision)
    estimated_category = classify_v_input(v_input, prototypes, k)

    print("\n\n === NORMAL LEARNING === ")
    print()
    print("Estimated category of input vector ({}, {}): {}".format(v_input.x, v_input.y, estimated_category))

    return v_input

def main(lazy=True, k=5, amount=50, runcount=10, xMin=-1, yMin=-1, xMax=1, yMax=1, precision=2):

    prototypes = csv_to_dict("spiral.txt")

    if lazy:
        run_lazy(prototypes, k, amount, runcount)
    else:
        v_input = run(prototypes, k, xMin, yMin, xMax, yMax, precision)
        visualize(prototypes, v_input)


if __name__ == '__main__':

    '''
    NORMAL LEARNING
    
    Creates a new, unclassified input vector and determines
    the class using k-nearest neighbor algorithm.
    
    Prints estimated class of input vector in console.
    The two spirals and input vector are then visualized to 
    verify the classification manually.
    
    '''
    main(lazy=False)


    ''' 
    LAZY LEARNING
    
    Uses a prototype as an input vector and determines
    the class using k-nearest neighbor algorithm.
    The step is repeated 50 times and the probability of 
    a successful classification for this run is printed.
    
    Test is run 10 times.
    '''
    main(lazy=True)


