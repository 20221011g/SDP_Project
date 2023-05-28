from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy

from Data.data_sd import data, nutrients


class Individual:
    def __init__(
        self,
        representation=None,
        size=None,
        replacement=True,
        valid_set=None,
    ):
        if representation is None:
            if replacement is True:
                self.representation = [choice(valid_set) for i in range(size)]
            elif replacement is False:
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation
        self.fitness = self.get_fitness()
        #print(self.representation)

    def get_fitness(self):
        total_monetary_cost = 0
        total_cost = 0
        not_empty = 0
        nutrient_val = []

        for i in range(len(self)):
            if self[i] == 1:
                not_empty = 1
                total_monetary_cost += data[i][2]  # Accumulate the monetary cost
                for j in range(3, len(data[i])):  # iterate over nutritional values
                    nutrient_val.append(data[i][j])

        if not_empty == 0:
            for n in range(len(nutrients)):
                total_cost += nutrients[n][1]
        else:
            for k in range(len(nutrients)):
                if nutrients[k][1] - nutrient_val[k] > 0:
                    total_cost += nutrients[k][1] - nutrient_val[k]

        fitness = total_monetary_cost + total_cost
        return fitness


    # def get_fitness(self):
    #     total_cost = 0
    #     nutrient_shortfalls = [0] * len(nutrients)
    #
    #     # Calculate total cost and nutrient shortfalls
    #     for i, food in enumerate(data):
    #         quantity = self[i]
    #         total_cost += food[2] * quantity
    #
    #         # Calculate nutrient shortfalls
    #         for j in range(len(nutrients)):
    #             nutrient_shortfalls[j] += max(0, nutrients[j][1] - (food[j + 3] * quantity))
    #
    #     # Calculate penalty based on nutrient shortfalls
    #     penalty = sum(nutrient_shortfalls)
    #
    #     # Calculate fitness score
    #     fitness = total_cost + penalty
    #
    #     return fitness

    def get_neighbours(self, func, **kwargs):
        neighbours = []
        for i in range(len(self)):
            neighbour = self.representation.copy()
            neighbour[i] = choice(kwargs["valid_set"])
            neighbours.append(Individual(representation=neighbour))
        return neighbours

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism):
        # We will create a list where we will save the fitness of the best individual of each generation, in order
        # to help us to understand if we are stopped in a solution and not improving the fitness
        best_fit = []
        # This value will increase every time that the fitness doesn't improve
        stopped_fitness = 0
        for i in range(gens):
            new_pop = []
            #print('Generation ', i, ':')
            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))


            while len(new_pop) < self.size:

                parent1, parent2 = select(self), select(self)

                if random() < xo_prob:
                    # print('crossover')
                    offspring1, offspring2 = crossover(parent1, parent2)

                else:
                    # print('no crossover')
                    offspring1, offspring2 = parent1, parent2

                if random() < mut_prob:
                    # print('mutation off1')
                    offspring1 = mutate(offspring1)

                if random() < mut_prob:
                    # print('mutation off2')
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)
            # print('End of ', i, ' Generation')
            self.individuals = new_pop

            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                best_ind = min(self, key=attrgetter("fitness"))
            best_fit.append(best_ind.fitness)

            # If we see that we didn't improve the fitness from the last generation, we are going to increment 1 to the
            # variable stopped_fitness
            if i != 0 and best_fit[i] == best_fit[i - 1]:
                stopped_fitness += 1

            # If we were stuck 100 times, we are going to restart the population
            # if stopped_fitness >= int(0.1 * gens):
            #     print("\n\nThe solutions got stuck... Re-starting the population...\n\n")
            #     break
        return best_fit

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
