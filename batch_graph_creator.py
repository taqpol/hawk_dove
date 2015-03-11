import numpy as np
import os
from pylab import *


file_number = 0
parent_dir = os.path.join(os.path.expanduser('~'), 'Desktop\\Graphs\\')
date_time = os.listdir(parent_dir)
date_time = [str(folder_number+1) + ': ' + date_time[folder_number] 
for folder_number in range(len(date_time))]
    
possible_choice = [number+1 for number in range(len(date_time))]
print("Folders with data available to be graphed: ")
for folders in date_time:
    print(folders)
folder_selection = input('Choose a folder number to graph its data: ')
while not folder_selection in possible_choice:
    folder_selection = input('Folder index not recognized. Choose another folder: ')
    
files = str(files).lstrip('[').rstrip(']').strip("'")
data_dir = os.path.join(date_time, files, 'RawData')
text = []
f = open(os.path.join(raw_dir, '%s' %files, 'conditions.txt'))
while line:
    line = f.readline()
    text.append(line)
    
  
os.makedirs(os.path.join(parent_dir, '2D Hist'))
os.makedirs(os.path.join(parent_dir, '1D Hist'))
os.makedirs(os.path.join(parent_dir, 'Scatter'))
for arrays in files:
    current_array = np.load(arrays)
    chromosome_contents = [numpy.mean(current_array[i,]) for i in range(pop_size)]
    hist2d(arrays, x_axis, bins = 50)
    hist2d(chromosome_contents,x_axis, bins = 50)
    savefig(os.path.join(parent_dir, '2D Hist\\%s.png' %file_number))
    pyplot.clf()
    hist(chromosome_contents)
    savefig(os.path.join(parent_dir, '1D Hist\\%s.png' %file_number))
    pyplot.clf()
    scatter(chromosome_contents,x_axis)
    savefig(os.path.join(parent_dir, 'Scatter\\%s.png' %file_number))
    pyplot.clf()