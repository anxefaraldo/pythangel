import math
import music21 as m21
import os


def load_midi_corpus(midi_corpus_location='/home/angel/Git/house-harmonic-filler/corpus'):
    midi_corpus_list = os.listdir(midi_corpus_location)
    for anyfile in midi_corpus_list:
        if ".mid" not in anyfile:
            midi_corpus_list.remove(midi_corpus_list[midi_corpus_list.index(anyfile)])
    for i in range(len(midi_corpus_list)):
        midi_corpus_list[i] = midi_corpus_location + '/' + midi_corpus_list[i]
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
            new_stream[i].duration = m21.duration.Duration(math.ceil(m21_stream.highestTime) - new_stream[i].offset)
    return new_stream


def force_4_bar(m21_stream):
    if m21_stream.highestTime == 8:
        four_bar_loop = m21.stream.Stream()
        four_bar_loop.repeatAppend(m21_stream, 2)
        four_bar_loop.makeNotation(inPlace=True)
        return four_bar_loop
    else:
        return m21_stream


def base_transposition(m21_stream):
    first_chord = m21_stream.flat.getElementsByClass('Chord')[0]
    root = first_chord.root().pitchClass
    octave = first_chord.root().octave
    print root, octave
    mode = first_chord.quality
    transposition = (0 - root) + (4 - octave) * 12
    print transposition
    key = 'C'
    if mode == 'minor':
        key = key.lower()
    elif mode == 'major':
        key = key.upper()
    m21_stream.insert(0, m21.key.Key(key))
    return m21_stream.transpose(transposition)


def complete_bar_with_rest(my_stream):
    if my_stream.quarterLengthFloat % 2.0 == 0.0:
        return my_stream
    else:
        add_rest = m21.note.Rest()
        add_rest.quarterLengthFloat = math.fabs(2.00**(my_stream.quarterLengthFloat//2.0) - my_stream.quarterLengthFloat)
        print add_rest.quarterLengthFloat
        my_stream.append(add_rest)
        return my_stream


def replace_time_signature(my_stream):
    if my_stream.quarterLengthFloat % 2.0 == 0.0:
        return my_stream
    else:
        add_rest = m21.note.Rest()
        add_rest.quarterLengthFloat = math.fabs(2.0**(my_stream.quarterLengthFloat//2.0) - my_stream.quarterLengthFloat)
        print add_rest.quarterLengthFloat
        my_stream.append(add_rest)
        return my_stream
