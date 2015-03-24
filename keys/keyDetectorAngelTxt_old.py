#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
This script estimates the key of the songs contained in a folder, and \n
performs an evaluation of its results according to the MIREX standard.

Ángel Faraldo, March 2015.
"""


# IO
# ==
import sys

try:
    audio_folder = sys.argv[1]
    annot_folder = sys.argv[2]
except:
    print "\nUSAGE: name_of_this_script.py <route to audio> <route to gt annotations>\n"
    sys.exit()


# LOAD MODULES
# ============
import os
import essentia as e
import essentia.standard as estd
import numpy as np
from time import time as tiempo



# PARAMETERS
# ==========
# ángel: 
avoid_edges = 0 # % of duration at the beginning and end that is not analysed.
shift_spectrum = True
spectral_whitening = True
verbose = True
results_to_file = False

# global
sample_rate = 44100
window_size = 4096
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
weight_type = "squaredCosine" # {none, cosine or squaredCosine}
weight_window_size = 1 # semitones

# key detector
num_harmonics = 4
profile_type = 'shaath'
slope = 0.6 # doesn't seem to make any difference!
use_polyphony = False
use_three_chords = False

# auto-derived
hop_size = window_size
tuning_resolution = (size / 12)


# ANALYSIS OPTONS
# ===============
print "\nANALYSING..."

# create temporary directory and unique time identifier
uniqueTime = str(int(tiempo()))
temp_folder = os.getcwd()+'/Estimations'+uniqueTime
os.mkdir(temp_folder)

# retrieve filenames from folder
soundfiles = os.listdir(audio_folder)
if '.DS_Store' in soundfiles: 
    soundfiles.remove('.DS_Store')

if verbose:
    print "\nestimation of individual songs:" 
    print "-------------------------------" 


# LOOP
# ====
for item in soundfiles:
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
    initial_frame = 0
    if avoid_edges > 0:
        initial_sample = (avoid_edges * duration) / 100
        initial_frame = initial_sample / hop_size
        number_of_frames = (duration - (initial_sample)) / hop_size
    chromean = []
    for i in range(int(initial_frame),int(number_of_frames)):
        chromean.append(chroma[i])
    chromean = np.mean(chromean, axis=0) # mean or median!!!!!!
    max_val = np.max(chromean)
    if max_val <= 0: max_val = 1
    chromean = np.divide(chromean,max_val) # normalises the hpcp... perhaps we shouldn't
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
    result = estimation[0] + ' ' + estimation[1] + ' (' + str(estimation[2]) + ')'
    if verbose : print item[:15]+'...     ', result
    # and eventually write them to a text file
    with open(temp_folder + '/' + item[:-3]+'txt', 'w') as textfile:
        textfile.write(result)

# EVALUATION
# ==========
# Dictionaries and Functions
name2class = {'B#':0,'C':0,
              'C#':1,'Db':1,
              'D':2,
              'D#':3,'Eb':3,
              'E':4,'Fb':4,
              'E#':5,'F':5,
              'F#':6,'Gb':6,
              'G':7,
              'G#':8,'Ab':8,
              'A':9,
              'A#':10,'Bb':10,
              'B':11,'Cb':11,
              'silence': 12}
            
mode2num = {'minor':0,
            'min':0,
            'aeolian': 0,
            'dorian': 0,
            'dor': 0,
            'modal': 1,
            'mixolydian': 1,
            'major':1,
            'maj':1,
            'mix':1,
            'lyd': 1,
            'None': 1}

def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]
    
def mode_to_num(mode):
    "converts a chord type into an arbitrary numeric value (maj = 1, min = 0)"
    return mode2num[mode]

# retrieve folder data
GT = os.listdir(annot_folder)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')

P = os.listdir(temp_folder)
if '.DS_Store' in P:
    P.remove('.DS_Store')

# run the evaluation algorithm
print "\n...EVALUATING..."
if verbose: 
    print "\nresults for individual songs:" 
    print "-----------------------------" 
total = []
for i in range(len(GT)):
    GTS = open(annot_folder+'/'+GT[i], 'r')
    lGT = GTS.readline()
    lGT = lGT.split(' ')
    lGT[-1] = lGT[-1].strip() # remove whitespace if existing
    if len(lGT) == 1 : lGT = [name_to_class(lGT[0]), 1]
    else: lGT = [name_to_class(lGT[0]), mode_to_num(lGT[1])]
    PS = open(temp_folder+'/'+P[i], 'r')
    lP = PS.readline()
    lP = lP.split(' ')
    lP[-1] = lP[-1].strip()
    lP = [name_to_class(lP[0]), mode_to_num(lP[1])]
    if lP[0] == lGT[0] and lP[1] == lGT[1]: score = 1        # perfect match
    elif lP[0] == lGT[0] and lP[1]+lGT[1] == 1: score = 0.2  # parallel key
    elif lP[0] == (lGT[0]+7)%12: score = 0.5  # ascending fifth
    elif lP[0] == (lGT[0]+5)%12: score = 0.5  # descending fifth
    elif lP[0] == (lGT[0]+3)%12 and lP[1] == 1 and lGT[1] == 0: score = 0.3  # relative minor
    elif lP[0] == (lGT[0]-3)%12 and lP[1] == 0 and lGT[1] == 1: score = 0.3  # relative major
    else : score = 0 # none of the above
    if verbose : print i+1, '- Prediction:', lP, '- Ground-Truth:', lGT, '- Score:', score
    total.append(score)
    GTS.close()
    PS.close()


# RESULTS
# =======
results = [0,0,0,0,0] # 1,0.5,0.3,0.2,0
for item in total:
    if item == 1     : results[0] += 1
    elif item == 0.5 : results[1] += 1
    elif item == 0.3 : results[2] += 1
    elif item == 0.2 : results[3] += 1
    elif item == 0   : results[4] += 1

l = float(len(total))
Weighted_Score = np.mean(total)
Correct= results[0]/l
Fifth = results[1]/l
Relative = results[2]/l
Parallel = results[3]/l
Error = results[4]/l

print "\nAVERAGE ESTIMATIONS"
print "==================="
print "Correct ", Correct 
print "Fifth   ", Fifth
print "Relative", Relative 
print "Parallel", Parallel
print "Error   ", Error
print "Weighted", Weighted_Score
print '\n'

if results_to_file:
    settings = "SETTINGS\n========\navoid edges (percentage of the duration of the song that is disregarded at the beginning and end (0 = full track)) = "+str(avoid_edges)+"\nshift spectrum to fit tempered scale= "+str(shift_spectrum)+"\nspectral whitening= "+str(spectral_whitening)+"\nsample rate = "+str(sample_rate)+"\nwindow size = "+str(window_size)+"\nhop size = "+str(hop_size)+"\nmagnitude threshold = "+str(magnitude_threshold)+"\nminimum frequency = "+str(min_frequency)+"\nmaximum frequency = "+str(max_frequency)+"\nmaximum peaks = "+str(max_peaks)+"\nband preset = "+str(band_preset)+"\nsplit frequency = "+str(split_frequency)+"\nharmonics = "+str(harmonics)+"\nnon linear = "+str(non_linear)+"\nnormalize = "+str(normalize)+"\nreference frequency = "+str(reference_frequency)+"\nhpcp size = "+str(size)+"\nweigth type = "+weight_type+"\nweight window size in semitones = "+str(weight_window_size)+"\nharmonics key = "+str(num_harmonics)+"\nslope = "+str(slope)+"\nprofile = "+profile_type+"\npolyphony = "+str(use_polyphony)+"\nuse three chords = "+str(use_three_chords)
    results_for_file = "\n\nEVALUATION RESULTS\n==================\nWeighted "+str(Weighted_Score)+"\nCorrect "+str(Correct)+"\nFifth "+str(Fifth)+"\nRelative "+str(Relative)+"\nParallel "+str(Parallel)+"\nError "+str(Error)
    write_to_file = open(temp_folder+'/_settings_and_evaluation.txt', 'w')
    write_to_file.write(settings)
    write_to_file.write(results_for_file)
    write_to_file.close()
else:
    from shutil import rmtree as rmt
    rmt(temp_folder)
