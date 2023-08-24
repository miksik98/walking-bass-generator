from music21.harmony import ChordSymbol
from Music21Helper import music21_helper
from model.ScaleRelation import ScaleRelation


class Chord(ScaleRelation):

    def __init__(self, symbol):

        self.symbol = symbol

        if len(symbol) > 1 and symbol[1] == 'b':
            symbol = symbol[0] + '-' + symbol[2:]

        # if 'sus' in symbol:
        #     self._pitches = list(map(lambda x: x.pitchClass, symbol.pitches))
        #     self.bass = symbol.bass().pitchClass
        #     self._root = symbol.root().pitchClass
        #     self.third = music21_helper.to_pitch_class(symbol.third)
        #     self.fifth = music21_helper.to_pitch_class(symbol.fifth)
        #     self.seventh = music21_helper.to_pitch_class(symbol.seventh)

        symbol = ChordSymbol(symbol)
        self._pitches = list(map(lambda x: x.pitchClass, symbol.pitches))
        self.bass = symbol.bass().pitchClass
        self._root = symbol.root().pitchClass
        self.third = music21_helper.to_pitch_class(symbol.third)
        self.fifth = music21_helper.to_pitch_class(symbol.fifth)
        self.seventh = music21_helper.to_pitch_class(symbol.seventh)
        self.second = music21_helper.to_pitch_class(symbol.getChordStep(2)) if '2' in self.symbol else None
        self.ninth = music21_helper.to_pitch_class(symbol.getChordStep(2)) if '9' in self.symbol else None
        self.fourth = music21_helper.to_pitch_class(symbol.getChordStep(4)) if '4' in self.symbol else None
        self.eleventh = music21_helper.to_pitch_class(symbol.getChordStep(4)) if '11' in self.symbol else None
        self.sixth = music21_helper.to_pitch_class(symbol.getChordStep(6)) if '6' in self.symbol else None
        self.thirteenth = music21_helper.to_pitch_class(symbol.getChordStep(6)) if '13' in self.symbol else None

    def root(self) -> int:
        return self._root

    def pitches(self) -> list:
        return self._pitches

    def get_common_scale_with(self, chord):
        result = []
        diff = abs(self.root() - chord.root())
        if self.root() > chord.root():
            diff = 12 - diff
        chord_related_scales = chord.related_scales()
        for scale in self.related_scales():
            for s in chord_related_scales:
                if scale.is_related_with(s, diff):
                    result.append(scale)
        return list(set(result))

    def is_major(self):
        if self.third is None:
            return None
        diff = abs(self.third - self.root())
        return diff == 4 if self.third > self.root() else diff == 8

    def is_diminished(self):
        if self.fifth is None:
            return None
        return abs(self.fifth - self.root()) == 6

    def is_half_diminished(self):
        return self.is_diminished() and self.has_minor_seventh()

    def has_minor_seventh(self):
        if self.seventh is None:
            return None
        diff = abs(self.seventh - self.root())
        return diff == 10 if self.seventh > self.root() else diff == 2

    def basic_components(self):
        return [element for element in
                [self.root(), self.second, self.third, self.fourth, self.fifth, self.sixth, self.seventh] if
                element is not None]

    def color_tones(self):
        return [element for element in [self.ninth, self.eleventh, self.thirteenth] if element is not None]

    def tritone_substitute_components(self):
        return [element + 6 if element < 6 else element - 6 for element in self.basic_components()]

    def is_sus(self):
        return self.third is None

    def has_not_basic_component_in_bass(self):
        return self.bass not in self.basic_components()

    def is_classic_dominant_relation_with(self, chord):
        return self.root() + 5 == chord.root() if self.root() < 5 else self.root() - 7 == chord.root()

    def is_substitute_dominant_relation_with(self, chord):
        return self.root() - 1 == chord.root() if self.root() != 0 else chord.root() == 11

    def is_deceptive_dominant_relation_with(self, chord):
        return self.root() + 1 == chord.root() if self.root() != 11 else chord.root() == 0

    def is_backdoor_dominant_relation_with(self, chord):
        return self.root() + 2 == chord.root() if self.root() < 10 else self.root() - 10 == chord.root()

    def is_in_dominant_relation_with(self, chord):
        if self.has_minor_seventh() and (self.is_major() or self.is_sus()):
            classic = self.is_classic_dominant_relation_with(chord)
            substitute = self.is_substitute_dominant_relation_with(chord)
            deceptive = self.is_deceptive_dominant_relation_with(chord)
            backdoor = self.is_backdoor_dominant_relation_with(chord)
            return classic or substitute or deceptive or backdoor
        elif self.is_diminished():
            return self.root() + 1 == chord.root if self.root() != 11 else chord.root() == 0
        else:
            return False

    def is_in_alt_subdominant_relation_with(self, chord):
        if self.has_minor_seventh() and self.is_major():
            lower_vi = self.root() + 4 == chord.root() if self.root() < 8 else self.root() - 8 == chord.root()
            ii = self.root() - 2 == chord.root() if self.root() > 1 else self.root() + 10 == chord.root()
            return lower_vi or ii
        elif self.is_half_diminished() or (self.is_diminished() and self.seventh is None):
            i = self.root() == chord.root()
            sharped_iv = abs(self.root() - chord.root()) == 6
            return i or sharped_iv
        else:
            return False

    def is_suspend(self):
        return self.third is None

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __str__(self):
        return self.symbol


print(Chord("C7b5b9b13").thirteenth)

## chord definitions
# print(Chord("C7")) # dominant
# print(Chord("CM7")) # major
# print(Chord("Cm7")) # minor
# print(Chord("Cdim")) # diminished
# print(Chord("C+")) # augmented
# print(Chord("Csus4")) # sus without color tones
# print(Chord("C7#5#9#11b13")) # more complicated dominant
# print(Chord("Cm6")) # minor with 6
# print(Chord("Cm13")) # minor
# print(Chord("Cdim7")) # diminished chord
# print(Chord("Cm7b5")) # half-diminished
# print(Chord("C6")) # some major
# print(Chord("D/C")) # slash chords
# print(Chord("Bb7")) # flat chords
# print(Chord("F#7")) # sharp chords
# print(Chord("F7sus").pitches())# sus with color tones
