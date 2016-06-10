import music21 as m21
import os
from math import ceil


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

# LINYX:
# corpus = load_midi_corpus()
# MAC
corpus = load_midi_corpus('/Users/angel/Git/house-harmonic-filler/corpus')
raw_loop = load_midfile(22222, corpus)
clean_loop = m21.stream.Stream()
last_chord = m21.chord.Chord()
for c in raw_loop.recurse().getElementsByClass('Chord'):
    c.sortAscending(inPlace=True)
    print c.pitches
    if c.pitches != last_chord.pitches:
        print c.offset, c.duration, c.pitches
        clean_loop.insert(c.offset, c.__deepcopy__())
    last_chord = c

for i in range(len(clean_loop)):
    print i
    if i < (len(clean_loop) - 1):
        clean_loop[i].duration = m21.duration.Duration(clean_loop[i + 1].offset - clean_loop[i].offset)
        print 'off', clean_loop[i].offset, clean_loop[i].duration
    elif i == (len(clean_loop) - 1):
        clean_loop[i].duration = m21.duration.Duration(ceil(raw_loop.highestTime) - clean_loop[i].offset)
        print 'off', clean_loop[i].offset, clean_loop[i].duration
clean_loop.show()


clean_loop.makeNotation(inPlace=True)

clean_loop.show()



