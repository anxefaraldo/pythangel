import os
import csv
import re
import essentia
from essentia.streaming import *

infolder  = "/Users/angelfaraldo/Desktop/EVALTESTS/queen-audio/"
outfolder = "/Users/angelfaraldo/Desktop/EVALTESTS/queen-chord-estimations-essentia/"

soundfiles = os.listdir(infolder)
if '.DS_Store' in soundfiles:
    soundfiles.remove('.DS_Store')

for item in soundfiles:
    loader = MonoLoader(filename=infolder+item)
    ts = TonalExtractor()
    pool = essentia.Pool()
    # and now we connect the algorithms
    loader.audio >> ts.signal
    ts.chords_changes_rate >> (pool, 'chords_changes_rate')
    ts.chords_histogram >> (pool, 'chords_histogram')
    ts.chords_key >> (pool, 'chords_key')
    ts.chords_number_rate >> (pool, 'chords_number_rate')
    ts.chords_progression >> (pool, 'chords_progression')
    ts.chords_scale >> (pool, 'chords_scale')
    ts.chords_strength >> (pool, 'chords_strength')
    ts.hpcp >> (pool, 'hpcp')
    ts.hpcp_highres >> (pool, 'hpcp_highres')
    ts.key_key >> (pool, 'key_key')
    ts.key_scale >> (pool, 'key_scale')
    ts.key_strength >> (pool, 'key_strength')
    essentia.run(loader)
    chordlist = pool['chords_progression']
    times = []
    for i in range(len(chordlist)):
        times.append(i*0.04643990929705) # duration in seconds of 44100/2048  
    mirexlist = []
    for i in range(len(chordlist)):
        mirexlist.append([times[i], chordlist[i]])             
    i = 0
    l = 1
    while i < l:
        while mirexlist[i][1]==mirexlist[i+1][1]:
            mirexlist.pop(i+1)
            l = len(mirexlist)
            if l == i+1:
                break
        i += 1  
    for i in range(len(mirexlist)):
        if len(mirexlist[i][1])>1:
            if mirexlist[i][1][1] == 'm':
                mirexlist[i][1] = mirexlist[i][1][0] + ':' + mirexlist[i][1][1]
            elif len(mirexlist[i][1])==3:
                mirexlist[i][1] = mirexlist[i][1][:1] + ':' + mirexlist[i][1][2]
    for i in range(len(mirexlist)-1):
        mirexlist[i] = [mirexlist[i][0], mirexlist[i+1][0], mirexlist[i][1]]
    mirexlist[-1] = [mirexlist[-1][0], mirexlist[-1][0]+0.5, mirexlist[-1][1]]
    for row in mirexlist:
        if 'm' in row[2]:
            row[2] = re.sub('m','min',row[2])
    newfile = open(outfolder +"ESSENTIA_"+ item[:-5] + '.csv', 'wb')
    wr = csv.writer(newfile, delimiter = ' ')
    wr.writerows(mirexlist)
    newfile.close()
    essentia.reset(loader)    