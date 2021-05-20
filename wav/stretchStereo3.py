import numpy as np
import os
from paulstretch_stereo3 import *

try:
    folder = sys.argv[1]
    os.chdir(folder)
    tracks = os.listdir(folder)
    durations = []
    for track in tracks:
        if '.wav' in track:
            print('OBTAINING', track)
            dur = length_wav(track)
            durations.append(dur)

    final_duration = 300  # np.max(durations) * 2

    for track in tracks:
        if '.wav' in track:
            outfilename = 'STRETCHED_' + track
            (samplerate, smp, trackdur) = load_wav(track)
            print('duration:', trackdur)
            stretch_factor = final_duration / float(trackdur)
            print(outfilename, stretch_factor)
            paulstretch(samplerate, smp, stretch_factor, 0.5, outfilename)

    print('Done!')

except IndexError:
    print("usage: script.py 'path-to-files'")
