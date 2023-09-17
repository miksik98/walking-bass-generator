import music21

from Chord import Chord
from Scale import Scale


class Note:

    def __init__(self, note: music21.note.Note, chord: Chord, anticipates_next: bool, on_beat: bool, scale: Scale, is_first: bool):
        self.note = note
        self.chord = chord
        self.anticipates_next = anticipates_next
        self.on_beat = on_beat
        self.scale = scale
        self.is_first = is_first

    def __str__(self):
        return f"{self.note.pitch} {self.note.quarterLength}"
