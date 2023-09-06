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
        all_time_best_score = 0
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
            if best_individual is None or scores[best_index] > all_time_best_score:
                best_individual = population[best_index]
            best_score.append(scores[best_index])

            parents = self.selection(population, scores, self.population_size // 2)
            survivors = [i for i in population if i not in parents]

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

            offspring.sort(key=lambda x: self.fitness_score(x), reverse=True)
            survivors.sort(key=lambda x: self.fitness_score(x), reverse=True)

            population = offspring[:offspring_pop] + survivors[:survivors_pop]
            # random.shuffle(population)

            if all_time_best_score >= scores[best_index]:
                stale_iteration += 1
            else:
                stale_iteration = 0
                all_time_best_score = scores[best_index]

            if stale_iteration >= self.max_stale_iterations:
                print("Reached max stale iterations")
                break
        return i, best_individual, population[best_index], best_score

class KnapsackProblem(GeneticAlgorithm):
    def __init__(self, population_size, max_iteration, max_stale_iterations, crossover_probability, mutators, offspringPercentage, weights, prices, capacity):
        super(KnapsackProblem, self).__init__(population_size, max_iteration, max_stale_iterations, crossover_probability, mutators, offspringPercentage)
        self.weights = weights
        self.prices = prices
        self.capacity = capacity


    def initial_population(self, size):
        def generate():
            return [random.randint(0, 1) for _ in range(len(self.prices))]
        return [generate() for _ in range(size)]


    def fitness_score(self, individual):
        score = 0
        weight = 0
        for i, gene in enumerate(individual):
            score += gene * self.prices[i]
            weight += gene * self.weights[i]
        return -1 if weight > self.capacity else score


    def selection(self, population, scores, size):
        total_fitness = sum(scores)
        probabilities = [score / total_fitness for score in scores]
        parents = random.choices(population, weights=probabilities, k=size)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_probability:
            crossover_point = random.randint(1, len(self.prices) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2


class BitMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def condition(self, individual, chromosome_id):
        return True

    def mutate_chromosome(self, chromosome):
        return 1 - chromosome

class ConditionMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def condition(self, individual, chromosome_id):
        return individual[chromosome_id] == 0

    def mutate_chromosome(self, chromosome):
        return random.randint(0, 1)


class RandomMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def condition(self, individual, chromosome_id):
        return True

    def mutate_chromosome(self, chromosome):
        return random.randint(0, 1)

# bit_mutator = BitMutator(0.3)
# random_mutator = RandomMutator(0.2)
# condition_mutator = ConditionMutator(0.5)
#
# alg = KnapsackProblem(
#     population_size = 4,
#     max_iteration = 5000,
#     max_stale_iterations = 100,
#     mutators = [
#         condition_mutator,
#         bit_mutator,
#         random_mutator,
#     ],
#     crossover_probability = 0.3,
#     weights = [13, 10, 13, 7, 2],
#     prices = [8, 7, 9, 6, 4],
#     capacity = 27,
#     offspringPercentage=0.3
# )
# Optimal is [0, 1, 1, 0, 1]
# print(alg.run())
