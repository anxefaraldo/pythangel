import pandas as pd
import os
import csv
import sys

#if len(argv[0]) != 3:
 #   Raise: 


def get_files(folder):
    "returns a list of files in a given directory"
    files = os.listdir(folder)
    print len(files), "files found"
    return files
    

def filter_files(files, symbolString):
    filtered_list = []
    for i in files:
        if symbolString in i:
            filtered_list.append(i)
    return filtered_list
        
  
    
files_to_process = list_folders(global_folder)
    
global_folder = '/Users/angelfaraldo/GoogleDrive/datasets/McGill/MIREX-format'
file_type = 'majmin'
ext = '.lab'
fileID = '0006'

os.mkdir(global_folder + '/GiantSteps/') + file_type + '/')
os.mkdir(global_folder + '/GiantSteps/' + file_type)

outroute = global_folder + '/GiantSteps/' + file_type + '/'

original = global_folder + '/' + fileID + '/' + file_type + ext
pd_table = pd.read_table(original, names=['a','b','c']) # import datafile from the dataset
pd_table['d'] = 'chord'
pd_table = pd.DataFrame(pd_table, columns=['d','a','c'])
outputFile = outroute + fileID + '.chords'

myl = list(pd_table)

pd_table.to_csv(outputFile, sep="\t", index=False, header=False)

if __name__ == '__main__':
    print 'como dios'
    