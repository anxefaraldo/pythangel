import os
import essentia
from essentia.streaming import *

infolder  = '/Users/angelfaraldo/Desktop/EVALTESTS/audio/'
outfolder = '/Users/angelfaraldo/Desktop/EVALTESTS/chord-estimations-essentia'

soundfiles = os.listdir(infolder)
soundfiles = soundfiles[1:]  

for item in soundfiles:
    loader = MonoLoader(filename=infolder+item)
    framecutter = FrameCutter(frameSize=16384, hopSize=16384)
    windowing = Windowing(size=16384, type="blackmanharris62")
    spectrum = Spectrum(size=16384)
    spectralpeaks = SpectralPeaks(orderBy="magnitude", magnitudeThreshold=1e-05, minFrequency=40, maxFrequency=5000, maxPeaks=100)
    hpcp = HPCP()
    # key = Key(useThreeChords=True) # key Profile
    chords = ChordsDetection(hopSize=16384, windowSize=2)
    pool = essentia.Pool()
    # and now we connect the algorithms
    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp >> chords.pcp
    chords.chords >> (pool, 'chords.symbol')
    chords.strength >> (pool, 'chords.strength')
    essentia.run(loader)
    result = pool['chords.symbol'] # + '(' + str(pool['chords.strength']) + ')'
    print result
    
    
    textfile = open(outfolder + item, 'w')
    textfile.write(result)
    textfile.close()
    essentia.reset(loader)