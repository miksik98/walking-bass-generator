from Scale import scales


class ScaleRelation:

    def root(self) -> int:
        pass

    def pitches(self) -> list:
        pass

    def _schema(self):
        result = [(pitch - self.root()) % 12 for pitch in self.pitches()]
        result.sort()
        return result

    def related_scales(self):
        return [scale for scale in scales if scale.contains(self._schema())]