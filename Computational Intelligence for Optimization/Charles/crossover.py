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
    co_point = random.randint(1, len(p1) - 2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2

    # def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    # offspring1 = [None] * len(p1)
    # offspring2 = [None] * len(p1)

    # while None in offspring1:
    #   index = offspring1.index(None)
    #  val1 = p1[index]
    #  val2 = p2[index]

    # copy the cycle elements
    #   while val1 != val2:
    #       offspring1[index] = p1[index]
    #       offspring2[index] = p2[index]
    ###       val2 = p2[index]
    #     index = p1.index(val2)

    # copy the rest
    #    for element in offspring1:
    # if element is None:
    #        index = offspring1.index(None)
    #        if offspring1[index] is None:
    #               offspring1[index] = p2[index]
    #            offspring2[index] = p1[index]
    # print(offspring1)

    # return offspring1, offspring2


def two_point_crossover(parent1, parent2):
    length = len(parent1)
    # Select two random crossover points
    point1 = random.randint(0, length - 1)
    point2 = random.randint(0, length - 1)

    # Make sure point2 is greater than point1
    if point2 < point1:
        point1, point2 = point2, point1

    # Perform crossover
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2


def pmx(p1, p2):
    xo_points = random.sample(range(len(p1)), 2)
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x)

        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]]
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])

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


def arithmetic_xo(p1, p2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = random.uniform(0, 1)
    o1 = [None] * len(p1)
    o2 = [None] * len(p1)
    for i in range(len(p1)):
        o1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        o2[i] = p2[i] * alpha + (1 - alpha) * p1[i]
    return o1, o2


if __name__ == '__main__':
    # p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    p1, p2 = [0.1, 0.15, 0.3], [0.3, 0.1, 0.2]
    o1, o2 = arithmetic_xo(p1, p2)
    print(o1, o2)
