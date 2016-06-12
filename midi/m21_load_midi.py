from math import ceil
import music21 as m21
import os
from sys import platform


def load_midi_corpus(midi_corpus_location='/home/angel/Git/house-harmonic-filler/corpus'):
    midi_corpus_list = os.listdir(midi_corpus_location)
    for anyfile in midi_corpus_list:
        if ".mid" not in anyfile:
            midi_corpus_list.remove(anyfile)
        else:
            midi_corpus_list[midi_corpus_list.index(anyfile)] = midi_corpus_location + '/' + anyfile
    return midi_corpus_list


def load_midfile(file_id, midi_corpus_list):
    file_id %= len(midi_corpus_list)
    score = m21.converter.parse(midi_corpus_list[file_id])
    return score[0]


def extract_chords(m21_stream):
    new_stream = m21.stream.Stream()
    last_chord = m21.chord.Chord()
    for c in m21_stream.recurse().getElementsByClass('Chord'):
        c.sortAscending(inPlace=True)
        print c.pitches
        if c.pitches != last_chord.pitches:
            new_stream.insert(c.offset, c.__deepcopy__())
        last_chord = c
    for i in range(len(new_stream)):
        if i < (len(new_stream) - 1):
            new_stream[i].duration = m21.duration.Duration(new_stream[i + 1].offset - new_stream[i].offset)
        elif i == (len(new_stream) - 1):
            new_stream[i].duration = m21.duration.Duration(ceil(m21_stream.highestTime) - new_stream[i].offset)
    return new_stream


def force_4_bar(m21_stream):
    if m21_stream.highestTime == 8:
        four_bar_loop = m21.stream.Stream()
        four_bar_loop.repeatAppend(m21_stream, 2)
        four_bar_loop.makeNotation(inPlace=True)
        return four_bar_loop
    else:
        return m21_stream


# Actions:

if platform == 'darwin':
    corpus = load_midi_corpus('/Users/angel/Git/house-harmonic-filler/corpus')
else:
    corpus = load_midi_corpus('/home/angel/Git/house-harmonic-filler/corpus')


prog = force_4_bar(extract_chords(load_midfile((1, corpus))))
prog.show()



