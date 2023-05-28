from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy

from Data.data_sd import data, nutrients


class Individual:
    """ An individual is a possible solution to the Stigler's Diet Problem """
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
        """
            This function calculates the fitness for each possible solution. It considers each food item present in a
            solution diet and compares its nutritional value with the daily requirements, penalizing the solutions
            that do not meet those requirements.
            The fitness score is a combination between the monetary cost of each solution and nutritional differences. Hence,
            the lower the fitness, the better.

            Returns:
            float value as a combination between the monetary cost of each solution and nutritional differences.

        """

        total_monetary_cost = 0
        total_cost = 0
        not_empty = 0
        nutrient_val = []

        for i in range(len(self)): # iterate over solution
            if self[i] == 1: # if the food item was selected for the solution
                not_empty = 1 # the solution is not empty
                total_monetary_cost += data[i][2]  # accumulate the monetary cost
                for j in range(3, len(data[i])): # iterate over nutritional values
                    nutrient_val.append(data[i][j]) # collect the nutrient values for the selected food item

        # if the solution is not constituted by any food items, then the nutritional difference will be equal to the
        # daily requirements
        if not_empty == 0:
            for n in range(len(nutrients)):
                total_cost += nutrients[n][1]
        else:
            for k in range(len(nutrients)): # iterate over each nutrient
                if nutrients[k][1] - nutrient_val[k] > 0:
                    total_cost += nutrients[k][1] - nutrient_val[k] # increment the penalization according to each nutrient difference

        fitness = total_monetary_cost + total_cost
        return fitness


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
    """ The population is a set of possible solutions (individuals) to the Stigler's Diet Problem """

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
        best_fit = []# list composed by the fitness of the best individual of each generation

        for i in range(gens): # iterate over each generation
            new_pop = []
            if elitism: #save the best individuals of every generation
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))


            while len(new_pop) < self.size: # while the new population is not complete

                parent1, parent2 = select(self), select(self) # choose 2 parents according to selection algorithm

                if random() < xo_prob: # random number is generated. if it is lower than the predefined crossover probability, crossover is applied
                    offspring1, offspring2 = crossover(parent1, parent2) # use the 2 chosen parents to originate offspring, using the selected method

                else: # if the previous condition is not met, then crossover is not applied
                    offspring1, offspring2 = parent1, parent2 # offspring is equal to parents

                if random() < mut_prob: # random number is generated. if it is lower than the predefined mutation probability, mutation is applied to the 1st element of the offspring
                    offspring1 = mutate(offspring1) # selected mutation method applied to the 1st element of offspring

                if random() < mut_prob: # random number is generated. if it is lower than the predefined mutation probability, mutation is applied to the 2nd element of the offspring
                    offspring2 = mutate(offspring2) # selected mutation method applied to the 2nd element of offspring

                new_pop.append(Individual(representation=offspring1)) # add the 1st element of the offspring to the new population
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2)) # if there is still space in the new population, the 2nd element is added to it

            # to give space to the best individual(from the previous population) in the new population,
            # it has to be compared to the worst individual from the new population. If that is the case, then the worst
            # individual from the new population is removed and the best from the old population is added.
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
            self.individuals = new_pop # update population with new individuals

            # according to the type of optimization problem, the best individual is selected,
            # so that the function ca return the best fitness from each generation
            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}') # the best individual has the higher fitness
            elif self.optim == "min":
                #print(f'Best Individual: {min(self, key=attrgetter("fitness"))}') # the best individual has the lower fitness
                best_ind = min(self, key=attrgetter("fitness"))
            best_fit.append(best_ind.fitness) # add the fitness from the best individual to the list of best fitnesses

        return best_fit

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
