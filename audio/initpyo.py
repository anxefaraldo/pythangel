from pyo import *
from random import randint

n_sines = 4

s = Server(sr=44100, nchnls=1,audio='offline').boot()
s.recordOptions(dur=5, filename='/home/angel/test_recording2.wav')
env = Adsr(attack=0.01, decay=0, sustain=1, release=0.01, dur=5, mul=1.00/n_sines)

freqs = []
sines = []

for i in range(n_sines):
    f = randint(100, 1000)
    sines.append(Sine(freq=f, mul=env).out())
    freqs.append(f)

env.play()
s.start()

print freqs
