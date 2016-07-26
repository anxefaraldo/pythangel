from fm21 import *
from sys import platform


if platform == 'darwin':
    corpus = load_midi_corpus('/Users/angel/Desktop/bass2d/corpus')
else:
    corpus = load_midi_corpus('/home/angel/Git/house-harmonic-filler/corpus')


f = load_midfile(0, corpus)

"""
Make a simple decission tree to determine the key of bassline loops.

a) count number of bars, and make ure they are complete.
b) look at the first note of the loop. this is the one with more weight.
c) calculate possible modes for the whole loop, and per bar. produce output with all possible options.
d) also look at repeated and long notes. Assign them extra weight. Have a look at Narmour?
"""

