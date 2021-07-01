# coding: utf-8

# import packages

import requests
import re
import os
import csv
import sys
import itertools
import fnmatch


# loop through CSV files

os.chdir(r'C:\Users\gelly\Documents\All Data\NSAR Data')
file_list = os.getcwd()

for filename in os.listdir(file_list):
    # initialization
    mothership = []
    mother = []
    
    if fnmatch.fnmatch(filename, 'index*.csv'):
        # read URLs
        path_to_file = os.path.join(r'C:\Users\gelly\Documents\All Data\NSAR Data', filename)
        inputFile = open(path_to_file, 'rt')
        paths = csv.reader(inputFile)
        print (filename)
        for i, path in enumerate(paths):
            if i == 0:
                continue
            else:
                # read NSAR and parse
                CIK = path[0]
                url = path[1]
                url = 'http://sec.gov/Archives/' + url
                formType = path[2]
                textFileName = os.path.splitext(filename)[0] + '_' + CIK + '_' + formType + '.txt'
                r = requests.get(url)
                textFile = os.path.join(r'C:\Users\gelly\Documents\All Data\NSAR Data\Filings', textFileName)

                print (url)

                if not os.path.isfile(textFile):
                    f = open(textFile, 'w+')
                    f.write(r.text)
                    f.close()
