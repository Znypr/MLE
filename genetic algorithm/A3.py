# author: Candra Mulyadhi (1920996)
# date: 17/10/2021


# The population size has a great influence, of how fast the genomes of
# all the individuals will be identical within a certain span of generations.
# Therefore I increased the amount to 25.
# Note: increasing the population size exponentially increases the runtime

# the constant c has been chosen by comparing fitness-functions and choosing
# the most fitting one
# the crossover- and mutationrate have been chosen by testing resulting in on average
# on average better results


# for testing purposes a function 'run_tests(iterations, generations)' has been implemented
# to deliver results with various rates.

import random
import copy
import math


# setup

volume = 100
amount_genes = 100
amount_individuals = 25

c = 0.0002
crossover_rate = 0.6
mutation_rate = 0.3

list = []
population = []
new_population = []


# initializers

def set_list():
    global list
    list = []
    for x in range(amount_genes):
        list.append(create_random_volume())

def set_population():
    global population
    population = []
    for i in range(amount_individuals):
        population.append(create_hypothesis())

def create_hypothesis():
    hypothesis = []

    for i in range(amount_genes):
        bit = random.randrange(0, 2)
        hypothesis.append(bit)

    return hypothesis

def create_random_volume():
    return random.uniform(1,10)


# helpers

def select_hypothesis():
    randNum = random.random()
    sum = 0
    idx = random.randrange(0, amount_individuals)

    while sum < randNum:
        idx = idx + 1
        idx = idx % amount_individuals
        sum = sum + pr(idx)

    return idx

def pr(i):
    return fitness(i) / total_fitness()

def fitness(i):
    w = get_weight(i)
    return math.e ** (-c * ((volume - w) ** 2))


def total_fitness():
    f = 0

    for j in range(amount_individuals):
        f += fitness(j)

    return f

def max_fitness():

    max = 0

    for i in range(amount_individuals):
        f = fitness(i)
        if f > max:
            max = f
    return max

def get_weight(i):

    w = 0

    for j in range(amount_genes):
        if population[i][j] == 1:
            w += list[j]

    return w

def get_weights():

    w = []
    for i in range(amount_individuals):
        w.append(round(get_weight(i)))

    return w


# genetics

def selection():
    amount_selections = round((1 - crossover_rate) * amount_individuals)
    for i in range(amount_selections):
        selectedIndividual = population[select_hypothesis()].copy()
        new_population.append(selectedIndividual)

def crossover():
    amount_crossovers = round(crossover_rate * amount_individuals / 2)
    for i in range(amount_crossovers):

        crossoverpoint = random.randrange(0, amount_genes)
        randIdx = select_hypothesis()
        h1 = population[randIdx].copy()
        h2 = population[(randIdx+1) % amount_individuals].copy()

        h1[:crossoverpoint], h2[:crossoverpoint] = h2[:crossoverpoint], h1[:crossoverpoint]

        new_population.append(h1)
        new_population.append(h2)

def mutation():
    amount_mutations = round(mutation_rate * amount_individuals)
    for i in range(amount_mutations):
        random_individual = random.randrange(0, amount_individuals)
        mutate_gene(random_individual)

def mutate_gene(i):
    random_gene = random.randrange(0, amount_genes)

    if new_population[i][random_gene] == 0:
        new_population[i][random_gene] = 1
    else:
        new_population[i][random_gene] = 0

def update():

    global new_population
    global population

    population = new_population.copy()
    new_population = []

def fitness_distribution():
    fit = []
    for j in range(amount_individuals):
        fit.append(round(fitness(j),2))
    return fit


# main loops

def run_with_generations(generations):

    set_list()
    set_population()
    w = get_weights()
    average_fitness = total_fitness() / amount_individuals
    start = average_fitness

    for generation in range(generations):
        selection()
        crossover()
        mutation()

        update()
        w = get_weights()
        average_fitness = total_fitness() / amount_individuals

    return start, average_fitness, sorted(get_weights(), reverse=True)[0]

def run_with_threshold(threshold):

    set_list()
    set_population()
    f = max_fitness()
    start = f
    g = 0

    while f < threshold:
        g = g + 1
        selection()
        crossover()
        mutation()

        update()

        f = max_fitness()
        print("Generation: ", g, "\nFitness: ", f, "\n")

    print("Delta: ", f - start)

def run(input):

    if input < 1:
        return(run_with_threshold(input))
    else:
        return(run_with_generations(input))


# execution

def handle_delta(delta):

    print("\nOverall improvement:")
    if delta >= 0:
        print("  +"+ str(round(delta * 100, 2)) + "%")
    else:
        print("  "+ str(round(delta * 100, 2)) + "%")
    print()

def print_setup():

    print()
    print("Volume Target: ", volume)
    print("Amount of Individuals: ", amount_individuals)
    print("Genes per Genome: ", amount_genes)
    print("Constant C: ", c)
    print()

def test_setup(i, g, m, c):

    global mutation_rate
    global crossover_rate

    weight_distribution = []
    avg_start = 0
    avg_end = 0
    mutation_rate = m
    crossover_rate = c

    for i in range(i):
        start_fitness, end_fitness, w = run(g)
        avg_start += start_fitness
        avg_end += end_fitness

    start = avg_start/i
    end = avg_end/i

    print("Mutationrate: ", m, "| Crossoverrate: ", c)
    print("Average Fitness:")
    print("  Start: ", round(start,3), "| End: ", round(end, 3))
    handle_delta(end-start)

def run_test(i, g):

    # this function runs the genetic cycle g times. (g := generations) => 1 lifecycle
    # each lifecycle is repeated i times (i := iterations) and returns an average improvement in percent (delta)

    print_setup()
    print("--MUTATIONS--")
    test_setup(i, g, 0, 0)
    test_setup(i, g, 0.5, 0)
    test_setup(i, g, 1, 0)

    print("--CROSSOVER--")
    test_setup(i, g, 0, 0.2)
    test_setup(i, g, 0, 0.4)
    test_setup(i, g, 0, 0.6)
    test_setup(i, g, 0, 0.8)
    test_setup(i, g, 0, 1)

def run_normal(g):

    print_setup()

    start, end, fittest = run(g)
    print("Mutationrate: ", mutation_rate, "| Crossoverrate: ", crossover_rate, "\n")
    print("Average Fitness within", g, "generations: ")
    print("  Start: ", round(start,5), "\n  End:   ", round(end,5))
    handle_delta(end-start)
    print("fittest individual:", fittest, "l")



if __name__ == '__main__':

    run_normal(50)
    #run_test(10, 50)
