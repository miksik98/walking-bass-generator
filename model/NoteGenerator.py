from fractions import Fraction

from model.Chord import Chord
from model.DoubleBassPitch import lowest_pitch, highest_pitch
from model.Note import Note
import music21

from model.Scale import Scale


class NoteWithPriority:

    def __init__(self, note: Note, priority: int):
        self.note = note
        self.priority = priority


class NoteGenerator:

    def _generate_note_from_pitchClass(self, pitchClass: int, chord: Chord, on_beat: bool, length: Fraction,
                                       is_anticipated: bool, priority: int) -> list[NoteWithPriority]:
        i = 0
        result = []
        while 12 * i + pitchClass <= highest_pitch:
            actual_pitch = 12 * i + pitchClass
            if actual_pitch >= lowest_pitch:
                note = music21.note.Note(actual_pitch)
                note.quarterLength = length
                result.append(NoteWithPriority(Note(note, chord, is_anticipated, on_beat), priority))
            i += 1
        return result

    def generate(self, is_first: bool, chord: Chord, scale: Scale, on_beat: bool, length: Fraction,
                 is_anticipated: bool) -> list[
        NoteWithPriority]:
        result = []
        scale_components = []
        for chord_comp in chord.basic_components() + chord.color_tones():
            for scale_comp in list(
                    map(lambda x: x + chord.root() if x + chord.root() < 12 else x + chord.root() - 12, scale.schema)):
                if scale_comp not in chord_comp:
                    scale_components.append(scale_comp)
        other_components = []
        for comp in chord.basic_components() + chord.color_tones() + scale_components:
            for other in [i for i in range(12)]:
                if other not in comp:
                    other_components.append(other)

        if is_first:
            for component in chord.basic_components():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 10)
            for component in chord.color_tones():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 2)
            for component in scale_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 2)
            for component in other_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 1)
        elif on_beat:
            for component in chord.basic_components():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 10)
            for component in chord.color_tones():
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 4)
            for component in scale_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 3)
            for component in other_components:
                result += self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 1)
        elif length < Fraction(1):
            for component in [i for i in range(12)]:
                result += (
                    self._generate_note_from_pitchClass(component, chord, on_beat, length, is_anticipated, 1))
        return result


note_generator = NoteGenerator()
