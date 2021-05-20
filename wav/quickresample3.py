from scipy.io import wavfile
from scipy.signal import resample
import numpy as np

root12of2 = np.float128(1.059463094359295)

file_name = '/Users/angelfaraldo/Desktop/a440.wav'

original_file = wavfile.read(file_name)

sr = original_file[0]
waveform = original_file[1]

print('initial sampling_rate...', sr)

semitones = -1

new_rate = sr * (root12of2**-semitones)

new_waveform = np.array(resample(waveform, new_rate), dtype=int16)

print('applying a resampling value of', new_rate)

# write resampled file to disk at the original sample rate
wavfile.write(file_name + '_resampled.wav', sr, new_waveform)
