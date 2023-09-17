from fractions import Fraction

from Chord import Chord
from DoubleBassPitch import lowest_pitch, highest_pitch
from Note import Note
import music21

from Scale import Scale, ionian


class NoteWithPriority:

    def __init__(self, note: Note, priority: int):
        self.note = note
        self.priority = priority

    def __str__(self):
        return f"note={self.note},priority={self.priority}"


class NoteGenerator:

    def _generate_note_from_pitchClass(self, pitchClass: int, chord: Chord, on_beat: bool, length: Fraction,
                                       anticipates_next: bool, priority: int, scale: Scale, is_first: bool) -> list[NoteWithPriority]:
        i = 0
        result = []
        while 12 * i + pitchClass <= highest_pitch:
            actual_pitch = 12 * i + pitchClass
            if actual_pitch >= lowest_pitch:
                note = music21.note.Note(actual_pitch)
                note.quarterLength = length
                result.append(NoteWithPriority(Note(note, chord, anticipates_next, on_beat, scale, is_first), priority))
            i += 1
        return result

    def generate(self, is_first: bool, chord: Chord, scale: Scale, on_beat: bool, length: Fraction,
                 anticipates_next: bool, as_mutation: bool = False) -> list[
        NoteWithPriority]:
        result = []
        scale_components = []
        root_priority = 45 if as_mutation else 300
        for scale_comp in list(
                map(lambda x: x + chord.root() if x + chord.root() < 12 else x + chord.root() - 12, scale.schema)):
            if scale_comp not in chord.basic_components() + chord.color_tones():
                scale_components.append(scale_comp)
        scale_components = list(set(scale_components))
        other_components = [i for i in range(12) if i not in chord.basic_components() + chord.color_tones() + scale_components]

        if is_first:
            for component in chord.basic_components():
                if component == chord.root():
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, root_priority, scale, is_first)
                else:
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 30, scale, is_first)
            for component in chord.color_tones():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 3, scale, is_first)
            for component in scale_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 2, scale, is_first)
            for component in other_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 1, scale, is_first)
        elif on_beat:
            for component in chord.basic_components():
                if component == chord.root():
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, (root_priority * 2) / 3, scale, is_first)
                else:
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 30, scale, is_first)
            for component in chord.color_tones():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 2, scale, is_first)
            for component in scale_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 5, scale, is_first)
            for component in other_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 1, scale, is_first)
        elif length < Fraction(1):
            for component in [i for i in range(12)]:
                result += (
                    self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 1, scale, is_first))
        else:
            for component in chord.basic_components():
                if component == chord.root():
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 30, scale, is_first)
                else:
                    result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 15, scale, is_first)
            for component in chord.color_tones():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 2, scale, is_first)
            for component in scale_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 5, scale, is_first)
            for component in other_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, anticipates_next, 1, scale, is_first)
        return result


note_generator = NoteGenerator()
