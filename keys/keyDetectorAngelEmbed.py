#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This script estimates the key of the songs contained in a folder,
and performs an evaluation of its results according to the MIREX 
standard. It expects that the Ground-Truth is contained within
the filename.

Ángel Faraldo, March 2015.
"""

# IO
# ==
import sys

try:
    audio_folder = sys.argv[1]
except:
    audio_folder = "/Users/angel/GoogleDrive/EDM/EDM_Collections/KEDM_mono_wav"
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
# import numpy as np
from random import sample
from keymods.keytools import *
from time import time as tiempo


# WHAT TO ANALYSE
# ===============
# comma separated list: {'KF100', KF1000', 'GSANG', 'ENDO100', 'DJTECHTOOLS60'}
collection = ['GSANG', 'ENDO100', 'DJTECHTOOLS60']
# comma separated list: {'edm', 'non-edm'}
genre = ['edm']
# comma separated list: {'major', 'minor'}
modality = ['major', 'minor']
# Limit the analysis to n RANDOM songs. 0 analyses all the collection:
limit_analysis = 0


# PARAMETERS
# ==========
# ángel:
avoid_edges = 10 # % of duration at the beginning and end that is not analysed.
shift_spectrum = True
spectral_whitening = True
verbose = True
results_to_file = True

# global
sample_rate = 44100
window_size = 4096
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
hpcp_size = 36
weight_type = "squaredCosine" # {none, cosine or squaredCosine}
weight_window_size = 1 # semitones

# key detector
num_harmonics = 4
profile_type = 'shaath'
slope = 0.6 # doesn't seem to make any difference!
use_polyphony = False
use_three_chords = False

#create directory and unique time identifier
if results_to_file:
    uniqueTime = str(int(tiempo()))
    temp_folder = '/Users/angel/KeyDetection_'+uniqueTime
    os.mkdir(temp_folder)

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

# ANALYSIS
# ========


if verbose:
    print "ANALYSING INDIVIDUAL SONGS..."
    print "============================" 
 
total = []
matrix = 24 * 24 * [0]
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
                       size=hpcp_size,
                       splitFrequency=split_frequency,
                       weightType=weight_type,
                       windowSize=weight_window_size)
    key    = estd.Key(numHarmonics=num_harmonics, 
                      pcpSize=hpcp_size,
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
        p1, p2 = speaks(spek) # p1 are frequencies; p2 magnitudes
        if spectral_whitening:
            p2 = sw(spek, p1, p2)
        chroma.append(hpcp(p1,p2))
    initial_frame = 0
    if avoid_edges > 0:
        initial_sample = (avoid_edges * duration) / 100
        initial_frame = initial_sample / hop_size
        number_of_frames = (duration - initial_sample) / hop_size
    chroma = chroma[int(initial_frame):int(number_of_frames)]
    chroma = np.mean(chroma, axis=0)
    if shift_spectrum:
        chroma = shift_vector(chroma, hpcp_size)
    estimation = key(chroma.tolist())
    result = estimation[0] + ' ' + estimation[1]
    confidence = estimation[2]
    ground_truth = item[item.find(' = ')+3:item.rfind(' < ')]
    if verbose:
        print item[:item.rfind(' = ')]
        print 'G:', ground_truth, '|| P:',
    ground_truth = key_to_list(ground_truth)
    estimation = key_to_list(result)
    score = mirex_score(ground_truth, estimation)
    total.append(score)
    xpos = (ground_truth[0] + (ground_truth[0] * 24)) + (-1*(ground_truth[1]-1) * 24 * 12)
    ypos = ((estimation[0] - ground_truth[0]) + (-1 * (estimation[1]-1) * 12))
    matrix[(xpos+ypos)] =+ matrix[(xpos+ypos)] + 1
    if verbose:
        print result, '(%.2f)' % confidence, '|| SCORE:', score, '\n'
    # and eventually write them to a text file
    if results_to_file:
        with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile:
            textfile.write(result)    
    
print len(total), "files analysed.\n"
matrix = np.matrix(matrix)
matrix = matrix.reshape(24,24)
print matrix
np.savetxt(temp_folder + '/_confusion_matrix.csv', matrix, fmt='%i', delimiter=',',  header='C,C#,D,Eb,E,F,F#,G,G#,A,Bb,B,Cm,C#m,Dm,Ebm,Em,Fm,F#m,Gm,G#m,Am,Bbm,Bm')

# MIREX RESULTS
# =============
results = [0,0,0,0,0] # 1,0.5,0.3,0.2,0
for item in total:
    if   item == 1   : results[0] += 1
    elif item == 0.5 : results[1] += 1
    elif item == 0.3 : results[2] += 1
    elif item == 0.2 : results[3] += 1
    elif item == 0   : results[4] += 1

l = float(len(total))
Correct= results[0]/l
Fifth = results[1]/l
Relative = results[2]/l
Parallel = results[3]/l
Error = results[4]/l
Weighted_Score = np.mean(total)

print "\nAVERAGE ESTIMATIONS"
print "==================="
print "Weighted", Weighted_Score
print "Correct ", Correct 
print "Fifth   ", Fifth
print "Relative", Relative 
print "Parallel", Parallel
print "Error   ", Error
print '\n'

if results_to_file:
    settings = "SETTINGS\n========\nAvoid edges ('%' of duration that is disregarded at the beginning and end (0 = full track)) = "+str(avoid_edges)+"\nshift spectrum to fit tempered scale = "+str(shift_spectrum)+"\nspectral whitening = "+str(spectral_whitening)+"\nsample rate = "+str(sample_rate)+"\nwindow size = "+str(window_size)+"\nhop size = "+str(hop_size)+"\nmagnitude threshold = "+str(magnitude_threshold)+"\nminimum frequency = "+str(min_frequency)+"\nmaximum frequency = "+str(max_frequency)+"\nmaximum peaks = "+str(max_peaks)+"\nband preset = "+str(band_preset)+"\nsplit frequency = "+str(split_frequency)+"\nharmonics = "+str(harmonics)+"\nnon linear = "+str(non_linear)+"\nnormalize = "+str(normalize)+"\nreference frequency = "+str(reference_frequency)+"\nhpcp size = "+str(hpcp_size)+"\nweigth type = "+weight_type+"\nweight window size in semitones = "+str(weight_window_size)+"\nharmonics key = "+str(num_harmonics)+"\nslope = "+str(slope)+"\nprofile = "+profile_type+"\npolyphony = "+str(use_polyphony)+"\nuse three chords = "+str(use_three_chords)
    corpus = "\n\nANALYSYS CORPUS\n===============\n" + str(collection) + '\n' + str(genre) + '\n' + str(modality) + '\n\n' + str(len(total)) + " files analysed.\n"
    results_for_file = "\n\nEVALUATION RESULTS\n==================\nWeighted "+str(Weighted_Score)+"\nCorrect "+str(Correct)+"\nFifth "+str(Fifth)+"\nRelative "+str(Relative)+"\nParallel "+str(Parallel)+"\nError "+str(Error)
    write_to_file = open(temp_folder + '/_SUMMARY.txt', 'w')
    write_to_file.write(settings)
    write_to_file.write(corpus)
    write_to_file.write(results_for_file)
    write_to_file.close()
