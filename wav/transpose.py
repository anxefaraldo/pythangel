import os
import sys
from scipy.io import wavfile
# from scikits.samplerate import resample
from samplerate import resample
import numpy as np


try:
    folder = sys.argv[1]
    os.chdir(folder)
    tracks = os.listdir(folder)
    root12of2 = 1.059463094359295
    for track in tracks:
        if '.wav' in track:
            original_file = wavfile.read(track)
            sr = original_file[0]
            waveform = original_file[1]
            """
            # convert file to mono
            channels = np.shape(waveform)[1]
            if channels > 1:
             waveform = np.sum(waveform, -1) / channels
            """
            #transposition / change of speed
            duration = len(waveform) / sr
            """
            key_indicator = int(track[4:6])
            if key_indicator % 2 == 0:
                label = (key_indicator - 2) / 2
            else:
                label = (key_indicator - 1) / 2
            """
            semitones = 12  # should be made interactive!!!!
            print '\n', track
            # print 'Label:', label
            print 'Sample Rate:', sr
            print 'Duration:', duration, 'secs.'
            print 'transposing/re-speeding file', semitones, 'semitone(s)'
            ratio = root12of2 ** -semitones
            new_duration = ratio * duration
            print 'New duration:', new_duration, 'secs.'
            new_waveform = np.array(resample(waveform, ratio, "sinc_fastest"), dtype="int16")
            # write resampled file to disk at the original sample rate:
            wavfile.write("TRANSPOSED_" + track,  sr, new_waveform)

    print '\nDone transposing files.\n'

except IndexError:
    print "usage: transpose.py 'path-to-files'"
