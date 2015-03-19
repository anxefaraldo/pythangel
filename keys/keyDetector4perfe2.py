#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This script estimates the key of all the songs contained in a folder, and \n
performs an evaluation of its results according to the MIREX context.

Ángel Faraldo, Nov 2014.
"""

# IO
# ==
import sys

try:
    audio_folder = sys.argv[1]
except:
    audio_folder = "/Users/angel/GoogleDrive/EDM/EDM_Collections/KEDM_wav"
    print "-------------------------------"
    print "Analysis folder NOT provided."
    print "Analysing contents in:"
    print audio_folder
    print "If you want to analyse a different folder you should type:"
    print "filename.py <route to folder with audio and annotations in filename>"
    print "-------------------------------"

# LOAD MODULES
# ============
import os
import essentia as e
import essentia.standard as estd
import numpy as np
import csv
from time import time as tiempo


# WHAT TO ANALYSE
# ===============
# comma separated list: {'KF100', KF1000', 'GSANG', 'ENDO100'}
collection = ['GSANG', 'KF100', 'KF1000']
# comma separated list: {'edm', 'non-edm'}
genre = ['edm']
# comma separated list: {'major', 'minor'}
modality = ['major', 'minor']
# Limit the analysis to n RANDOM songs. 0 analyses all the collection:
limit_analysis = 0

# retrieve filenames according to the desired settings...
allfiles = os.listdir(audio_folder)
if '.DS_Store' in allfiles: 
    allfiles.remove('.DS_Store')

for item in collection:
    collection[collection.index(item)] = ' > ' + item + '.'

for item in genre:
    genre[genre.index(item)] = ' < ' + item + ' > '

for item in modality:
    modality[modality.index(item)] = ' ' + item + ' < '

analysis_files = []
for item in allfiles:
    if any(e1 for e1 in collection if e1 in item):
        if any(e2 for e2 in genre if e2 in item):
            if any(e3 for e3 in modality if e3 in item):
                analysis_files.append(item)

song_instances = len(analysis_files)
print song_instances, 'songs matching the selected criteria:'
print collection, genre, modality

if limit_analysis == 0:
    pass
elif limit_analysis < song_instances:
    analysis_files = sample(analysis_files, limit_analysis)
    print "taking", limit_analysis, "random samples...\n"


# PARAMETERS
# ==========
# Ángel 
analysis_portion = 0 # in seconds. 0 == full track
shift_spectrum = True
spectral_whitening = True
verbose = True
# global
sample_rate = 44100
window_size = 4096 # 32768
hop_size = window_size
window_type = 'hann'
min_frequency = 25
max_frequency = 3500
# spectral peaks
magnitude_threshold = 0.0001
max_peaks = 60
# hpcp
band_preset = False
split_frequency = 250 # only used with band_preset=True
harmonics = 4
non_linear = True
normalize = True
reference_frequency = 440
size = 36
weight_type = "squaredCosine" # none, cosine or squaredCosine
weight_window_size = 1 # in semitones
# key detector
num_harmonics = 4
profile_type = 'shaath'
slope = 0.6 # doesn't seem to make any difference!
use_polyphony = False
use_three_chords = False
# self-derived
tuning_resolution = (size / 12)
    
    
    
# ANALYSIS
# ========
print "\nANALYSING..."

# create temporary directory and unique time identifier
# uniqueTime = str(int(tiempo()))
# temp_folder = os.getcwd()+'/Estimations'+uniqueTime
# os.mkdir(temp_folder)
csvFile = open('csvResults.csv', 'w')
lineWriter = csv.writer(csvFile, delimiter=',')
""""""
# retrieve filenames from folder
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles: 
    soundfiles.remove('.DS_Store')

""""""
if verbose: 
    print "\nestimation of individual songs:" 
    print "-------------------------------" 
for item in analysis_files:
    loader = estd.MonoLoader(filename=audio_folder+'/'+item,
    						 sampleRate=sample_rate)
    cut    = estd.FrameCutter(frameSize=window_size, 
                              hopSize=hop_size)
    window = estd.Windowing(size=window_size,
                            type=window_type)
    rfft   = estd.Spectrum(size=window_size)
    sw     = estd.SpectralWhitening(maxFrequency=max_frequency, 
                                    sampleRate=sample_rate)
    speaks = estd.SpectralPeaks(magnitudeThreshold=magnitude_threshold,
                                maxFrequency=max_frequency,
                                minFrequency=min_frequency,
                                maxPeaks=max_peaks,
                                sampleRate=sample_rate)
    hpcp   = estd.HPCP(bandPreset=band_preset, 
                       harmonics=harmonics, 
                       maxFrequency=max_frequency, 
                       minFrequency=min_frequency,
                       nonLinear=non_linear,
                       normalized=normalize,
                       referenceFrequency=reference_frequency,
                       sampleRate=sample_rate,
                       size=size,
                       splitFrequency=split_frequency,
                       weightType=weight_type,
                       windowSize=weight_window_size)
    key    = estd.Key(numHarmonics=num_harmonics, 
                      pcpSize=size,
                      profileType=profile_type,
                      slope=slope, 
                      usePolyphony=use_polyphony, 
                      useThreeChords=use_three_chords)
    audio = loader()
    duration = len(audio)
    number_of_frames = duration / hop_size		
    chroma = []
    for bang in range(number_of_frames):
        spek = rfft(window(cut(audio)))
        p1, p2 = speaks(spek)
        if spectral_whitening:
            p2 = sw(spek, p1, p2)
        chroma.append(hpcp(p1,p2))
    chromean = [0] * size
    for vector in chroma:
        chromean = np.add(chromean,vector)
    max_val = np.max(chromean)
    if max_val <= 0:
        max_val = 1
    chromean = np.divide(chromean,max_val)
    if shift_spectrum:
        max_val_index = np.where(chromean==1)
        max_val_index = max_val_index[0][0] % tuning_resolution
        shiftDistance = 0
        if max_val_index > (tuning_resolution / 2):
            shiftDistance = tuning_resolution - max_val_index
        else: 
            shiftDistance = max_val_index
        chromean = np.roll(chromean, shiftDistance)
    estimation = key(chromean.tolist())
    result = estimation[0] + ' ' + estimation[1]
    ground_truth = item[item.find(' = ')+3:item.rfind(' < ')]
    title = item[:item.rfind(' = ')]
    if verbose : print item[:15]+'...     ', result
    # add line to csv file
    chromean = list(chromean)
    lineWriter.writerow([title, ground_truth, chromean, result])

csvFile.close() 