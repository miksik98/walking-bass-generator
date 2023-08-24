from model.Chord import Chord
from model.Scale import Scale, lydian_dominant, locrian_sharp2
import random


def _rand_scale(scales: list[Scale]) -> Scale:
    return random.choices(scales, weights=list(map(lambda x: x.priority, scales)), k=1)[0]


class ChooseScaleAlgorithm:

    def choose(self, prev_chord: Chord, actual_chord: Chord, next_chord: Chord) -> Scale:
        actual_scales = actual_chord.related_scales()

        if actual_chord.is_in_dominant_relation_with(next_chord):
            actual_scales = list(filter(lambda x: x.has_dominant_character(), actual_scales))
        elif prev_chord.is_in_dominant_relation_with(actual_chord):
            actual_scales = list(filter(lambda x: x.has_tonic_character(), actual_scales))
        elif actual_chord.is_in_alt_subdominant_relation_with(next_chord):
            if actual_chord.root() + 4 == next_chord.root() if actual_chord.root() < 8 else actual_chord.root() - 8 == next_chord.root():
                actual_scales = [lydian_dominant]
            elif actual_chord.root() - 2 == next_chord.root() if actual_chord.root() > 1 else actual_chord.root() + 10 == next_chord.root():
                actual_scales = [lydian_dominant]
            elif actual_chord.root() == next_chord.root():
                actual_scales = [locrian_sharp2]
            elif abs(actual_chord.root() - next_chord.root()) == 6:
                actual_scales = [locrian_sharp2]
        elif prev_chord.is_in_alt_subdominant_relation_with(actual_chord):
            actual_scales = list(filter(lambda x: x.has_tonic_character(), actual_scales))
        elif len(actual_chord.get_common_scale_with(prev_chord)) != 0:
            actual_scales = actual_chord.get_common_scale_with(prev_chord)
        elif len(actual_chord.get_common_scale_with(next_chord)) != 0:
            actual_scales = actual_chord.get_common_scale_with(next_chord)

        return _rand_scale(actual_scales)


choose_scale_algorithm = ChooseScaleAlgorithm()

# print(choose_scale_algorithm.choose(Chord("Gm7"), Chord("Db7"), Chord("FM7")))
