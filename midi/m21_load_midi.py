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
    file_id = file_id % len(midi_corpus_list)
    return m21.converter.parse(midi_corpus_list[file_id])


def load_midfile(file_id, midi_corpus_list=load_midi_corpus()):
    file_id = file_id % len(midi_corpus_list)
    mf = m21.midi.MidiFile()
    mf.open(midi_corpus_list[file_id])
    mf.read()
    s = m21.midi.translate.midiFileToStream(mf)
    return s


# Now we need a way to properly quantise all the midi file
