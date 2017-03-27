from datetime import datetime
import time
import sys
import os

PYTHON_VERSION = sys.version_info[0]

def print_(*args):
        line = ''
        for ar in args:
            line += str(ar) + ' '
        print(line)
    #if PYTHON_VERSION == 3:
    #    print
    ##else:
    
def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(i)
    else:
        return range(i)
        
def nowStr():
    return str(datetime.now())