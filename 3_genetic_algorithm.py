# author: Candra Mulyadhi (1920996)
# date: 11/10/2021

## fitness:
##


import random
import numpy as np
import copy
import math



c = 0.001
V = 100
l = 100
p = 10
r = 0.8



population = []
newPopulation = []
list = []



def setList():

    for x in range(l):
        list.append(generateRandomVolume())

    print(list)

def generateRandomVolume():

    return round(random.random()*10, 2)

def createHypothesis():

    hypothesis = []

    for i in range(l):
        bit = random.randrange(0,2)
        hypothesis.append(bit)

    return hypothesis

def setPopulation():

    for i in range(p):
        population.append(createHypothesis())

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

def getWeight(i):

    w = 0

    for j in range(l):
        if population[i][j] == 1:
            w += list[j]

    return w

def fitness(i):

    w = getWeight(i)

    return math.e ** -c*(V-getWeight(i))**2

def totalFitness():

    f = 0.0

    for j in range(p):
        f += fitness(j)

    return f




def selection():

    for i in range(int((1-r)*p)):

        selectedIndividual = population[selectHypothesis()]
        newPopulation.append(selectedIndividual)

def crossover():

    for i in range(int(r*p)):

        randIdx = selectHypothesis()
        crossoverPoint = random.randrange(0,l)

        dna1 = population[randIdx]
        dna2 = population[(randIdx+1)%p]
        copyDNA1 = copy(dna1)

        for j in range(crossoverPoint):
            dna1[j] = dna2[j]
            dna2[j] = copyDNA1[j]

def mutation():

    for i in range(p):
        if random.randrange(0,math.pow(c, -1)) == 1:
            bitSwitch(population[i])

def bitSwitch(i):

    randIdx = random.randrange(0,1)

    for j in i:
        if randIdx == j:
            if i[j] == 0:
                i[j] = 1
            else:
                i[j] = 0

def update():
    population = newPopulation


def run(generations):

    setList()
    setPopulation()
    f = totalFitness()

    for generation in range(generations):

        selection()
        crossover()
        mutation()
        update()

        #f = totalFitness()

    return f



if __name__ == '__main__':

    run(50)
