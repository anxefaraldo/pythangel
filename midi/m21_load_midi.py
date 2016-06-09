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
    score = m21.converter.parse(midi_corpus_list[file_id])
    return score[0]

c = load_midi_corpus()
f = load_midfile(5, c)

f.highestTime

f.timeSignature = m21.meter.TimeSignature('4/4')
f.makeMeasures(inPlace=True)
f.makeBeams(inPlace=True)
f.makeNotation(inPlace=True)
f.show('midi')



"""
def load_midfile2(file_id, midi_corpus_list=load_midi_corpus()):
    file_id = file_id % len(midi_corpus_list)
    mf = m21.midi.MidiFile()
    mf.open(midi_corpus_list[file_id])
    mf.read()
    s = m21.midi.translate.midiFileToStream(mf)
    return s
"""

# Now we need a way to properly quantise all the midi file

chord_density = GSAPI.create_FloatParameter()
COMPUTE_NEW = gsapi.PARAMETER

def change_chord_density(slider_value):

DEF COMPUTE_NEW(TOGGLEvALUE)
    changePattern

def changePattern(GSPattern)current_melodia):

    music12Obj = current_meliody.tom21()

    // transform music12Obj
    CHORD_DENSITY

    GSPattern = music21Obj.toGSP()

    return GSPattern

