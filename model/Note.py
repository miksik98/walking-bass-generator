import music21

from model.Chord import Chord


class Note:

    def __init__(self, note: music21.note.Note, chord: Chord, anticipates_next: bool, on_beat: bool):
        self.note = note
        self.chord = chord
        self.anticipates_next = anticipates_next
        self.on_beat = on_beat


