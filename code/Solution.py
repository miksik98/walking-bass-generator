from music21 import stream, meter, key, clef
from music21.tie import Tie

from Note import Note


class Solution:
    def __init__(self, notes: list[Note]):
        self.notes = notes

    def print(self):
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
        s.show()

# note1 = note.Note(60)
# note1.quarterLength = Fraction(1/3)
# note1 = Note(note1, Chord("C"), False, False)
# note2 = note.Note(67)
# note2.quarterLength = Fraction(2/3)
# note2 = Note(note2, Chord("C"), False, False)
# note3 = Note(note.Note(61), Chord("A7"), False, False)
# note3.note.quarterLength = Fraction(2/3)
# note4 = Note(note.Note(62), Chord("A7"), True, False)
# note4.note.quarterLength = Fraction(1/3)
#
# s = Solution([note1, note2, note3, note4,
#               Note(note.Note(62), Chord("Dm"), False, False), Note(note.Note(63), Chord("F7"), False, False)])
#
# s.print()
