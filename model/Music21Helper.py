class Music21Helper:

    @staticmethod
    def to_pitch_class(pitch):
        if pitch is not None:
            return pitch.pitchClass
        else:
            return None

music21_helper = Music21Helper()