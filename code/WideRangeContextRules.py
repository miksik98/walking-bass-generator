from Solution import Solution
from Rule import Rule
from Consts import MAXIMUM_RULE_PENALTY
from DoubleBassPitch import shift_help_pitches


class WideRangeContextRule(Rule):
    def __init__(self, solution: Solution):
        self.solution = solution


class AmbitusRule(WideRangeContextRule):
    min_ambitus = 18  # 1.5 * octave

    def check(self) -> float:
        midis = list(map(lambda x: x.note.pitch.midi, self.solution.notes))
        minimum = min(midis)
        maximum = max(midis)
        return 0 if abs(maximum - minimum) >= 18 else MAXIMUM_RULE_PENALTY


class LineShapeRule(WideRangeContextRule):
    max_one_direction = 6

    def check(self) -> float:
        notes = list(map(lambda x: x.note.pitch, self.solution.notes))
        result = 0
        direction = 0  # 0 - ascending, 1 - descending
        counter = 0
        prev_note = None
        for note in notes:
            if prev_note is not None and note > prev_note:
                if direction == 1:
                    counter = 0
                    direction = 0
                else:
                    counter += 1
            if prev_note is not None and note < prev_note:
                if direction == 0:
                    counter = 0
                    direction = 1
                else:
                    counter += 1
            if counter > self.max_one_direction:
                result += 100
        return result


class IdeasRule(WideRangeContextRule):

    def check(self) -> float:
        notes = self.solution.notes
        result = 0.0
        i = 0
        prev_pattern = None
        while i < len(notes):
            actual_pattern = []
            chord = notes[i].chord
            j = i
            while j < len(notes) and notes[j].chord == chord:
                if notes[j].on_beat:
                    pitch = notes[j].note.pitch.pitchClass
                    element = pitch - chord.bass if pitch > chord.bass else 12 - chord.bass + pitch
                    actual_pattern.append(element)
                j += 1
            if prev_pattern is not None and len(prev_pattern) == len(actual_pattern) and prev_pattern != actual_pattern:
                result += 100

            prev_pattern = actual_pattern
            i += 1
        return result


class JumpRule(WideRangeContextRule):

    def check(self) -> float:
        notes = self.solution.notes
        result = 0.0
        i = 0
        while i < len(notes):
            chord = notes[i].chord
            chord_line = [notes[i]]
            j = i
            while j + 1 < len(notes) and notes[j + 1].chord == chord:
                chord_line.append(notes[j + 1])
                j += 1
            chord_line = [c.note for c in chord_line]
            k = 0
            jumps_avg = 0.0
            while k + 1 < len(chord_line):
                jumps_avg += abs(chord_line[k].pitch.midi - chord_line[k + 1].pitch.midi) / (len(chord_line) - 1)
                k += 1
            result += jumps_avg
            i += 1
        return result


class RhythmicRule(WideRangeContextRule):

    rhythmic_percentage = 0.15

    def check(self) -> float:
        number_of_quarters = len(list(filter(lambda x: x.on_beat, self.solution.notes))) * 2
        number_of_additional_triplets = len(self.solution.notes) - number_of_quarters
        return abs(self.rhythmic_percentage - (number_of_additional_triplets / (2 * number_of_quarters))) * MAXIMUM_RULE_PENALTY


class AmbitusPerChordRule(WideRangeContextRule):

    def check(self) -> float:
        current_line = []
        current_chord = None
        result = 0.0
        contains_shift_pitch = False
        for note in self.solution.notes:
            if current_chord is None or current_chord != note.chord:
                if len(current_line) > 0 and max(current_line) - min(current_line) > 12 and not contains_shift_pitch:
                    result += 100
                if len(current_line) > 0 and max(current_line) - min(current_line) < 3 and not contains_shift_pitch:
                    result += 100
                current_chord = note.chord
                current_line = []
                contains_shift_pitch = False
            current_line.append(note.note.pitch.midi)
            contains_shift_pitch = contains_shift_pitch or note.note.pitch.midi in shift_help_pitches
        if current_chord is None or current_chord != note.chord:
            if max(current_line) - min(current_line) > 12 and not contains_shift_pitch:
                result += 100
            if max(current_line) - min(current_line) < 3 and not contains_shift_pitch:
                result += 100
        return result

class AmbitusBetweenChordRule(WideRangeContextRule):

    def check(self) -> float:
        current_note = None
        current_chord = None
        result = 0.0
        for note in self.solution.notes:
            if current_chord is not None and current_note is not None and current_chord != note.chord and abs(current_note - note.note.pitch.midi) > 5:
                result += 100
            current_note = note.note.pitch.midi
            current_chord = note.chord
        return result



wide_range_context_rules = [JumpRule, AmbitusRule, LineShapeRule, IdeasRule, RhythmicRule]
