#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys,os
import scipy.io.wavfile as wav
import numpy as np

replace_original = True

try:
    infolder = sys.argv[1]
except:
    print "\nUSAGE: stereo2mono_batch.py <folder to convert> OPTIONAL: <replace original file (1, 0)>\n"
    sys.exit()

if len(sys.argv) > 2:
	if sys.argv[2] == '1':
		replace_original = True

# retrieve filenames from folder:
allfiles = os.listdir(infolder)
soundfiles = []
for item in allfiles:
	if item[-4:] == '.wav':
		soundfiles.append(item)

for item in soundfiles:
	print infolder+item
	stereo_file = wav.read(infolder+'/'+item)
	audio = stereo_file[1]
	number_of_channels = len(np.shape(audio))
	sample_rate = stereo_file[0]
	print '\nConverting "' + item + '" to MONO'
	if number_of_channels == 1:
		print 'The input file is already MONO. No modifications have been made.'
	elif number_of_channels == 2:
		print 'Sample Rate =', sample_rate
		duration = len(audio)
		mono_file = np.array([0]*duration, dtype='int16')
		for i in range(duration):
			mono_file[i] = np.sum(audio[i]) * 0.5
		if replace_original:
			wav.write(infolder+'/'+item, sample_rate, mono_file)
		else:
			wav.write(infolder+'/'+item[:-4]+'_MONO.wav', sample_rate, mono_file)
		print 'File sucecssfully converted'
