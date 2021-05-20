import numpy as np
import time
import sounddevice as sd
from scipy.io.wavfile import write

# samples per second
sps = 48000

# sine wave parameters
freq_hz = 440.0
duration_s = 5.0

# NumPy processing
t_samples = np.arange(duration_s * sps)
waveform = np.sin(2 * np.pi * t_samples * freq_hz / sps)
waveform_quiet = waveform * 0.1

# play it straight away
sd.play(waveform_quiet, sps)
time.sleep(duration_s)
sd.stop()

# integer conversion ad save to file
waveform_integers = np.int16(waveform_quiet * 32767)
write("first_sine_with_numpy.wav", sps, waveform_integers)

# this series of tutorials also cover how to amplitude and frequency-modulate
# the signal. At https://github.com/akey7
