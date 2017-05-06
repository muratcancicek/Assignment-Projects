from datetime import datetime
import time
import sys
import os
import paths

PYTHON_VERSION = sys.version_info[0]

def print_(*args):
    line = ''
    for ar in args:
        line += str(ar) + ' '
    line = line[:-1]+'\n'
    print(line[:-1])
    outputFileName = paths.joinPath(paths.dataFolder, 'output2.txt')
    if os.path.isfile(outputFileName):
        open(outputFileName, 'a').write(line)  
    else:
        open(outputFileName, 'w').write(line)  
    
def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(i)
    else:
        return range(i)
        
def nowStr():
    return str(datetime.now())