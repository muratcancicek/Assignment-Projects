from datetime import datetime
import time
import sys
import os
import paths

PYTHON_VERSION = sys.version_info[0]
WRITE_OUTPUTS = True
LOGGING = False
HIGH_LOGGING = LOGGING and True

def print_(*args):
    line = ''
    for ar in args:
        line += str(ar) + ' '
    line = line[:-1]+'\n'
    print(line[:-1])
    if WRITE_OUTPUTS:
        outputFileName = paths.joinPath(paths.dataFolder, 'output3.txt')
        if os.path.isfile(outputFileName):
            open(outputFileName, 'a').write(line)  
        else:
            open(outputFileName, 'w').write(line)  
    
def print_logging(*args):
    if LOGGING: 
        line = ''
        for ar in args:
            line += str(ar) + ' '
        line = line[:-1]+'\n'
        print_(line[:-1])

def print_high_logging(*args):
    if HIGH_LOGGING: 
        line = ''
        for ar in args:
            line += str(ar) + ' '
        line = line[:-1]+'\n'
        print_(line[:-1])

def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(i)
    else:
        return range(i)
        
def nowStr():
    return str(datetime.now())

def uniqueList(l): 
    return list(set(l))