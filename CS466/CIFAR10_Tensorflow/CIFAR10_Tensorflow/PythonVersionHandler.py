from datetime import datetime
import time
import sys
import os
from paths import outputFileName

def print_(*args):
    line = ''
    for ar in args:
        line += str(ar) + ' '
    line = line[:-1]+'\n'
    sys.stdout.write(line)
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