# 
# File: dbgen.py
# Author: Martin Yrjola
# Desc: An object database generator for the level editor,
#       Parses the gameinstances and fills a dictionary with
#       their names and pictures. 
#

import sys
import os
import pickle

global dbdict
dbdict = {}

def dirwalk(pathtowalk):
    '''Goes through the directories and opens every '.py'-file for parsing'''
    for root, dirs, files in os.walk(pathtowalk):
        for filename in files:
            if filename[-3:] == '.py':
                print filename
                parsefile(os.path.join(root, filename))

def parsefile(file):
    f = open(file, 'r')
    # first the object
    for line in f:
        if line[:6] == 'class ':
            print line
            objname = line[6:line.find('(')]
            # then the image
            for line in f:
                imgindex = line.find('imgLoad')
                if imgindex != -1:
                    imgname = line[imgindex + 9:-2]
                    dbdict[objname] = imgname
                    print dbdict
                    break
    f.close()
                
def main():
    dbfile = open('objdict.db', 'w')
    os.chdir(os.path.join(os.getcwd(), '..')) # to get to the project root
    os.chdir(os.path.join(os.getcwd(), 'lib/gameinstances'))
    dirwalk(os.getcwd())
    print dbdict
    pickle.dump(dbdict, dbfile)
    dbfile.close()

if __name__ == '__main__':
    main()

