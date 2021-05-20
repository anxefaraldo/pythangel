import numpy as np
import sox

# sample rate in Hz
sample_rate = 44100

# generate a 1-second sine tone at 440 Hz
y = np.sin(2 * np.pi * 440.0 * np.arange(sample_rate * 1.0) / sample_rate)

# create a transformer
tfm = sox.Transformer()

# shift the pitch up by 2 semitones
tfm.pitch(2)

# transform an in-memory array and return an array
y_out = tfm.build_array(input_array=y, sample_rate_in=sample_rate)

# instead, save output to a file
tfm.build_file(
    input_array=y, sample_rate_in=sample_rate,
    output_filepath='path/to/output.wav'
)

# create an output file with a different sample rate
tfm.set_output_format(rate=8000)
tfm.build_file(
    input_array=y, sample_rate_in=sample_rate,
    output_filepath='path/to/output_8k.wav'
)


sample_rate = sox.file_info.sample_rate('path/to/file.mp3')
# get the number of samples
n_samples = sox.file_info.num_samples('path/to/file.wav')
# determine if a file is silent
is_silent = sox.file_info.silent('path/to/file.aiff')
# file info doesn't currently support array input