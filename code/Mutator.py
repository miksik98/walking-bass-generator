import random

from music21 import note

from Note import Note
from DoubleBassPitch import highest_pitch, lowest_pitch


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
            else individual[chromosome_id]


class ChangeOctaveMutator(Mutator):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, individual, chromosome_id):
        chromosome = individual[chromosome_id]
        if random.random() < self.probability and chromosome_id > 0:
            previous = individual[chromosome_id - 1].note.pitch.midi
            notes = [chromosome.note.pitch.midi + i for i in range(-24, 24, 12)]
            notes = [n for n in notes if lowest_pitch <= n <= highest_pitch]
            notes.sort(key=lambda x: abs(x - previous))
            # notes.sort(key=lambda x: abs(x - previous) + abs(
            #     x - individual[chromosome_id + 1].note.pitch.midi) if chromosome_id < len(individual) - 1 else abs(
            #     x - previous))
            return Note(note.Note(notes[0]), chromosome.chord, chromosome.anticipates_next, chromosome.on_beat)
        return chromosome

# pomysły:
#   * mutacja skali
#   * mutacja dźwięku
#   * wprowadzenie pustej struny / flażoletu g
#   * mutacja rytmiczna - wprowadzenie jednej z trzech grup triolowych
#   * możliwość antycypacji kolejnej wartości (wyprzedzanie, legowanie nut)
#   * uproszczenia rytmiczne - usuwanie jednej z triol lub po prostu wstawianie ćwierćnuty zamiast całego zagęszczenia
#   * ????
