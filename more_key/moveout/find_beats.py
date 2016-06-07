import numpy as np
import os.path
import essentia.standard as estd


def extract_onsets(audio_file, window_size=2048, hop_size=512, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    # onset_detector = estd.OnsetRate()
    onset_detector = estd.SuperFluxExtractor()  # TODO Ask martin and Dmitri why only gives first 24 secs
    onsets = list(onset_detector(loader()))
    if write_to_file:
        f = open(audio_file + '.onsets', 'w')
        for item in onsets:
            f.write(str(item) + '\n')
        f.close()
    return onsets

"""
def extract_onsets(audio_file, window_size=2048, hop_size=512, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    cutter = estd.FrameCutter(frameSize=window_size,
                              hopSize=hop_size)
    spectrum = estd.Spectrum(size=window_size)
    onset_detector = estd.OnsetDetection()
    phases = [0] * window_size
    # onset_detector = estd.SuperFluxExtractor() TODO Ask martin and Dmitri why only gives first 24 secs
    sig = loader()
    n_frames = len(sig) / hop_size
    print n_frames
    onsets = []
    for i in range(n_frames):
        print i
        ons = onset_detector(spectrum(cutter(sig)), phases)
        # print ons
        onsets.append(ons)
    #if write_to_file:
    #    f = open(audio_file + '.onsets', 'w')
    #    for item in onsets:
    #        f.write(str(item) + '\n')
    #    f.close()
    #print onsets
    return onsets
"""

def extract_beat_positions(audio_file, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    beat_tracker = estd.BeatTrackerDegara()
    results = list(beat_tracker(loader()))
    if write_to_file:
        f = open(audio_file + '.beats', 'w')
        for item in results:
            f.write(str(item) + '\n')
        f.close()
    return results


def sec_to_nwindow(input_data, sample_rate=44100, hop_size=256):
    if type(input_data) is list:
        pass
    elif os.path.isfile(input_data):
        f = open(input_data, 'r')
        input_data = f.readlines()
        f.close()
        for item in input_data:
            input_data[input_data.index(item)] = float(item[:-1])
    else:
        raise ValueError("Input data must be ot type list, float or a textfile")
    beat_frames = [0]
    for item in input_data:
        beat_frames.append(int(item * sample_rate))
    beat_frames = np.divide(beat_frames, [hop_size])
    return beat_frames


def beat_stats(window_indexes, feature, n_beats=1, window_increment=1):
    stats = []
    i = 0
    while i < (len(window_indexes) - n_beats):
        beat_info = np.median(feature[window_indexes[i]:window_indexes[i + n_beats]], axis=0)
        stats.append(beat_info)
        i += window_increment
    return stats


if __name__ == "__main__":
    import sys
    try:
        o = extract_onsets(sys.argv[1])
        print o
        # print sec_to_nwindow(extract_beat_positions(sys.argv[1], False))
        # b = beat_stats(a, audio_features, 4, 1)
        print 'Done!'
    except StandardError:
        print "usage: filename.py <folder to analyse>\n"
        sys.exit()



