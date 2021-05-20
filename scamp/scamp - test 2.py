from scamp import *
from random import *

s = Session(tempo=200)

cello = s.new_midi_part("m1", midi_output_device = "Arturia BeatStep")

#s.start_transcribing() # only needed if we want to generate a printed score
#
#for pitch in (45,47,48):
#   cello.play_note(pitch, 1, 0.1)
#
#s.stop_transcribing().to_score().show_xml() # end of the score


while True:
    cello.play_note(randint(50, 120), random(), random())
