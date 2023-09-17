import numpy as np
import random

from Mutator import Mutator

from tqdm import tqdm


class GeneticAlgorithm:
    def __init__(self, population_size, max_iteration, max_stale_iterations, crossover_probability, mutators: list[Mutator], offspringPercentage):
        self.population_size = population_size
        self.max_iteration = max_iteration
        self.max_stale_iterations = max_stale_iterations
        self.crossover_probability = crossover_probability
        self.mutators = mutators
        self.offspringPercentage = offspringPercentage


    def initial_population(self, size):
        raise NotImplementedError()

    def fitness_score(self, individual):
        raise NotImplementedError()


    def selection(self, population, scores, size):
        raise NotImplementedError()


    def crossover(self, parent1, parent2):
        raise NotImplementedError()


    def mutate(self, individual):
        result = []
        for chromosome_id in range(len(individual)):
            chromosome = individual[chromosome_id]
            for mutator in self.mutators:
                chromosome = mutator.mutate(individual, chromosome_id)
            result.append(chromosome)
        return result


    def run(self):
        all_time_best_score = 1000000000000000000
        stale_iteration = 0
        best_individual = None
        best_score = []
        population = self.initial_population(self.population_size)
        offspring_pop = int(self.offspringPercentage * self.population_size)
        survivors_pop = self.population_size - offspring_pop
        best_index = -1
        for i in tqdm(range(self.max_iteration)):
            scores = [self.fitness_score(individual) for individual in population]
            best_index = np.argmin(scores)
            if best_individual is None or scores[best_index] < all_time_best_score:
                best_individual = population[best_index]
            best_score.append(scores[best_index])

            parents = self.selection(population, scores, self.population_size // 2)
            survivors = population.copy()

            offspring = []

            for j in range(len(parents)):
                next_id = j + 1 if j + 1 < len(parents) else 0
                parent1 = parents[j]
                parent2 = parents[next_id]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                offspring.append(child1)
                offspring.append(child2)

            offspring.sort(key=self.fitness_score)
            survivors.sort(key=self.fitness_score)

            population = offspring[:offspring_pop] + survivors[:survivors_pop]

            if all_time_best_score <= scores[best_index]:
                stale_iteration += 1
            else:
                stale_iteration = 0
                all_time_best_score = scores[best_index]

            if stale_iteration >= self.max_stale_iterations:
                print("Reached max stale iterations")
                break
        scores = [self.fitness_score(individual) for individual in population]
        best_index = np.argmin(scores)
        if best_individual is None or scores[best_index] > all_time_best_score:
            best_individual = population[best_index]
        best_score.append(scores[best_index])
        return i, best_individual, population[best_index], best_score
