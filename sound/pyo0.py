from pyo import *

s = Server().boot()
s.setAmp(0.1)

lfo=(1)

s1 = Sine(1999, mul=lfo).out()
s1.ctrl()
s.gui(locals())