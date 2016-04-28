#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from collections import Counter

import essentia.standard as estd
import numpy as np

from fodules.folder import *
from fodules.pcp import shift_pcp


def estimate_key_globally(soundfile, folder_to_write_results):
    """
    Estimates the overall key of an audio track
    by looking at its global pitch-class profile.
    :type soundfile: str
    :type folder_to_write_results: str
    """
    loader = estd.MonoLoader(filename=soundfile,
                             sampleRate=SAMPLE_RATE)
    hpf = estd.HighPass(cutoffFrequency=HIGHPASS_CUTOFF,
                        sampleRate=SAMPLE_RATE)
    window = estd.Windowing(size=WINDOW_SIZE,
                            type=WINDOW_TYPE,
                            zeroPhase=False)  # True = cos (default), False = sin
    rfft = estd.Spectrum(size=WINDOW_SIZE)
    flatness = estd.Flatness()
    sw = estd.SpectralWhitening(maxFrequency=MAX_HZ,
                                sampleRate=SAMPLE_RATE)
    speaks = estd.SpectralPeaks(magnitudeThreshold=SPECTRAL_PEAKS_THRESHOLD,
                                maxFrequency=MAX_HZ,
                                minFrequency=MIN_HZ,
                                maxPeaks=SPECTRAL_PEAKS_MAX,
                                sampleRate=SAMPLE_RATE)
    hpcp = estd.HPCP(bandPreset=HPCP_BAND_PRESET,
                     harmonics=HPCP_HARMONICS,
                     maxFrequency=MAX_HZ,
                     minFrequency=MIN_HZ,
                     nonLinear=HPCP_NON_LINEAR,
                     normalized=HPCP_NORMALIZE,
                     referenceFrequency=HPCP_REFERENCE_HZ,
                     sampleRate=SAMPLE_RATE,
                     size=HPCP_SIZE,
                     splitFrequency=HPCP_SPLIT_HZ,
                     weightType=HPCP_WEIGHT_TYPE,
                     windowSize=HPCP_WEIGHT_WINDOW_SIZE,
                     maxShifted=HPCP_SHIFT)
    if ANALYSIS_DETAIL == 'majmin':
        key = estd.KeyEDM(pcpSize=HPCP_SIZE, profileType=KEY_PROFILE)
    else:
        key = estd.KeyExtended(pcpSize=HPCP_SIZE)
    audio = hpf(hpf(hpf(loader())))
    duration = len(audio)
    frame_start = 0
    chroma = []
    if SKIP_FIRST_MINUTE and duration > (SAMPLE_RATE * 60):
        audio = audio[SAMPLE_RATE * 60:]
        duration = len(audio)
    if FIRST_N_SECS > 0:
        if duration > (FIRST_N_SECS * SAMPLE_RATE):
            audio = audio[:FIRST_N_SECS * SAMPLE_RATE]
            duration = len(audio)
    if AVOID_EDGES > 0:
        initial_sample = (AVOID_EDGES * duration) * 0.01
        final_sample = duration - initial_sample
        audio = audio[initial_sample:final_sample]
        duration = len(audio)
    while frame_start <= (duration - WINDOW_SIZE):
        spek = rfft(window(audio[frame_start:frame_start + WINDOW_SIZE]))
        if sum(spek) <= 0.001:
            frame_start += WINDOW_SIZE
            continue
        p1, p2 = speaks(spek)  # p1 = freqs; p2 = magnitudes
        if SPECTRAL_WHITENING:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        # sum_pcp = np.sum(pcp)
        # if sum_pcp > 0:  # TODO: Most likely this is redudant!
        if flatness(pcp) > FLATNESS_THRESHOLD:  # TODO: check this flatness business!
            frame_start += WINDOW_SIZE
            continue
        if not DETUNING_CORRECTION or SHIFT_SCOPE == 'average':
            chroma.append(pcp)
        elif DETUNING_CORRECTION and SHIFT_SCOPE == 'frame':
            pcp = shift_pcp(pcp, HPCP_SIZE)
            chroma.append(pcp)
        else:
            raise NameError("SHIFT_SCOPE must be set to 'frame' or 'average'")
        frame_start += WINDOW_SIZE
    if np.sum(chroma) <= 0.001:
        return 'Silence', 1.0, [0] * 36
    chroma = np.sum(chroma, axis=0)  # TODO: have a look at variance or std!
    if DETUNING_CORRECTION and SHIFT_SCOPE == 'average':
        chroma = shift_pcp(list(chroma), HPCP_SIZE)
    chroma = chroma.tolist()
    estimation = key(chroma)
    result = estimation[0] + ' ' + estimation[1]
    confidence = estimation[2]
    textfile = open(folder_to_write_results + soundfile[soundfile.rfind('/'):soundfile.rfind('.')] + '.key', 'w')
    results_string = result + '\t' + '%.2f' % confidence + '\t' + str(chroma)[1:-1]
    textfile.write(results_string)
    textfile.close()
    return result, confidence, chroma


def estimate_key_locally(soundfile, folder_to_write_results):
    """
    Estimates the overall key of an audio track
    by looking at local pitch-class profiles.
    :type soundfile: str
    :type folder_to_write_results: str
    """
    loader = estd.MonoLoader(filename=soundfile,
                             sampleRate=SAMPLE_RATE)
    hpf = estd.HighPass(cutoffFrequency=HIGHPASS_CUTOFF,
                        sampleRate=SAMPLE_RATE)
    window = estd.Windowing(size=WINDOW_SIZE,
                            type=WINDOW_TYPE,
                            zeroPhase=False)  # True = cos (default), False = sin
    rfft = estd.Spectrum(size=WINDOW_SIZE)
    flatness = estd.Flatness()
    sw = estd.SpectralWhitening(maxFrequency=MAX_HZ,
                                sampleRate=SAMPLE_RATE)
    speaks = estd.SpectralPeaks(magnitudeThreshold=SPECTRAL_PEAKS_THRESHOLD,
                                maxFrequency=MAX_HZ,
                                minFrequency=MIN_HZ,
                                maxPeaks=SPECTRAL_PEAKS_MAX,
                                sampleRate=SAMPLE_RATE)
    hpcp = estd.HPCP(bandPreset=HPCP_BAND_PRESET,
                     harmonics=HPCP_HARMONICS,
                     maxFrequency=MAX_HZ,
                     minFrequency=MIN_HZ,
                     nonLinear=HPCP_NON_LINEAR,
                     normalized=HPCP_NORMALIZE,
                     referenceFrequency=HPCP_REFERENCE_HZ,
                     sampleRate=SAMPLE_RATE,
                     size=HPCP_SIZE,
                     splitFrequency=HPCP_SPLIT_HZ,
                     weightType=HPCP_WEIGHT_TYPE,
                     windowSize=HPCP_WEIGHT_WINDOW_SIZE,
                     maxShifted=HPCP_SHIFT)
    if ANALYSIS_DETAIL == 'majmin':
        key = estd.KeyEDM(pcpSize=HPCP_SIZE, profileType=KEY_PROFILE)
    else:
        key = estd.KeyExtended(pcpSize=HPCP_SIZE)
    audio = hpf(hpf(hpf(loader())))
    duration = len(audio)
    chroma = []
    keys = []
    frame_start = 0
    if SKIP_FIRST_MINUTE and duration > (SAMPLE_RATE * 60):
        audio = audio[SAMPLE_RATE * 60:]
        duration = len(audio)
    if FIRST_N_SECS > 0:
        if duration > (FIRST_N_SECS * SAMPLE_RATE):
            audio = audio[:FIRST_N_SECS * SAMPLE_RATE]
            duration = len(audio)
    if AVOID_EDGES > 0:
        initial_sample = (AVOID_EDGES * duration) / 100
        final_sample = duration - initial_sample
        audio = audio[initial_sample:final_sample]
        duration = len(audio)
    while frame_start < (duration - WINDOW_SIZE):
        spek = rfft(window(audio[frame_start:frame_start + WINDOW_SIZE]))
        if sum(spek) <= 0.001:
            frame_start += WINDOW_SIZE
            continue
        p1, p2 = speaks(spek)  # p1 = freqs; p2 = magnitudes
        if SPECTRAL_WHITENING:
            p2 = sw(spek, p1, p2)
        pcp = hpcp(p1, p2)
        #  pcp_sum = np.sum(pcp)
        #  if pcp_sum > 0:  # TODO: Most likely this is redudant!
        if flatness(pcp) > FLATNESS_THRESHOLD:  # TODO: check this flatness business!
            frame_start += WINDOW_SIZE
            continue
        if not DETUNING_CORRECTION or SHIFT_SCOPE == 'average':
            chroma.append(pcp)
        elif DETUNING_CORRECTION and SHIFT_SCOPE == 'frame':
            pcp = shift_pcp(pcp, HPCP_SIZE)
            chroma.append(pcp)
        else:
            print "SHIFT_SCOPE must be set to 'frame' or 'average'"
            sys.exit()
        if len(chroma) == N_WINDOWS:
            if np.sum(chroma) <= 0.001:  # ESTA PARTE ES NUEVA! CHECK IT WORKS!
                keys.append('Silence')
                chroma = chroma[WINDOW_INCREMENT:]
                frame_start += WINDOW_SIZE
                continue
            pcp = np.sum(chroma, axis=0)
            if DETUNING_CORRECTION and SHIFT_SCOPE == 'average':
                pcp = shift_pcp(list(pcp), HPCP_SIZE)
            pcp = pcp.tolist()
            local_key = key(pcp)
            result = local_key[0] + ' ' + local_key[1]
            keys.append(result)
            chroma = chroma[WINDOW_INCREMENT:]
        frame_start += WINDOW_SIZE
    mode = Counter(keys)
    textfile = open(folder_to_write_results + soundfile[soundfile.rfind('/'):soundfile.rfind('.')] + '.key', 'w')
    try:
        results = mode.most_common(1)[0][0]
    except NameError:
        print mode
        results = 'Unknown'
    textfile.write(results + '\t')
    textfile.close()
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="global key estimation and evaluation algorithms")
    parser.add_argument("input", help="file or dir to analyse")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-f", "--file", action="store_true", help="analyse a single file")
    group1.add_argument("-d", "--dir", action="store_true", help="analyse a whole dir (default)")
    parser.add_argument("-v", "--verbose", action="store_true", help="print estimations to console")
    parser.add_argument("-o", "--overwrite", action="store_true", help="overwrite existing subdir if exists.")
    parser.add_argument("-w", "--write_to", help="specify dir to export results")
    args = parser.parse_args()

    if args.write_to:
        if not os.path.isdir(args.write_to):
            raise parser.error("'{0}' is not a valid directory for writing.".format(args.input))
        else:
            output_dir = args.write_to
    else:
        output_dir = args.input
    print "Creating subfolder with results in '{0}'.".format(output_dir)

    if args.single:
        if not os.path.isfile(args.input):
            raise parser.error("'{0}' is not a valid file.".format(args.input))
        else:
            output_dir = create_subfolder_with_parameters(output_dir, overwrite=args.overwrite)
            if ANALYSIS_TYPE == 'local':
                r = estimate_key_locally(args.input, output_dir)
                if args.verbose:
                    print args.input, '-', r
            elif ANALYSIS_TYPE == 'global':
                r, c, ch = estimate_key_globally(args.input, output_dir)
                if args.verbose:
                    print args.input, '-', r, '(%.2f)' % c
            else:
                raise NameError("ANALYSIS TYPE must be set to 'local' or 'global'")
    else:
        if not os.path.isdir(args.input):
            raise parser.error("'{0}' is not a directory.".format(args.input))
        else:
            analysis_folder = args.input[1 + args.input.rfind('/'):]
            output_dir = create_subfolder_with_parameters(output_dir, tag=analysis_folder, overwrite=args.overwrite)
            settings_file = open('settings_edm.py', 'r')
            write_settings_to = open(output_dir + '/settings.txt', 'w')
            write_settings_to.write(settings_file.read())
            write_settings_to.close()
            settings_file.close()
            list_all_files = os.listdir(args.input)
            print 'Analysing files...'
            count_files = 0
            for item in list_all_files:
                if any(soundfile_type in item for soundfile_type in AUDIO_FILE_TYPES):
                    audiofile = args.input + '/' + item
                    if ANALYSIS_TYPE == 'local':
                        r = estimate_key_locally(audiofile, output_dir)
                        if args.verbose:
                            print audiofile, '-', r
                    elif ANALYSIS_TYPE == 'global':
                        r, c, ch = estimate_key_globally(audiofile, output_dir)
                        if args.verbose:
                            print audiofile, '-', r, '(%.2f)' % c
                    count_files += 1
            print "{} audio files analysed".format(count_files)
