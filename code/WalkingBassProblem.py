import random
from fractions import Fraction

from GeneticAlgorithm import GeneticAlgorithm
from Mutator import Mutator, ChangeOctaveMutator
from ChooseScaleAlgorithm import choose_scale_algorithm
from Chord import Chord
from NoteGenerator import note_generator
from Solution import Solution
from NarrowContextRules import narrow_context_rules

from WideRangeContextRules import wide_range_context_rules

class WalkingBassProblem(GeneticAlgorithm):
    def __init__(self, population_size, max_iteration, max_stale_iterations, crossover_probability,
                 mutators: list[Mutator], offspringPercentage, input_chords: list[Chord]):
        super().__init__(population_size, max_iteration, max_stale_iterations, crossover_probability, mutators,
                         offspringPercentage)
        self.input_chords = input_chords
        self.scales = []

    def generate_scale_for_id(self, chord_id: int):
        actual_chord = self.input_chords[chord_id]

        prev_chord = None
        for i in range(chord_id-1, -1, -1):
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
                    if i > 0 and self.input_chords[i-1] == chord:
                        scale = self.scales[i-1]
                    else:
                        scale = self.generate_scale_for_id(i)
                    self.scales.append(scale)
                else:
                    scale = self.scales[i]
                possible_notes = note_generator.generate(i % 4 == 0, chord, scale,
                                                         (i % 4) % 2 == 0,
                                                         Fraction(1, 1), False)
                note = random.choices([n.note for n in possible_notes], weights=[n.priority for n in possible_notes], k=1)[0]
                notes.append(note)
            return Solution(notes)

        return [generate() for _ in range(size)]

    def mutate(self, individual):
        notes = individual.notes
        result = []
        for chromosome_id in range(len(notes)):
            chromosome = notes[chromosome_id]
            for mutator in self.mutators:
                chromosome = mutator.mutate(result[:chromosome_id] + notes[chromosome_id:], chromosome_id)
            result.append(chromosome)
        return Solution(result)

    def fitness_score(self, individual):
        result = 0
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
            probabilities = [score / total_fitness for score in _scores]
            parents = random.choices(_population, weights=probabilities, k=_size)
            return parents

        return random_wheel(population, scores, size)

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_probability:
            crossover_points = [i for i in range(0, len(self.input_chords), 4) if
                                i != 0 and i != len(self.input_chords) - 1]
            crossover_point = random.choice(crossover_points)

            parent1_crossover_point = Fraction()
            parent2_crossover_point = Fraction()
            acc = 0
            for i, note in enumerate(parent1.notes):
                acc += note.note.quarterLength
                if acc == crossover_point:
                    parent1_crossover_point = i
                    break
            acc = 0
            for i, note in enumerate(parent2.notes):
                acc += note.note.quarterLength
                if acc == crossover_point:
                    parent2_crossover_point = i
                    break

            child1 = parent1.notes[:parent1_crossover_point] + parent2.notes[parent2_crossover_point:]
            child2 = parent2.notes[:parent2_crossover_point] + parent1.notes[parent1_crossover_point:]
            return Solution(child1), Solution(child2)
        else:
            return parent1, parent2


# chords = [Chord("Dm7"), Chord("Dm7"), Chord("G7"), Chord("G7"), Chord("CM7"), Chord("CM7"), Chord("A7"), Chord("A7"),
#           Chord("Dm7"), Chord("Dm7"), Chord("G7"), Chord("G7"), Chord("CM7"), Chord("CM7"), Chord("CM7"), Chord("CM7")]

chords = [Chord("F7"), Chord("F7"), Chord("F7"), Chord("F7"), Chord("Bb7"), Chord("Bb7"), Chord("Bb7"), Chord("Bb7"),
          Chord("F7"), Chord("F7"), Chord("F7"), Chord("F7"), Chord("Cm7"), Chord("Cm7"), Chord("F7"), Chord("F7"),
          Chord("Bb7"), Chord("Bb7"), Chord("Bb7"), Chord("Bb7"), Chord("Bo"), Chord("Bo"), Chord("Bo"), Chord("Bo"),
          Chord("F7"), Chord("F7"), Chord("F7"), Chord("F7"), Chord("Am7b5"), Chord("Am7b5"), Chord("D7"), Chord("D7"),
          Chord("Gm7"), Chord("Gm7"), Chord("Gm7"), Chord("Gm7"), Chord("C7"), Chord("C7"), Chord("C7"), Chord("C7"),
          Chord("F7"), Chord("F7"), Chord("Dm7"), Chord("Dm7"), Chord("Gm7"), Chord("Gm7"), Chord("C7"), Chord("C7")]

# chords = [Chord("Dm7"), Chord("Dm7"), Chord("Dm7"), Chord("Dm7"), Chord("Dm7"), Chord("Dm7"), Chord("Dm7"),Chord("Dm7")]

mutators = [
    ChangeOctaveMutator(0.5)
]

problem = WalkingBassProblem(
    population_size=200,
    max_iteration=2000,
    max_stale_iterations=100,
    crossover_probability=0.4,
    mutators=mutators,
    offspringPercentage=0.6,
    input_chords=chords
)

result = problem.run()

print(result[3][-1])
print(problem.scales)

solution = result[1]
print(problem.fitness_score(solution))

solution.print()
# for n in solution.notes:
#     print(n)
# print(problem[0])
