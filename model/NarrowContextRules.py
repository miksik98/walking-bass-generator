from model.DoubleBassPitch import shift_help_pitches, g_string
from model.Note import Note
from model.Rule import Rule


class NarrowContextRule(Rule):
    def __init__(self, prev_prev_note: Note, prev_note: Note, actual_note: Note, next_note: Note):
        self.prev_prev_note = prev_prev_note
        self.prev_note = prev_note
        self.actual_note = actual_note
        self.next_note = next_note


class LeadingToneRule(NarrowContextRule):

    def check_leading(self) -> float:
        pass

    def check(self) -> float:
        if self.actual_note.chord != self.next_note.chord:
            self.check_leading()
        return 0


class RootOfNextRule(LeadingToneRule):

    def check_leading(self) -> float:
        return 10 if self.actual_note.note.pitch.pitchClass == self.next_note.chord.bass() else 0


class ClosestMoveRule(LeadingToneRule):

    def check_leading(self) -> float:
        return abs(self.actual_note.note.pitch.midi - self.next_note.note.pitch.midi)


class FourthDownRule(LeadingToneRule):

    def check_leading(self) -> float:
        actual_midi = self.actual_note.note.pitch.midi
        next_midi = self.next_note.note.pitch.midi
        return 10 if actual_midi > next_midi and actual_midi - next_midi == 5 else 0


class PrimeLeadingRule(LeadingToneRule):

    def check_leading(self) -> float:
        return 0 if self.actual_note.note.pitch.pitchClass == self.actual_note.chord.bass else 1


class FunctionalHarmonyRule(LeadingToneRule):

    def check_leading(self) -> float:
        actual_pitch_class = self.actual_note.note.pitch.pitchClass
        actual_chord = self.actual_note.chord
        next_chord = self.next_note.chord
        if actual_chord.is_classic_dominant_relation_with(
                next_chord) or actual_chord.is_substitute_dominant_relation_with(next_chord):
            return 0 if actual_chord.third == actual_pitch_class or actual_chord.seventh == actual_pitch_class else 5
        if actual_chord.is_deceptive_dominant_relation_with(
                next_chord) or actual_chord.is_backdoor_dominant_relation_with(next_chord):
            return 0 if actual_pitch_class in actual_chord.basic_components() else 5
        return 0


class SurroundingsLeadingRule(LeadingToneRule):

    def check_leading(self) -> float:
        prev = self.prev_note.note.pitch.midi
        actual = self.actual_note.note.pitch.midi
        next = self.next_note.note.pitch.midi
        return 0 if abs(prev - next) == 1 and abs(
            actual - next) == 1 and prev != actual and self.prev_note.note.quarterLength < 1 and self.actual_note.note.quarterLength < 1 else 2


class OnBeatRule(NarrowContextRule):

    def check(self) -> float:
        if self.actual_note.on_beat:
            if self.prev_note.chord != self.actual_note.chord and self.actual_note.chord.is_sus() or self.actual_note.chord.has_not_basic_component_in_bass():
                return 1000 if self.actual_note.note.pitch.pitchClass != self.actual_note.chord.bass else 0
            elif self.prev_note.chord != self.actual_note.chord:
                return 10 if self.actual_note.note.pitch.pitchClass != self.actual_note.chord.bass else 0
            else:
                return 10 if self.actual_note.note.pitch.pitchClass not in self.actual_note.chord.basic_components() else 0
        return 0


class UseOfTritoneSubstitutionsRule(NarrowContextRule):

    def check(self) -> float:
        if self.actual_note.chord.is_classic_dominant_relation_with(
                self.next_note.chord) or self.actual_note.chord.is_substitute_dominant_relation_with(
            self.next_note.chord):
            components = self.actual_note.chord.tritone_substitute_components()
            if self.actual_note.note.pitch.pitchClass in components:
                return 0
            elif self.prev_note.chord == self.actual_note.chord and self.prev_note.note.pitch.pitchClass in components:
                return 0
            elif self.prev_note.chord == self.actual_note.chord and self.prev_note.chord == self.actual_note.chord and self.prev_note.note.pitch.pitchClass in components:
                return 0
            else:
                return 5
        return 0


class SecondaryDominantsRule(NarrowContextRule):

    def check(self) -> float:
        if self.actual_note.chord == self.next_note.chord:
            actual_note = self.actual_note.note.pitch.midi
            next_note = self.next_note.note.pitch.midi
            is_fifth_diff = actual_note - next_note == 7 if actual_note > next_note else next_note - actual_note == 7
            return 0 if is_fifth_diff else 1
        return 0


class ColorTonesRule(NarrowContextRule):

    def check(self) -> float:
        if self.prev_note.chord == self.actual_note.chord:
            chord = self.prev_note.chord
            prev_pitch = self.prev_note.note.pitch.pitchClass
            actual_pitch = self.actual_note.note.pitch.pitchClass
            if prev_pitch == chord.ninth:
                return 0 if actual_pitch == chord.fifth or actual_pitch == chord.root else 2
            if prev_pitch == chord.eleventh:
                return 0 if actual_pitch == chord.third else 2
            if prev_pitch == chord.thirteenth:
                return 0 if actual_pitch == chord.fifth or actual_pitch == chord.root else 2
        return 0


class TripletsRule(NarrowContextRule):

    def check(self) -> float:
        if self.next_note.on_beat and self.actual_note.note.quarterLength < 1:
            if self.prev_prev_note.on_beat and self.prev_note.note.quarterLength < 1:
                chord = self.actual_note.chord
                actual_pitch = self.actual_note.note.pitch
                return 0 if actual_pitch.pitchClass in chord.basic_components() or abs(
                    actual_pitch.midi - self.next_note.note.pitch.midi) or actual_pitch in shift_help_pitches else 1


class JumpRule(NarrowContextRule):

    def check(self) -> float:
        actual_pitch = self.actual_note.note.pitch.midi
        prev_pitch = self.prev_note.note.pitch.midi
        if abs(actual_pitch - prev_pitch) > 12 and (actual_pitch.midi > g_string or prev_pitch > g_string) and (
                actual_pitch not in shift_help_pitches or prev_pitch not in shift_help_pitches):
            return 20
        return 0


narrow_context_rules = [RootOfNextRule, ClosestMoveRule, FourthDownRule, PrimeLeadingRule, FunctionalHarmonyRule,
                        SurroundingsLeadingRule, OnBeatRule, UseOfTritoneSubstitutionsRule, SecondaryDominantsRule,
                        ColorTonesRule, TripletsRule, JumpRule]
