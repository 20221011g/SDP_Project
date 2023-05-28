from Charles.charles import Individual, Population
from Charles.selection import tournament_selection, fps, ranking
from Charles.crossover import pmx, single_point_co, two_point_crossover, uniform_crossover, discrete_crossover
from Charles.mutation import inversion_mutation, swap_mutation, binary_mutation

import numpy as np
from matplotlib import pyplot as plt
from Data.data_sd import data, nutrients

selection_list = [fps, tournament_selection, ranking]
mutation_list = [inversion_mutation, binary_mutation, swap_mutation]
crossover_list = [discrete_crossover, single_point_co, two_point_crossover, uniform_crossover]
num_gens = 100
n = 1

best_fit = np.inf
valid_set = [0, 1]  # Change the valid set to a list of indices
sol_size = len(data)
pop_size = 50
fitness_results = {}

best_fit_val = []
iterations = 0
max_iterations = 80


# Try and see
def crossers_for_mutation(mutation):
    best_result = 10000
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for i, crosser in enumerate(crossover_list):
        # Create empty lists to store the best fitness values for each selection method
        best_fitness_fps = []
        best_fitness_tournament = []
        best_fitness_ranking = []

        # Iterate over selection methods
        for selec in selection_list:
            print(f"Running combination:{mutation.__name__}_{selec.__name__}_{crosser.__name__}")
            pop = Population(
                size=pop_size,
                optim="min",
                sol_size=sol_size,
                valid_set=valid_set,
                replacement=True
            )

            # Creating a Population of 20 possible solutions
            evolved_pop = pop.evolve(
                gens=num_gens,
                select=selec,
                crossover=crosser,
                mutate=mutation,  # Modify as per your mutation selection
                xo_prob=0.9,
                mut_prob=0.1,
                elitism=True
            )

            # Get the best fitness value for each generation
            best_fitness = evolved_pop
            min_result = min(best_fitness)
            if best_result > min_result:
                best_result = min_result

            # Store the best fitness values for the selection method
            if selec.__name__ == 'fps':
                best_fitness_fps = best_fitness
            elif selec.__name__ == 'tournament_selection':
                best_fitness_tournament = best_fitness
            elif selec.__name__ == 'ranking':
                best_fitness_ranking = best_fitness

            print(f"Completed combination: {selec.__name__}_{crosser.__name__}")

        # Plot the graph for the crossover method
        generations = range(1, num_gens + 1)
        ax = axes[i]
        ax.plot(generations, best_fitness_fps[:num_gens], label='FPS')
        ax.plot(generations, best_fitness_tournament[:num_gens], label='Tournament Selection')
        ax.plot(generations, best_fitness_ranking[:num_gens], label='Ranking Selection')
        ax.set_title(crosser.__name__)
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()

    plt.suptitle(f"Crossovers for {mutation.__name__}")
    plt.tight_layout()
    plt.show()
    return best_result


#REMOVE THE COMMENTS TO RUN AND COMPARE THE DIFFERENT CROSSOVERS WITH MUTATIONS

swap_mutation_result = crossers_for_mutation(swap_mutation)
binary_mutation_result = crossers_for_mutation(binary_mutation)
inversion_mutation_result = crossers_for_mutation(inversion_mutation)
print("The best Score with the swap mutation is " + str(swap_mutation_result))
print("The best Score with the binary mutation is " + str(round(binary_mutation_result, 2)))
print("The best Score with the inversion mutation is " + str(round(inversion_mutation_result, 2)))


# Now that we can see our best Scores, lets see the true best score.

def true_best(sele, cross, mut):
    pop = Population(
        size=pop_size,
        optim="min",
        sol_size=sol_size,
        valid_set=valid_set,
        replacement=True
    )
    best_fitness = pop.evolve(
        gens=80,
        select=sele,
        crossover=cross,
        mutate=mut,
        xo_prob=0.90,
        mut_prob=0.10,
        elitism=True
    )
    return best_fitness


# Dictionary to store fitness results
best_fitness_tournament = true_best(tournament_selection, single_point_co, inversion_mutation)
best_fitness_ranking = true_best(ranking, single_point_co, inversion_mutation)
best_fitness_fps = true_best(fps, single_point_co, inversion_mutation)

generations = range(1, max_iterations + 1)

min_tournament = min(best_fitness_tournament)
min_ranking = min(best_fitness_ranking)
min_fps = min(best_fitness_fps)
best = 0
result_name = ""
# Find the maximum value and corresponding result name
if min_tournament < min_ranking and min_tournament < min_fps:
    best = min_tournament
    result_name = "Tournament"
elif min_ranking < min_fps:
    best = min_ranking
    result_name = "Ranking"
else:
    best = min_fps
    result_name = "FPS"

# Plotting the graph
plt.plot(generations, best_fitness_fps[:max_iterations], label='FPS')
plt.plot(generations, best_fitness_tournament[:max_iterations], label='Tournament Selection')
plt.plot(generations, best_fitness_ranking[:max_iterations], label='Ranking Selection')

plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.legend()
plt.suptitle("Best result is " + result_name)
plt.show()

print("Best fitness in all possibilities:", result_name, "With the value of", best)


#Tunning the best result might take some time to run
print("Running plz wait...")

# Define the parameter ranges for tuning
population_sizes = [50, 100, 200]  # Different population sizes to try
mutation_probs = [0.05, 0.1, 0.2]  # Different mutation probabilities to try
crossover_probs = [0.8, 0.9, 1.0]  # Different crossover probabilities to try

best_fitness = np.inf  # Initialize the best fitness

# Iterate over the parameter combinations
for pop_size in population_sizes:
    for mut_prob in mutation_probs:
        for xo_prob in crossover_probs:
            # Create a new population
            pop = Population(
                size=pop_size,
                optim="min",
                sol_size=sol_size,
                valid_set=valid_set,
                replacement=True
            )

            # Evolve the population with the current parameter values
            evolved_pop = pop.evolve(
                gens=num_gens,
                select=fps,  # Use the selection method you found to be the best
                crossover=single_point_co,  # Use the crossover method you found to be the best
                mutate=inversion_mutation,  # Use the mutation method you found to be the best
                xo_prob=xo_prob,
                mut_prob=mut_prob,
                elitism=True
            )

            # Get the best fitness value for this parameter combination
            min_fitness = min(evolved_pop)

            # Check if the current parameter combination improves the best fitness
            if min_fitness < best_fitness:
                best_fitness = min_fitness
                best_parameters = (pop_size, mut_prob, xo_prob)

# Print the best result and the corresponding parameters
print("Best fitness:", best_fitness)
print("Best parameters (Population Size, Mutation Probability, Crossover Probability):", best_parameters)
