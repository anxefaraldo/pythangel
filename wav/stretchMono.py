#!/usr/bin/env python

import os
import numpy as np
from paulstretch_mono import *

try:
    folder = sys.argv[1]
    os.chdir(folder)
    tracks = os.listdir(folder)
    durations = []
    for track in tracks:
        if '.wav' in track:
             print 'OBTAINING', track
             dur = length_wav(track)
             durations.append(dur)

    final_duration = 60 * 15

    for track in tracks:
        if '.wav' in track:
            outfilename = 'STRETCHED_' + track
            (samplerate,smp,trackdur) = load_wav(track)
            print 'duration:', trackdur
            STRETCH = final_duration / float(trackdur)
            print outfilename, STRETCH
            paulstretch(samplerate, smp, STRETCH,0.5, outfilename)

    print 'Done!'

except IndexError:
    print "usage: script.py 'path-to-files'"
