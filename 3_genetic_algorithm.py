# author: Candra Mulyadhi (1920996)
# date: 11/10/2021

# fitness:
#


import random
import copy
import math

V = 100
l = 100
p = 10

c = 0.001
r = 0.8
m = 0.3

list = []
population = []
newPopulation = []



def setList():
    for x in range(l):
        list.append(generateRandomVolume())

def setPopulation():
    for i in range(p):
        population.append(createHypothesis())

def createHypothesis():
    hypothesis = []

    for i in range(l):
        bit = random.randrange(0, 2)
        hypothesis.append(bit)

    return hypothesis

def generateRandomVolume():
    return random.uniform(1,10)



def selectHypothesis():
    randNum = random.random()
    sum = 0
    idx = random.randrange(0, p)

    while sum < randNum:
        idx = idx + 1
        idx = idx % p
        sum = sum + pr(idx)

    return idx

def pr(i):
    return fitness(i) / totalFitness()

def fitness(i):
    w = getWeight(i)

    return math.e ** (-c * ((V - w) ** 2))

def totalFitness():
    f = 0

    for j in range(p):
        f += fitness(j)
    return f

def maxFitness():

    max = 0

    for i in range(p):
        f = fitness(i)
        if f > max:
            max = f
    return max

def getWeight(i):

    w = 0

    for j in range(l):
        if population[i][j] == 1:
            w += list[j]

    return w

def getWeights():

    w = []
    for i in range(p):
        w.append(round(getWeight(i)))

    return w



def selection():
    x = round((1-r)*p)
    for i in range(x):
        selectedIndividual = population[selectHypothesis()]
        newPopulation.append(selectedIndividual)

def crossover():
    x = round(r*p/2)
    for i in range(x):

        randIdx = selectHypothesis()
        crossoverPoint = random.randrange(0, l)

        h1 = population[randIdx]
        h2 = population[(randIdx + 1) % p]
        c1 = copy.copy(h1)

        for idx in range(crossoverPoint):
            h1[idx] = h2[idx]
            h2[idx] = c1[idx]

        newPopulation.append(h1)
        newPopulation.append(h2)

def mutation():
    x = round(m*p)
    for i in range(x):
        randIdx = random.randrange(0, len(newPopulation))
        bitSwitch(newPopulation[randIdx])

def bitSwitch(i):
    randIdx = random.randrange(0, l)

    if i[randIdx] == 0:
        i[randIdx] = 1
    else:
        i[randIdx] = 0

def update():

    global newPopulation
    global population

    population = newPopulation
    newPopulation = []

def runWithGenerations(generations):

    setList()
    setPopulation()
    f = maxFitness()
    start = f
    g = 0

    for generation in range(generations):
        g = g + 1
        selection()
        crossover()
        mutation()

        update()
        w = getWeights()

        f = maxFitness()
        print("Generation: ", g, "\nFitness: ", f, "\n")

    print("Delta: ", f - start)

def runWithTreshold(treshold):

    setList()
    setPopulation()
    f = maxFitness()
    start = f
    g = 0

    while f < treshold:
        g = g + 1
        selection()
        crossover()
        mutation()

        update()

        f = maxFitness()
        print("Generation: ", g, "\nFitness: ", f, "\n")

    print("Delta: ", f - start)

def run(input):

    if input < 1:
        runWithTreshold(input)
    else:
        runWithGenerations(input)



if __name__ == '__main__':

    run(100)
