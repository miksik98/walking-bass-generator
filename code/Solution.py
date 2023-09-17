from music21 import stream, meter, key, clef
from music21.tie import Tie

from Note import Note


class Solution:
    def __init__(self, notes: list[Note]):
        self.notes = notes

    def print(self, file_name=None):
        s = stream.Score(id='mainScore')
        part = stream.Part(id='bass')
        part.append(clef.BassClef())
        s.append(meter.TimeSignature('4/4'))
        k = key.Key("C")
        part.append(k)
        prev_chord = None
        is_anticipated = False
        for note in self.notes:
            if prev_chord is None or prev_chord != note.chord:
                note.note.addLyric(note.chord.symbol)
            if is_anticipated:
                note.note.tie = Tie('stop')
                is_anticipated = False
            if note.anticipates_next:
                note.note.tie = Tie('start')
            part.append(note.note)
            prev_chord = note.chord
        s.insert(0, part)
        if file_name is not None:
            s.write('musicxml', fp=file_name)
        else:
            s.show()
