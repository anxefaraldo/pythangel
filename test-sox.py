import sox

# create transformer
tfm = sox.Transformer()

# trim the audio between 5 and 10.5 seconds.
tfm.trim(5, 10.5)

# apply compression
tfm.compand()

# apply a fade in and fade out
tfm.fade(fade_in_len=1.0, fade_out_len=0.5)

# create an output file.
tfm.build_file('/Users/angel/Desktop/aeiou.wav', '/Users/angel/Desktop/aeiou2.wav')

# or equivalently using the legacy API
tfm.build('path/to/input_audio.wav', 'path/to/output/audio.aiff')

# get the output in-memory as a numpy array
# by default the sample rate will be the same as the input file
array_out = tfm.build_array(input_filepath='/Users/angel/Desktop/aeiou.wav')

# see the applied effects
tfm.effects_log

###### Simple pitch-shifter to in audio files... ######

pps = sox.Transformer()
pps.pitch(12)
pps.build_file('/Users/angel/Music/Canciones/Todos Ellos.mp3', '/Users/angel/Desktop/aeiou-pitcht.mp3')
