"""
02-band-limited-oscs.py - Oscillators whose spectrum is kept under the Nyquist frequency.

This tutorial presents an object (misnamed LFO but it's too late
to change its name!) that implements various band-limited waveforms.
A band-limited signal is a signal that none of its partials exceeds
the nyquist frequency (sr/2).

The LFO object, despite its name, can be use as a standard oscillator,
with very high fundamental frequencies. At lower frequencies (below 20 Hz)
this object will give a true LFO with various shapes.

The "type" slider in the controller window lets choose between these
particular waveforms:

0. Saw up (default)
1. Saw down
2. Square
3. Triangle
4. Pulse
5. Bipolar pulse
6. Sample and hold
7. Modulated Sine

"""
from pyo import *

s = Server().boot()


# Various band-limited waveforms
osc = LFO(freq=1, sharp=0.5, mul=0.4).out()
osc.ctrl()

sin = Sine(freq=8000,mul=osc)

# Displays the waveform
sc = Scope(osc)

# Displays the spectrum contents
sp = Spectrum(osc)

s.gui(locals())
