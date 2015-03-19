import os
import numpy as np

folder_GT = '/Users/angel/Datasets/Shaat/key'
folder_P = '/Users/angel/Datasets/Shaat/estimation_keyFinder'

name2class = {'B#':0,'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'Fb':4,'E#':5,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11,'Cb':11, 'None': 0}
            
mode2num = {'minor':0, 'min':0, 'aeolian': 0, 'dorian': 0, 'dor': 0, 'modal': 1, 'mixolydian': 1, 'major':1, 'maj':1, 'mix':1, 'lyd': 1, 'None': 1}

def name_to_class(key):
    "converts a pitch name into its pitch-class value (c=0, c#=1, ... b=11)"
    return name2class[key]
    
def mode_to_num(mode):
    "converts a chord type into an arbitrary numeric value (maj = 0, min = 12)"
    return mode2num[mode]

GT = os.listdir(folder_GT)
if '.DS_Store' in GT:
    GT.remove('.DS_Store')

P = os.listdir(folder_P)
if '.DS_Store' in P:
    P.remove('.DS_Store')

total = []
for i in range(len(GT)):
    GTS = open(folder_GT+'/'+GT[i], 'r')
    lGT = GTS.readline()
    if lGT.find(' ') == -1:
        lGT = [name_to_class(lGT[:lGT.find('\t')]), 1]
    else: 
        splitpos = lGT.find(' ')
        name = lGT[:splitpos]
        splitpos2 = lGT.find('\t')
        mode = lGT[splitpos+1:splitpos2]
        lGT = [name_to_class(name), mode_to_num(mode)]
        print lGT
    PS = open(folder_P+'/'+P[i], 'r')
    lP = PS.readline()
    lP = lP.split(' ')
    lP[-1] = lP[-1].strip()
    print lP
    lP = [name_to_class(lP[0]), mode_to_num(lP[1])]
    if lP[0] == lGT[0] and lP[1] == lGT[1]: score = 1        # perfect match
    elif lP[0] == lGT[0] and lP[1]+lGT[1] == 1: score = 0.2  # parallel key
    elif lP[0] == (lGT[0]+7)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Dominant (in major)
    elif lP[0] == (lGT[0]+5)%12 and lP[1]+lGT[1] == 2: score = 0.5  # Subdominant (in major)
    elif lP[0] == (lGT[0]+9)%12 and lP[1] == 1 and lGT[1] == 0: score = 0.3  # relative minor
    elif lP[0] == (lGT[0]-3)%12 and lP[1] == 0 and lGT[1] == 1: score = 0.3  # relative major
    else : score = 0 # none of the above
    total.append(score)
    print 1+i, 'P:', lP, 'GT:', lGT, 'Score:', score
    GTS.close()
    PS.close()
    
results = [0,0,0,0,0] # 1,0.5,0.3,0.2,0
for item in total:
    if item == 1     : results[0] += 1
    elif item == 0.5 : results[1] += 1
    elif item == 0.3 : results[2] += 1
    elif item == 0.2 : results[3] += 1
    elif item == 0   : results[4] += 1
    
l = float(len(total))
Weighted_Score = np.mean(total)
Correct = results[0]/l
Fifth = results[1]/l
Relative = results[2]/l
Parallel = results[3]/l
Error = results[4]/l

print Weighted_Score, Correct, Fifth, Relative, Parallel, Error