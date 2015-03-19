#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
Function definitions for key analysis and symbolic manipulation."

Ángel Faraldo, March 2015.
"""

import numpy as np

# Dictionaries
# ============

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


# Functions
# =========

def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0,...,b=11)"
    return name2class[key]


    
def mode_to_num(mode):
    "converts a chord type into an arbitrary numeric value (maj = 1, min = 0)"
    return mode2num[mode]



def key_to_list(key):
	"converts a key (i.e. C major) type into a numeric list containing [tonal center, mode] using the name_to_class and mode_to_num functions"
	key = key.split(' ')
	key[-1] = key[-1].strip()
	if len(key) == 1:
		key = [name_to_class(key[0]), 1]
	else:
		key = [name_to_class(key[0]), mode_to_num(key[1])]
	return key



def mirex_score(ground_truth, estimation):
	"performs an evaluation of the key estimation according to the MIREX competition, assigning a 1 to correctly identified keys, 0.5 to keys at a distance of a perfect fifth, 0.3 to relative keys, 0.2 to parallel keys and 0 to other tyoes of errors."
	if estimation[0] == ground_truth[0] and estimation[1] == ground_truth[1]:
		score = 1 # perfect match
	elif estimation[0] == ground_truth[0] and estimation[1]+ground_truth[1] == 1:
		score = 0.2 # parallel key
	elif estimation[0] == (ground_truth[0]+7)%12:
		score = 0.5 # ascending 5th
	elif estimation[0] == (ground_truth[0]+5)%12:
		score = 0.5 # descending 5th
	elif estimation[0] == (ground_truth[0]+3)%12 and estimation[1] == 1 and ground_truth[1] == 0:
		score = 0.3 # relative minor
	elif estimation[0] == (ground_truth[0]-3)%12 and estimation[1] == 0 and ground_truth[1] == 1:
		score = 0.3 # relative major
	else:
		score = 0 # none of the above
	return score


def shift_vector(hpcp, hpcp_size=12):
    "shifts the spectrum to the nearest tempered bin."
    tuning_resolution = hpcp_size / 12
    max_val = np.max(hpcp)
    if max_val <= 0:
        max_val = 1
    hpcp = np.divide(hpcp,max_val)
    max_val_index = np.where(hpcp==1)
    max_val_index = max_val_index[0][0] % tuning_resolution
    shiftDistance = 0
    if max_val_index > (tuning_resolution / 2):
        shiftDistance = tuning_resolution - max_val_index
    else: 
        shiftDistance = max_val_index
    hpcp = np.roll(hpcp, shiftDistance)
    return hpcp

