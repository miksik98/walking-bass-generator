import random
from fractions import Fraction

from ChooseScaleAlgorithm import choose_scale_algorithm
from Chord import Chord
from GeneticAlgorithm import GeneticAlgorithm
from Mutator import Mutator, OneOctaveMutator, PitchMutation, ChangeOctaveMutator, IntroduceFlagoletOrOpenString, \
    IntroduceTriplet
from NarrowContextRules import narrow_context_rules
from NoteGenerator import note_generator
from Solution import Solution
from WideRangeContextRules import wide_range_context_rules
import matplotlib.pyplot as plt
from datetime import datetime

from Note import Note


class WalkingBassProblem(GeneticAlgorithm):
    def __init__(self, population_size, max_iteration, max_stale_iterations, crossover_probability,
                 mutators: list[Mutator], offspringPercentage, input_chords: list[Chord], mutation_probability,
                 repair_operators: list[Mutator]):
        super().__init__(population_size, max_iteration, max_stale_iterations, crossover_probability, mutators,
                         offspringPercentage)
        self.input_chords = input_chords
        self.scales = []
        self.mutation_probability = mutation_probability
        self.repair_operators = repair_operators

    def generate_scale_for_id(self, chord_id: int):
        actual_chord = self.input_chords[chord_id]

        prev_chord = None
        for i in range(chord_id - 1, -1, -1):
            if self.input_chords[i] != actual_chord:
                prev_chord = self.input_chords[i]
                break

        next_chord = None
        for i in range(chord_id + 1, len(self.input_chords)):
            if self.input_chords[i] != actual_chord:
                next_chord = self.input_chords[i]
                break

        return choose_scale_algorithm.choose(prev_chord, actual_chord, next_chord)

    def initial_population(self, size):
        def generate():
            notes = []
            for i, chord in enumerate(self.input_chords):
                if len(self.scales) == i:
                    if i > 0 and self.input_chords[i - 1] == chord:
                        scale = self.scales[i - 1]
                    else:
                        scale = self.generate_scale_for_id(i)
                    self.scales.append(scale)
                else:
                    scale = self.scales[i]
                possible_notes = note_generator.generate(i % 4 == 0, chord, scale,
                                                         (i % 4) % 2 == 0,
                                                         Fraction(3, 3), False)
                note = \
                random.choices([n.note for n in possible_notes], weights=[n.priority for n in possible_notes], k=1)[0]
                notes.append(note)
            return Solution(notes)

        return [generate() for _ in range(size)]

    def mutate(self, individual):
        notes = individual.notes
        result_after_mutation = []
        chromosome_id = 0
        after_mutation_id = 0
        while chromosome_id < len(notes):
            chromosomes = [notes[chromosome_id]]
            for mutator in self.mutators:
                if random.random() < self.mutation_probability:
                    chromosomes = mutator.mutate(result_after_mutation[:after_mutation_id] + notes[chromosome_id:],
                                                after_mutation_id)
                    after_mutation_id += len(chromosomes) - 1
            result_after_mutation += chromosomes
            chromosome_id += 1
            after_mutation_id += 1
        result_after_repair = []
        for chromosome_id in range(len(result_after_mutation)):
            chromosomes = [result_after_mutation[chromosome_id]]
            for mutator in self.repair_operators:
                chromosomes = mutator.mutate(result_after_repair[:chromosome_id] + result_after_mutation[chromosome_id:],
                                            chromosome_id)
            result_after_repair += chromosomes
        return Solution(result_after_repair)

    def fitness_score(self, individual):
        result = 0.0
        for rule in wide_range_context_rules:
            result += rule(individual).check()
        for rule in narrow_context_rules:
            prev_prev_note = None
            prev_note = None
            actual_note = None
            next_note = None
            for i in range(len(individual.notes)):
                if i > 2:
                    prev_prev_note = individual.notes[i - 2]
                if i > 1:
                    prev_note = individual.notes[i - 1]
                if i < len(individual.notes) - 1:
                    next_note = individual.notes[i + 1]
                actual_note = individual.notes[i]
                result += rule(prev_prev_note, prev_note, actual_note, next_note).check()
        return result

    def selection(self, population, scores, size):

        def random_wheel(_population, _scores, _size):
            total_fitness = sum(_scores)
            probabilities = [total_fitness - score for score in _scores]
            if sum(probabilities) == 0.0:
                return random.choices(_population, k=_size)
            parents = random.choices(_population, weights=probabilities, k=_size)
            return parents

        return random_wheel(population, scores, size)

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_probability:
            crossover_points = [i for i in range(0, len(self.input_chords), 4) if
                                i != 0 and i != len(self.input_chords) - 1]
            crossover_point = Fraction(random.choice(crossover_points))

            parent1_crossover_point = None
            parent2_crossover_point = None
            acc = Fraction(0)
            eps = 0.0001
            for i, note in enumerate(parent1.notes):
                if abs(crossover_point + eps) > acc > abs(crossover_point - eps):
                    parent1_crossover_point = i
                    break
                acc += note.note.quarterLength
            acc = Fraction(0)
            for i, note in enumerate(parent2.notes):
                if abs(crossover_point + eps) > acc > abs(crossover_point - eps):
                    parent2_crossover_point = i
                    break
                acc += note.note.quarterLength

            child1 = parent1.notes[:parent1_crossover_point] + parent2.notes[parent2_crossover_point:]
            child2 = parent2.notes[:parent2_crossover_point] + parent1.notes[parent1_crossover_point:]
            return Solution(child1), Solution(child2)
        else:
            return parent1, parent2


chords = []

blues = "../tasks/blues_f.txt"
coltrane = "../tasks/26-2.txt"
so_what = "../tasks/so_what.txt"
time_remembered = "../tasks/time_remembered.txt"
yes_or_no = "../tasks/yes_or_no.txt"

num_of_iterations = 10
file = blues
with open(file, "r") as f:
    for line in f:
        bars = list(map(lambda x: x.strip().split(" "), line.split("|")))
        for bar in bars:
            if len(bar) == 1:
                chords += [Chord(bar[0]) for _ in range(4)]
            elif len(bar) == 2:
                for i in range(2):
                    chords += [Chord(bar[i]) for _ in range(2)]
            elif len(bar) == 4:
                for i in range(4):
                    chords += Chord(bar[i])
            else:
                raise(NotImplementedError(f"unknown bar {bar}"))

mutators = [
    PitchMutation(0.5),
    IntroduceFlagoletOrOpenString(0.05),
    ChangeOctaveMutator(0.1),
    IntroduceTriplet(0.05),
]

repair_operators = [
    OneOctaveMutator(1.0)
]

for _ in range(num_of_iterations):

    problem = WalkingBassProblem(
        population_size=200,
        max_iteration=1,
        max_stale_iterations=50,
        crossover_probability=0.2,
        mutators=mutators,
        offspringPercentage=0.6,
        input_chords=chords,
        mutation_probability=0.4,
        repair_operators=repair_operators
    )

    result = problem.run()

    solution = result[1]

    notes = []
    for i, n in enumerate(solution.notes):
        if i < len(solution.notes) - 1 and n.note.pitch.midi == solution.notes[i+1].note.pitch.midi and solution.notes[i+1].is_first:
            notes.append(Note(n.note, n.chord, True, n.on_beat, n.scale, n.is_first))
        else:
            notes.append(n)

    solution = Solution(notes)
    fitness = problem.fitness_score(solution)
    task_name = file.split("/")[-1][:-4]
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    result_file_name = f"../results/{task_name}_{int(fitness)}_fitness_{dt_string}.mxl"



    # plt.plot(result[3])
    # plt.ylabel('wartość kary')
    # plt.xlabel('numer epoki')
    # plt.savefig('example_fitness.pdf')

    solution.print(result_file_name)
