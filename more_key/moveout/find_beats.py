import numpy as np
import os.path
import essentia.standard as estd


def get_beats_in_secs(audio_file, write_to_file=False):
    loader = estd.MonoLoader(filename=audio_file)
    beat_tracker = estd.BeatTrackerDegara()
    results = list(beat_tracker(loader()))
    if write_to_file:
        f = open(audio_file + '.beats', 'w')
        for item in results:
            f.write(str(item) + '\n')
        f.close()
    return results


def sec_to_window(input_data, sample_rate=44100, hop_size=512):
    # we check if the input is a text file (expecting a single column with time values)
    if os.path.isfile(input_data):
        f = open(input_data, 'r')
        input_data = f.readlines()
    # otherwise we assume the input is a list
    for item in input_data:
        input_data[input_data.index(item)] = item[:-1]
    beat_frames = []
    for item in input_data:
        beat_frames.append(int(float(item) * sample_rate))
    beat_frames = np.divide(beat_frames, hop_size)
    return beat_frames


if __name__ == "__main__":
    import sys
    try:
        print get_beats_in_secs(sys.argv[1], True)
        print sec_to_window(sys.argv[1]+'.beats')
        print 'Done!'
    except StandardError:
        print "usage: filename.py <folder to analyse>\n"
        sys.exit()

