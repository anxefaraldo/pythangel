#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import argparse
from edmkey_two import *
from key_eval import *

parser = argparse.ArgumentParser(description="global key estimation and evaluation algorithms")
parser.add_argument("input", help="file or dir to analyse")
parser.add_argument("annotations", help="dir with ground-truth annotations")
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

if args.file:
    if not os.path.isfile(args.input):
        raise parser.error("'{0}' is not a valid file.".format(args.input))
    else:
        output_dir = create_subfolder_with_parameters(output_dir, overwrite=args.overwrite)
        if ANALYSIS_TYPE == 'local':
            r = edmkey_two(args.input, output_dir)
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
                    r = edmkey_two(audiofile, output_dir)
                    if args.verbose:
                        print audiofile, '-', r
                elif ANALYSIS_TYPE == 'global':
                    r, c, ch = estimate_key_globally(audiofile, output_dir)
                    if args.verbose:
                        print audiofile, '-', r, '(%.2f)' % c
                count_files += 1
        print "{} audio files analysed".format(count_files)
if not os.path.isdir(args.annotations):
    raise parser.error(
        "Warning: '{0}' not a directory.".format(args.annotations))
else:
    key_evaluation(output_dir, args.annotations)
