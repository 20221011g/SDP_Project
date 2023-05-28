from random import uniform, choice, sample
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        # sum total fitness --> if we do 1/fitness, the individuals with smaller values of fitness (which is better in minimization problems), will have a bigger chance of being selected
        total_fitness = sum([(1 / i.fitness) for i in population])
        # get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # find individual in the position of the spin
        for individual in population:
            position += (1 / individual.fitness)
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_selection(population, size=4):
    """Tournament selection implementation.

    Args:
        population (Population): The selected population.
        size (int): Tournament size.

    Returns:
        Individual: The best individual from tournament.
    """

    # selection of individuals based on tournament size
    tournament = [choice(population.individuals) for ind in range(size)]

    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness")) # returns the best individual (higher fitness)
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness")) # returns the best individual (lower fitness)




def ranking(population):
    """
    Ranking selection implementation.

    Args:
        population (Population): The selected population.

    Returns:
        Individual: Selected individual.
    """
    # sorting the population
    population_sort = sorted(population.individuals, key=attrgetter("fitness"))

    # generates a random number between 0 and 1 as the spin
    spin = uniform(0, 1)
    position = 0
    # index of each individual.
    index = 1
    # the sum of indexes will be used for the probability of selecting an individual
    sum_of_indexes = len(population_sort)

    # iterating over individuals, we will add the respective index to sum_of_indexes
    for individual_index in range(len(population_sort)):
        sum_of_indexes += individual_index

    # the probability of being chosen is the position occupied by the
    # individual in the ranking, divided by the sum of the ranking indexes of all the individuals.
    for individual in population_sort:
        position += index / sum_of_indexes
        # if the spin lands in the position of that individual, we will return it
        if position > spin:
            return individual
        # at the end of each iteration, add 1 to the variable index
        index += 1
