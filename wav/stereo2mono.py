#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys
import scipy.io.wavfile as wav
import numpy as np

replace_original = False

try:
    infile = sys.argv[1]
except:
    print "\nUSAGE: stereo2mono.py <file to convert> OPTIONAL: <replace original file (1, 0)>\n"
    sys.exit()

if len(sys.argv) > 2:
	if sys.argv[2] == '1':
		replace_original = True

stereo_file = wav.read(infile)
audio = stereo_file[1]
number_of_channels = len(np.shape(audio))
sample_rate = stereo_file[0]
if number_of_channels == 1:
	print '\n The input file is already MONO. No modifications have been made.'
elif number_of_channels == 2:
	print '\nConverting "' + infile + '" to MONO'
	print 'Sample Rate =', sample_rate
	duration = len(audio)
	mono_file = np.array([0]*duration, dtype='int16')
	for i in range(duration):
		mono_file[i] = np.sum(audio[i]) * 0.5
	if replace_original:
		wav.write(infile, sample_rate, mono_file)
	else:
		wav.write(infile[:-4]+'_MONO.wav', sample_rate, mono_file)
	print 'File sucecssfully converted'