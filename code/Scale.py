from enum import Enum

class ScaleCharacter(Enum):
    TONIC = 1
    DOMINANT = 2

class Scale:

    def __init__(self, schema, name, priority, character=None):
        self.schema = schema
        self.name = name
        self.priority = priority
        self.character = character

    def has_dominant_character(self):
        return self.character == ScaleCharacter.DOMINANT

    def has_tonic_character(self):
        return self.character == ScaleCharacter.TONIC

    def contains(self, schema):
        return all(x in self.schema for x in schema)

    def is_related_with(self, scale, diff):
        length = len(scale.schema)
        if length != len(self.schema) or diff not in self.schema:
            return False

        place = self.schema.index(diff)

        compare = list(map(lambda x: x-diff, self.schema[place:length]))
        compare += list(map(lambda x: 12-diff+x, self.schema[0:place]))
        return compare == scale.schema

    def __repr__(self):
        return self.name




ionian = Scale([0, 2, 4, 5, 7, 9, 11], "ionian", 20, ScaleCharacter.TONIC)
dorian = Scale([0, 2, 3, 5, 7, 9, 10], "dorian", 20, ScaleCharacter.TONIC)
phrygian = Scale([0, 1, 3, 5, 7, 9, 10], "phrygian", 20, ScaleCharacter.TONIC)
lydian = Scale([0, 2, 4, 6, 7, 9, 11], "lydian", 20, ScaleCharacter.TONIC)
mixolydian = Scale([0, 2, 4, 5, 7, 9, 10], "mixolydian", 20, ScaleCharacter.DOMINANT)
aeloian = Scale([0, 2, 3, 5, 7, 8, 10], "aeolian", 20, ScaleCharacter.TONIC)
locrian = Scale([0, 1, 3, 5, 6, 8, 10], "locrian", 20, ScaleCharacter.DOMINANT)

melodic_minor = Scale([0, 2, 3, 5, 7, 9, 11], "melodic minor", 20, ScaleCharacter.TONIC)
dorian_b2 = Scale([0, 1, 3, 5, 7, 9, 10], "dorian b2", 20, ScaleCharacter.TONIC)
lydian_aug = Scale([0, 2, 4, 6, 8, 9, 11], "lydian augmented", 20, ScaleCharacter.TONIC)
lydian_dominant = Scale([0, 2, 4, 6, 7, 9, 10], "lydian dominant", 20, ScaleCharacter.DOMINANT)
mixolydian_b6 = Scale([0, 2, 4, 5, 7, 8, 10], "mixolydian b6", 20, ScaleCharacter.DOMINANT)
locrian_sharp2 = Scale([0, 2, 3, 5, 6, 8, 10], "locrian #2", 20, ScaleCharacter.DOMINANT)
altered = Scale([0, 1, 3, 4, 6, 8, 10], "altered", 20, ScaleCharacter.DOMINANT)

whole_tone = Scale([0, 2, 4, 6, 8, 10], "whole tone", 5, ScaleCharacter.DOMINANT)
whole_half = Scale([0, 2, 3, 5, 6, 8, 9, 11], "whole half", 5, ScaleCharacter.DOMINANT)
half_whole = Scale([0, 1, 3, 4, 6, 7, 9, 10], "half whole", 5, ScaleCharacter.DOMINANT)

pentatonic_major = Scale([0, 2, 4, 7, 9], "major pentatonic", 2)
pentatonic_minor = Scale([0, 3, 5, 7, 10], "minor pentatonic", 2)

harmonic_diminished = Scale([0, 1, 3, 4, 6, 8, 9], "harmonic diminished", 5)

dorian_sharp4 = Scale([0, 2, 3, 6, 7, 9, 10], "dorian #4", 5, ScaleCharacter.TONIC)
locrian_sharp6 = Scale([0, 1, 3, 5, 6, 9, 10], "locrian #6", 5, ScaleCharacter.DOMINANT)
ionian_aug = Scale([0, 2, 4, 6, 7, 9, 11], "ionian augmented", 5, ScaleCharacter.TONIC)
double_harmonic = Scale([0, 1, 4, 5, 7, 8, 11], "double harmonic", 5, ScaleCharacter.TONIC)
phrygian_sharp3 = Scale([0, 1, 4, 5, 7, 8, 10], "phrygian #3", 5, ScaleCharacter.DOMINANT)

harmonic_major = Scale([0, 2, 4, 5, 7, 8, 11], "harmonic major", 5, ScaleCharacter.TONIC)
lydian_sharp2 = Scale([0, 3, 4, 6, 7, 9, 11], "lydian #2", 5, ScaleCharacter.TONIC)
neapolitan_major = Scale([0, 1, 3, 5, 7, 9, 11], "neapolitan major", 5, ScaleCharacter.TONIC)
neapolitan_minor = Scale([0, 1, 3, 5, 7, 8, 10], "neapolitan minor", 5, ScaleCharacter.TONIC)
lydian_minor = Scale([0, 2, 4, 6, 7, 8, 10], "lydian minor", 5, ScaleCharacter.DOMINANT)
lydian_dim = Scale([0, 2, 3, 6, 7, 8, 10], "lydian diminished", 5, ScaleCharacter.TONIC)
locrian_major = Scale([0, 2, 4, 5, 6, 8, 10], "locrian major", 5, ScaleCharacter.DOMINANT)

six_tone_symmetrical1 = Scale([0, 1, 4, 5, 8, 9], "six tone symmetrical type 1", 5)
six_tone_symmetrical2 = Scale([0, 1, 4, 7, 8, 11], "six tone symmetrical type 1", 5, ScaleCharacter.TONIC)

locrian_flatflat7 = Scale([0, 1, 3, 5, 6, 8, 9], "locrian bb7", 5)
dorian_b5 = Scale([0, 2, 3, 5, 6, 9, 11], "dorian b5", 5)
mixolydian_b2 = Scale([0, 1, 4, 5, 7, 9, 11], "mixolydian b2", 5)
augmented = Scale([0, 3, 4, 6, 8, 11], "augmented", 5, ScaleCharacter.TONIC)

prometheus = Scale([0, 2, 4, 6, 9, 10], "prometheus", 5, ScaleCharacter.DOMINANT)
prometheus_neopolitan = Scale([0, 1, 4, 6, 9, 10], "prometheus neopolitan", 5, ScaleCharacter.DOMINANT)
spanish_8tone = Scale([0, 1, 3, 4, 5, 6, 8, 10], "spanish 8 tone", 3, ScaleCharacter.DOMINANT)
leading_whole_tone = Scale([0, 2, 4, 6, 8, 9, 10], "leading whole tone", 3, ScaleCharacter.DOMINANT)

minor_pentatonic1_6 = Scale([0, 3, 5, 7, 9], "pentatonic minor 6 (type 1)", 2, ScaleCharacter.TONIC)
minor_pentatonic2_6 = Scale([0, 2, 3, 7, 9], "pentatonic minor 6 (type 2)", 2, ScaleCharacter.TONIC)
minor_pentatonic_7 = Scale([0, 2, 3, 7, 10], "pentatonic minor 7", 2, ScaleCharacter.TONIC)
bali_pentatonic = Scale([0, 2, 3, 7, 8], "bali pentatonic", 2, ScaleCharacter.TONIC)
sus_pentatonic = Scale([0, 2, 5, 7, 10], "sus pentatonic", 2)
dominant_pentatonic = Scale([0, 2, 4, 7, 11], "dominant pentatonic", 2, ScaleCharacter.DOMINANT)
pentatonic_minor_b5 = Scale([0, 3, 5, 6, 10], "pentatonic minor b5", 2, ScaleCharacter.DOMINANT)
dominant_suspend = Scale([0, 2, 5, 7, 9, 10], "dominant suspend", 2, ScaleCharacter.DOMINANT)

enigmatic = Scale([0, 1, 4, 6, 8, 10, 11], "enigmatic", 2, ScaleCharacter.DOMINANT)

## TODO blues scales?

scales = [ionian, dorian, phrygian, lydian, mixolydian, aeloian, locrian,
          melodic_minor, dorian_b2, lydian_aug, lydian_dominant, mixolydian_b6, locrian_sharp2, altered,
          whole_tone, whole_half, half_whole, pentatonic_major, pentatonic_minor, harmonic_diminished,
          dorian_sharp4, locrian_sharp6, ionian_aug, double_harmonic, phrygian_sharp3, harmonic_major, lydian_sharp2,
          neapolitan_major, neapolitan_minor, lydian_minor, lydian_dim, locrian_major, six_tone_symmetrical1,
          six_tone_symmetrical2, locrian_flatflat7, dorian_b5, mixolydian_b2, augmented, prometheus,
          prometheus_neopolitan, spanish_8tone, leading_whole_tone, minor_pentatonic1_6, minor_pentatonic2_6,
          minor_pentatonic_7, bali_pentatonic, sus_pentatonic, dominant_pentatonic, pentatonic_minor_b5, enigmatic]
