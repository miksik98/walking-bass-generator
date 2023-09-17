import random
from fractions import Fraction

from music21 import note

from Note import Note
from DoubleBassPitch import highest_pitch, lowest_pitch, shift_help_pitches
from NoteGenerator import note_generator


class Mutator:

    def __init__(self, probability):
        self.probability = probability

    def condition(self, individual, chromosome_id):
        raise NotImplemented()

    def mutate_chromosome(self, chromosome):
        raise NotImplemented()

    def mutate(self, individual, chromosome_id):
        return self.mutate_chromosome(individual[chromosome_id]) if self.condition(individual, chromosome_id) and \
                                                                    random.random() < self.probability \
            else [individual[chromosome_id]]


class OneOctaveMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        # if random.random() < self.probability and chromosome_id > 0:
        if chromosome_id > 0:
            previous = individual[chromosome_id - 1].note.pitch.midi
            notes = [chromosome.note.pitch.midi + i for i in range(-24, 24, 12)]
            notes = [n for n in notes if lowest_pitch <= n <= highest_pitch]
            notes.sort(key=lambda x: abs(x - previous))
            n = note.Note(notes[0])
            n.quarterLength = chromosome.note.quarterLength
            return [Note(n, chromosome.chord, chromosome.anticipates_next, chromosome.on_beat, chromosome.scale, chromosome.is_first)]
        return [chromosome]


class ChangeOctaveMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        if random.random() < self.probability and chromosome_id > 0 and individual[chromosome_id - 1].chord == chromosome.chord:
            previous = individual[chromosome_id - 1].note.pitch.midi
            notes = [previous + 12, previous - 12]
            notes = [n for n in notes if lowest_pitch <= n <= highest_pitch]
            n = note.Note(random.choice(notes))
            n.quarterLength = chromosome.note.quarterLength
            return [Note(n, chromosome.chord, chromosome.anticipates_next, chromosome.on_beat, chromosome.scale, chromosome.is_first)]
        return [chromosome]


class PitchMutation(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        probability = self.probability / 5 if chromosome.note.quarterLength == Fraction(1) else self.probability
        if random.random() < probability and chromosome_id > 0 and not chromosome.is_first and not chromosome.on_beat:
            notes = note_generator.generate(chromosome.is_first, chromosome.chord, chromosome.scale, chromosome.on_beat,
                                           chromosome.note.quarterLength, chromosome.anticipates_next, True)
            return [random.choices([n.note for n in notes], weights=[n.priority for n in notes], k=1)[0]]
        return [chromosome]


class IntroduceFlagoletOrOpenString(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        if random.random() < self.probability and chromosome_id > 0:
            previous = individual[chromosome_id - 1].note.pitch.midi
            notes = note_generator.generate(chromosome.is_first, chromosome.chord, chromosome.scale, chromosome.on_beat,
                                           chromosome.note.quarterLength, chromosome.anticipates_next, True)
            notes = [n for n in notes if n.note.note.pitch.midi in shift_help_pitches and abs(n.note.note.pitch.midi-previous) <= 12]
            return [random.choices([n.note for n in notes], weights=[n.priority for n in notes], k=1)[0]]
        return [chromosome]


class IntroduceTriplet(Mutator):

    mutation_options = [
        [Fraction(2, 3), Fraction(1, 3)],
        [Fraction(1, 3), Fraction(2, 3)],
        [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]
    ]

    weights = [10, 5, 10]

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        probability = self.probability / 5 if chromosome.is_first or chromosome.on_beat else self.probability
        if random.random() < probability and chromosome.note.quarterLength == Fraction(1):
            mutation_option = random.choices(self.mutation_options, weights=self.weights, k=1)[0]
            result = []
            for fraction in mutation_option:
                if len(result) == 0:
                    n = note.Note(chromosome.note.pitch.midi)
                    n.quarterLength = fraction
                    result.append(Note(n, chromosome.chord, False, chromosome.on_beat, chromosome.scale, chromosome.is_first))
                else:
                    notes = note_generator.generate(False, chromosome.chord, chromosome.scale,
                                                    False,
                                                    fraction, False, True)
                    result.append(random.choices([n.note for n in notes], weights=[n.priority for n in notes], k=1)[0])
            return result
        return [chromosome]
