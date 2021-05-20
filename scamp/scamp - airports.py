from scamp import *
import random

s = Session()

inst1 = s.new_midi_part("m1", midi_output_device="Arturia BeatStep")
inst2 = s.new_part("synth")

def player(inst, pitch, dur, wait_time):
    wait(wait_time)
    inst.play_note(pitch, [0.2, 0.8, 0.3], dur)


pitches = [36, 48, 51, 55, 64, 72, 73]
durs = [3 + x for x in range(5)]

while True:
    s.fork(player, args=[inst1, random.choice(pitches), random.choice(durs), 0.5])
    s.fork(player, args=[inst2, random.choice(pitches), random.choice(durs), random.choice(durs)])
    s.fork(player, args=[inst2, random.choice(pitches), random.choice(durs), random.choice(durs)])
    s.fork(player, args=[inst2, random.choice(pitches), random.choice(durs), random.choice(durs)])
    #s.fork(player, args=[inst1, random.choice(pitches), random.choice(durs), random.choice(durs)])
    wait_for_children_to_finish()

