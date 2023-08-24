from model.Chord import Chord
from model.ScaleRelation import ScaleRelation


class PolyChord(ScaleRelation):

    def __init__(self, lower, upper):
        self.lower = Chord(lower)
        self.upper = Chord(upper)
        self._root = self.lower.root()
        self._pitches = self.lower.pitches() + self.upper.pitches()

    def root(self) -> int:
        return self._root

    def pitches(self) -> list:
        return self._pitches
