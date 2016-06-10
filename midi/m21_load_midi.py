import music21 as m21
import os


def load_midi_corpus(midi_corpus_location='/home/angel/Git/house-harmonic-filler/corpus'):
    midi_corpus_list = os.listdir(midi_corpus_location)
    for anyfile in midi_corpus_list:
        if ".mid" not in anyfile:
            midi_corpus_list.remove(anyfile)
        else:
            midi_corpus_list[midi_corpus_list.index(anyfile)] = midi_corpus_location + '/' + anyfile
    return midi_corpus_list


def load_midfile(file_id, midi_corpus_list=load_midi_corpus()):
    file_id %= len(midi_corpus_list)
    score = m21.converter.parse(midi_corpus_list[file_id])
    return score[0]


corpus = load_midi_corpus()
raw_loop = load_midfile(33, corpus)
raw_loop.timeSignature = m21.meter.TimeSignature('4/4')
raw_loop.makeNotation(inPlace=True)
clean_loop = m21.stream.Stream()
last_chord = m21.chord.Chord()
for c in raw_loop.flat.recurse().getElementsByClass('Chord'):
    if c.pitches != last_chord.pitches:
        print c.offset, c.duration
        clean_loop.insert(c.offset, c.__deepcopy__())
    last_chord = c
clean_loop.show('text')


for i in range(len(clean_loop)):
    print i
    if i < (len(clean_loop) - 1):
        print 'off', clean_loop[i].offset, clean_loop[i].duration
        dur = m21.duration.Duration(clean_loop[i + 1].offset - clean_loop[i].offset)
        print 'dur', dur
        clean_loop[i].duration = dur
        print 'off', clean_loop[i].offset, clean_loop[i].duration
    elif i == (len(clean_loop) - 1):
        print 'off', clean_loop[i].offset, clean_loop[i].duration
        dur = m21.duration.Duration(raw_loop.flat.highestTime - clean_loop[i].offset)
        # clean_loop[i].duration = m21.duration.Duration(raw_loop.flat.highestTime - clean_loop.offset)
        clean_loop[i].duration = dur
        print 'off', clean_loop[i].offset, clean_loop[i].duration
clean_loop.makeNotation(inPlace=True)

clean_loop.show()



