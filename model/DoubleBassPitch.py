from music21.pitch import Pitch

g_string = Pitch(55)
d_string = Pitch(50)
a_string = Pitch(45)
e_string = Pitch(40)

lowest_pitch = e_string
highest_pitch = Pitch(72)

g_flagolet = Pitch(67)
d_flagolet = Pitch(62)
a_flagolet = Pitch(57)
e_flagolet = Pitch(52)

open_strings = [g_string, d_string, a_string, e_string]
flagolets = [g_flagolet, d_flagolet, a_flagolet, e_flagolet]
shift_help_pitches = open_strings + flagolets
