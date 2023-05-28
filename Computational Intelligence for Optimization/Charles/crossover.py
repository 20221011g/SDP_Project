import random

import numpy as np


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = random.randint(1, len(p1) - 2) # generates a random integer between 1 and the length of p1 minus 2

    offspring1 = p1[:co_point] + p2[co_point:] # creates the first offspring by concatenating the genes before the crossover point from p1 with the genes after the crossover point from p2.
    offspring2 = p2[:co_point] + p1[co_point:] # creates the first offspring by concatenating the genes before the crossover point from p2 with the genes after the crossover point from p1.

    return offspring1, offspring2


def two_point_crossover(parent1, parent2):
    """Implementation of single point crossover.

       Args:
           parent1 (Individual): First parent for crossover.
           parent2 (Individual): Second parent for crossover.

       Returns:
           Individuals: Two offspring, resulting from the crossover.
    """
    length = len(parent1)
    # Select two random crossover points
    point1 = random.randint(0, length - 1)
    point2 = random.randint(0, length - 1)

    # Make sure point2 is greater than point1
    if point2 < point1:
        point1, point2 = point2, point1

    # Perform crossover

    # creates the first offspring by concatenating the genes before the first crossover point from parent1,
    # the genes between the two crossover points from parent2, and the genes after the second crossover point from parent1
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]

    # creates the second offspring by concatenating the genes before the first crossover point from parent2,
    # the genes between the two crossover points from parent1, and the genes after the second crossover point from parent2
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2


def pmx(p1, p2):
    """
    Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = random.sample(range(len(p1)), 2) # the indices of two crossover points randomly sampled from the range of the length of p1 are assigned to xo_points
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x) # offspring individual

        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]] # segment of x is assigned to o
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]]) # compares same segment in y and x and isolates the values to be mapped in z

        assigned_values = set()

        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])

            while o[index] is not None:
                temp = index
                index = y.index(x[temp])

            while index in assigned_values:
                temp = index
                index = y.index(x[temp])

            assigned_values.add(index)
            o[index] = i

        for index, element in enumerate(o):
            if element is None:
                o[index] = y[index]

        return o

    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2


def discrete_crossover(p1, p2):
    """
    Implementation of discrete crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    o1 = []
    o2 = []

    # Randomly select a subset of genes from one parent
    subset_indices = random.sample(range(len(p1)), k=len(p1) // 2)

    # Fill the remaining genes with the corresponding genes from the other parent
    for i in range(len(p1)):
        if i in subset_indices:
            o1.append(p1[i])
            o2.append(p2[i])
        else:
            o1.append(p2[i])
            o2.append(p1[i])

    return o1, o2


def uniform_crossover(parent1, parent2):
    """
    Implementation of uniform crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    length = len(parent1)
    child1 = []
    child2 = []

    for i in range(length):
        # Randomly select gene from either parent
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])

    return child1, child2




